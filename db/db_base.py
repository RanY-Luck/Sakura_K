#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 19:48
# @Author  : 冉勇
# @Site    : 
# @File    : db_base.py
# @Software: PyCharm
# @desc    : 数据库公共ORM模型
"""
这里介绍下alembic，他的作用是：
1、创建、修改和删除数据库表结构；
2、管理约束和索引；
3、生成可重复的数据库 schema 版本；
4、自动执行 schema 迁移，保证数据库 schema 和代码的一致性；
5、支持多个数据库引擎（如 MySQL、PostgreSQL、SQLite 等）；
6、支持多个开发环境（如开发、测试、生产环境等）。
使用 Alembic 可以有效地管理数据库 schema 的变化，避免手动修改数据库 schema 带来的错误和不一致，同时也方便了多个开发人员之间的协作。
官方网址：https://hellowac.github.io/alembic_doc/zh/_front_matter.html
"""

from core.database import Model
from sqlalchemy import Column, DateTime, Integer, func, Boolean


class BaseModel(Model):
    """
    公共ORM模型，基表
    代码解释：
    id: 表示该表的主键 ID，Integer 类型，primary_key = True 表示该字段为该表的主键，unique = True 表示唯一性约束，nullable = False 表示该字段不能为空；
    create_datetime: 表示该记录的创建时间，DateTime 类型，server_default=func.now() 表示默认值为当前时间；
    update_datetime: 表示该记录的最近一次更新时间，DateTime 类型，server_default=func.now() 表示默认值为当前时间，onupdate=func.now() 表示每次更新都会自动更新该字段为当前时间；
    delete_datetime: 表示该记录的删除时间，DateTime 类型，nullable=True 表示该字段可以为空；
    is_delete: 表示该记录是否已经被软删除，Boolean 类型，default=False 表示默认为未删除状态。
    这些字段为所有基于 BaseModel 的子模型提供了基础的表结构，也方便了在多个表中共用相同的字段。
    """
    __abstract__ = True
    id = Column(Integer, primary_key=True, unique=True, comment="主键ID", index=True, nullable=False)
    create_datetime = Column(DateTime, server_default=func.now(), comment="创建时间")
    update_datetime = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
    delete_datetime = Column(DateTime, nullable=True, comment="删除时间")
    is_delete = Column(Boolean, default=False, comment="是否软删除")
