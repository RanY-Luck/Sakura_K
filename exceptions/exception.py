#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:39
# @Author  : 冉勇
# @Site    : 
# @File    : exception.py
# @Software: PyCharm
# @desc    : 自定义异常捕获
class LoginException(Exception):
    """
    自定义登录异常LoginException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class AuthException(Exception):
    """
    自定义令牌异常AuthException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class PermissionException(Exception):
    """
    自定义权限异常PermissionException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message


class ModelValidatorException(Exception):
    """
    自定义模型校验异常ModelValidatorException
    """

    def __init__(self, data: str = None, message: str = None):
        self.data = data
        self.message = message
