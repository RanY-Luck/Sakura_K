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

from typing import List
from fastapi import Body
import copy


class QueryParams:
    def __init__(self, params=None):
        if params:
            self.page = params.page
            self.limit = params.limit
            self.v_order = params.v_order
            self.v_order_field = params.v_order_field

    def dict(self, exclude: List[str] = None) -> dict:
        """
        将对象的属性以字典形式返回
        如果传入参数 exclude（一个字符串列表），则会从结果中删除对应的属性。
        :param exclude:
        :return:
        """
        result = copy.deepcopy(self.__dict__)
        if exclude:
            for item in exclude:
                try:
                    del result[item]
                except KeyError:
                    pass
        return result

    def to_count(self, exclude: List[str] = None) -> dict:
        """
        将对象的属性以字典形式返回，但是排除 page、limit、v_order 和 v_order_field 这四个属性
        :param exclude:
        :return:
        """
        params = self.dict(exclude=exclude)
        del params["page"]
        del params["limit"]
        del params["v_order"]
        del params["v_order_field"]
        return params


class Paging(QueryParams):
    """
    列表分页
    代码解释：
    在初始化方法中，首先调用父类的初始化方法 super().__init__()，以便将父类的一些属性也初始化，
    然后为自身的属性 page、limit、v_order 和 v_order_field 赋值，参数默认值即可覆盖父类中相同名称的属性。
    """

    def __init__(
            self,
            page: int = 1,
            limit: int = 10,
            v_order_field: str = "id",
            v_order: str = None
    ):
        super().__init__()
        self.page = page
        self.limit = limit
        self.v_order = v_order
        self.v_order_field = v_order_field


class IdList:
    """
    Id列表
    """

    def __init__(self, ids: List[int] = Body(None, title="ID 列表")):
        self.ids = ids
