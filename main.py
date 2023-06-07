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
import typer
import uvicorn
import asyncio
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from application import settings
from application import urls
from starlette.staticfiles import StaticFiles  # 依赖安装：pip3 install aiofiles
from core.exception import register_exception
from scripts.initialize.initialize import InitializeData, Environment
from scripts.create_app.main import CreateApp
from core.event import lifespan
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
        title="Sakura_K",  # 标题
        description="本项目基于Fastapi与Vue3+Typescript+Vite4+element-plus的基础项目 前端基于vue-element-plus-admin框架开发",
        version=settings.VERSION,  # 版本号
        lifespan=lifespan  # 指定了应用程序的生命周期管理器
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
    if settings.TEMP_ENABLE:
        app.mount(settings.TEMP_URL, app=StaticFiles(directory=settings.TEMP_DIR))
    # 引入应用中的路由
    for url in urls.urlpatterns:
        # 最后，使用 include_router 方法来引入应用程序中的路由。
        app.include_router(url["ApiRouter"], prefix=url["prefix"], tags=url["tags"])
    return app


@shell_app.command()
def run(
        host: str = typer.Option(default='0.0.0.0', help='监听主机IP，默认开放给本网络所有主机'),
        port: int = typer.Option(default=9000, help='监听端口')
):
    """
    启动项目
    :return:
    代码解释：
    该函数使用了 uvicorn.run() 函数来启动一个 ASGI 应用程序，其中：
    - app 参数指定要运行的应用程序。这里使用了字符串 "main:create_app"，表示要从 main 模块中导入 create_app 函数作为应用程序。
    - host 参数指定服务器绑定的主机名或 IP 地址，这里设置为 "0.0.0.0"，表示可以接受来自任何 IP 地址的请求。
    - port 参数指定服务器绑定的端口号，这里设置为 9000。
    - lifespan 参数指定应用程序的生命周期管理器，这里设置为 "on" 表示使用 FastAPI 的 Lifespan 生命周期管理器。
    - factory 参数指定是否使用工厂模式启动应用程序。这里设置为 True，表示使用工厂模式启动应用程序。
    """
    uvicorn.run(app='main:create_app', host=host, port=port, lifespan="on", factory=True)


@shell_app.command()  # 装饰器将该函数注册为命令行命令。当用户在命令行中输入 python main.py init 时，就会执行该函数。
def init(env: Environment = Environment.pro):
    """
    初始化数据
    :param env: 指定数据库环境 如果没有提供该参数，则默认为 Environment.pro。
    :return:
    """
    print("开始初始化数据")
    # InitializeData 是一个自定义的类，用于初始化应用程序的数据库。asyncio.run() 是一个异步函数，用于运行异步任务，这里用于异步运行 data.run(env) 方法。
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
    # InitializeData 是一个自定义的类，其中定义了一个静态方法 migrate_model，用于将模型迁移到数据库，并更新数据库表结构。
    InitializeData.migrate_model(env)


@shell_app.command()  # 该函数注册为命令行命令。当用户在命令行中输入 python main.py init_app <path> 时，就会执行该函数。
def init_app(path: str):
    """
    自动创建初始化APP结构
    :param path: app路径，根目录为apps，填写apps后面路径即可，例子：vadmin/auth
    :return:
    """
    print(f"开始创建并初始化{path}APP")
    # CreateApp 是一个自定义的类，用于自动创建和初始化 APP 的目录结构和文件。
    # 该类的 run 方法会执行一系列操作，例如创建目录，生成配置文件，安装依赖等，最终生成一个完整的 APP 目录结构和文件。
    app = CreateApp(path)
    app.run()


if __name__ == '__main__':
    shell_app()
