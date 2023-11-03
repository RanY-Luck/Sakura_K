#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/3 15:28
# @Author   : 冉勇
# @File     : api_report.py
# @Software : PyCharm
# @Desc     : 接口报告表

from sqlalchemy import String, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from apps.vadmin.auth.models import VadminUser
from db.db_base import BaseModel


class ApiReportInfo(BaseModel):
    __tablename__ = "api_report"
    __table_args__ = ({'comment': '接口测试报告表'})

    report_name: Mapped[str] = mapped_column(String(255), nullable=False, comment='报告名称', index=True)
    start_time: Mapped[DateTime] = mapped_column(DateTime, comment='执行时间')
    duration: Mapped[str] = mapped_column(String(255), comment='运行耗时')
    case_id: Mapped[int] = mapped_column(Integer, comment='执行用例id')
    run_mode: Mapped[str] = mapped_column(String(255), comment='运行模式:api 接口|case 用例')
    run_type: Mapped[int] = mapped_column(Integer, comment='运行类型:10 同步|20 异步|30 定时任务')
    success: Mapped[int] = mapped_column(Integer, comment='是否成功:成功 True|失败 False')
    run_count: Mapped[int] = mapped_column(Integer, comment='运行步骤数')
    actual_run_count: Mapped[int] = mapped_column(Integer, comment='实际步骤数')
    run_success_count: Mapped[int] = mapped_column(Integer, comment='运行成功数')
    run_fail_count: Mapped[int] = mapped_column(Integer, comment='运行失败数')
    run_skip_count: Mapped[int] = mapped_column(Integer, comment='运行跳过数')
    run_err_count: Mapped[int] = mapped_column(Integer, comment='运行错误数')
    run_log: Mapped[int] = mapped_column(Text, comment='运行日志')
    project_id: Mapped[int] = mapped_column(Integer, comment='项目id')
    module_id: Mapped[int] = mapped_column(Integer, comment='模块id')
    env_id: Mapped[int] = mapped_column(Integer, comment='运行环境')
    exec_user_id: Mapped[int] = mapped_column(Integer, comment='执行人id')
    exec_user_name: Mapped[int] = mapped_column(Integer, comment='执行人昵称')

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
