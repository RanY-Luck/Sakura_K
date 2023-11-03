#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/3 17:09
# @Author   : 冉勇
# @File     : functions.py
# @Software : PyCharm
# @Desc     : 自定义函数查询
from fastapi import Depends

from core.dependencies import Paging, QueryParams


class FunctionsParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str | None = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ('like', name)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
