#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:34
# @Author  : 冉勇
# @Site    : 
# @File    : dict_type.py
# @Software: PyCharm
# @desc    : 查询参数-类依赖项
"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends
from core.dependencies import Paging, QueryParams


class DictTypeParams(QueryParams):
    """
    字典类型查询参数并提供模糊查询
    代码解释：
    DictTypeParams类用于处理字典类型的查询参数，包括了dict_name、dict_type和params三个参数。
    其中，dict_name表示字典类型名称，可以为None；dict_type表示字典类型的分类，可以为None；params表示页面分页的参数，使用了依赖注入的方式进行传递。
    在初始化函数中，调用了父类的构造函数，并将params作为参数传递给父类。
    同时，也给新的参数dict_name和dict_type赋值，并对其进行了一些特殊处理。
    其中，对于dict_name和dict_type参数，通过元组加字符串的形式，将其封装成了一个特殊的查询条件，表示需要进行模糊匹配。
    """

    def __init__(self, dict_name: str = None, dict_type: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.dict_name = ("like", dict_name)
        self.dict_type = ("like", dict_type)
