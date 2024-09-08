#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:36
# @Author  : 冉勇
# @Site    : 
# @File    : cors_middleware.py
# @Software: PyCharm
# @desc    : 跨域相关
import time
from utils.log_util import logger
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI):
    """
    添加跨域中间件

    :param app: FastAPI对象
    :return:
    """
    origins = [
        "http://localhost:80",
        "http://127.0.0.1:80"
        "http://localhost:9088",
        "http://127.0.0.1:9088"
    ]
    # 前端页面url

    # 后台api允许跨域
    app.add_middleware(
        # 跨域中间件
        CORSMiddleware,
        # 允许跨域的url
        allow_origins=origins,
        # 允许跨域请求携带cookie
        allow_credentials=True,
        # 允许跨域请求的方法
        allow_methods=["*"],
        # 允许跨域请求的header
        allow_headers=["*"]
    )


def write_request_log(request: Request, response: Response):
    """
    写入log
    """
    # 请求方法
    http_version = f"http/{request.scope['http_version']}"
    # 请求内容
    content_length = response.raw_headers[0][1]
    # 处理时间
    process_time = response.headers["X-Process-Time"]
    # 日志内容
    content = f"basehttp.log_message:\n '请求方法:{request.method} 请求地址:{request.url} {http_version}' 状态码:{response.status_code} {response.charset} {content_length} 耗时:{process_time}秒"
    logger.info(content)


def register_request_log_middleware(app: FastAPI):
    """
    记录请求日志中间件
    :param app:
    :return:
    """

    # 请求日志中间件
    @app.middleware("http")
    async def request_log_middleware(request: Request, call_next):
        # 请求开始时间
        start_time = time.time()
        # 调用下一个中间件
        response = await call_next(request)
        # 请求结束时间
        process_time = time.time() - start_time
        # 写入日志
        response.headers["X-Process-Time"] = str(process_time)
        # 写入日志
        write_request_log(request, response)
        # 返回响应
        return response
