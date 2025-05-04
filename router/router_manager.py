#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/7 17:06
# @Author   : 冉勇
# @File     : router_manager.py
# @Software : PyCharm
# @Desc     : 路由管理
import os
import importlib
from fastapi import APIRouter
from utils.log_util import logger
from module_admin.controller.api_controller import apiController
from module_admin.controller.cache_controller import cacheController
from module_admin.controller.captcha_controller import captchaController
from module_admin.controller.common_controller import commonController
from module_admin.controller.config_controller import configController
from module_admin.controller.datasource_controller import dataSourceController
from module_admin.controller.dept_controller import deptController
from module_admin.controller.dict_controller import dictController
from module_admin.controller.post_controller import postController
from module_admin.controller.job_controller import jobController
from module_admin.controller.log_controller import logController
from module_admin.controller.login_controller import loginController
from module_app.controller.app_login_controller import appLoginController
from module_admin.controller.menu_controller import menuController
from module_admin.controller.notice_controller import noticeController
from module_admin.controller.online_controller import onlineController
# 路由列表(自己写的功能)
from module_admin.controller.project_controller import projectController
from module_admin.controller.robot_controller import robotController
from module_admin.controller.role_controller import roleController
from module_admin.controller.server_controller import serverController
from module_admin.controller.user_controller import userController
from module_admin.controller.env_controller import envController
from module_admin.controller.testcase_controller import testcaseController
from module_generator.controller.gen_controller import genController
from module_website.controller.home_controller import homeRouter
from module_ssh.controller.ssh_controller import sshController
from module_admin.controller.servermanage_controller import serverManageController

# 控制器标签映射，用于自动注册时设置合适的标签
controller_tags_mapping = {
    'loginController': ['登录模块'],
    'appLoginController': ['登录模块'],
    'captchaController': ['验证码模块'],
    'userController': ['系统管理-用户管理'],
    'roleController': ['系统管理-角色管理'],
    'menuController': ['系统管理-菜单管理'],
    'deptController': ['系统管理-部门管理'],
    'postController': ['系统管理-岗位管理'],
    'dictController': ['系统管理-字典管理'],
    'configController': ['系统管理-参数管理'],
    'noticeController': ['系统管理-通知公告管理'],
    'logController': ['系统管理-日志管理'],
    'onlineController': ['系统监控-在线用户'],
    'jobController': ['系统监控-定时任务'],
    'serverController': ['系统监控-服务资源'],
    'cacheController': ['系统监控-缓存监控'],
    'commonController': ['通用模块'],
    'genController': ['代码生成'],
    'projectController': ['项目管理'],
    'robotController': ['机器人管理'],
    'dataSourceController': ['数据源管理'],
    'apiController': ['接口管理'],
    'envController': ['环境管理'],
    'testcaseController': ['测试用例管理'],
    'sshController': ['SSH远程操作'],
    'serverManageController': ['服务器管理'],
    'homeRouter': ['产品官网'],
}

# 加载路由列表 - 手动方式
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


def auto_discover_controllers():
    """
    自动发现并注册所有模块中的控制器
    """
    discovered_controllers = []
    app_discovered_controllers = []

    # 定义需要扫描的模块目录列表
    module_dirs = [
        'module_admin',
        'module_app',
        'module_website',
        'module_ssh',
        'module_generator'
    ]

    for module_dir in module_dirs:
        # 拼接控制器目录路径
        controller_dir = f"{module_dir}/controller"

        # 检查目录是否存在
        if not os.path.isdir(controller_dir):
            logger.warning(f"目录不存在: {controller_dir}")
            continue

        # 扫描控制器目录
        for filename in os.listdir(controller_dir):
            if not filename.endswith('_controller.py'):
                continue

            # 构建模块导入路径
            module_path = f"{module_dir}.controller.{filename[:-3]}"

            try:
                # 动态导入模块
                module = importlib.import_module(module_path)

                # 查找模块中的控制器对象
                for attr_name, attr_value in module.__dict__.items():
                    # 查找类型为APIRouter的对象
                    if isinstance(attr_value, APIRouter):
                        controller_name = attr_name
                        controller = attr_value
                        # 确定controller的tags
                        if controller_name in controller_tags_mapping:
                            tags = controller_tags_mapping[controller_name]
                        else:
                            # 如果没有预设标签，则根据控制器名称生成一个默认标签
                            default_tag = controller_name.replace('Controller', '').replace('controller', '')
                            tags = [default_tag]
                        # 区分admin和app控制器
                        if module_dir == 'module_app':
                            # 为app控制器添加特殊的prefix
                            prefix = '/wechat'  # 默认前缀，可根据需要修改
                            app_discovered_controllers.append(
                                {
                                    'router': controller,
                                    'prefix': prefix,
                                    'tags': tags
                                }
                            )
                            logger.info(f"自动注册app控制器: {module_path}.{controller_name}")
                        else:
                            discovered_controllers.append(
                                {
                                    'router': controller,
                                    'tags': tags
                                }
                            )
                            logger.info(f"自动注册控制器: {module_path}.{controller_name}")
            except Exception as e:
                logger.error(f"加载控制器 {module_path} 时出错: {str(e)}")

    return discovered_controllers, app_discovered_controllers


def get_admin_router():
    admin_router = APIRouter(prefix="")

    # 启用自动发现控制器 (如果要使用手动方式，请注释下面两行并取消注释第三行)
    auto_controllers, _ = auto_discover_controllers()
    for controller in auto_controllers:
        admin_router.include_router(router=controller.get('router'), tags=controller.get('tags'))

    # 手动控制器注册方式 (如果要使用此方式，请取消注释下面一行并注释上面的三行)
    # for controller in controller_list:
    #     admin_router.include_router(router=controller.get('router'), tags=controller.get('tags'))

    return admin_router


def get_app_router():
    app_router = APIRouter(prefix="/api/v1")

    # 启用自动发现控制器 (如果要使用手动方式，请注释下面两行并取消注释第三行)
    _, auto_app_controllers = auto_discover_controllers()
    for controller in auto_app_controllers:
        app_router.include_router(
            router=controller.get('router'),
            prefix=controller.get('prefix'),
            tags=controller.get('tags')
        )

    # 手动控制器注册方式 (如果要使用此方式，请取消注释下面一行并注释上面的三行)
    # for controller in app_controllers:
    #     app_router.include_router(
    #         router=controller.get('router'),
    #         prefix=controller.get('prefix'),
    #         tags=controller.get('tags')
    #     )

    return app_router


def register_router():
    all_router = APIRouter()
    all_router.include_router(router=get_admin_router())
    all_router.include_router(router=get_app_router())
    return all_router
