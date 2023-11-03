#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/3 17:02
# @Author   : 冉勇
# @File     : api_report.py
# @Software : PyCharm
# @Desc     : api测试报告查询
from fastapi import Depends

from core.dependencies import Paging, QueryParams


class ApiReportParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            report_name: str | None = None,
            exec_user_name: str | None = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.report_name = ('like', report_name)
        self.exec_user_name = ('like', exec_user_name)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
