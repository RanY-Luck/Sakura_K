#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 19:44
# @Author  : 冉勇
# @Site    : 
# @File    : middleware.py
# @Software: PyCharm
# @desc    : 中间件
"""
官方文档——中间件：https://fastapi.tiangolo.com/tutorial/middleware/
官方文档——高级中间件：https://fastapi.tiangolo.com/advanced/middleware/
"""
import datetime
import json
import time

from fastapi import FastAPI
from fastapi import Request, Response
from fastapi.routing import APIRoute
from user_agents import parse

from application.settings import OPERATION_RECORD_METHOD, MONGO_DB_ENABLE, IGNORE_OPERATION_FUNCTION, \
    DEMO_WHITE_LIST_PATH, DEMO
from apps.vadmin.record.crud import OperationRecordDal
from core.database import mongo_getter
from core.logger import logger
from utils.response import ErrorResponse


def write_request_log(request: Request, response: Response):
    http_version = f"http/{request.scope['http_version']}"
    content_length = response.raw_headers[0][1]
    process_time = response.headers["X-Process-Time"]
    content = f"basehttp.log_message: '{request.method} {request.url} {http_version}' {response.status_code}" \
              f"{response.charset} {content_length} {process_time}"
    logger.info(content)


def register_request_log_middleware(app: FastAPI):
    """
    记录所有HTTP请求的信息并写入请求日志
    :param app:
    :return:
    代码解释：
    在这个函数中，我们首先使用了 FastAPI 框架提供的装饰器@app.middleware("http")来将request_log_middleware函数注册为一个HTTP请求中间件。
    这个中间件函数接收两个参数：request表示HTTP请求对象，call_next是一个异步调用，用于执行下一个中间件或路由处理函数。
    在中间件函数内部，我们使用time.time()函数来获取当前时间戳，并计算出请求处理时间。
    通过 response.headers['X-Process-Time'] 将请求处理时间添加到 HTTP 响应头中，以便客户端可以查看请求的处理时间。
    最后，我们调用 write_request_log 函数来将请求和响应信息写入请求日志。
    """

    @app.middleware("http")
    async def request_log_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        write_request_log(request, response)
        return response


def register_operation_record_middleware(app: FastAPI):
    """
    记录所有具有认证的HTTP操作到MongoDB数据库中
    :param app:
    :return:
    代码解释：
    使用了 FastAPI 框架提供的装饰器@app.middleware("http")来将operation_record_middleware函数注册为一个HTTP请求中间件。
    在中间件函数内部，我们首先使用time.time()函数获取时间戳，并计算请求处理时间。
    接着，我们使用request.scope.get()方法获取 HTTP 请求对象中的认证信息，包括telephone、user_id和user_name等数据。
    我们还获取请求路由信息，如路由名称、请求方法、URL路径、请求正文、查询参数和路由标签等数据，并将这些信息保存到一个字典中。
    最终，我们将这个字典与其他请求信息一起保存到 MongoDB 数据库中。
    """

    @app.middleware("http")
    async def operation_record_middleware(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        if not MONGO_DB_ENABLE:
            return response
        telephone = request.scope.get('telephone', None)
        user_id = request.scope.get('user_id', None)
        user_name = request.scope.get('user_name', None)
        route = request.scope.get('route')
        if not telephone:
            return response
        elif request.method not in OPERATION_RECORD_METHOD:
            return response
        elif route.name in IGNORE_OPERATION_FUNCTION:
            return response
        process_time = time.time() - start_time
        user_agent = parse(request.headers.get("user-agent"))
        system = f"{user_agent.os.family} {user_agent.os.version_string}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        query_params = dict(request.query_params.multi_items())
        path_params = request.path_params
        if isinstance(request.scope.get('body'), str):
            body = request.scope.get('body')
        else:
            body = request.scope.get('body').decode()
            if body:
                body = json.loads(body)
        params = {
            "body": body,
            "query_params": query_params if query_params else None,
            "path_params": path_params if path_params else None,
        }
        content_length = response.raw_headers[0][1]
        assert isinstance(route, APIRoute)
        document = {
            "process_time": process_time,
            "telephone": telephone,
            "user_id": user_id,
            "user_name": user_name,
            "request_api": request.url.__str__(),
            "client_ip": request.client.host,
            "system": system,
            "browser": browser,
            "request_method": request.method,
            "api_path": route.path,
            "summary": route.summary,
            "description": route.description,
            "tags": route.tags,
            "route_name": route.name,
            "status_code": response.status_code,
            "content_length": content_length,
            "create_datetime": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "params": json.dumps(params)
        }
        await OperationRecordDal(mongo_getter(request)).create_data(document)
        return response

def register_demo_env_middleware(app: FastAPI):
    """
    演示环境中间件
    :param app:
    :return:
    代码解释：
    使用了 FastAPI 框架提供的装饰器@app.middleware("http")来将demo_env_middleware函数注册为一个HTTP请求中间件。
    该中间件函数首先获取请求路径信息，并根据请求方法和请求路径对请求进行处理。如果请求方法是 GET，则输出请求路径和请求方法。
    如果应用程序处于演示环境并且请求方法不是 GET 并且请求路径不在白名单中，则直接返回一个自定义响应对象，要求用户不要在演示环境中执行非法操作。
    """

    @app.middleware("http")
    async def demo_env_middleware(request: Request, call_next):
        path = request.scope.get("path")
        if request.method != "GET":
            print("路由：", path, request.method)
        if DEMO and request.method != "GET" and path not in DEMO_WHITE_LIST_PATH:
            return ErrorResponse(msg="演示环境，禁止操作")
        return await call_next(request)


def register_jwt_refresh_middleware(app: FastAPI):
    """
    JWT刷新中间件
    :param app:
    :return:
    代码解释：
    该中间件的作用是在 HTTP 请求中间拦截，并为每个响应添加一个名为 "if-refresh" 的头部信息。
    中间件接受两个参数：请求对象 Request 和一个回调函数 call_next，主要功能是将请求传递给下一个中间件或路由处理程序，并获取其返回值。
    在这个中间件中，我们从请求对象的作用域中获取了一个名为 "if-refresh" 的值，默认为 0。然后将这个值转换为字符串，并将其添加到响应头中。
    """

    @app.middleware("http")
    async def jwt_refresh_middleware(request: Request, call_next):
        response = await call_next(request)
        refresh = request.scope.get('if-refresh', 0)
        response.headers["if-refresh"] = str(refresh)
        return response
