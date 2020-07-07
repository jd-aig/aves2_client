# [Aves2Client]()

Aves2Client是[Aves2]()平台的命令行工具，支持用户进行提交、查看、删除任务等基本等任务管理功能。

## 软件包依赖
- simplejson
- requests>=2.1.8
- configobj>=5.0
- pyyaml>=3.12
- prettytable

## 安装
```
pip install aves2_client
```

## 配置
### 获取API Token
访问Aves2，获取API Token。
http://&lt;AVES2 HOST&gt;/aves2/center/token/

### 配置aves2 client
```
# mkdir ~/.aves2/
# vim ~/.aves2/aves2.cfg
[Aves2Server]
    host = 'http://<AVES2_HOST>/aves2/'
    api_token ='<YOUR API TOKEN>'
 
[UserInfo]
    username = '<YOUR NAME>'
    namespace = ''  # 训练任务将提交到指定的namespace
 
[StorageConf]
    [[S3]]
        S3Endpoint = ''
        S3AccessKeyId = ''
        S3SecretAccessKey = ''
```

### 获取Job定义模版
训练任务可以使用本地共享文件系统、对象存储、PVC等类型的数据。通过aves2 example命令可以获取任务模版：
```
# aves2 example hostpath

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
```

```
# aves2 example pvc

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
```

```
# aves2 example ossfile

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
```

### 提交任务
```
aves2 create -f xxx.jaml
```

### 查看任务
```
aves2 list
+-------+------------+---------------------------------+-----------------------------+----------+
| jobId | Namespace  | job名称                         | 创建时间                    | 状态     |
+-------+------------+---------------------------------+-----------------------------+----------+
| 128   | aiplatform | pytorch mnist-HostPath          | 2020-03-20T18:09:48.770668Z | 运行成功 |
| 124   | aiplatform | pytorch mnist-HostPath          | 2020-03-20T17:31:17.836239Z | 运行失败 |
| 123   | aiplatform | pytorch mnist-HostPath          | 2020-03-20T17:25:09.654684Z | 已取消   |
+-------+------------+---------------------------------+-----------------------------+----------+
```

### 更多命令
```
# aves2 --help
usage: aves2 [-h] {create,rerun,list,show,delete,cancel,log,example} ...

Command line for AVES2

optional arguments:
  -h, --help            show this help message and exit

Available commands:
  {create,rerun,list,show,delete,cancel,log,example}
    create              Create aves2 job
    rerun               Rerun aves2 job
    list                List aves2 jobs
    show                Show aves2 job info
    delete              delete aves2 job
    cancel              cancel aves2 job
    log                 log aves2 job
    example             show aves2 job example
```
