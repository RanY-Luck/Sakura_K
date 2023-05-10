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
# 日志存放目录
log_path = os.path.join(BASE_DIR, 'logs')
# 如果日志目录不存在，则自建目录
if not os.path.exists(log_path):
    os.mkdir(log_path)
# 记录日志info级别
log_path_info = os.path.join(log_path, f'info_{time.strftime("%Y-%m-%d")}.log')
# 记录日志error级别
log_path_error = os.path.join(log_path, f'error_{time.strftime("%Y-%m-%d")}.log')
# 写入日志格式：2023-04-11 16:14:00.799 | ERROR    | __main__:<module>:46 - 未从Redis中获取到配置信息，正在重新更新配置信息，重试次数：1。
"""
log_path_info:定义日志文件的路径和名称
rotation="00:00":定义日志轮转的时间点，默认为每天的00:00
retention="3 days":定义日志保存的时间，超过该时间的日志会被自动删除，默认为保存3天。
enqueue=True:定义是否在异步线程中处理日志文件，默认为True，执行异步处理，避免主线程因为日志处理而被阻塞
encoding="UTF-8":定义日志文件的编码方式，默认为UTF-8。
level="INFO":定义日志记录的级别，默认为INFO级别，即记录全部信息。
"""
info = logger.add(log_path_info, rotation="00:00", retention="3 days", enqueue=True, encoding="UTF-8", level="INFO")
error = logger.add(log_path_error, rotation="00:00", retention="3 days", enqueue=True, encoding="UTF-8", level="INFO")
