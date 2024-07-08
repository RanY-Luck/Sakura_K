#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:36
# @Author  : 冉勇
# @Site    : 
# @File    : cors_middleware.py
# @Software: PyCharm
# @desc    : 跨域
import time
from utils.log_util import logger
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware


def add_cors_middleware(app: FastAPI):
    # 前端页面url
    origins = [
        "http://localhost:80",
        "http://127.0.0.1:80"
    ]

    # 后台api允许跨域
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )


def write_request_log(request: Request, response: Response):
    http_version = f"http/{request.scope['http_version']}"
    content_length = response.raw_headers[0][1]
    process_time = response.headers["X-Process-Time"]
    content = f"basehttp.log_message: '{request.method} {request.url} {http_version}' {response.status_code}" \
              f"{response.charset} {content_length} {process_time}"
    logger.info(content)


def register_request_log_middleware(app: FastAPI):
    """
    记录请求日志中间件
    :param app:
    :return:
    """

    @app.middleware("http")
    async def request_log_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        write_request_log(request, response)
        return response
