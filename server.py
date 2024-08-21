#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:31
# @Author  : 冉勇
# @Site    : 
# @File    : server.py
# @Software: PyCharm
# @desc    :
from fastapi import FastAPI
from contextlib import asynccontextmanager
from sub_applications.handle import handle_sub_applications
from middlewares.handle import handle_middleware
from exceptions.handle import handle_exception
from module_admin.controller.login_controller import loginController
from module_admin.controller.captcha_controller import captchaController
from module_admin.controller.user_controller import userController
from module_admin.controller.role_controller import roleController
from module_admin.controller.menu_controller import menuController
from module_admin.controller.dept_controller import deptController
from module_admin.controller.post_controler import postController
from module_admin.controller.dict_controller import dictController
from module_admin.controller.config_controller import configController
from module_admin.controller.notice_controller import noticeController
from module_admin.controller.log_controller import logController
from module_admin.controller.online_controller import onlineController
from module_admin.controller.job_controller import jobController
from module_admin.controller.server_controller import serverController
from module_admin.controller.cache_controller import cacheController
from module_admin.controller.common_controller import commonController
from config.env import AppConfig, PROJECT_DESCRIPTION
from config.get_redis import RedisUtil
from config.get_db import init_create_table
from config.get_scheduler import SchedulerUtil
from utils.log_util import logger
from utils.common_util import worship, panel


# 生命周期事件
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 该函数用于管理FastAPI应用的生命周期，包括启动和关闭时的初始化和清理操作
    try:
        logger.info(f"{AppConfig.app_name}开始启动")
        # 启动 Banner
        await worship()
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
        logger.info(f"{AppConfig.app_name}启动成功")
        await panel()
        yield
    except Exception as e:
        logger.error(f"应用启动失败: {e}")
    finally:
        await RedisUtil.close_redis_pool(app)
        await SchedulerUtil.close_system_scheduler()


# 初始化FastAPI对象
app = FastAPI(
    title=AppConfig.app_name,
    description=PROJECT_DESCRIPTION,  # Swagger描述
    version=AppConfig.app_version,
    lifespan=lifespan
)

# 挂载子应用
handle_sub_applications(app)
# 加载中间件处理方法
handle_middleware(app)
# 加载全局异常处理方法
handle_exception(app)

# 加载路由列表
controller_list = [
    {'router': loginController, 'tags': ['登录模块']},
    {'router': captchaController, 'tags': ['验证码模块']},
    {'router': userController, 'tags': ['系统管理-用户管理']},
    {'router': roleController, 'tags': ['系统管理-角色管理']},
    {'router': menuController, 'tags': ['系统管理-菜单管理']},
    {'router': deptController, 'tags': ['系统管理-部门管理']},
    {'router': postController, 'tags': ['系统管理-岗位管理']},
    {'router': dictController, 'tags': ['系统管理-字典管理']},
    {'router': configController, 'tags': ['系统管理-参数管理']},
    {'router': noticeController, 'tags': ['系统管理-通知公告管理']},
    {'router': logController, 'tags': ['系统管理-日志管理']},
    {'router': onlineController, 'tags': ['系统监控-在线用户']},
    {'router': jobController, 'tags': ['系统监控-定时任务']},
    {'router': serverController, 'tags': ['系统监控-服务资源']},
    {'router': cacheController, 'tags': ['系统监控-缓存监控']},
    {'router': commonController, 'tags': ['通用模块']},
]

for controller in controller_list:
    app.include_router(router=controller.get('router'), tags=controller.get('tags'))
