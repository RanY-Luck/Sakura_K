#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/26 16:20
# @Author   : 冉勇
# @File     : demo_generate.py
# @Software : PyCharm
# @Desc     :
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from db.db_base import BaseModel


class VadminAutomatic(BaseModel):
    __tablename__ = "vadmin_demo_generate"
    __table_args__ = ({'comment': '自动生成测试表'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="名字")
    url: Mapped[str] = mapped_column(String(255), index=True, nullable=False, comment="链接")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否可见")
