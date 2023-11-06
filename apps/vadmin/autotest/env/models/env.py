#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/31 11:40
# @Author   : 冉勇
# @File     : env.py
# @Software : PyCharm
# @Desc     : 环境管理表
from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class EnvInfo(BaseModel):
    __tablename__ = "env_management"
    __table_args__ = ({'comment': '环境管理表'})

    env_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="环境名称", index=True)
    dns: Mapped[str] = mapped_column(String(255), comment="环境域名")
    remarks: Mapped[str] = mapped_column(String(255), comment="备注")
    env_variables: Mapped[JSON] = mapped_column(JSON, comment="环境变量")
    headers: Mapped[JSON] = mapped_column(JSON, comment="环境请求头")
    data_sources: Mapped[JSON] = mapped_column(JSON, comment="数据源")
    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
