#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:29
# @Author  : 冉勇
# @Site    : 
# @File    : dict_detail.py
# @Software: PyCharm
# @desc    : 查询参数--类依赖项
"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends
from core.dependencies import Paging, QueryParams


class DictDetailParams(QueryParams):
    """
    字典查询参数并提供模糊查询
    代码解释：
    DictDetailParams类用于处理字典的查询参数，包括了dict_type_id、label和params三个参数。
    其中，dict_type_id表示字典类型的ID，可以为None；label表示需要模糊匹配的标签，可以为None；params表示页面分页的参数，使用了依赖注入的方式进行传递。
    在初始化函数中，调用了父类的构造函数，并将params作为参数传递给父类。
    同时，也给新的参数dict_type_id和label赋值，并对label进行了一些特殊处理。
    其中，对于label参数，通过元组加字符串的形式，将其封装成了一个特殊的查询条件，表示需要进行模糊匹配。
    """

    def __init__(self, dict_type_id: int = None, label: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.dict_type_id = dict_type_id
        self.label = ("like", label)
