#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 14:37
# @Author  : 冉勇
# @Site    : 
# @File    : apinfo.py
# @Software: PyCharm
# @desc    : 接口管理表
from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class ApiInfo(BaseModel):
    __tablename__ = "api_info"
    __table_args__ = ({'comment': '接口管理表'})

    api_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="用例名称", index=True)
    project_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="所属项目")
    module_id: Mapped[int] = mapped_column(Integer, nullable=False, comment="所属模块")
    status: Mapped[int] = mapped_column(Integer, comment="用例状态：10 生效 20 失效", default=10)
    priority: Mapped[int] = mapped_column(Integer, comment="优先级", default=3)
    tags: Mapped[JSON] = mapped_column(JSON, comment="用例标签")
    url: Mapped[str] = mapped_column(String(255), nullable=False, comment="请求地址")
    method: Mapped[str] = mapped_column(String(255), nullable=False, comment="请求方式")
    remarks: Mapped[str] = mapped_column(String(255), comment="描述")
    headers: Mapped[JSON] = mapped_column(JSON, comment="请求头")
    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
