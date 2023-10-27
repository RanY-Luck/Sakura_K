#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 00:02
# @Author  : 冉勇
# @Site    : 
# @File    : module.py
# @Software: PyCharm
# @desc    : 模块分页

from fastapi import Depends
from core.dependencies import Paging, QueryParams


class ModuleParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            module_name: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.module_name = ('like', module_name)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
