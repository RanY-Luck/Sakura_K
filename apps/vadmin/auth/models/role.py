#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 19:37
# @Author  : 冉勇
# @Site    :
# @File    : role.py
# @Software: PyCharm
# @desc    : 角色模型
from sqlalchemy import String, Boolean, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.db_base import BaseModel
from .m2m import vadmin_auth_role_menus
from .menu import VadminMenu


class VadminRole(BaseModel):
    __tablename__ = "vadmin_auth_role"
    __table_args__ = ({'comment': '角色表'})

    name: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="名称")
    role_key: Mapped[str] = mapped_column(String(50), index=True, nullable=False, comment="权限字符")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    order: Mapped[int | None] = mapped_column(Integer, comment="排序")
    desc: Mapped[str | None] = mapped_column(String(255), comment="描述")
    is_admin: Mapped[bool] = mapped_column(Boolean, comment="是否为超级角色", default=False)
    menus: Mapped[set[VadminMenu]] = relationship(secondary=vadmin_auth_role_menus)
