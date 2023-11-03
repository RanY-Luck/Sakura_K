#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/3 17:08
# @Author   : 冉勇
# @File     : env.py
# @Software : PyCharm
# @Desc     : 环境管理查询

from fastapi import Depends

from core.dependencies import Paging, QueryParams


class EnvParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            env_name: str | None = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.env_name = ('like', env_name)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
