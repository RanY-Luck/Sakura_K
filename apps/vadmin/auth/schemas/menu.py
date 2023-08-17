# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 14:24
# @Author  : 冉勇
# @Site    :
# @File    : menu.py
# @Software: PyCharm
# @desc    : pydantic 菜单模型，用于数据库序列化操作
"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
定义了几个Pydantic模型类，用于表示菜单、路由和树形结构等数据结构。
其中，Menu类表示了一个菜单项，包含了标题、图标、组件名、重定向、路径、是否禁用、是否隐藏、排序、权限、父菜单ID、菜单类型和是否总是展示等属性。
MenuSimpleOut类继承自Menu类，并新增了ID、创建时间和更新时间等属性，用于查询时返回简单的菜单信息。
Meta类表示了一个用于描述菜单或路由元数据的模型，包含了标题、图标、是否隐藏、是否缓存、是否显示面包屑、是否附加到导航栏、是否在标签视图中显示、是否可以跳转等属性。
RouterOut类表示了一个路由项，包含了名称、组件名、路径、重定向、元数据、排序和子路由等属性。children属性是一个由RouterOut对象构成的列表，表示该路由包含的子路由。
TreeListOut类继承自MenuSimpleOut类，并新增了children属性，表示该菜单项包含的子菜单，即树形结构。
其中，children属性也是一个由TreeListOut对象构成的列表，表示该菜单项包含的子菜单。
"""
from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class Menu(BaseModel):
    title: str
    icon: str | None = None
    component: str | None = None
    redirect: str | None = None
    path: str | None = None
    disabled: bool = False
    hidden: bool = False
    order: int | None = None
    perms: str | None = None
    parent_id: int | None = None
    menu_type: str
    alwaysShow: bool | None = True


class MenuSimpleOut(Menu):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class Meta(BaseModel):
    title: str
    icon: str | None = None
    hidden: bool = False
    noCache: bool | None = False
    breadcrumb: bool | None = True
    affix: bool | None = False
    noTagsView: bool | None = False
    canTo: bool | None = False
    alwaysShow: bool | None = True


# 路由展示
class RouterOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str | None = None
    component: str | None = None
    path: str
    redirect: str | None = None
    meta: Meta | None = None
    order: int | None = None
    children: list[dict] = []


class TreeListOut(MenuSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    children: list[dict] = []
