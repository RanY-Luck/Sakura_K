#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/28 14:54
# @Author   : 冉勇
# @File     : __init__.py
# @Software : PyCharm
# @Desc     : Text2SQL模块初始化

import os
from dotenv import load_dotenv
import logging

# 获取当前环境，默认为 'dev'
ENV = os.getenv("ENV", "dev")
env_file = f".env.{ENV}"

# 加载环境变量
try:
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        print(f"成功从 {env_file} 加载环境变量")
    else:
        print(f"警告：环境变量文件 {env_file} 不存在，使用默认值")
except Exception as e:
    print(f"加载环境变量失败：{e}") 