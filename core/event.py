#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/27 19:54
# @Author  : 冉勇
# @Site    : 
# @File    : event.py
# @Software: PyCharm
# @desc    : 全局事件
import aioredis
from fastapi import FastAPI
from application.settings import REDIS_DB_URL, MONGO_DB_URL, MONGO_DB_NAME, EVENTS
from core.mongo import db
from utils.cache import Cache
from contextlib import asynccontextmanager
from utils.tools import import_modules_async


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    :param app:
    :return:
    代码解释：
    该函数使用了异步上下文管理器的语法，使用 yield 将函数分为两部分。在 yield 之前的代码用于初始化全局事件，而在 yield 之后的代码用于析构全局事件。
    """
    # 函数调用了 import_modules_async 函数，同样传入了 EVENTS、"全局事件" 和 app 作为参数，但是 status 参数为 True，表示执行导入模块的操作。
    await import_modules_async(EVENTS, "全局事件", app=app, status=True)
    yield
    # 函数调用了 import_modules_async 函数，同样传入了 EVENTS、"全局事件" 和 app 作为参数，但是 status 参数为 False，表示执行卸载模块的操作。
    await import_modules_async(EVENTS, "全局事件", app=app, status=False)


async def connect_redis(app: FastAPI, status: bool):
    """
    把redis挂在到app对象上
    博客：https://blog.csdn.net/wgPython/article/details/107668521
    博客：https://www.cnblogs.com/emunshe/p/15761597.html
    官网：https://aioredis.readthedocs.io/en/latest/getting-started/
    Github: https://github.com/aio-libs/aioredis-py
    aioredis.from_url(url, *, encoding=None, parser=None, decode_responses=False, db=None, password=None, ssl=None,
    connection_cls=None, loop=None, **kwargs) 方法是 aioredis 库中用于从 Redis 连接 URL 创建 Redis 连接对象的方法。
    以下是该方法的参数说明：
    url：Redis 连接 URL。例如 redis://localhost:6379/0。
    encoding：可选参数，Redis 编码格式。默认为 utf-8。
    parser：可选参数，Redis 数据解析器。默认为 None，表示使用默认解析器。
    decode_responses：可选参数，是否将 Redis 响应解码为 Python 字符串。默认为 False。
    db：可选参数，Redis 数据库编号。默认为 None。
    password：可选参数，Redis 认证密码。默认为 None，表示无需认证。
    ssl：可选参数，是否使用 SSL/TLS 加密连接。默认为 None。
    connection_cls：可选参数，Redis 连接类。默认为 None，表示使用默认连接类。
    loop：可选参数，用于创建连接对象的事件循环。默认为 None，表示使用默认事件循环。
    **kwargs：可选参数，其他连接参数，用于传递给 Redis 连接类的构造函数。
    aioredis.from_url() 方法的主要作用是将 Redis 连接 URL 转换为 Redis 连接对象。
    除了 URL 参数外，其他参数用于指定 Redis 连接的各种选项，例如 Redis 数据库编号、密码、SSL/TLS 加密等等。可以根据需要选择使用这些选项。
    health_check_interval 是 aioredis.from_url() 方法中的一个可选参数，用于设置 Redis 连接的健康检查间隔时间。
    健康检查是指在 Redis 连接池中使用的连接对象会定期向 Redis 服务器发送 PING 命令来检查连接是否仍然有效。
    该参数的默认值是 0，表示不进行健康检查。如果需要启用健康检查，则可以将该参数设置为一个正整数，表示检查间隔的秒数。
    例如，如果需要每隔 5 秒对 Redis 连接进行一次健康检查，则可以将 health_check_interval 设置为 5
    :param app:
    :param status:
    :return:
    代码解释：
    首先根据参数 status 的值来判断是连接 Redis 还是关闭 Redis 缓存连接。
    如果 status 为 True，则会调用 app.state.redis 连接 Redis 缓存，传入 Redis 数据库的 URL 作为参数。
    同时，使用 aioredis.from_url 方法来创建 Redis 连接对象，并将其挂载到 FastAPI 应用程序对象的 app.state.redis 属性上。
    在连接 Redis 缓存之后，代码调用 Cache(app.state.redis).cache_tab_names() 方法，使用 Cache 类来初始化 Redis 缓存，并缓存表名。
    如果 status 为 False，则会调用 app.state.redis.close() 来关闭 Redis 连接。
    """
    if status:
        print("正在连接到Redis")
        app.state.redis = aioredis.from_url(REDIS_DB_URL, decode_responses=True, health_check_interval=1)
        await Cache(app.state.redis).cache_tab_names()
    else:
        print("正在关闭Redis")
        await app.state.redis.close()


async def connect_mongo(app: FastAPI, status: bool):
    """
    把 mongo 挂载到 app 对象上面
    博客：https://www.cnblogs.com/aduner/p/13532504.html
    mongodb 官网：https://www.mongodb.com/docs/drivers/motor/
    motor 文档：https://motor.readthedocs.io/en/stable/
    :param app:
    :param status:
    :return:
    代码解释：
    首先，函数会根据参数 status 的值来判断是连接数据库还是关闭连接。
    如果 status 为 True，则会调用 db 模块中的 connect_to_database() 函数连接数据库，传入了 MongoDB 数据库的 URL 和数据库名称作为参数。
    如果 status 为 False，则会调用 db 模块中的 close_database_connection() 函数，关闭数据库连接。
    """
    if status:
        print("正在连接到MongoDB")
        await db.connect_to_database(path=MONGO_DB_URL, db_name=MONGO_DB_NAME)
    else:
        print("正在关闭MongoDB")
        await db.close_database_connection()
