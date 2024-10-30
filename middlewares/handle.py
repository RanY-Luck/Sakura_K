#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:37
# @Author  : 冉勇
# @Site    : 
# @File    : handle.py
# @Software: PyCharm
# @desc    : 全局中间件
from fastapi import FastAPI
from middlewares.cors_middleware import add_cors_middleware, register_request_log_middleware
from middlewares.gzip_middleware import add_gzip_middleware


def handle_middleware(app: FastAPI):
    """
    全局中间件处理
    """
    # 加载跨域中间件
    add_cors_middleware(app)
    # 加载记录请求日志中间件
    register_request_log_middleware(app)
    # 加载gzip压缩中间件
    add_gzip_middleware(app)
