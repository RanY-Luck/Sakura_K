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


class Data_Source(BaseModel):
    __tablename__ = "data_source"
    __table_args__ = ({'comment': '数据源表'})

    name: Mapped[str] = mapped_column(String(255), index=True, comment="数据源名称")
    type: Mapped[str] = mapped_column(String(255), comment="类型")
    host: Mapped[str] = mapped_column(String(255), comment="Ip")
    port: Mapped[int] = mapped_column(Integer, comment="端口")
    user: Mapped[str] = mapped_column(String(255), comment="用户名")
    password: Mapped[str] = mapped_column(String(255), comment="密码")
    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
