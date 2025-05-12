#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:33
# @Author  : 冉勇
# @Site    : 
# @File    : handle.py
# @Software: PyCharm
# @desc    : 全局挂载
from fastapi import FastAPI
from sub_applications.staticfiles import mount_staticfiles


def handle_sub_applications(app: FastAPI):
    """
    全局处理子应用挂载
    """
    # 挂载静态文件
    mount_staticfiles(app)