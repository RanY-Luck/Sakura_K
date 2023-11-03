#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/31 17:57
# @Author   : 冉勇
# @File     : functions.py
# @Software : PyCharm
# @Desc     : 自定义函数表
from sqlalchemy import String, Integer, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class FunctionsInfo(BaseModel):
    __tablename__ = "functions"
    __table_args__ = ({'comment': '自定义函数表'})

    name: Mapped[str] = mapped_column(String(255), nullable=False, comment="函数名称")
    remarks: Mapped[str] = mapped_column(String(255), comment="备注")
    project_id: Mapped[int] = mapped_column(Integer, comment="关联项目")
    content: Mapped[Text] = mapped_column(Text, comment="自定义函数内容")
    func_type: Mapped[str] = mapped_column(String(50), comment="函数类型")
    func_tags: Mapped[str] = mapped_column(String(50), comment="函数标签")
    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
