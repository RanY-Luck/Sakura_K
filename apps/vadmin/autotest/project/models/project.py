#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/23 15:51
# @Author   : 冉勇
# @File     : project.py
# @Software : PyCharm
# @Desc     : 项目列表

from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class ProjectInfo(BaseModel):
    __tablename__ = "project_info"
    __table_args__ = ({'comment': '项目列表'})

    project_name: Mapped[str] = mapped_column(String(10), nullable=False, comment='项目名称', index=True)
    responsible_name: Mapped[str] = mapped_column(String(10), comment='负责人')
    test_user: Mapped[str] = mapped_column(String(10), comment='测试人员')
    dev_user: Mapped[str] = mapped_column(String(10), comment='开发人员')
    publish_app: Mapped[str] = mapped_column(String(32), comment='发布应用')
    simple_desc: Mapped[str] = mapped_column(String(100), nullable=True, comment='简要描述')
    remarks: Mapped[str] = mapped_column(String(100), nullable=True, comment='备注')

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
