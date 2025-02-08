#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:48
# @Author   : 冉勇
# @File     : gen_config.py
# @Software : PyCharm
# @Desc     :
class GenConfig:
    def __init__(self):
        pass

    # 作者
    author: str = '冉勇'
    # 默认生成包路径 system 需改成自己的模块名称 如 system monitor tool
    packageName: str = ''
    # 自动去除表前缀，默认是false
    autoRemovePre: bool = False
    # 表前缀（生成类名不会包含表前缀，多个用逗号分隔）
    tablePrefix: str = 'sys_'
    # 是否允许生成文件覆盖到本地（自定义路径），默认不允许
    allowOverwrite: bool = False
