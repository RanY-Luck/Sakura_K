#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/31 11:11
# @Author   : 冉勇
# @File     : testcase.py
# @Software : PyCharm
# @Desc     : 测试用例表
from sqlalchemy import String, Integer, ForeignKey, BigInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class TestCase(BaseModel):
    __tablename__ = "test_case"
    __table_args__ = ({'comment': '测试用例表'})

    case_name: Mapped[str] = mapped_column(String(255), nullable=True, comment="用例名称", index=True)
    project_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="所属项目")
    remarks: Mapped[str] = mapped_column(String(255), comment="备注")
    headers: Mapped[JSON] = mapped_column(JSON, nullable="场景请求头")
    variables: Mapped[JSON] = mapped_column(JSON, comment="场景变量")
    step_data: Mapped[JSON] = mapped_column(JSON, comment="场景步骤")
    step_rely: Mapped[int] = mapped_column(Integer, comment="步骤依赖 0:不依赖|1:依赖")
    version: Mapped[int] = mapped_column(Integer, comment="版本", default=0)
    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
