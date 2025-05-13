#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 22:00
# @Author  : 冉勇
# @Site    :
# @File    : ssh_client.py
# @Software: PyCharm
# @desc    : SSH客户端核心类
import threading
import paramiko
from typing import Dict, Tuple
from utils.log_util import logger


class SSHClient:
    """SSH客户端类，管理与远程服务器的连接"""

    # 连接池 - 存储所有活跃的SSH连接
    _connections: Dict[str, 'SSHClient'] = {}
    _lock = threading.Lock()

    @classmethod
    def get_connection(
            cls, host: str, username: str, password: str = None,
            port: int = 22, timeout: int = 10
    ) -> 'SSHClient':
        """
        获取或创建SSH连接
        :param host: 主机地址
        :param username: 用户名
        :param password: 密码（可选）
        :param port: SSH端口，默认22
        :param timeout: 连接超时时间（秒）
        :return: SSHClient实例
        """
        conn_key = f"{username}@{host}:{port}"

        with cls._lock:
            if conn_key in cls._connections:
                conn = cls._connections[conn_key]
                if conn.is_active():
                    return conn
                else:
                    # 连接断开，删除旧连接
                    logger.info(f"连接已断开，重新创建: {conn_key}")
                    del cls._connections[conn_key]

            # 创建新连接
            conn = cls(host, username, password, port, timeout)
            cls._connections[conn_key] = conn
            return conn

    def __init__(
            self, host: str, username: str, password: str = None,
            port: int = 22, timeout: int = 10
    ):
        """
        初始化SSH连接
        :param host: 主机地址
        :param username: 用户名
        :param password: 密码（可选）
        :param port: SSH端口，默认22
        :param timeout: 连接超时时间（秒）
        """
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
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
                'timeout': self.timeout,
                'allow_agent': False,
                'look_for_keys': False
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
        """
        检查连接是否活跃
        :return: 如果连接活跃返回True，否则返回False
        """
        if not self.client:
            return False

        try:
            transport = self.client.get_transport()
            if transport and transport.is_active():
                # 发送一个简单命令测试连接
                try:
                    self.client.exec_command('echo 1', timeout=5)
                    return True
                except Exception:
                    return False
            return False
        except Exception:
            return False

    def reconnect(self) -> bool:
        """
        重新连接到服务器
        :return: 如果重连成功返回True，否则返回False
        """
        try:
            self.close()
            self._connect()
            return True
        except Exception as e:
            logger.error(f"重新连接失败: {str(e)}")
            return False

    def close(self) -> None:
        """关闭连接"""
        if self.sftp:
            try:
                self.sftp.close()
            except Exception as e:
                logger.warning(f"关闭SFTP连接时出错: {str(e)}")
            finally:
                self.sftp = None

        if self.client:
            try:
                self.client.close()
            except Exception as e:
                logger.warning(f"关闭SSH连接时出错: {str(e)}")
            finally:
                self.client = None
        # 从连接池中移除
        conn_key = f"{self.username}@{self.host}:{self.port}"
        with self._lock:
            if conn_key in self._connections:
                del self._connections[conn_key]

        logger.info(f"已关闭与服务器 {self.username}@{self.host}:{self.port} 的连接")

    def execute_command(
            self, command: str, timeout: int = 60
    ) -> Tuple[str, str, int]:
        """
        执行远程命令
        :param command: 要执行的命令
        :param timeout: 命令超时时间（秒）
        :return: 元组 (标准输出, 标准错误, 退出码)
        """
        if not self.is_active():
            self.reconnect()

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

    def __enter__(self):
        """支持上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文时关闭连接"""
        self.close()

    @classmethod
    def test_connection(
            cls, host: str, username: str, password: str = None,
            port: int = 22, timeout: int = 5
    ) -> Tuple[bool, str]:
        """
        测试SSH连接是否可用
        :param host: 主机地址
        :param username: 用户名
        :param password: 密码（可选）
        :param port: SSH端口，默认22
        :param timeout: 连接超时时间（秒）
        :return: 元组 (是否成功, 错误信息)
        """
        client = None
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            connect_kwargs = {
                'hostname': host,
                'username': username,
                'port': port,
                'timeout': timeout,
                'allow_agent': False,
                'look_for_keys': False
            }

            if password:
                connect_kwargs['password'] = password

            client.connect(**connect_kwargs)

            # 执行简单命令确认连接正常
            stdin, stdout, stderr = client.exec_command('echo "Connection Test"', timeout=timeout)
            exit_code = stdout.channel.recv_exit_status()

            if exit_code == 0:
                return True, ""
            else:
                error = stderr.read().decode('utf-8')
                return False, f"连接测试失败: {error}"

        except Exception as e:
            return False, f"连接失败: {str(e)}"

        finally:
            if client:
                client.close()


if __name__ == "__main__":
    # 简单测试
    try:
        host = "192.168.1.50"
        username = "root"
        password = "123456"
        # 测试连接
        success, error = SSHClient.test_connection(host, username, password)
        print(f"连接测试结果: {'成功' if success else '失败'}")
        if not success:
            print(f"错误: {error}")
        # 执行命令
        with SSHClient.get_connection(host, username, password) as ssh_client:
            output, error, status = ssh_client.execute_command("ls -la")
            print(f"命令状态: {status}")
            print(f"输出:\n{output}")
            if error:
                print(f"错误:\n{error}")

    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")
