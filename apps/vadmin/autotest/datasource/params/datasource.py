#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/3 17:06
# @Author   : 冉勇
# @File     : datasource.py
# @Software : PyCharm
# @Desc     : 数据源管理查询
from fastapi import Depends

from core.dependencies import Paging, QueryParams


class DataSourceParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            data_name: str | None = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.data_name = ('like', data_name)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"

