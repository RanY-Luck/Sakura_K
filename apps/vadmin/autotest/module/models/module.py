#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/23 17:11
# @Author   : 冉勇
# @File     : module.py
# @Software : PyCharm
# @Desc     : 模块列表

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class ModuleInfo(BaseModel):
    __tablename__ = "module_info"
    __table_args__ = ({'comment': '模块列表'})

    module_name: Mapped[str] = mapped_column(String(64), nullable=False, comment="模块名称")
    test_user: Mapped[str] = mapped_column(String(100), comment="测试人员")
    simple_desc: Mapped[str] = mapped_column(String(100), comment="描述")
    remarks: Mapped[str] = mapped_column(String(100), comment="备注")
    module_packages: Mapped[str] = mapped_column(String(64), comment="模块对应的包名称")
    leader_user: Mapped[str] = mapped_column(String(100), comment="负责人")
    priority: Mapped[int] = mapped_column(Integer, comment="默认执行用例优先级", default=4)

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
