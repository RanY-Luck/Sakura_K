#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 15:25
# @Author  : 冉勇
# @Site    :
# @File    : issue.py
# @Software: PyCharm
# @desc    : 常见问题

from fastapi import Depends

from core.dependencies import Paging, QueryParams


class IssueParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            params: Paging = Depends(),
            is_active: bool = None,
            title: str = None,
            category_id: int = None
    ):
        super().__init__(params)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
        self.is_active = is_active
        self.category_id = category_id
        self.title = ("like", title)


class IssueCategoryParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            params: Paging = Depends(),
            is_active: bool = None,
            platform: str = None,
            name: str = None
    ):
        super().__init__(params)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
        self.is_active = is_active
        self.platform = platform
        self.name = ("like", name)
