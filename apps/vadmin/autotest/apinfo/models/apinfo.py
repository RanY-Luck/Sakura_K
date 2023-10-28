#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 14:37
# @Author  : 冉勇
# @Site    : 
# @File    : apinfo.py
# @Software: PyCharm
# @desc    : 接口管理表
from sqlalchemy import String, Integer, ForeignKey, BigInteger, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class ApiInfo(BaseModel):
    __tablename__ = "api_info"
    __table_args__ = ({'comment': '接口管理表'})

    api_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="用例名称", index=True)
    project_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="所属项目")
    module_id: Mapped[int] = mapped_column(BigInteger, nullable=False, comment="所属模块")
    status: Mapped[int] = mapped_column(Integer, comment="用例状态：10 生效 20 失效", default=10)
    code_id: Mapped[int] = mapped_column(BigInteger, comment="关联接口id")
    code: Mapped[str] = mapped_column(String(255), comment="接口code")
    priority: Mapped[int] = mapped_column(Integer, comment="优先级", default=3)
    tags: Mapped[JSON] = mapped_column(JSON, comment="用例标签")
    url: Mapped[str] = mapped_column(String(255), nullable=False, comment="请求地址")
    method: Mapped[str] = mapped_column(String(255), comment="请求方式")
    remarks: Mapped[str] = mapped_column(String(255), comment="描述")
    step_type: Mapped[str] = mapped_column(String(255), comment="步骤类型")
    pre_steps: Mapped[JSON] = mapped_column(JSON, comment="前置步骤")
    post_steps: Mapped[JSON] = mapped_column(JSON, comment="后置步骤")
    setup_code: Mapped[JSON] = mapped_column(JSON, comment="前置code")
    teardown_code: Mapped[JSON] = mapped_column(JSON, comment="后置code")
    setup_hooks: Mapped[JSON] = mapped_column(JSON, comment="前置操作")
    teardown_hooks: Mapped[JSON] = mapped_column(JSON, comment="后置操作")
    headers: Mapped[JSON] = mapped_column(JSON, comment="请求头")
    variables: Mapped[JSON] = mapped_column(JSON, comment="变量")
    validators: Mapped[JSON] = mapped_column(JSON, comment="断言规则")
    extracts: Mapped[JSON] = mapped_column(JSON, comment="提取")
    export: Mapped[JSON] = mapped_column(JSON, comment="输出")
    request: Mapped[JSON] = mapped_column(JSON, comment="请求参数")
    sql_request: Mapped[JSON] = mapped_column(JSON, comment="sql请求参数")
    loop_data: Mapped[JSON] = mapped_column(JSON, comment="循环数据")
    if_data: Mapped[JSON] = mapped_column(JSON, comment="中频存储")
    wait_data: Mapped[JSON] = mapped_column(JSON, comment="等待数据")

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
