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

from datetime import datetime

from sqlalchemy import DateTime, Integer, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class BaseModel(Base):
    """
    公共 ORM 模型，基表,每张表都会有以下字段
    """
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment='主键ID')
    create_datetime: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), comment='创建时间')
    update_datetime: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间'
    )
    delete_datetime: Mapped[datetime | None] = mapped_column(DateTime, nullable=True, comment='删除时间')
    is_delete: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否软删除")
