#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 22:00
# @Author  : 冉勇
# @Site    :
# @File    : ssh_operations.py
# @Software: PyCharm
# @desc    : SSH操作类，提供文件传输等功能
import os
from utils.log_util import logger
from typing import List, Optional, Callable, Dict, Any, Tuple
from module_ssh.core.ssh_client import SSHClient


class SSHOperations:
    """SSH操作类，提供文件传输、文本操作等功能"""

    def __init__(self, ssh_client: SSHClient):
        """
        初始化SSH操作
        :param ssh_client: ssh_client: SSHClient实例
        """
        self.ssh_client = ssh_client

    @classmethod
    def from_credentials(
            cls, host: str, username: str, password: str = None,
            port: int = 22
    ) -> 'SSHOperations':
        """
        从凭据创建SSH操作实例
        :param host: 主机地址
        :param username: 用户名
        :param password: 密码（可选）
        :param port: SSH端口，默认22
        :return: SSHOperations实例
        """
        ssh_client = SSHClient.get_connection(
            host, username, password, port
        )
        return cls(ssh_client)

    def upload_file(
            self, local_path: str, remote_path: str,
            callback: Optional[Callable[[int, int], None]] = None
    ) -> bool:
        """
        上传文件到远程服务器
        :param local_path: 本地文件路径
        :param remote_path: 远程文件路径
        :param callback: 进度回调函数，参数为(已传输字节数, 总字节数)
        :return: 成功返回True，失败返回False
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
                self.ssh_client.sftp.stat(remote_dir)
            except FileNotFoundError:
                # 目录不存在，创建它
                self._mkdir_p(remote_dir)

            # 执行上传
            self.ssh_client.sftp.put(local_path, full_remote_path, callback=callback)
            logger.info(f"文件已成功上传: {local_path} -> {full_remote_path}")
            return True

        except Exception as e:
            logger.error(f"上传文件失败: {str(e)}")
            return False

    def download_file(
            self, remote_path: str, local_path: str,
            callback: Optional[Callable[[int, int], None]] = None
    ) -> bool:
        """
        从远程服务器下载文件
        :param remote_path: 远程文件路径
        :param local_path: 本地文件路径
        :param callback: 进度回调函数，参数为(已传输字节数, 总字节数)
        :return: 成功返回True，失败返回False
        """
        try:
            # 确保本地目录存在
            local_dir = os.path.dirname(local_path)
            if local_dir and not os.path.exists(local_dir):
                os.makedirs(local_dir)

            self.ssh_client.sftp.get(remote_path, local_path, callback=callback)
            logger.info(f"文件已成功下载: {remote_path} -> {local_path}")
            return True

        except Exception as e:
            logger.error(f"下载文件失败: {str(e)}")
            return False

    def write_text(self, remote_path: str, content: str) -> bool:
        """
        写入文本到远程文件
        :param remote_path: 远程文件路径
        :param content: 要写入的文本内容
        :return: 成功返回True，失败返回False
        """
        try:
            # 确保远程目录存在
            remote_dir = os.path.dirname(remote_path)
            try:
                self.ssh_client.sftp.stat(remote_dir)
            except FileNotFoundError:
                # 目录不存在，创建它
                self._mkdir_p(remote_dir)

            with self.ssh_client.sftp.file(remote_path, 'w') as f:
                f.write(content)

            logger.info(f"文本已成功写入: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"写入文本失败: {str(e)}")
            return False

    def read_text(self, remote_path: str) -> Optional[str]:
        """
        读取远程文件内容
        :param remote_path: 远程文件路径
        :return: 文件内容或None（失败时）
        """
        try:
            with self.ssh_client.sftp.file(remote_path, 'r') as f:
                content = f.read()

            if isinstance(content, bytes):
                content = content.decode('utf-8')

            logger.info(f"成功读取文件内容: {remote_path}")
            return content

        except Exception as e:
            logger.error(f"读取文件失败: {str(e)}")
            return None

    def list_dir(self, remote_path: str) -> List[str]:
        """
        列出远程目录内容
        :param remote_path: 远程目录路径
        :return: 文件和目录名列表
        """
        try:
            files = self.ssh_client.sftp.listdir(remote_path)
            logger.info(f"列出目录内容: {remote_path}")
            return files
        except Exception as e:
            logger.error(f"列出目录失败: {str(e)}")
            return []

    def get_file_info(self, remote_path: str) -> Optional[Dict[str, Any]]:
        """
        获取远程文件信息
        :param remote_path: 远程文件路径
        :return: 文件信息字典或None（失败时）
        """
        try:
            stat = self.ssh_client.sftp.stat(remote_path)
            info = {
                'size': stat.st_size,
                'uid': stat.st_uid,
                'gid': stat.st_gid,
                'mode': stat.st_mode,
                'atime': stat.st_atime,
                'mtime': stat.st_mtime
            }
            # 判断是文件还是目录
            info['is_dir'] = bool(stat.st_mode & 0o40000)
            info['is_file'] = bool(stat.st_mode & 0o100000)
            # 获取权限字符串
            mode_str = ''
            mode_str += 'd' if info['is_dir'] else '-'
            mode_str += 'r' if stat.st_mode & 0o400 else '-'
            mode_str += 'w' if stat.st_mode & 0o200 else '-'
            mode_str += 'x' if stat.st_mode & 0o100 else '-'
            mode_str += 'r' if stat.st_mode & 0o40 else '-'
            mode_str += 'w' if stat.st_mode & 0o20 else '-'
            mode_str += 'x' if stat.st_mode & 0o10 else '-'
            mode_str += 'r' if stat.st_mode & 0o4 else '-'
            mode_str += 'w' if stat.st_mode & 0o2 else '-'
            mode_str += 'x' if stat.st_mode & 0o1 else '-'

            info['mode_str'] = mode_str

            return info

        except Exception as e:
            logger.error(f"获取文件信息失败: {str(e)}")
            return None

    def make_dir(self, remote_path: str) -> bool:
        """
        创建远程目录
        :param remote_path: 远程目录路径
        :return: 成功返回True，失败返回False
        """
        try:
            self.ssh_client.sftp.mkdir(remote_path)
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
        """
        递归创建目录（类似mkdir -p）
        :param remote_path: 远程目录路径
        :return: 成功返回True，失败返回False
        """
        if remote_path == '/':
            return True

        try:
            self.ssh_client.sftp.stat(remote_path)
            return True
        except IOError:
            parent = os.path.dirname(remote_path)
            if parent and parent != '/':
                self._mkdir_p(parent)
            if remote_path != '/':
                self.ssh_client.sftp.mkdir(remote_path)
                return True

    def remove_file(self, remote_path: str) -> bool:
        """
        删除远程文件
        :param remote_path: 远程文件路径
        :return: 成功返回True，失败返回False
        """
        try:
            self.ssh_client.sftp.remove(remote_path)
            logger.info(f"成功删除文件: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"删除文件失败: {str(e)}")
            return False

    def remove_dir(self, remote_path: str, recursive: bool = False) -> bool:
        """
        删除远程目录
        :param remote_path: 远程目录路径
        :param recursive: 是否递归删除内容
        :return: 成功返回True，失败返回False
        """
        try:
            if recursive:
                files = self.list_dir(remote_path)
                for file in files:
                    file_path = os.path.join(remote_path, file)
                    file_info = self.get_file_info(file_path)

                    if file_info and file_info['is_dir']:
                        # 递归删除子目录
                        self.remove_dir(file_path, recursive=True)
                    else:
                        # 删除文件
                        self.remove_file(file_path)

            self.ssh_client.sftp.rmdir(remote_path)
            logger.info(f"成功删除目录: {remote_path}")
            return True

        except Exception as e:
            logger.error(f"删除目录失败: {str(e)}")
            return False

    def execute_command(self, command: str, timeout: int = 60) -> Tuple[str, str, int]:
        """执行远程命令
        
        Args:
            command: 要执行的命令
            timeout: 命令超时时间（秒）
            
        Returns:
            元组 (标准输出, 标准错误, 退出码)
        """
        return self.ssh_client.execute_command(command, timeout)

    def execute_script(self, script_content: str, timeout: int = 60) -> Tuple[str, str, int]:
        """
        执行远程脚本
        :param script_content: 脚本内容
        :param timeout: 命令超时时间（秒）
        :return: 元组 (标准输出, 标准错误, 退出码)
        """
        # 创建临时脚本文件
        remote_script_path = f"/tmp/temp_script_{os.urandom(4).hex()}.sh"

        try:
            # 写入脚本内容
            if not self.write_text(remote_script_path, script_content):
                return "", "无法创建临时脚本文件", -1

            # 设置脚本可执行权限
            chmod_cmd = f"chmod +x {remote_script_path}"
            _, _, exit_code = self.ssh_client.execute_command(chmod_cmd)
            if exit_code != 0:
                return "", f"无法设置脚本可执行权限: {remote_script_path}", exit_code

            # 执行脚本
            execute_cmd = f"bash {remote_script_path}"
            output, error, exit_code = self.ssh_client.execute_command(execute_cmd, timeout)

            return output, error, exit_code

        finally:
            # 清理临时脚本文件
            try:
                self.remove_file(remote_script_path)
            except Exception:
                pass


if __name__ == "__main__":
    # 简单测试
    try:
        host = "192.168.1.50"
        username = "root"
        password = "123456"

        # 创建SSH操作实例
        ssh_ops = SSHOperations.from_credentials(host, username, password)

        # 列出目录
        files = ssh_ops.list_dir("/usr/local")
        print(f"目录内容: {files}")

        # 执行命令
        output, error, status = ssh_ops.execute_command("ls -la")
        print(f"命令执行结果: {status}")
        print(output)
        # 下载文件
        ssh_ops.download_file(remote_path="/usr/local/1.jpeg", local_path="././assets/1.jpeg")
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
