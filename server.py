#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:31
# @Author  : 冉勇
# @Site    : 
# @File    : server.py
# @Software: PyCharm
# @desc    :
from contextlib import asynccontextmanager
from time import sleep
from sub_applications.handle import handle_sub_applications
from utils.common_util import worship, panel
from utils.log_util import logger
from fastapi import FastAPI
from config.env import AppConfig, PROJECT_DESCRIPTION
from config.get_db import init_create_table
from config.get_redis import RedisUtil
from config.get_scheduler import SchedulerUtil
from exceptions.handle import handle_exception
from middlewares.handle import handle_middleware
from router import router_manager
from mcp_server.ai_websocket import init_ai_websocket


# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 该函数用于管理FastAPI应用的生命周期，包括启动和关闭时的初始化和清理操作
    try:
        logger.info(f"{AppConfig.app_name}开始启动")
        # 启动 Banner
        await worship()
        sleep(0.1)
        # 初始化数据库
        await init_create_table()
        # 初始化Redis连接池
        app.state.redis = await RedisUtil.create_redis_pool()
        # 初始化系统字典和系统参数
        await RedisUtil.init_sys_dict(app.state.redis)
        # 初始化系统参数
        await RedisUtil.init_sys_config(app.state.redis)
        # 初始化定时任务
        await SchedulerUtil.init_system_scheduler()
        # 初始化AI WebSocket
        await init_ai_websocket(app)
        # 挂载子应用
        handle_sub_applications(app)
        logger.info(f"{AppConfig.app_name}启动成功")
        sleep(0.1)
        await panel()
        yield
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
    finally:
        await RedisUtil.close_redis_pool(app)
        await SchedulerUtil.close_system_scheduler()


# 初始化FastAPI对象
app = FastAPI(
    title=AppConfig.app_name,  # 项目名称
    description=PROJECT_DESCRIPTION,  # Swagger描述
    version=AppConfig.app_version,  # 版本号
    lifespan=lifespan  # 生命周期事件
)

# 加载中间件处理方法
handle_middleware(app)
# 加载全局异常处理方法
handle_exception(app)
# 加载路由列表
app.include_router(router_manager.register_router())
