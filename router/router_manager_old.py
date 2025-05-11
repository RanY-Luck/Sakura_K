#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/7 17:06
# @Author   : 冉勇
# @File     : router_manager.py
# @Software : PyCharm
# @Desc     : 老版本路由管理(方便还原)
from fastapi import APIRouter
from module_admin.controller.api_controller import apiController
from module_admin.controller.cache_controller import cacheController
from module_admin.controller.captcha_controller import captchaController
from module_admin.controller.common_controller import commonController
from module_admin.controller.config_controller import configController
from module_admin.controller.datasource_controller import dataSourceController
from module_admin.controller.dept_controller import deptController
from module_admin.controller.dict_controller import dictController
from module_admin.controller.job_controller import jobController
from module_admin.controller.log_controller import logController
from module_admin.controller.login_controller import loginController
from module_admin.controller.menu_controller import menuController
from module_admin.controller.notice_controller import noticeController
from module_admin.controller.online_controller import onlineController
from module_admin.controller.post_controller import postController
# 路由列表
from module_admin.controller.project_controller import projectController
from module_admin.controller.robot_controller import robotController
from module_admin.controller.role_controller import roleController
from module_admin.controller.server_controller import serverController
from module_admin.controller.user_controller import userController
from module_admin.controller.env_controller import envController
from module_admin.controller.testcase_controller import testcaseController
from module_app.controller.app_login_controller import appLoginController
from module_generator.controller.gen_controller import genController
from module_website.controller.home_controller import homeRouter
from module_ssh.controller.ssh_controller import sshController
from module_admin.controller.servermanage_controller import serverManageController

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
    {'router': genController, 'tags': ['代码生成']},
    {'router': projectController, 'tags': ['项目管理']},
    {'router': robotController, 'tags': ['机器人管理']},
    {'router': dataSourceController, 'tags': ['数据源管理']},
    {'router': apiController, 'tags': ['接口管理']},
    {'router': envController, 'tags': ['环境管理']},
    {'router': testcaseController, 'tags': ['测试用例管理']},
    {'router': sshController, 'tags': ['SSH远程操作']},
    {'router': serverManageController, 'tags': ['服务器管理']},
    {'router': homeRouter, 'tags': ['产品官网']},
]

app_controllers = [
    {'router': appLoginController, 'prefix': '/wechat', 'tags': ['登录模块']},
]


def get_admin_router():
    admin_router = APIRouter(prefix="")
    for controller in controller_list:
        admin_router.include_router(router=controller.get('router'), tags=controller.get('tags'))
    return admin_router


def get_app_router():
    app_router = APIRouter(prefix="/api/v1")
    for controller in app_controllers:
        app_router.include_router(
            router=controller.get('router'), prefix=controller.get('prefix'),
            tags=controller.get('tags')
        )
    return app_router


def register_router():
    all_router = APIRouter()
    all_router.include_router(router=get_admin_router())
    all_router.include_router(router=get_app_router())
    return all_router
