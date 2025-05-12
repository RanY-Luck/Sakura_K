#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:12
# @Author  : 冉勇
# @Site    : 
# @File    : message_util.py
# @Software: PyCharm
# @desc    : 短信验证码工具类
from utils.log_util import logger


def message_service(sms_code: str):
    logger.info(f"短信验证码为{sms_code}")
