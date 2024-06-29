#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/27 19:07
# @Author  : 冉勇
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @desc    : 路由文件

import importlib
import pkgutil

# 导入视图
from apps.vadmin.analysis.views import app as vadmin_analysis_app
from apps.vadmin.auth.utils.login import app as auth_app
from apps.vadmin.auth.views import app as vadmin_auth_app
from apps.vadmin.autotest.apinfo.views import app as apinfo_app
from apps.vadmin.autotest.datasource.views import app as datasource_app
from apps.vadmin.autotest.env.views import app as env_app
from apps.vadmin.autotest.functions.views import app as functions_app
from apps.vadmin.autotest.module.views import app as module_app
from apps.vadmin.autotest.project.views import app as project_app
from apps.vadmin.autotest.testcase.views import app as testcase_app
from apps.vadmin.help.views import app as vadmin_help_app
from apps.vadmin.record.views import app as vadmin_record_app
from apps.vadmin.redbook.views import app as red_book_app
from apps.vadmin.resource.views import app as vadmin_resource_app
from apps.vadmin.system.views import app as vadmin_system_app
from apps.vadmin.workplace.views import app as vadmin_workplace_app
from apps.vadmin.monitor.server import app as vadmin_server_app
from apps.vadmin.monitor.redis import app as vadmin_redis_app

# 引入应用中的路由
urlpatterns = [
    {"ApiRouter": auth_app, "prefix": "/auth", "tags": ["系统认证"]},
    {"ApiRouter": vadmin_auth_app, "prefix": "/vadmin/auth", "tags": ["权限管理"]},
    {"ApiRouter": vadmin_server_app, "prefix": "/vadmin/monitors", "tags": ["服务器监控"]},
    {"ApiRouter": vadmin_redis_app, "prefix": "/vadmin/monitors", "tags": ["服务器监控"]},
    {"ApiRouter": vadmin_system_app, "prefix": "/vadmin/system", "tags": ["系统管理"]},
    {"ApiRouter": vadmin_record_app, "prefix": "/vadmin/record", "tags": ["记录管理"]},
    {"ApiRouter": vadmin_workplace_app, "prefix": "/vadmin/workplace", "tags": ["工作区管理"]},
    {"ApiRouter": vadmin_analysis_app, "prefix": "/vadmin/analysis", "tags": ["数据分析管理"]},
    {"ApiRouter": vadmin_help_app, "prefix": "/vadmin/help", "tags": ["帮助中心管理"]},
    {"ApiRouter": vadmin_resource_app, "prefix": "/vadmin/resource", "tags": ["资源管理"]},
    {"ApiRouter": project_app, "prefix": "/vadmin/autotest/project", "tags": ["项目管理"]},
    {"ApiRouter": module_app, "prefix": "/vadmin/autotest/module", "tags": ["模块管理"]},
    {"ApiRouter": apinfo_app, "prefix": "/vadmin/autotest/apinfo", "tags": ["接口管理"]},
    {"ApiRouter": env_app, "prefix": "/vadmin/autotest/env", "tags": ["环境管理"]},
    {"ApiRouter": testcase_app, "prefix": "/vadmin/autotest/testcase", "tags": ["测试用例管理"]},
    {"ApiRouter": functions_app, "prefix": "/vadmin/autotest/functions", "tags": ["自定义函数管理"]},
    {"ApiRouter": datasource_app, "prefix": "/vadmin/autotest/datasource", "tags": ["数据源管理"]},
    {"ApiRouter": red_book_app, "prefix": "/vadmin/redbook", "tags": ["小红书素材"]},
]
# 导入apps.quant模块的所有子模块的.model模块
apps = importlib.import_module('apps')
for _, app_name, _ in pkgutil.iter_modules(apps.__path__):
    if app_name == "vadmin":
        continue
    quant_module = importlib.import_module(f'apps.{app_name}')
    for _, module_name, _ in pkgutil.iter_modules(quant_module.__path__):
        module = importlib.import_module(f'apps.{app_name}.{module_name}.views')
        # 导入模块中的所有类
        for attr in dir(module):
            if attr == "app":
                class_obj = getattr(module, "app")
                globals()[attr] = class_obj
                urlpatterns.append(
                    {"ApiRouter": class_obj, "prefix": f"/{app_name}/{module_name}", "tags": [module_name]}
                )
