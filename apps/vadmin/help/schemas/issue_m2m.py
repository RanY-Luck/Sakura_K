#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 17:23
# @Author  : 冉勇
# @Site    : 
# @File    : issue_m2m.py
# @Software: PyCharm
# @desc    :
from typing import Optional, List
from pydantic import BaseModel
from core.data_types import DatetimeStr
from .issue import IssueSimpleOut

"""
代码解释：
定义了一个Pydantic模型类IssueCategoryPlatformOut，用于表示问题分类和平台相关的数据结构。
该模型类包含了一些属性，如分类名称、所属平台、是否启用、创建者ID、分类ID、创建时间、修改时间等。
这些属性都是可选的，并且可以设置默认值为None。同时，还有一个issues属性，用于表示该分类下的问题列表，并使用IssueSimpleOut模型类来表示简单的问题信息。
在模型类中，使用了Config类中的orm_mode = True参数，以便在后续操作中能够方便地将数据库查询结果转换成该模型类的实例。
同时，该模型类中的issues属性使用了List[IssueSimpleOut]类型，表示问题列表是一个由多个IssueSimpleOut实例组成的列表。
"""


class IssueCategoryPlatformOut(BaseModel):
    name: Optional[str] = None
    platform: Optional[str] = None
    is_active: Optional[bool] = None
    user_id: Optional[int] = None
    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr
    issues: Optional[List[IssueSimpleOut]] = None

    class Config:
        orm_mode = True
