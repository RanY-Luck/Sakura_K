#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 18:58
# @Author  : 冉勇
# @Site    :
# @File    : sms.py
# @Software: PyCharm
# @desc    : 查询参数-类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""

from fastapi import Depends

from core.dependencies import Paging, QueryParams


class SMSParams(QueryParams):
    """
    列表分页
    """

    def __init__(self, telephone: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.telephone = ("like", telephone)
