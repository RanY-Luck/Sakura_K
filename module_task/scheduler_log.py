#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/6 10:29
# @Author  : 冉勇
# @Site    : 
# @File    : scheduler_log.py
# @Software: PyCharm
# @desc    : 定时任务-删除、打包日志
from utils.log_util import archive_and_delete_yesterdays_logs


async def log():
    archive_and_delete_yesterdays_logs()
