#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/12 17:10
# @Author   : 冉勇
# @File     : path_conf.py
# @Software : PyCharm
# @Desc     :
from pathlib import Path

# 项目根目录
BASE_PATH = Path(__file__).resolve().parent.parent

# 插件目录
PLUGIN_DIR = BASE_PATH / 'plugin'
