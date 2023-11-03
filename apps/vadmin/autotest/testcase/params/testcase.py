#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/3 17:11
# @Author   : 冉勇
# @File     : testcase.py
# @Software : PyCharm
# @Desc     : 测试用例查询
from fastapi import Depends

from core.dependencies import Paging, QueryParams


class TestCaseParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            case_name: str | None = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.case_name = ('like', case_name)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
