#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/6 19:52
# @Author  : 冉勇
# @Site    : 
# @File    : scheduler_test.py
# @Software: PyCharm
# @desc    : 测试定时任务
from datetime import datetime


def job(*args, **kwargs):
    """
    定时任务执行同步函数示例
    """
    print(args)
    print(kwargs)
    print(f"{datetime.now()}执行了")


async def async_job(*args, **kwargs):
    """
    定时任务执行异步函数示例
    """
    print(args)
    print(kwargs)
    print(f'{datetime.now()}异步函数执行了')
