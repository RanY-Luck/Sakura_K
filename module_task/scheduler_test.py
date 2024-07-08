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
    print(args)
    print(kwargs)
    print(f"{datetime.now()}执行了")
