#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 18:15
# @Author  : 冉勇
# @Site    : 
# @File    : dependencies.py
# @Software: PyCharm
# @desc    : 常用依赖项


"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""

import copy

from fastapi import Body


class QueryParams:

    def __init__(self, params=None):
        if params:
            self.page = params.page
            self.limit = params.limit
            self.v_order = params.v_order
            self.v_order_field = params.v_order_field

    def dict(self, exclude: list[str] = None) -> dict:
        result = copy.deepcopy(self.__dict__)
        if exclude:
            for item in exclude:
                try:
                    del result[item]
                except KeyError:
                    pass
        return result

    def to_count(self, exclude: list[str] = None) -> dict:
        params = self.dict(exclude=exclude)
        del params["page"]
        del params["limit"]
        del params["v_order"]
        del params["v_order_field"]
        return params


class Paging(QueryParams):
    """
    列表分页
    """

    def __init__(self, page: int = 1, limit: int = 20, v_order_field: str = None, v_order: str = None):
        super().__init__()
        self.page = page
        self.limit = limit
        self.v_order = v_order
        self.v_order_field = v_order_field


class IdList:
    """
    id 列表
    """

    def __init__(self, ids: list[int] = Body(..., title="ID 列表")):
        self.ids = ids
