#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/9 10:34
# @Author  : 冉勇
# @Site    : 
# @File    : gzip_middleware.py
# @Software: PyCharm
# @desc    : gzip压缩中间件
from fastapi import FastAPI
from starlette.middleware.gzip import GZipMiddleware


def add_gzip_middleware(app: FastAPI):
    """
    添加gzip压缩中间件

    :param app: FastAPI对象
    :return:
    """
    app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=9)
