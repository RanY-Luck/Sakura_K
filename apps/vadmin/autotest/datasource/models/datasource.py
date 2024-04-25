#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/31 17:24
# @Author   : 冉勇
# @File     : datasource.py
# @Software : PyCharm
# @Desc     : 数据源表
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class DataType(BaseModel):
    __tablename__ = "data_type"
    __table_args__ = ({'comment': '数据源类型表'})

    type_name: Mapped[str] = mapped_column(String(10), comment="数据源名称")
    type_id: Mapped[int] = mapped_column(Integer, index=True, comment="类型：1 Mysql", default=1)
    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)


class DataSourceInfo(BaseModel):
    __tablename__ = "data_source"
    __table_args__ = ({'comment': '数据源表'})

    data_name: Mapped[str] = mapped_column(String(10), index=True, comment="数据源名称")
    host: Mapped[str] = mapped_column(String(255), comment="IP")
    port: Mapped[int] = mapped_column(Integer, comment="端口")
    username: Mapped[str] = mapped_column(String(255), comment="用户名")
    password: Mapped[str] = mapped_column(String(255), comment="密码")
    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    type_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("data_type.type_id", ondelete='RESTRICT'),
        comment="类型"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
    type: Mapped[DataType] = relationship(foreign_keys=type_id)
