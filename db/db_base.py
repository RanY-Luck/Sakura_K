#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/16 23:35
# @Author  : 冉勇
# @Site    : 
# @File    : db_base.py
# @Software: PyCharm
# @desc    :
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, String, func, inspect
from core.database import Base


# 使用命令：alembic init alembic 初始化迁移数据库环境
# 这时会生成alembic文件夹 和 alembic.ini文件
class BaseModel(Base):
    """
    公共 ORM 模型，基表
    """
    __abstract__ = True
    __mapper_args__ = {"eager_defaults": True}  # 防止 insert 插入后不刷新

    create_by: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment='创建者')
    create_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='创建时间'
    )
    update_by: Mapped[str] = mapped_column(String(64), nullable=True, default='', comment='更新者')
    update_time: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        comment='更新时间'
    )
    remark: Mapped[str] = mapped_column(String(100), nullable=True, default=None, comment='备注')

    @classmethod
    def get_column_attrs(cls) -> list:
        """
        获取模型中除 relationships 外的所有字段名称
        :return:
        """
        mapper = inspect(cls)

        # for attr_name, column_property in mapper.column_attrs.items():
        #     # 假设它是单列属性
        #     column = column_property.columns[0]
        #     # 访问各种属性
        #     print(f"属性: {attr_name}")
        #     print(f"类型: {column.type}")
        #     print(f"默认值: {column.default}")
        #     print(f"服务器默认值: {column.server_default}")

        return mapper.column_attrs.keys()

    @classmethod
    def get_attrs(cls) -> list:
        """
        获取模型所有字段名称
        :return:
        """
        mapper = inspect(cls)
        return mapper.attrs.keys()

    @classmethod
    def get_relationships_attrs(cls) -> list:
        """
        获取模型中 relationships 所有字段名称
        :return:
        """
        mapper = inspect(cls)
        return mapper.relationships.keys()
