import os
import yaml
import logging
import copy
import prettytable as pt

from aves2_client.aves2_api import job as job_api
from aves2_client.utils import print_warning, print_success, sleep_and_print
from aves2_client.settings import aves2_cfg


aves2_cfg = aves2_cfg.dict()


logger = logging.getLogger(__name__)

JOB_STATUS_MAP = {
    'STARTING': "\033[1;33m启动中\033[0m",
    'RUNNING': "\033[1;34m运行中\033[0m",
    'FINISHED': "\033[0;32m运行成功\033[0m",
    'FAILURE': "\033[1;31m运行失败\033[0m",
    'CANCELED': "\033[0;33m已取消\033[0m",
}


def check_cmd_args(running_spec):
    data = {}
    cmd = running_spec['cmd']
    args = [{i['name']: i['value']} for i in running_spec.get('normal_args', [])]
    data['cmd'] = cmd
    data['args'] = args
    return data


def check_resource_spec(distribute_type, resource_spec, cmd_info):
    cmd = cmd_info['cmd']
    args = cmd_info['args']
    resource_spec = copy.deepcopy(resource_spec)
    key_set = set(resource_spec.keys())
    if distribute_type == 'HOROVOD':
        role_set = set(['worker'])
    elif distribute_type == 'TF_PS':
        role_set = set(['ps', 'worker'])
    else:
        role_set = set(['worker'])
    unknown = key_set - role_set
    miss = role_set - key_set
    if unknown:
        raise Exception('Unknown keys in resource_spec: {0}'.format(','.join(unknown)))
    if miss:
        raise Exception('Miss keys in resource_spec: {0}'.format(','.join(miss)))

    for role, conf in resource_spec.items():
        conf['mem'] = '{}Gi'.format(conf.get('mem', 1))
        conf['entry_point'] = cmd
        conf['args'] = args
    return resource_spec


def parse_data_path(path):
    if path.startswith('s3://'):
        if os.path.basename(path).split('.')[-1] in ['zip', 'tar', 'gz']:
            code_dir = os.path.join(os.path.dirname(path), '')
            filename = os.path.basename(path)
        else:
            code_dir = path
            filename = ''
    else:
        if os.path.basename(path).split('.')[-1] in ['zip', 'tar', 'gz']:
            code_dir = os.path.join(os.path.dirname(path), '')
            filename = os.path.basename(path)
        else:
            code_dir = path
            filename = ''
        #code_dir = path
        #filename = ''
    return code_dir, filename


def get_nfs_path(path):
    df_info = [i.strip('\n').split() for i in os.popen("df | awk '{print $1, $6}'").readlines()]
    export_path = None
    for source, mount in df_info:
        if ':' not in source:
            continue
        if path.startswith(mount):
            export_path = os.path.join(source, path.split(mount)[1].lstrip('/'))
    if not export_path:
        raise Exception(f'{path} is not a valid nfs path')
    else:
        return export_path


def check_code_spec(code_spec):
    data = {}
    data['type'] = code_spec['storage_mode']
    code_path = code_spec['storage_conf']['path']
    path, filename = parse_data_path(code_path)
    data['path'] = path
    # TODO
    data['filename'] = filename
    if data['type'] == 'K8SPVC':
        data['pvc'] = code_spec['storage_conf']['pvc']
    if data['type'] == 'NFSPath':
        data['path'] = get_nfs_path(data['path'])
    if data['type'] == 'HostPath':
        pass
    return data


def check_log_spec(code_spec):
    if not code_spec:
        return {}
    data = {}
    data['type'] = code_spec['storage_mode']
    code_path = code_spec['storage_conf']['path']
    path, filename = parse_data_path(code_path)
    data['path'] = path
    # TODO
    data['filename'] = filename
    if data['type'] == 'K8SPVC':
        data['pvc'] = code_spec['storage_conf']['pvc']
    if data['type'] == 'NFSPath':
        data['path'] = get_nfs_path(data['path'])
    if data['type'] == 'HostPath':
        pass
    return data


