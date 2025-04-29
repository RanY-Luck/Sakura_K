#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/18 10:44
# @Author  : 冉勇
# @Site    :
# @File    : ssh_operation.py
# @Software: PyCharm
# @desc    : ssh连接服务器方法
import os
import threading
import paramiko
from utils.log_util import logger
from typing import Dict, List, Optional, Tuple


# 配置日志


class SSHConnection:
    """SSH连接类，管理与远程服务器的连接"""

    _connections: Dict[str, 'SSHConnection'] = {}
    _lock = threading.Lock()

    @classmethod
    def get_connection(
            cls, host: str, username: str, password: str = None,
            port: int = 22
    ) -> 'SSHConnection':
        """获取或创建SSH连接
        
        Args:
            host: 主机地址
            username: 用户名
            password: 密码（可选）
            port: SSH端口，默认22
            
        Returns:
            SSHConnection实例
        """
        conn_key = f"{username}@{host}:{port}"

        with cls._lock:
            if conn_key in cls._connections:
                conn = cls._connections[conn_key]
                if conn.is_active():
                    return conn
                else:
                    # 连接断开，删除旧连接
                    del cls._connections[conn_key]

            # 创建新连接
            conn = SSHConnection(host, username, password, port)
            cls._connections[conn_key] = conn
            return conn

    def __init__(
            self, host: str, username: str, password: str = None,
            port: int = 22
    ):
        """初始化SSH连接
        
        Args:
            host: 主机地址
            username: 用户名
            password: 密码（可选）
            port: SSH端口，默认22
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port

        self.client = None
        self.sftp = None
        self._connect()

    def _connect(self) -> None:
        """建立SSH连接"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            connect_kwargs = {
                'hostname': self.host,
                'username': self.username,
                'port': self.port,
            }

            if self.password:
                connect_kwargs['password'] = self.password

            self.client.connect(**connect_kwargs)
            self.sftp = self.client.open_sftp()
            logger.info(f"成功连接到服务器 {self.username}@{self.host}:{self.port}")

        except Exception as e:
            logger.error(f"连接服务器失败: {str(e)}")
            if self.client:
                self.client.close()
                self.client = None
            raise

    def is_active(self) -> bool:
        """检查连接是否活跃"""
        if not self.client:
            return False

        try:
            transport = self.client.get_transport()
            if transport and transport.is_active():
                # 发送一个简单命令测试连接
                self.client.exec_command('echo 1', timeout=5)
                return True
            return False
        except Exception:
            return False

    def close(self) -> None:
        """关闭连接"""
        if self.sftp:
            self.sftp.close()
            self.sftp = None

        if self.client:
            self.client.close()
            self.client = None

        # 从连接池中移除
        conn_key = f"{self.username}@{self.host}:{self.port}"
        with self._lock:
            if conn_key in self._connections:
                del self._connections[conn_key]

        logger.info(f"已关闭与服务器 {self.username}@{self.host}:{self.port} 的连接")

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时关闭连接"""
        self.close()

    def upload_file(
            self, local_path: str, remote_path: str,
            callback=None
    ) -> bool:
        """上传文件到远程服务器
        
        Args:
            local_path: 本地文件路径
            remote_path: 远程文件路径
            callback: 进度回调函数，参数为(已传输字节数, 总字节数)
            
        Returns:
            成功返回True，失败返回False
        """
        try:
            if not os.path.exists(local_path):
                logger.error(f"本地文件不存在: {local_path}")
                return False

            # 获取源文件的文件名
            local_filename = os.path.basename(local_path)

            # 检查远程路径是否以斜杠结尾(表示目录)
            if remote_path.endswith('/'):
                # 如果是目录，则在末尾添加文件名
                full_remote_path = os.path.join(remote_path, local_filename)
            else:
                # 如果不是以斜杠结尾，假设用户已提供完整路径
                full_remote_path = remote_path

            # 确保远程目录存在
            remote_dir = os.path.dirname(full_remote_path)
            try:
                self.sftp.stat(remote_dir)
            except FileNotFoundError:
                # 目录不存在，创建它
                self._mkdir_p(remote_dir)

            # 执行上传
            self.sftp.put(local_path, full_remote_path, callback=callback)
            logger.info(f"文件已成功上传: {local_path} -> {full_remote_path}")
            return True

        except Exception as e:
            logger.error(f"上传文件失败: {str(e)}")
            return False

    def download_file(
            self, remote_path: str, local_path: str,
            callback=None
    ) -> bool:
        """从远程服务器下载文件
        
        Args:
            remote_path: 远程文件路径
            local_path: 本地文件路径
            callback: 进度回调函数，参数为(已传输字节数, 总字节数)
            
        Returns:
            成功返回True，失败返回False
        """
        try:
            # 确保本地目录存在
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir)

            self.sftp.get(remote_path, local_path, callback=callback)
            logger.info(f"文件已成功下载: {remote_path} -> {local_path}")
            return True

        except Exception as e:
            logger.error(f"下载文件失败: {str(e)}")
            return False

    def write_text(self, remote_path: str, content: str) -> bool:
        """写入文本到远程文件
        
        Args:
            remote_path: 远程文件路径
            content: 要写入的文本内容
            
        Returns:
            成功返回True，失败返回False
        """
        try:
            # 确保远程目录存在
            remote_dir = os.path.dirname(remote_path)
            try:
                self.sftp.stat(remote_dir)
            except FileNotFoundError:
                # 目录不存在，创建它
                self._mkdir_p(remote_dir)

            with self.sftp.file(remote_path, 'w') as f:
                f.write(content)

            logger.info(f"文本已成功写入: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"写入文本失败: {str(e)}")
            return False

    def read_text(self, remote_path: str) -> Optional[str]:
        """读取远程文件内容
        
        Args:
            remote_path: 远程文件路径
            
        Returns:
            文件内容或None（失败时）
        """
        try:
            with self.sftp.file(remote_path, 'r') as f:
                content = f.read()

            if isinstance(content, bytes):
                content = content.decode('utf-8')

            logger.info(f"成功读取文件内容: {remote_path}")
            return content

        except Exception as e:
            logger.error(f"读取文件失败: {str(e)}")
            return None

    def execute_command(self, command: str, timeout: int = 60) -> Tuple[str, str, int]:
        """执行远程命令
        
        Args:
            command: 要执行的命令
            timeout: 命令超时时间（秒）
            
        Returns:
            元组 (标准输出, 标准错误, 退出码)
        """
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
            exit_status = stdout.channel.recv_exit_status()
            output = stdout.read().decode('utf-8')
            error = stderr.read().decode('utf-8')

            if exit_status != 0:
                logger.warning(f"命令执行返回非零状态: {exit_status}, 错误: {error}")
            else:
                logger.info(f"命令执行成功: '{command}'")

            return output, error, exit_status

        except Exception as e:
            logger.error(f"执行命令失败: {str(e)}")
            return "", str(e), -1

    def list_dir(self, remote_path: str) -> List[str]:
        """列出远程目录内容
        
        Args:
            remote_path: 远程目录路径
            
        Returns:
            文件和目录名列表
        """
        try:
            files = self.sftp.listdir(remote_path)
            logger.info(f"列出目录内容: {remote_path}")
            return files

        except Exception as e:
            logger.error(f"列出目录失败: {str(e)}")
            return []

    def make_dir(self, remote_path: str) -> bool:
        """创建远程目录
        
        Args:
            remote_path: 远程目录路径
            
        Returns:
            成功返回True，失败返回False
        """
        try:
            self.sftp.mkdir(remote_path)
            logger.info(f"成功创建目录: {remote_path}")
            return True

        except IOError as e:
            if 'exists' in str(e).lower():
                logger.info(f"目录已存在: {remote_path}")
                return True
            logger.error(f"创建目录失败: {str(e)}")
            return False

        except Exception as e:
            logger.error(f"创建目录失败: {str(e)}")
            return False

    def _mkdir_p(self, remote_path: str) -> bool:
        """递归创建目录（类似mkdir -p）
        
        Args:
            remote_path: 远程目录路径
            
        Returns:
            成功返回True，失败返回False
        """
        if remote_path == '/':
            return True

        try:
            self.sftp.stat(remote_path)
            return True
        except IOError:
            parent = os.path.dirname(remote_path)
            if parent and parent != '/':
                self._mkdir_p(parent)
            if remote_path != '/':
                self.sftp.mkdir(remote_path)
                return True

    def remove_file(self, remote_path: str) -> bool:
        """删除远程文件
        
        Args:
            remote_path: 远程文件路径
            
        Returns:
            成功返回True，失败返回False
        """
        try:
            self.sftp.remove(remote_path)
            logger.info(f"成功删除文件: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"删除文件失败: {str(e)}")
            return False

    def remove_dir(self, remote_path: str, recursive: bool = False) -> bool:
        """删除远程目录
        
        Args:
            remote_path: 远程目录路径
            recursive: 是否递归删除内容
            
        Returns:
            成功返回True，失败返回False
        """
        try:
            if recursive:
                files = self.list_dir(remote_path)
                for file in files:
                    file_path = os.path.join(remote_path, file)
                    try:
                        # 尝试作为文件删除
                        self.remove_file(file_path)
                    except IOError:
                        # 如果不是文件，尝试作为目录递归删除
                        self.remove_dir(file_path, recursive=True)

            self.sftp.rmdir(remote_path)
            logger.info(f"成功删除目录: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"删除目录失败: {str(e)}")
            return False


# 兼容旧接口的函数
def ssh_operation(
        host: str,
        username: str,
        password: str,
        operation: str,
        local_path=None,
        remote_path=None,
        content=None,
        port=22
):
    """
    执行各种SSH操作，包括上传、下载文件，读写文本，执行命令等（兼容旧接口）

    参数:
    host (str): 虚拟机主机地址
    username (str): 登录用户名
    password (str): 登录密码
    operation (str): 操作类型 - "upload_file", "download_file", "write_text", "read_text",
                    "execute_command", "list_dir", "make_dir", "remove_file", "remove_dir"
    local_path (str): 本地文件或目录路径
    remote_path (str): 远程文件或目录路径
    content (str): 文本内容或命令字符串
    port (int): SSH端口，默认22

    返回:
    根据操作类型返回不同的结果
    """
    conn = None
    try:
        conn = SSHConnection.get_connection(host, username, password, port)
        
        if operation == "upload_file":
            if not local_path or not remote_path:
                raise ValueError("上传文件需要提供本地和远程路径")
            return conn.upload_file(local_path, remote_path)
            
        elif operation == "download_file":
            if not local_path or not remote_path:
                raise ValueError("下载文件需要提供本地和远程路径")
            return conn.download_file(remote_path, local_path)
            
        elif operation == "write_text":
            if not remote_path or content is None:
                raise ValueError("写入文本需要提供远程路径和内容")
            return conn.write_text(remote_path, content)
            
        elif operation == "read_text":
            if not remote_path:
                raise ValueError("读取文本需要提供远程路径")
            return conn.read_text(remote_path)
            
        elif operation == "execute_command":
            if not content:
                raise ValueError("执行命令需要提供命令内容")
            output, error, _ = conn.execute_command(content)
            return output
            
        elif operation == "list_dir":
            if not remote_path:
                raise ValueError("列出目录需要提供远程路径")
            return conn.list_dir(remote_path)
            
        elif operation == "make_dir":
            if not remote_path:
                raise ValueError("创建目录需要提供远程路径")
            return conn.make_dir(remote_path)
            
        elif operation == "remove_file":
            if not remote_path:
                raise ValueError("删除文件需要提供远程路径")
            return conn.remove_file(remote_path)
            
        elif operation == "remove_dir":
            if not remote_path:
                raise ValueError("删除目录需要提供远程路径")
            return conn.remove_dir(remote_path)
            
        else:
            raise ValueError(f"不支持的操作: {operation}")
            
    except Exception as e:
        logger.error(f"SSH操作失败: {str(e)}")
        raise
    finally:
        # 不关闭连接，留给连接池管理
        pass


# 使用示例
if __name__ == "__main__":
    os.environ["SSH_HOST"] = "192.168.1.50"
    os.environ["SSH_USERNAME"] = "root"
    os.environ["SSH_PASSWORD"] = "123456"
    host = os.getenv("SSH_HOST")  # 虚拟机IP地址
    username = os.getenv("SSH_USERNAME")  # 虚拟机用户名
    password = os.getenv("SSH_PASSWORD")  # 虚拟机密码

    # 使用类接口的示例
    try:
        with SSHConnection.get_connection(host, username, password) as conn:
    # 执行命令示例
            output, error, status = conn.execute_command("docker ps")
            print(f"命令输出: {output}")

            # 上传文件示例
            # conn.upload_file("../assets/images/realm.svg", "/usr/local/1.svg")

    # 列出目录内容示例
            # files = conn.list_dir("/usr/local")
    # for file in files:
    #     print(file)
    except Exception as e:
        print(f"操作失败: {str(e)}")

    # 使用兼容旧接口的示例
    # result = ssh_operation(host, username, password, "execute_command", content="docker ps")
    # print("命令输出:", result)
