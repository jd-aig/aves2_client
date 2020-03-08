import os
import yaml
import logging
import copy
import prettytable as pt

from aves2_client.settings import aves2_cfg


aves2_cfg = aves2_cfg.dict()


logger = logging.getLogger(__name__)


def show_ossfile_template(args):
    s = """
job_name: 'Job名称'
namespace: default
distribute_type: Null  # 可选值: Null, HOROVOD, TF_PS
image: '运行任务的镜像'
resource_spec:
  worker:
    count: 1
    cpu: 4
    mem: 2  # 单位G
    gpu: 1  # 如果不需要GPU填写0
running_spec:
  source_code:
    storage_mode: OSSFile
    storage_conf:
      path: s3://xxxxxx/  # 代码路径
  envs: []
  cmd: "python3 main.py"
  normal_args:  # 普通类型的参数
    - name: lr
      value: 0.001
    - name: batchsize
      value: 10
  input_args:  # 输入数据参数
    - name: train-data
      data_conf:
        storage_mode: OSSFile
        storage_conf:
          path: s3://xxxxx/train-data/
  output_args:  # 输出数据参数
    - name: output-dir
      data_conf:
        storage_mode: OSSFile
        storage_conf:
          path: s3://xxxx/output/
"""
    print(s)


def show_pvc_template(args):
    s = """
job_name: 'Job名称'
namespace: default
distribute_type: Null  # 可选值: Null, HOROVOD, TF_PS
image: '运行任务的镜像‘
resource_spec:
  worker:
    count: 1
    cpu: 4
    mem: 2  # 单位G
    gpu: 1  # 如果不需要GPU填写0
running_spec:
  source_code:
    storage_mode: K8SPVC
    storage_conf:
      pvc: 'pvc名称'
      path: 'pvc中的子路径'
  envs: []
  cmd: "python3 main.py"
  normal_args:  # 普通类型的参数
    - name: lr
      value: 0.001
    - name: batchsize
      value: 10
  input_args:  # 输入数据参数
    - name: train-data
      data_conf:
        storage_mode: K8SPVC
        storage_conf:
          pvc: 'pvc名称'
          path: 'pvc中的子路径'
  output_args:  # 输出数据参数
    - name: 'output-dir'
      data_conf:
        storage_mode: K8SPVC
        storage_conf:
          pvc: 'pvc名称'
          path: 'pvc中的子路径'
"""
    print(s)


def show_hostpath_template(args):
    s = """
job_name: 'Job名称'
namespace: default
distribute_type: Null  # 可选值: Null, HOROVOD, TF_PS
image: '运行任务的镜像‘
resource_spec:
  worker:
    count: 1
    cpu: 4
    mem: 2  # 单位G
    gpu: 1  # 如果不需要GPU填写0
running_spec:
  source_code:
    storage_mode: HostPath
    storage_conf:
      path: /export/<username>/code/  # Jupyter容器内路径
  envs: []
  cmd: "python3 main.py"
  normal_args:  # 普通类型的参数
    - name: lr
      value: 0.01
    - name: batchsize
      value: 10
  input_args:  # 输入数据参数
    - name: data-dir
      data_conf:
        storage_mode: HostPath
        storage_conf:
          path: /export/<username>/data/  # Jupyter容器内路径
  output_args:  # 输出数据参数
    - name: output-dir
      data_conf:
        storage_mode: HostPath
        storage_conf:
          path: /export/<username>/output/  # Jupyter容器内路径

"""
    print(s)
