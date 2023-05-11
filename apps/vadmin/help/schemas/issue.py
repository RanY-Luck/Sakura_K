#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 16:43
# @Author  : 冉勇
# @Site    :
# @File    : issue.py
# @Software: PyCharm
# @desc    : 常见问题
from typing import Optional
from pydantic import BaseModel
from core.data_types import DatetimeStr
from apps.vadmin.auth.schemas import UserSimpleOut
from .issue_category import IssueCategorySimpleOut

"""
代码解释：
定义了一些Pydantic模型类，用于表示问题相关的数据结构。
首先定义了一个Issue模型类，包含了问题的各种属性，如分类ID、创建者ID、标题、内容、浏览量、是否启用等。这些属性都是可选的，并且可以设置默认值为None。
接着，定义了一个IssueSimpleOut模型类，继承自Issue模型类，并加上了问题ID、创建时间和修改时间三个属性。
这些属性都使用DatetimeStr类型来表示时间字符串，具有更好的可读性。
同时，使用了Config类中的orm_mode = True参数，以便在后续操作中能够方便地将数据库查询结果转换成该模型类的实例。
另外，定义了一个IssueListOut模型类，继承自IssueSimpleOut模型类，并添加了创建者信息user属性和分类信息category属性。
user属性使用了apps.vadmin.auth.schemas模块中的UserSimpleOut模型类，用于表示简单的用户信息。
category属性使用了当前模块下的IssueCategorySimpleOut模型类，用于表示简单的问题分类信息。
同样，使用了Config类中的orm_mode = True参数以方便将数据库查询结果转换成该模型类的实例。
"""


class Issue(BaseModel):
    category_id: Optional[int] = None
    user_id: Optional[int] = None

    title: Optional[str] = None
    content: Optional[str] = None
    view_number: Optional[int] = None
    is_active: Optional[bool] = None


class IssueSimpleOut(Issue):
    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr

    class Config:
        orm_mode = True


class IssueListOut(IssueSimpleOut):
    user: UserSimpleOut
    category: IssueCategorySimpleOut

    class Config:
        orm_mode = True
