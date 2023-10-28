#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 15:17
# @Author  : 冉勇
# @Site    : 
# @File    : apinfo.py
# @Software: PyCharm
# @desc    :

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class ApInfoParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            api_name: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.api_name = ('like', api_name)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
