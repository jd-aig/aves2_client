import sys
import os
import logging
# import pprint
import requests

from aves2_client.settings import aves2_cfg
from aves2_client.version import aves2_version
from aves2_client.err import *


AVES2_HOST = aves2_cfg['Aves2Server']['host']
AVES2_TOKEN = aves2_cfg['Aves2Server']['api_token']
AVES2_APIS = {
    'list_job': '/api/aves_job/',
    'create_job': '/api/aves_job/',
    'get_job': '/api/aves_job/{jobid}',
    'start_job': '/api/aves_job/{jobid}/start_job/',
    'cancel_job': '/api/aves_job/{jobid}/cancel_job/',
    'log_job': '/api/aves_job/{jobid}/logs/',
    'delete_job': '/api/aves_job/{jobid}/',
    'client_check': '/api/client_check',
}

HEADERS = {
    'Authorization': f'Token {AVES2_TOKEN}',
}


def url_join(host, uri):
    return os.path.join(host, uri.lstrip('/'))

def client_check():
    url = url_join(AVES2_HOST, AVES2_APIS['client_check'])
    rst = requests.get(url, params=dict(version=aves2_version()))
    if rst.ok and not rst.json().get('success'):
        raise Aves2ClientError('Please upgrade aves2 client')

def list_job():
    client_check()
    url = url_join(AVES2_HOST, AVES2_APIS['create_job'])
    rst = requests.get(url, headers=HEADERS)
    return rst

def create_job(job_data):
    client_check()
    url = url_join(AVES2_HOST, AVES2_APIS['create_job'])
    rst = requests.post(url, json=job_data, headers=HEADERS)
    return rst

def get_job(jobid):
    client_check()
    url = url_join(AVES2_HOST, AVES2_APIS['get_job']).format(**locals())
    rst = requests.get(url, headers=HEADERS)
    return rst

def start_job(jobid):
    client_check()
    url = url_join(AVES2_HOST, AVES2_APIS['start_job']).format(**locals())
    rst = requests.get(url, headers=HEADERS)
    return rst

def cancel_job(jobid):
    client_check()
    url = url_join(AVES2_HOST, AVES2_APIS['cancel_job']).format(**locals())
    rst = requests.get(url, headers=HEADERS)
    return rst

def delete_job(jobid):
    client_check()
    url = url_join(AVES2_HOST, AVES2_APIS['delete_job']).format(**locals())
    ret = requests.delete(url, headers=HEADERS)
    return ret

def log_job(jobid):
    client_check()
    url = url_join(AVES2_HOST, AVES2_APIS['log_job']).format(**locals())
    ret = requests.get(url, headers=HEADERS)
    return ret
