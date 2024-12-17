#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/2 11:51
# @Author  : 冉勇
# @Site    : 
# @File    : database.py
# @Software: PyCharm
# @desc    :
"""
导入SQLAlchemy 部分
安装： pip install sqlalchemy[asyncio]
官方文档：https://docs.sqlalchemy.org/en/20/intro.html#installation
"""
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase


class Base(AsyncAttrs, DeclarativeBase):
    """
    创建基本映射类
    稍后，我们将继承该类，创建每个 ORM 模型
    """
    pass
