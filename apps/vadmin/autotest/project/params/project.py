#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/23 17:53
# @Author   : 冉勇
# @File     : project.py
# @Software : PyCharm
# @Desc     : 项目分页
from fastapi import Depends

from core.dependencies import Paging, QueryParams


class ProjectParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            name: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.filename = ('like', name)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
