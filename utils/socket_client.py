#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/12/18 16:53
# @Author   : 冉勇
# @File     : socket_client.py
# @Software : PyCharm
# @Desc     :
import socket


class SocketClient:
    """
    socket客户端操作
    """

    def __init__(self, host, str="127.0.0.1", port: int = 3636):
        """
        :param host:
        :param str:
        :param port:
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.host = host
        self.port = port

    def udp_send_message(self, message):
        """
        发送信息
        :param message:
        :return:
        """
        # 如果你想接受响应
        self.client_socket.sendto(message.encode('utf-8'), self.host, self.port)

    def close(self):
        """
        关闭socket连接
        :return:
        """
        self.client_socket.close()
