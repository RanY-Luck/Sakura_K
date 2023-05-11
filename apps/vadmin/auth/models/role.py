#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/17 19:37
# @Author  : 冉勇
# @Site    :
# @File    : role.py
# @Software: PyCharm
# @desc    : 角色模型
from sqlalchemy.orm import relationship
from sqlalchemy_utils import aggregated
from .user import VadminUser
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, func
from .m2m import vadmin_user_roles, vadmin_role_menus


class VadminRole(BaseModel):
    """
    代码解释：
    定义了一个名为vadmin_auth_role的角色表
    name: 角色名称，长度为50个字符。
    role_key: 权限字符，长度为50个字符。
    disabled: 是否禁用，布尔类型，默认为False。
    order: 排序，整数类型，可为空。
    desc: 描述信息，长度为255个字符，可为空。
    is_admin: 是否为超级角色，布尔类型，默认为False。
    users: 表示与用户表之间的多对多关系，通过vadmin_user_roles联接表关联。
    menus: 表示与菜单表之间的多对多关系，通过vadmin_role_menus联接表关联。
    此外，该ORM模型还定义了一个装饰器，使用@aggregated来修饰函数user_total_number。
    这个函数将以聚合的方式返回用户总数，函数使用了func.count(VadminUser.id)来计算用户数量。
    在使用该ORM模型查询角色表数据时，可以使用该函数来返回统计信息。
    """
    __tablename__ = "vadmin_auth_role"
    __table_args__ = ({'comment': '角色表'})
    name = Column(String(50), index=True, nullable=False, comment="名称")
    role_key = Column(String(50), index=True, nullable=False, comment="权限字符")
    disabled = Column(Boolean, default=False, comment="是否禁用")
    order = Column(Integer, comment="排序")
    desc = Column(String(255), comment="描述")
    is_admin = Column(Boolean, comment="是否为超级角色", default=False)
    users = relationship("VadminUser", back_populates='roles', secondary=vadmin_user_roles)
    menus = relationship("VadminMenu", back_populates='roles', secondary=vadmin_role_menus)

    @aggregated('users', Column(Integer, default=0, comment="用户总数"))
    def user_total_number(self):
        return func.count(VadminUser.id)
