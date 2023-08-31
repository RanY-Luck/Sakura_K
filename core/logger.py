#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 16:03
# @Author  : 冉勇
# @Site    : 
# @File    : logger.py
# @Software: PyCharm
# @desc    : 日志记录

import os
import time

from loguru import logger

from application.settings import BASE_DIR

"""
日志配置
更多的配置参考官方文档：https://github.com/Delgan/loguru
"""

# 移除控制台输出
logger.remove(handler_id=None)

log_path = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(log_path):
    os.mkdir(log_path)

log_path_info = os.path.join(log_path, f'info_{time.strftime("%Y-%m-%d")}.log')
log_path_error = os.path.join(log_path, f'error_{time.strftime("%Y-%m-%d")}.log')

info = logger.add(log_path_info, rotation="00:00", retention="3 days", enqueue=True, encoding="UTF-8", level="INFO")
error = logger.add(log_path_error, rotation="00:00", retention="3 days", enqueue=True, encoding="UTF-8", level="ERROR")
