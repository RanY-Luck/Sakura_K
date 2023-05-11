#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 11:11
# @Author  : 冉勇
# @Site    :
# @File    : menu.py
# @Software: PyCharm
# @desc    : 菜单模型
from sqlalchemy.orm import relationship
from .m2m import vadmin_role_menus
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey


class VadminMenu(BaseModel):
    __tablename__ = "vadmin_auth_menu"
    __table_args__ = ({'comment': '菜单表'})
    """
    代码解释：
    义了一个名为VadminMenu的ORM模型，表示菜单表。该表包括以下字段：
    title: 菜单标题，长度为50个字符。
    icon: 菜单图标，长度为50个字符，可为空。
    redirect: 重定向地址，长度为100个字符，可为空。
    component: 前端组件地址，长度为50个字符，可为空。
    path: 前端路由地址，长度为50个字符，可为空。
    disabled: 是否禁用，布尔类型，默认为False。
    hidden: 是否隐藏，布尔类型，默认为False。
    order: 排序，整数类型，可为空。
    menu_type: 菜单类型，字符串类型，长度为8个字符，可为空。
    parent_id: 父菜单，在本表中与id相关联，通过ForeignKey外键实现关联关系，可为空。
    perms: 权限标识，字符串类型，长度为50个字符，可为空，可重复，可加索引。
    noCache: 如果设置为True，则不会被<keep-alive>缓存，默认为False。
    breadcrumb: 如果设置为False，则不会在breadcrumb面包屑中显示，默认为True。
    affix: 如果设置为True，则会一直固定在tag项中，默认为False。
    noTagsView: 如果设置为True，则不会出现在tag中，默认为False。
    canTo: 设置为True即使hidden为True，也依然可以进行路由跳转，默认为False。
    alwaysShow: 关于嵌套模式的显示规则，如果想不管路由下面的children声明的个数都显示你的根路由，可以设置alwaysShow为True，这样它就会忽略之前定义的规则，一直显示根路由，默认为True。
    此外，该ORM模型还定义了一个属性roles，表示与角色表之间的多对多关系，通过vadmin_role_menus联接表关联。
    """
    title = Column(String(50), index=True, nullable=False, comment="名称")
    icon = Column(String(50), comment="菜单图标")
    redirect = Column(String(100), comment="重定向地址")
    component = Column(String(50), comment="前端组件地址")
    path = Column(String(50), comment="前端路由地址")
    disabled = Column(Boolean, default=False, comment="是否禁用")
    hidden = Column(Boolean, default=False, comment="是否隐藏")
    order = Column(Integer, comment="排序")
    menu_type = Column(String(8), comment="菜单类型")
    parent_id = Column(ForeignKey("vadmin_auth_menu.id", ondelete='CASCADE'), comment="父菜单")
    perms = Column(String(50), comment="权限标识", unique=False, nullable=True, index=True)
    noCache = Column(Boolean, comment="如果设置为true，则不会被 <keep-alive> 缓存(默认 false)", default=False)
    breadcrumb = Column(Boolean, comment="如果设置为false，则不会在breadcrumb面包屑中显示(默认 true)", default=True)
    affix = Column(Boolean, comment="如果设置为true，则会一直固定在tag项中(默认 false)", default=False)
    noTagsView = Column(Boolean, comment="如果设置为true，则不会出现在tag中(默认 false)", default=False)
    canTo = Column(Boolean, comment="设置为true即使hidden为true，也依然可以进行路由跳转(默认 false)", default=False)
    alwaysShow = Column(Boolean, comment="""当你一个路由下面的 children 声明的路由大于1个时，自动会变成嵌套的模式，
    只有一个时，会将那个子路由当做根路由显示在侧边栏，若你想不管路由下面的 children 声明的个数都显示你的根路由，
    你可以设置 alwaysShow: true，这样它就会忽略之前定义的规则，一直显示根路由(默认 true)""", default=True)
    roles = relationship("VadminRole", back_populates='menus', secondary=vadmin_role_menus)
