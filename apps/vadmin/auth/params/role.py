#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 14:13
# @Author  : 冉勇
# @Site    :
# @File    : role.py
# @Software: PyCharm
# @desc    : 角色列表查询--类依赖项
"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends
from core.dependencies import Paging, QueryParams


class RoleParams(QueryParams):
    """
    角色列表查询含模糊查询
    代码解释：
    定义了一个名为RoleParams的类，该类继承了QueryParams类，实现了对角色列表的查询。
    通过FastAPI中的Depends注入查询参数，其中包括name、role_key和disabled三个参数，以及Paging依赖项。
    在初始化方法中，首先调用了父类的初始化方法。然后，通过self.name将name参数赋值为('like', name)，表示进行模糊查询。
    同理，通过self.role_key将role_key参数赋值为('like', role_key)，同样表示进行模糊查询。
    最后，将disabled参数直接赋值给self.disabled。
    """

    def __init__(
            self,
            name: str | None = None,
            role_key: str | None = None,
            disabled: bool | None = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.role_key = ("like", role_key)
        self.disabled = disabled
