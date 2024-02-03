#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 14:37
# @File           : redbook.py
# @IDE            : PyCharm
# @desc           : 小红书素材表

from fastapi import Depends

from core.dependencies import Paging, QueryParams


class RedbookParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)


class UrlsParams(QueryParams):
    def __init__(self, params: Paging = Depends()):
        super().__init__(params)
