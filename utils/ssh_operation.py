#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/18 10:44
# @Author  : 冉勇
# @Site    :
# @File    : ssh_operation.py
# @Software: PyCharm
# @desc    : ssh连接服务器方法
import os
import paramiko


def ssh_operation(
        host: str,
        username: str,
        password: str,
        operation: str,
        local_path=None,
        remote_path=None,
        content=None
):
    """
    执行各种SSH操作，包括上传、下载文件，读写文本，执行命令等

    参数:
    host (str): 虚拟机主机地址
    username (str): 登录用户名
    password (str): 登录密码
    operation (str): 操作类型 - "upload_file", "download_file", "write_text", "read_text",
                    "execute_command", "list_dir", "make_dir", "remove_file", "remove_dir"
    local_path (str): 本地文件或目录路径
    remote_path (str): 远程文件或目录路径
    content (str): 文本内容或命令字符串

    返回:
    根据操作类型返回不同的结果
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(host, username=username, password=password)
        sftp = client.open_sftp()

        # if operation == "upload_file":
        #     # 上传文件到虚拟机
        #     if not local_path or not remote_path:
        #         raise ValueError("上传文件需要提供本地和远程路径")
        #     sftp.put(local_path, remote_path)
        #     print(f"文件已成功上传到虚拟机: {local_path} -> {remote_path}")

        if operation == "upload_file":
            # 上传文件到虚拟机
            if not local_path or not remote_path:
                raise ValueError("上传文件需要提供本地和远程路径")

            # 获取源文件的文件名
            local_filename = os.path.basename(local_path)

            # 检查远程路径是否以斜杠结尾(表示目录)
            if remote_path.endswith('/'):
                # 如果是目录，则在末尾添加文件名
                full_remote_path = os.path.join(remote_path, local_filename)
            else:
                # 如果不是以斜杠结尾，假设用户已提供完整路径
                full_remote_path = remote_path
            # 执行上传
            sftp.put(local_path, full_remote_path)
            print(f"文件已成功上传到虚拟机: {local_path} -> {full_remote_path}")

        elif operation == "download_file":
            # 从虚拟机下载文件
            if not local_path or not remote_path:
                raise ValueError("下载文件需要提供本地和远程路径")
            sftp.get(remote_path, local_path)
            print(f"文件已成功从虚拟机下载: {remote_path} -> {local_path}")

        elif operation == "write_text":
            # 写入文本内容到虚拟机上的文件
            if not remote_path or content is None:
                raise ValueError("写入文本需要提供远程路径和内容")
            with sftp.file(remote_path, 'w') as f:
                f.write(content)
            print(f"文本内容已成功写入虚拟机上的 {remote_path}")

        elif operation == "read_text":
            # 读取虚拟机上文件的文本内容
            if not remote_path:
                raise ValueError("读取文本需要提供远程路径")
            with sftp.file(remote_path, 'r') as f:
                content = f.read()
            print(f"已从虚拟机上的 {remote_path} 读取内容")
            return content

        elif operation == "execute_command":
            # 在虚拟机上执行命令
            if not content:
                raise ValueError("执行命令需要提供命令内容")
            stdin, stdout, stderr = client.exec_command(content)
            output = stdout.read().decode()
            error = stderr.read().decode()
            if error:
                print(f"命令执行出错: {error}")
            print(f"命令执行完成")
            return output

        elif operation == "list_dir":
            # 列出虚拟机上目录的内容
            if not remote_path:
                raise ValueError("列出目录需要提供远程路径")
            files = sftp.listdir(remote_path)
            print(f"目录 {remote_path} 的内容:")
            return files

        elif operation == "make_dir":
            # 在虚拟机上创建目录
            if not remote_path:
                raise ValueError("创建目录需要提供远程路径")
            try:
                sftp.mkdir(remote_path)
                print(f"已在虚拟机上创建目录: {remote_path}")
            except IOError:
                print(f"目录可能已存在: {remote_path}")

        elif operation == "remove_file":
            # 删除虚拟机上的文件
            if not remote_path:
                raise ValueError("删除文件需要提供远程路径")
            sftp.remove(remote_path)
            print(f"已删除虚拟机上的文件: {remote_path}")

        elif operation == "remove_dir":
            # 删除虚拟机上的目录
            if not remote_path:
                raise ValueError("删除目录需要提供远程路径")
            sftp.rmdir(remote_path)
            print(f"已删除虚拟机上的目录: {remote_path}")

        else:
            raise ValueError(f"不支持的操作: {operation}")

    finally:
        if 'sftp' in locals():
            sftp.close()
        client.close()


# 使用示例
if __name__ == "__main__":
    os.environ["SSH_HOST"] = "192.168.1.50"
    os.environ["SSH_USERNAME"] = "root"
    os.environ["SSH_PASSWORD"] = "Ranyong_123"
    host = os.getenv("SSH_HOST")  # 虚拟机IP地址
    username = os.getenv("SSH_USERNAME")  # 虚拟机用户名
    password = os.getenv("SSH_PASSWORD")  # 虚拟机密码
    # 上传文件示例
    ssh_operation(host, username, password, "upload_file", "../assets/images/realm.svg", "/usr/local/1.svg")

    # 下载文件示例
    # ssh_operation(host, username, password, "download_file", "assets/images/downloaded_file.txt", "/usr/local/remote_file.txt")

    # 写入文本示例
    # ssh_operation(host, username, password, "write_text", remote_path="/usr/local/test.txt", content="这是测试内容")

    # 读取文本示例
    # content = ssh_operation(host, username, password, "read_text", remote_path="/usr/local/test.txt")
    # print("读取的内容:", content)

    # 执行命令示例
    # result = ssh_operation(host, username, password, "execute_command", content="docker ps")
    # print("命令输出:", result)

    # 列出目录内容示例
    # files = ssh_operation(host, username, password, "list_dir", remote_path="/usr/local")
    # for file in files:
    #     print(file)

    # 创建目录示例
    # ssh_operation(host, username, password, "make_dir", remote_path="/usr/local/new_folder")
