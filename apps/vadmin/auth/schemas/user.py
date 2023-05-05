#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 14:54
# @Author  : 冉勇
# @Site    : 
# @File    : user.py
# @Software: PyCharm
# @desc    : pydantic 用户模型，用于数据库序列化操作
"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
定义了一些Pydantic模型类，用于表示用户对象和相关的数据结构。
其中，User类表示一个用户对象，包含了用户名称、电话、邮箱、昵称、头像链接、是否激活、是否是员工、性别、是否为微信服务openid等属性。
UserIn类继承自User类，新增了role_ids和password属性，用于接收一个与用户关联的角色ID列表和密码信息。这个模型类可以用于创建用户操作，方便校验参数和进行数据解析。
UserUpdateBaseInfo类和UserUpdate类表示更新用户信息的模型类，分别用于更新用户基本信息和详细信息。
UserSimpleOut类和UserOut类表示查询用户信息时返回的简单信息和详细信息。
ResetPwd类表示重置密码的模型类，包含了密码和进行二次验证的密码two字段。
check_passwords_match方法是一个验证方法，用于检查两次输入的密码是否相同。
"""
from typing import Optional, List
from pydantic import BaseModel, root_validator
from core.data_types import Telephone, DatetimeStr, Email
from .role import RoleSimpleOut


class User(BaseModel):
    name: Optional[str] = None
    telephone: Telephone
    email: Optional[Email] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False
    gender: Optional[str] = "0"
    is_wx_server_openid: Optional[bool] = False


class UserIn(User):
    """
    创建用户
    """
    role_ids: Optional[List[int]] = []
    password: Optional[str] = ""


class UserUpdateBaseInfo(BaseModel):
    """
    更新用户基本信息
    """
    name: str
    telephone: Telephone
    email: Optional[Email] = None
    nickname: Optional[str] = None
    gender: Optional[str] = "0"


class UserUpdate(User):
    """
    更新用户详细信息
    """
    name: Optional[str] = None
    telephone: Telephone
    email: Optional[Email] = None
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    is_active: Optional[bool] = True
    is_staff: Optional[bool] = False
    gender: Optional[str] = "0"
    role_ids: Optional[List[int]] = []


class UserSimpleOut(User):
    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr

    is_reset_password: Optional[bool] = None
    last_login: Optional[DatetimeStr] = None
    last_ip: Optional[str] = None

    class Config:
        orm_mode = True


class UserOut(UserSimpleOut):
    roles: Optional[List[RoleSimpleOut]] = []

    class Config:
        orm_mode = True


class ResetPwd(BaseModel):
    password: str
    password_two: str

    @root_validator
    def check_passwords_match(cls, values):
        pw1, pw2 = values.get('password'), values.get('password_two')
        if pw1 is not None and pw2 is not None and pw1 != pw2:
            raise ValueError('两次密码不一致!')
        return values
