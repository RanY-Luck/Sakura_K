#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/3 15:28
# @Author   : 冉勇
# @File     : api_report.py
# @Software : PyCharm
# @Desc     : 接口报告表

from sqlalchemy import String, Integer, ForeignKey, DateTime, Text, JSON, DECIMAL, Boolean
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
    success: Mapped[int] = mapped_column(Boolean, comment='是否成功:成功 True|失败 False')
    run_count: Mapped[int] = mapped_column(Integer, comment='运行步骤数')
    actual_run_count: Mapped[int] = mapped_column(Integer, comment='实际步骤数')
    run_success_count: Mapped[int] = mapped_column(Integer, comment='运行成功数')
    run_fail_count: Mapped[int] = mapped_column(Integer, comment='运行失败数')
    run_skip_count: Mapped[int] = mapped_column(Integer, comment='运行跳过数')
    run_err_count: Mapped[int] = mapped_column(Integer, comment='运行错误数')
    run_log: Mapped[Text] = mapped_column(Text, comment='运行日志')
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


class ApiReportDetail(BaseModel):
    __tablename__ = "api_test_report_detail"
    __table_args__ = ({'comment': 'API测试报告明细'})

    step_name: Mapped[str] = mapped_column(String(255), nullable=False, comment="步骤名称", index=True)
    case_id: Mapped[str] = mapped_column(String(255), comment='用例id')
    success: Mapped[int] = mapped_column(Integer, comment='是否成功: 1 成功|0 失败')
    status: Mapped[str] = mapped_column(String(255), comment='步骤状态: success 成功|fail 失败|skip 跳过')
    step_id: Mapped[str] = mapped_column(String(255), comment='步骤id')
    parent_step_id: Mapped[str] = mapped_column(String(255), comment='父级步骤id')
    step_type: Mapped[str] = mapped_column(String(255), comment='步骤类型')
    step_tag: Mapped[str] = mapped_column(String(255), comment='步骤标签: pre 前置|post 后置|controller 控制器')
    message: Mapped[Text] = mapped_column(Text, comment='步骤信息')
    variables: Mapped[JSON] = mapped_column(JSON, comment='步骤变量')
    env_variables: Mapped[JSON] = mapped_column(JSON, comment='环境变量')
    case_variables: Mapped[JSON] = mapped_column(JSON, comment='会话变量')
    session_data: Mapped[JSON] = mapped_column(JSON, comment='请求会话数据')
    export_vars: Mapped[JSON] = mapped_column(JSON, comment='导出变量')
    report_id: Mapped[int] = mapped_column(Integer, comment='报告id', index=True)
    url: Mapped[str] = mapped_column(String(255), comment='请求地址')
    method: Mapped[str] = mapped_column(String(255), comment='请求方法')
    start_time: Mapped[DateTime] = mapped_column(DateTime, comment='开始时间')
    duration: Mapped[DECIMAL] = mapped_column(DECIMAL(), comment='耗时')
    pre_hook_data: Mapped[JSON] = mapped_column(JSON, comment='前置步骤')
    post_hook_data: Mapped[JSON] = mapped_column(JSON, comment='后置步骤')
    setup_hook_results: Mapped[JSON] = mapped_column(JSON, comment='前置hook结果')
    teardown_hook_results: Mapped[JSON] = mapped_column(JSON, comment='后置hook结果')
    index: Mapped[int] = mapped_column(Integer, comment='顺序')
    status_code: Mapped[int] = mapped_column(Integer, comment='状态码')
    response_time_ms: Mapped[DECIMAL] = mapped_column(DECIMAL(), comment='响应耗时')
    elapsed_ms: Mapped[DECIMAL] = mapped_column(DECIMAL(), comment='请求耗时')
    log: Mapped[Text] = mapped_column(Text, comment='运行日志')
    exec_user_id: Mapped[int] = mapped_column(Integer, comment='执行人id')
    exec_user_name: Mapped[str] = mapped_column(String(255), comment='执行人昵称')

    create_user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_auth_user.id", ondelete='RESTRICT'),
        comment="创建人"
    )
    create_user: Mapped[VadminUser] = relationship(foreign_keys=create_user_id)
