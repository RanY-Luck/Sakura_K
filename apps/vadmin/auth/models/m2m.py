#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 18:06
# @Author  : 冉勇
# @Site    :
# @File    : m2m.py
# @Software: PyCharm
# @desc    : 关联中间件
"""
数据库表 操作博客：http://www.ttlsa.com/python/sqlalchemy-concise-guide/
代码解释：
以下定义了两个 SQLAlchemy 的表格对象 vadmin_user_roles 和 vadmin_role_menus
其中 vadmin_user_roles 表格定义了三个列：id 列用于标识唯一的用户角色关联 ID，user_id 列表示此行数据对应的用户 ID，role_id 表示此行数据对应的角色 ID。
这个表格的作用是用于保存用户与角色之间的多对多关系。
vadmin_role_menus 表格定义了三个列：id 列用于标识唯一的角色菜单关联 ID，role_id 列表示此行数据对应的角色 ID，ment_id 列表示对应的菜单 ID。
这个表格的作用是用于保存角色与菜单之间的多对多关系。
这两个表格都使用 Model.metadata 元数据对象作为其所属的元数据，这说明这两个表格都是继承自 db_base.Model 对象的数据库模型类。
同时，这两个表格的列都有相应的约束条件以确保列的合法性和正确性。
commmit="主键ID" 表示这个列的中文注释为“主键ID”。
unique=True 表示唯一，意味该值在整个表格不能重复
index=True 表示该列需要被索引，便于查询和检索操作。
autoincrement=True 表示这个列的值是自增的，每当有新数据插入到表格时，这个列的值会自动加 1。
"""
from db.db_base import Model
from sqlalchemy import Column, Table, Integer, ForeignKey, INT

vadmin_user_roles = Table(
    'vadmin_auth_user_roles',
    Model.metadata,
    Column("id", INT, primary_key=True, unique=True, comment='主键ID', index=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('vadmin_auth_user.id', ondelete='CASCADE'), primary_key=True),
    Column('role_id', Integer, ForeignKey('vadmin_auth_role.id', ondelete='CASCADE'), primary_key=True),
)

vadmin_role_menus = Table(
    'vadmin_auth_role_menus',
    Model.metadata,
    Column("id", INT, primary_key=True, unique=True, comment='主键ID', index=True, autoincrement=True),
    Column('role_id', Integer, ForeignKey('vadmin_auth_role.id', ondelete='CASCADE'), primary_key=True),
    Column('menu_id', Integer, ForeignKey('vadmin_auth_menu.id', ondelete='CASCADE'), primary_key=True),
)
