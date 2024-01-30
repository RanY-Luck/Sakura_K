#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/30 17:40
# @Author   : 冉勇
# @File     : redbook.py
# @Software : PyCharm
# @Desc     : 小红书表

from datetime import datetime

from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from db.db_base import BaseModel


class RedBook(BaseModel):
    __tablename__ = "red_book"
    __table_args__ = ({'comment': '小红书资源表'})

    tags: Mapped[str] = mapped_column(String(512), index=True, nullable=False, comment="标签")
    title: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="作品标题")
    describe: Mapped[str] = mapped_column(String(512), index=False, nullable=False, comment="作品描述")
    type: Mapped[str] = mapped_column(String(10), index=True, nullable=False, comment="作品类型")
    affiliation: Mapped[str] = mapped_column(String(10), index=False, nullable=False, comment="ID归属地")
    release_time: Mapped[datetime] = mapped_column(DateTime, index=False, nullable=False, comment="发布时间")
    auth_name: Mapped[str] = mapped_column(String(50), index=False, nullable=False, comment="作者昵称")
    url: Mapped[str] = mapped_column(String(255), index=False, nullable=False, comment="下载地址")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否可见")
