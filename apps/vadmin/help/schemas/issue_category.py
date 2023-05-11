#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 16:47
# @Author  : 冉勇
# @Site    :
# @File    : issue_category.py
# @Software: PyCharm
# @desc    : 常见问题类别
from typing import Optional
from pydantic import BaseModel, Field
from core.data_types import DatetimeStr
from apps.vadmin.auth.schemas import UserSimpleOut
"""
代码解释：
定义了一些Pydantic模型类，用于表示问题分类相关的数据结构。
首先定义了一个IssueCategory模型类，包含了问题分类的各种属性，如分类名称、所属平台、是否启用等。这些属性都是可选的，并且可以设置默认值为None。其中，user_id属性用于指定该分类的创建者，也是可选的。
接着，定义了一个IssueCategorySimpleOut模型类，继承自IssueCategory模型类，并加上了分类ID、创建时间和修改时间三个属性。这些属性都使用DatetimeStr类型来表示时间字符串，具有更好的可读性。
同时，使用了Config类中的orm_mode = True参数，以便在后续操作中能够方便地将数据库查询结果转换成该模型类的实例。
另外，定义了一个IssueCategoryListOut模型类，继承自IssueCategorySimpleOut模型类，并添加了创建者信息user属性。
user属性使用了apps.vadmin.auth.schemas模块中的UserSimpleOut模型类，用于表示简单的用户信息。
同样，使用了Config类中的orm_mode = True参数，以方便将数据库查询结果转换成该模型类的实例。
最后，定义了一个IssueCategoryOptionsOut模型类，用于表示选择框和下拉菜单中的选项。
该模型类包含两个字段，分别是标签label和对应的值value。
这里使用了Field(alias="name")和Field(alias="id")来重命名model类中的字段，以便与数据库中的列名匹配。
同样地，使用了Config类中的orm_mode = True参数以方便将数据库查询结果转换成该模型类的实例。
"""

class IssueCategory(BaseModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    is_active: Optional[bool] = None

    user_id: Optional[int] = None


class IssueCategorySimpleOut(IssueCategory):
    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr

    class Config:
        orm_mode = True


class IssueCategoryListOut(IssueCategorySimpleOut):
    user: UserSimpleOut

    class Config:
        orm_mode = True


class IssueCategoryOptionsOut(BaseModel):
    label: str = Field(alias='name')
    value: int = Field(alias='id')

    class Config:
        orm_mode = True
