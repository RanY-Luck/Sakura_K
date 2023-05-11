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
    问题列表分页查询
    代码解释：
    定义了一个名为IssueParams的Pydantic模型类，用于表示问题列表分页查询的参数。
    该类继承自FastAPI框架自带的QueryParams类，重写了初始化方法，添加了一些用于查询参数的属性。
    其中，通过super()调用父类的初始化方法，将请求中传来的params参数解析出当前页码、页面大小等信息。
    接着，该类中定义了v_order和v_order_field两个属性，分别用于指定查询结果排序的方向和字段。
    is_active、title和category_id三个属性用于指定查询过滤条件，对应的是问题是否可见、问题标题和问题所属的类别ID。
    在初始化方法中，这些属性分别被赋予了传入的参数值或None，其中title属性使用元组表示一个查询条件，属性值为"like"和传入的title参数。
    这样，在后续查询中，可以使用这些参数作为筛选条件和排序信息，进行数据查询和返回。
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
    问题分类列表分页查询
    代码解释：
    定义了一个名为IssueCategoryParams的Pydantic模型类，用于表示问题分类列表分页查询的参数。
    该类继承自FastAPI框架自带的QueryParams类，重写了初始化方法，添加了一些用于查询参数的属性。
    其中，通过super()调用父类的初始化方法，将请求中传来的params参数解析出当前页码、页面大小等信息。
    接着，该类中定义了v_order和v_order_field两个属性，分别用于指定查询结果排序的方向和字段。
    is_active、platform和name三个属性用于指定查询过滤条件，对应的是分类是否可见、分类所属的平台和分类名称。
    在初始化方法中，这些属性分别被赋予了传入的参数值或None，其中name属性使用元组表示一个查询条件，属性值为"like"和传入的name参数。
    这样，在后续查询中，可以使用这些参数作为筛选条件和排序信息，进行数据查询和返回。
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
