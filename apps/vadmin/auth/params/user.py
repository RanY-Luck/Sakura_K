#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 14:19
# @Author  : 冉勇
# @Site    :
# @File    : user.py
# @Software: PyCharm
# @desc    : 用户查询--类依赖项

"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""

from fastapi import Depends, Query

from core.dependencies import Paging, QueryParams


class UserParams(QueryParams):
    """
    用户列表查询含模糊查询
    代码解释：
    定义了一个名为UserParams的类，该类继承了QueryParams类，实现了对用户列表的查询。
    同样地，通过FastAPI中的Depends注入查询参数，其中包括name、telephone、email、is_active和is_staff五个参数，以及Paging依赖项。
    在初始化方法中，首先调用了父类的初始化方法。
    然后，通过self.name将name参数赋值为('like', name)，表示进行模糊查询。
    同理，通过self.telephone将telephone参数赋值为('like', telephone)，表示进行模糊查询；
    通过self.email将email参数赋值为('like', email)，同样表示进行模糊查询。
    最后，将is_active和is_staff参数直接赋值给self.is_active和self.is_staff。
    """

    def __init__(
            self,
            name: str | None = Query(None, title="用户名称"),
            telephone: str | None = Query(None, title="手机号"),
            email: str | None = Query(None, title="邮箱"),
            is_active: bool | None = Query(None, title="是否可用"),
            is_staff: bool | None = Query(None, title="是否为工作人员"),
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.name = ("like", name)
        self.telephone = ("like", telephone)
        self.email = ("like", email)
        self.is_active = is_active
        self.is_staff = is_staff
