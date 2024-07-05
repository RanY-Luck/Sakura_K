#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:51
# @Author  : 冉勇
# @Site    : 
# @File    : log_util.py
# @Software: PyCharm
# @desc    : 日志工具
import os
import time
from loguru import logger

# 日志路径
log_path = os.path.join(os.getcwd(), 'logs')
# 判断是否创建
if not os.path.exists(log_path):
    os.mkdir(log_path)

# 仅保存 error 日志
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

logger.add(log_path_error, rotation="50MB", encoding="utf-8", enqueue=True, compression="zip")
