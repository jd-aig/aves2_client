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
job_name: 'ossfile demo'
debug: true
distribute_type: Null  # Null, HOROVOD, TF_PS
image: <镜像地址>
resource_spec:
  worker:
    count: 1
    cpu: 4
    mem: 2  # 2G
    gpu: 0
running_spec:
  source_code:                          # 源代码相关配置
    storage_mode: OSSFile
    storage_conf:
      path: s3://<代码路径>/demo.zip
  envs: []                              # 用户可以设置环境变量
  cmd: "python3 main.py"                # 启动命令
  normal_args: []
    # - name: batch-size
    #   value: 64
    # - name: epochs
    #   value: 10
    # - name: lr
    #   value: 0.01
  input_args:                           # 输入类参数
    - name: data-dir
      data_conf:
        storage_mode: OSSFile
        storage_conf:
          path: s3://<输入数据集路径>/
  output_args:                          # 输出类参数
    - name: output-dir
      data_conf:
        storage_mode: OSSFile
        storage_conf:
          path: s3://<输出路径/
"""
    print(s)


def show_pvc_template(args):
    s = """
job_name: 'k8spvc demo'  # 仅在kubernets集群中支持
debug: true
namespace: default
distribute_type: Null  # Null, HOROVOD, TF_PS
image: <镜像地址>
resource_spec:
  worker:
    count: 1
    cpu: 4
    mem: 2  # 2G
    gpu: 1
running_spec:
  source_code:                          # 源代码相关配置
    storage_mode: K8SPVC
    storage_conf:
      pvc: <PVC NAME>
      path: <代码所在的子路径>
  envs: []                              # 用户可以设置环境变量
  cmd: "python3 main.py"                # 启动命令
  normal_args: []                       # 超参数
    # - name: batch-size
    #   value: 64
    # - name: epochs
    #   value: 10
    # - name: lr
    #   value: 0.01
  input_args:                           # 输入类参数
    - name: data-dir
      data_conf:
        storage_mode: K8SPVC
        storage_conf:
          pvc: <PVC NAME>
          path: <输入数据所在的子路径>
  output_args:                          # 输出类参数
    - name: output-dir
      data_conf:
        storage_mode: OSSFile
        storage_conf:
          path: s3://<输出路径/         # 输出将被保存到对象存储
"""
    print(s)


def show_hostpath_template(args):
    s = """
job_name: 'hostpath demo'
debug: true
distribute_type: Null  # Null, HOROVOD, TF_PS
image: <镜像地址>
resource_spec:
  worker:
    count: 1
    cpu: 4
    mem: 2  # 2G
    gpu: 1
running_spec:
  source_code:                          # 源代码相关配置
    storage_mode: HostPath
    storage_conf:
      path: <代码所在本地路径>
  envs: []                              # 用户可以设置环境变量
  cmd: "python3 main.py"                # 启动命令
  normal_args: []                       # 超参数
    # - name: batch-size
    #   value: 64
    # - name: epochs
    #   value: 10
    # - name: lr
    #   value: 0.01
  input_args:                           # 输入类参数
    - name: data-dir
      data_conf:
        storage_mode: HostPath
        storage_conf:
          path: <输入数据集的本地路径>
  output_args:                          # 输出类参数
    - name: output-dir
      data_conf:
        storage_mode: HostPath
        storage_conf:
          path: <输出本地路径>
"""
    print(s)