def check_data_spec(data_spec):
    data = {}
    for input_i in data_spec:
        i_name = input_i['name']
        i_type = input_i['data_conf']['storage_mode']
        i_path = input_i['data_conf']['storage_conf']['path']
        i_path, i_filename = parse_data_path(i_path)
        data[i_name] = {
            'type': i_type,
            'path': i_path,
            'filename': i_filename
        }
        if data[i_name]['type'] == 'K8SPVC':
            data[i_name]['pvc'] = input_i['data_conf']['storage_conf']['pvc']
        if data[i_name]['type'] == 'NFSPath':
            data[i_name]['path'] = get_nfs_path(data[i_name]['path'])
        if data[i_name]['type'] == 'HostPath':
            pass
    return data


def parse_conf(job_data):
    post_data = {}

    post_data['need_report'] = job_data.get('need_report', False)
    post_data['name'] = job_data.get('job_name', '')
    post_data['debug'] = job_data.get('debug', False)
    post_data['namespace'] = job_data.get('namespace', 'default')
    # Note: image
    post_data['image'] = job_data['image']

    # Note: deprecated
    post_data['package_uri'] = 'deprecated'
    post_data['engine'] = 'deprecated'
    post_data['storage_mode'] = 'OSSFile'

    # Note: storage_config
    post_data['storage_config'] = {
        'mode': 'OSSFile',
        'config': aves2_cfg.get('StorageConf', {}).get('S3')
    }

    # Note: distribute type
    distribute_type = job_data.get('distribute_type')
    if distribute_type not in [None, 'HOROVOD', 'TF_PS', 'mpi']:
        raise Exception('Invalid distribute type')
    post_data['is_distribute'] = True if distribute_type else False
    post_data['distribute_type'] = distribute_type

    cmd_info = check_cmd_args(job_data['running_spec'])
    # Note: resource spec
    resource_spec = check_resource_spec(distribute_type, job_data['resource_spec'], cmd_info)
    post_data['resource_spec'] = resource_spec

    # Note: envs
    post_data['envs'] = {i['name']: i['value'] for i in job_data['running_spec']['envs']}

    # Note: code spec
    post_data['code_spec'] = check_code_spec(job_data['running_spec']['source_code'])

    # Note: inputspec
    post_data['input_spec'] = check_data_spec(job_data['running_spec']['input_args'])

    # Note: outputspec
    post_data['output_spec'] = check_data_spec(job_data['running_spec']['output_args'])

    # Note: log spec
    post_data['log_dir'] = check_log_spec(job_data['running_spec'].get('log_dir', {}))

    return post_data


def create_job(args):
    job_conf = args.job_conf
    try:
        f = open(job_conf)
        job_data = yaml.load(f)
    except FileNotFoundError:
        print_warning('Job config file is not exist')
        return
    except Exception as e:
        print(e)
        print_warning('Invalid config file')
        return
    finally:
        f.close()

    try:
        post_data = parse_conf(job_data)
    except Exception as e:
        raise

    rt = job_api.create_job(post_data)
    if rt.status_code == 201:
        print_success('JOB Created: %s' % rt.json()['id'])
    else:
        print_warning('Fail to create job: %s' % rt.text)


def list_jobs(args):
    rt = job_api.list_job()
    job_set = []
    if rt.ok:
        data = rt.json()
        for item in data[::-1]:
            job_set.append((
                item['id'],
                item['namespace'],
                item['job_name'],
                item['create_time'],
                JOB_STATUS_MAP.get(item['status'])
            ))
        tb = pt.PrettyTable(['jobId', 'Namespace', 'job名称', '创建时间', '状态'])
        tb.align = 'l'
        rows = list(map(lambda x: tb.add_row(x), job_set))
        print(tb)
        print('')
    else:
        print_warning('Fail to get job list')


def rerun_job(args):
    job_id = args.job_id
    rt = job_api.start_job(job_id)
    if rt.ok:
        print_success('job is starting')
        list_jobs(args)
    else:
        print_warning('Fail to star job: {}'.format(rt.text))


def show_job(args):
    pass


def delete_job(args):
    job_id = args.job_id
    rt = job_api.delete_job(job_id)
    if rt.ok:
        print_success('JOB is deleted')
    else:
        print_warning('Fail to delete job: {}'.format(rt.text))


def cancel_job(args):
    job_id = args.job_id
    rt = job_api.cancel_job(job_id)
    if rt.ok:
        print_success('JOB is canceld')
        list_jobs(args)
    else:
        print_warning('Fail to stop job')


def log_job(args):
    job_id = args.job_id
    rt = job_api.log_job(job_id)
    if rt.ok:
        for line in rt.text.splitlines():
            print(line)
    else:
        print_warning('Fail to get job log')
