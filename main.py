#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/27 19:50
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    : 主程序入口

"""
FastApi 更新文档：https://github.com/tiangolo/fastapi/releases
FastApi Github：https://github.com/tiangolo/fastapi
Typer 官方文档：https://typer.tiangolo.com/
"""

import asyncio

import click
import typer
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles  # 依赖安装：pip install aiofiles

from application import settings
from application import urls
from core.docs import custom_api_docs
from core.event import lifespan
from core.exception import register_exception
from scripts.create_app.main import CreateApp
from scripts.initialize.initialize import InitializeData, Environment
from utils.tools import import_modules

shell_app = typer.Typer()


def create_app():
    """
    启动项目
    docs_url：配置交互文档的路由地址，如果禁用则为None，默认为 /docs
    redoc_url： 配置 Redoc 文档的路由地址，如果禁用则为None，默认为 /redoc
    openapi_url：配置接口文件json数据文件路由地址，如果禁用则为None，默认为/openapi.json
    :return:
    """
    app = FastAPI(
        title="sakura_k",  # 标题
        version=settings.VERSION,  # 版本号
        description=settings.PROJECT_DESCRIPTION,  # Swagger描述
        lifespan=lifespan,  # 指定了应用程序的生命周期管理器
        docs_url=None,
        redoc_url=None
    )
    # 调用了 import_modules 函数来导入指定的中间件，该函数接受三个参数：modules 表示要导入的模块列表，message 表示当前导入的模块的消息，
    # app 表示 FastAPI 应用程序对象的引用。在这里，modules 和 message 都是 settings.MIDDLEWARES 和 "中间件"，而 app 则是传入的参数。
    import_modules(settings.MIDDLEWARES, "中间件", app=app)
    # 函数中调用了 register_exception 函数来注册全局异常捕获处理。
    register_exception(app)
    # 如果配置了跨域，使用 CORSMiddleware 中间件来解决跨域问题。
    if settings.CORS_ORIGIN_ENABLE:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.ALLOW_ORIGINS,
            allow_credentials=settings.ALLOW_CREDENTIALS,
            allow_methods=settings.ALLOW_METHODS,
            allow_headers=settings.ALLOW_HEADERS
        )
    # 此外，如果启用了静态文件服务，使用 StaticFiles 中间件来挂载静态目录。
    if settings.STATIC_ENABLE:
        app.mount(settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT))
    # 引入应用中的路由
    for url in urls.urlpatterns:
        # 最后，使用 include_router 方法来引入应用程序中的路由。
        app.include_router(url["ApiRouter"], prefix=url["prefix"], tags=url["tags"])
    # 配置接口文档静态资源
    custom_api_docs(app)
    return app


@shell_app.command()
def run(
        host: str = typer.Option(default='0.0.0.0', help='监听主机IP，默认开放给本网络所有主机'),
        port: int = typer.Option(default=9000, help='监听端口')
):
    """
    启动项目
    :return:
    """
    click.echo(settings.BANNER)
    uvicorn.run(app='main:create_app', host=host, port=port, lifespan="on", factory=True)


@shell_app.command()  # 装饰器将该函数注册为命令行命令。当用户在命令行中输入 python main.py init 时，就会执行该函数。
def init(env: Environment = Environment.pro):
    """
    初始化数据
    比如要初始化开发环境，那么env参数应该为 dev，并且 application/settings.DEBUG 应该 = True
    比如要初始化生产环境，那么env参数应该为 pro，并且 application/settings.DEBUG 应该 = False
    :param env: 指定数据库环境 如果没有提供该参数，则默认为 Environment.pro。
    :return:
    """
    print("开始初始化数据")
    data = InitializeData()
    asyncio.run(data.run(env))


@shell_app.command()
def migrate(env: Environment = Environment.pro):
    """
    将模型迁移到数据库，更新数据库表结构
    :param env: 指定数据库环境。如果没有提供该参数，则默认为 Environment.pro。
    :return:
    """
    print("开始更新数据库表")
    InitializeData.migrate_model(env)


@shell_app.command()  # 该函数注册为命令行命令。当用户在命令行中输入 python main.py init_app <path> 时，就会执行该函数。
def init_app(path: str):
    """
    自动创建初始化APP结构
    命令例子：python main.py init-app vadmin/test
    :param path: app路径，根目录为apps，填写apps后面路径即可，例子：vadmin/auth
    :return:
    """
    print(f"开始创建并初始化{path}APP")
    app = CreateApp(path)
    app.run()


if __name__ == '__main__':
    shell_app()
