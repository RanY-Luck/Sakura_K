#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 19:56
# @Author  : 冉勇
# @Site    : 
# @File    : validator.py
# @Software: PyCharm
# @desc    : Pydantic 模型重用验证器针对 手机号、邮箱

"""
官方文档：https://pydantic-docs.helpmanual.io/usage/validators/#reuse-validators
"""

import re


def vali_telephone(value: str) -> str:
    """
    手机号验证器
    :param value: 手机号
    :return: 手机号
    """
    if not value or len(value) != 11 or not value.isdigit():
        raise ValueError("请输入正确手机号")
    regex = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'
    if not re.match(regex, value):
        raise ValueError("请输入正确手机号")
    return value


def vali_email(value: str) -> str:
    """
    邮箱地址验证器
    :param value: 邮箱
    :return: 邮箱
    """
    if not value:
        raise ValueError("请输入邮箱地址")
    regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(regex, value):
        raise ValueError("请输入正确邮箱地址")
    return value
