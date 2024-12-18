#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/19 11:24
# @Author  : 冉勇
# @Site    : 
# @File    : db_base.py
# @Software: PyCharm
# @desc    :
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
from datetime import datetime
from sqlalchemy import DateTime, Column, String
from config.database import Base


class BaseModel(Base):
    """
    公共 ORM 模型，基表,每张表都会有以下字段
    """
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}  # 防止 insert 插入后不刷新

    create_by = Column(String(64), nullable=True, default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='创建时间')
    update_by = Column(String(64), nullable=True, default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    remark = Column(String(100), nullable=True, default=None, comment='备注')

    @staticmethod
    def get_current_time():
        return datetime.now()

    # 初始化方法，继承父类的初始化参数，并在没有提供create_time和update_time时设置当前时间为默认值
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'create_time' not in kwargs:
            self.create_time = self.get_current_time()
        if 'update_time' not in kwargs:
            self.update_time = self.get_current_time()

    # 返回对象的字符串表示形式，包含对象的类名以及各个属性的值
    def __repr__(self):
        return f"<{self.__class__.__name__}(id={self.id}, create_by={self.create_by}, create_time={self.create_time}, update_by={self.update_by}, update_time={self.update_time}, remark={self.remark})>"