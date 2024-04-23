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
from apps.vadmin.autotest.project.models import ProjectInfo
from db.db_base import BaseModel


class ModuleInfo(BaseModel):
    __tablename__ = "module_info"
    __table_args__ = ({'comment': '模块列表'})

    module_name: Mapped[str] = mapped_column(String(10), nullable=False, comment="模块名称", index=True)
    test_user: Mapped[str] = mapped_column(String(10), comment="测试人员")
    dev_user: Mapped[str] = mapped_column(String(10), comment="开发人员")
    responsible_name: Mapped[str] = mapped_column(String(10), comment="负责人")
    priority: Mapped[int] = mapped_column(Integer, comment="默认执行用例优先级", default=4)
    simple_desc: Mapped[str] = mapped_column(String(100), nullable=True, comment="简要描述")
    remarks: Mapped[str] = mapped_column(String(100), nullable=True, comment="备注")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    project_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("project_info.id", ondelete='CASCADE'),
        comment="对应的项目的ID"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
    project_name: Mapped[ProjectInfo] = relationship(foreign_keys=project_id)
