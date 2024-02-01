"""
@Project : Sakura_K
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


class RedBook(BaseModel):
    __tablename__ = "red_book"
    __table_args__ = ({'comment': '小红书素材表'})

    tags: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="标签")
    title: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="作品标题")
    describe: Mapped[str] = mapped_column(String(512), index=False, nullable=False, comment="作品描述")
    type: Mapped[str] = mapped_column(String(10), index=True, nullable=False, comment="作品类型")
    affiliation: Mapped[str] = mapped_column(String(10), index=False, nullable=False, comment="ID归属地")
    release_time: Mapped[datetime] = mapped_column(DateTime, index=False, nullable=False, comment="发布时间")
    auth_name: Mapped[str] = mapped_column(String(50), index=False, nullable=False, comment="作者昵称")
    url: Mapped[str] = mapped_column(String(255), index=False, nullable=False, comment="下载地址")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="是否可见")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
