"""
@Project : Sakura_K
@File    : XHS-SDK.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/10/13 10:46
@Desc    : 小红书素材表
"""
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class VadminRedBook(BaseModel):
    __tablename__ = "vadmin_redbook_images"
    __table_args__ = ({'comment': '小红书素材表'})

    noteurl: Mapped[str] = mapped_column(String(255), nullable=False, comment="笔记url")
    notetype: Mapped[str | None] = mapped_column(String(8), comment="笔记类型")
    notetitle: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="笔记标题")
    notedescription: Mapped[str] = mapped_column(String(500), comment="笔记描述")
    notetags: Mapped[str] = mapped_column(String(255), comment="笔记标签")
    filename: Mapped[str] = mapped_column(String(255), nullable=False, comment="原图片名称")
    image_url: Mapped[str] = mapped_column(String(500), nullable=False, comment="图片链接")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
