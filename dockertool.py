import docker

client = docker.from_env()

def create_docker(docker_name):
    '''
     作用：运行一个(ubuntu)容器实例，可选参数detach=True为后台运行
     参数：docker_name为容器的名称
     返回：容器对象
    '''
    container = client.containers.run("ubuntu:latest", name=docker_name, detach=True, tty=True, command=['/bin/bash'])

def remove_docker(docker_name):
    '''
     作用：删除一个(ubuntu)容器实例
     参数：docker_name为容器的名称
     返回：无
    '''
    container = client.containers.get(docker_name)
    container.remove()

def stop_docker(container_name):
    '''
     作用：停用容器
     参数：container_name需要停用的容器名称
     返回：无
    '''
    container = client.containers.get(container_name)
    container.stop()

def start_docker(container_name):
    '''
     作用：启用容器
     参数：container_name需要启用的容器名称
     返回：无
    '''
    container = client.containers.get(container_name)
    container.start()

def run_command(container_name, command):
    '''
     作用：执行命令
     参数：container_name需要运行命令的容器名称 command需要运行的命令
     返回：命令输出
    '''
    container = client.containers.get(container_name)
    return container.exec_run(command, stream=True)
