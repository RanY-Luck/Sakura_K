#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-05-28 18:35:00
# @Author   : 冉勇
# @File     : __init__.py
# @Software : PyCharm
# @Desc     : Text2SQL模块初始化文件

__version__ = '1.0.0'

# 导出控制器路由
from plugin.module_text2sql.controller.text2sql_controller import text2sqlController

# 方便直接导入常用类和路由
__all__ = ['text2sqlController'] 