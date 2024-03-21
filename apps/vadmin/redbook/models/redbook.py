"""
@Project : sakura_k
@File    : XHS-SDK.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/10/13 10:46
@Desc    : 小红书素材表
"""
from datetime import datetime

from sqlalchemy import String, Boolean, DateTime, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class URL(BaseModel):
    __tablename__ = "red_book_urls"
    __table_args__ = ({'comment': '小红书下载链接'})

    red_book_id: Mapped[str] = mapped_column(Integer, ForeignKey("red_book.id"))
    url: Mapped[str] = mapped_column(String(255), index=False, nullable=False, comment="下载地址")


class RedBook(BaseModel):
    __tablename__ = "red_book"
    __table_args__ = ({'comment': '小红书素材表'})

    source: Mapped[str] = mapped_column(String(255), index=False, nullable=False, comment="原文地址")
    tags: Mapped[str] = mapped_column(String(255), index=True, nullable=False, comment="标签")
    title: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="作品标题")
    describe: Mapped[str] = mapped_column(String(1000), index=False, nullable=False, comment="作品描述")
    type: Mapped[str] = mapped_column(String(10), index=True, nullable=False, comment="作品类型")
    affiliation: Mapped[str] = mapped_column(String(10), index=False, nullable=False, comment="ID归属地")
    release_time: Mapped[datetime] = mapped_column(DateTime, index=False, nullable=False, comment="发布时间")
    auth_name: Mapped[str] = mapped_column(String(50), index=False, nullable=False, comment="作者昵称")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否可见")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
