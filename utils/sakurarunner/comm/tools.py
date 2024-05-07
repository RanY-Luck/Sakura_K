#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/7 14:57
# @Author   : 冉勇
# @File     : tools.py
# @Software : PyCharm
# @Desc     :
import datetime
import random
import string
import time

import urllib3

# 禁用安全验证警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def module_id():
    """
    测试模块编号
    :return:
    """
    for i in range(1, 1000):
        id = 'Module_' + str(i).zfill(3) + '_'
        yield id


m_id = module_id()


def case_id():
    """
    测试用例编号
    :return:
    """
    for i in range(1, 10000):
        id = str(i).zfill(4) + '_'
        yield id


c_id = case_id()


def gen_random_string(str_len):
    """ 获取随机字符串
    """
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(str_len)
    )


def get_timestamp(str_len=13):
    """ 获取时间戳
    """
    if isinstance(str_len, int) and 0 < str_len < 17:
        return str(time.time()).replace(".", "")[:str_len]


def get_current_date(fmt="%Y-%m-%d"):
    """获取当前日期
    """
    return datetime.datetime.now().strftime(fmt)


if __name__ == '__main__':
    print(gen_random_string(3))
    print(get_timestamp())
    print(get_current_date())
