#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/7 17:06
# @Author   : 冉勇
# @File     : router_manager.py
# @Software : PyCharm
# @Desc     : 路由管理(新版自动导入)
import os
import importlib
from fastapi import APIRouter
from utils.log_util import logger
from module_app.controller.app_login_controller import appLoginController

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
    'pluginController': ['插件管理'],
    'text2sqlController': ['文本转SQL'],
}

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
        'module_generator',
        'plugin'  # 添加plugin目录
    ]

    for module_dir in module_dirs:
        if module_dir == 'plugin':
            # 处理plugin目录下的模块
            if not os.path.isdir(module_dir):
                logger.warning(f"Plugin目录不存在: {module_dir}")
                continue

            # 遍历plugin目录下的所有模块
            for plugin_module in os.listdir(module_dir):
                plugin_module_path = os.path.join(module_dir, plugin_module)
                if not os.path.isdir(plugin_module_path) or plugin_module.startswith('__'):
                    continue

                # 拼接控制器目录路径
                controller_dir = os.path.join(plugin_module_path, 'controller')
                if not os.path.isdir(controller_dir):
                    logger.warning(f"控制器目录不存在: {controller_dir}")
                    continue

                # 扫描控制器目录
                for filename in os.listdir(controller_dir):
                    if not filename.endswith('_controller.py'):
                        continue

                    # 构建模块导入路径 - 修改这里以使用正确的导入路径
                    module_path = f"{module_dir}.{plugin_module}.controller.{filename[:-3]}"
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
                                if 'app' in module_path.lower():
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
        else:
            # 处理原有的模块目录
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
    return app_router


def register_router():
    all_router = APIRouter()
    all_router.include_router(router=get_admin_router())
    all_router.include_router(router=get_app_router())
    return all_router
