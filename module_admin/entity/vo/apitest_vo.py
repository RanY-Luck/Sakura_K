#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/24 21:40
# @Author  : 冉勇
# @Site    : 
# @File    : apitest_vo.py
# @Software: PyCharm
# @desc    :
from pydantic import BaseModel


# 定义请求体模型
class LoginRequest(BaseModel):
    username: str
    password: str
    baseurl: str = "https://www.convercomm.com"
