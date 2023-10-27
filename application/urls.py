#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/27 19:07
# @Author  : 冉勇
# @Site    : 
# @File    : urls.py
# @Software: PyCharm
# @desc    : 路由文件

from apps.vadmin.analysis.views import app as vadmin_analysis_app
from apps.vadmin.auth.utils.login import app as auth_app
from apps.vadmin.auth.views import app as vadmin_auth_app
from apps.vadmin.help.views import app as vadmin_help_app
from apps.vadmin.record.views import app as vadmin_record_app
from apps.vadmin.redbook.views import app as redbook_app
from apps.vadmin.resource.views import app as vadmin_resource_app
from apps.vadmin.system.views import app as vadmin_system_app
from apps.vadmin.workplace.views import app as vadmin_workplace_app
from apps.vadmin.autotest.project.views import app as project_app
from apps.vadmin.autotest.module.views import app as module_app

# 引入应用中的路由
urlpatterns = [
    {"ApiRouter": auth_app, "prefix": "/auth", "tags": ["系统认证"]},
    {"ApiRouter": vadmin_auth_app, "prefix": "/vadmin/auth", "tags": ["权限管理"]},
    {"ApiRouter": vadmin_system_app, "prefix": "/vadmin/system", "tags": ["系统管理"]},
    {"ApiRouter": vadmin_record_app, "prefix": "/vadmin/record", "tags": ["记录管理"]},
    {"ApiRouter": vadmin_workplace_app, "prefix": "/vadmin/workplace", "tags": ["工作区管理"]},
    {"ApiRouter": vadmin_analysis_app, "prefix": "/vadmin/analysis", "tags": ["数据分析管理"]},
    {"ApiRouter": vadmin_help_app, "prefix": "/vadmin/help", "tags": ["帮助中心管理"]},
    {"ApiRouter": vadmin_resource_app, "prefix": "/vadmin/resource", "tags": ["资源管理"]},
    {"ApiRouter": redbook_app, "prefix": "/vadmin/redbook", "tags": ["小红书资源管理"]},
    {"ApiRouter": project_app, "prefix": "/vadmin/autotest/project", "tags": ["项目管理"]},
    {"ApiRouter": module_app, "prefix": "/vadmin/autotest/module", "tags": ["模块管理"]},
]
