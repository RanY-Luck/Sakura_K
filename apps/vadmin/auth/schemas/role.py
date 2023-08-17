#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 14:39
# @Author  : 冉勇
# @Site    :
# @File    : role.py
# @Software: PyCharm
# @desc    : pydantic 角色模型，用于数据库序列化操作
"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
定义了一些Pydantic模型类，用于表示角色对象和相关的数据结构。
其中，Role类表示一个角色对象，包含了角色名称、是否禁用、排序、描述、角色键和是否为管理员等属性。
RoleSimpleOut类继承自Role类，并新增了ID、创建时间和更新时间等属性，用于查询时返回角色的简单信息。
RoleOut类继承自RoleSimpleOut类，并新增了menus属性，表示该角色对应的菜单列表。
RoleIn类也继承自Role类，但是新增了menu_ids属性，用于接收一个与角色关联的菜单ID列表。这个模型类可以用于角色的创建和更新操作，方便校验参数和进行数据解析。
RoleSelectOut类表示了一个用于下拉选择框的角色对象，包含了角色ID、名称和是否禁用等属性。
"""
from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr
from .menu import MenuSimpleOut


class Role(BaseModel):
    name: str
    disabled: bool = False
    order: int | None = None
    desc: str | None = None
    role_key: str
    is_admin: bool = False


class RoleSimpleOut(Role):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class RoleOut(RoleSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    menus: list[MenuSimpleOut] = []


class RoleIn(Role):
    menu_ids: list[int] = []


class RoleSelectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    disabled: bool
