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

from pydantic import BaseModel, ConfigDict, field_validator
from pydantic_core.core_schema import FieldValidationInfo

from core.data_types import Telephone, DatetimeStr, Email
from .role import RoleSimpleOut


class User(BaseModel):
    name: str | None = None
    telephone: Telephone
    email: Email | None = None
    nickname: str | None = None
    avatar: str | None = None
    is_active: bool | None = True
    is_staff: bool | None = True
    gender: str | None = "0"
    is_wx_server_openid: bool | None = False


class UserIn(User):
    """
    创建用户
    """
    role_ids: list[int] = []
    password: str | None = ""


class UserUpdateBaseInfo(BaseModel):
    """
    更新用户基本信息
    """
    name: str
    telephone: Telephone
    email: Email | None = None
    nickname: str | None = None
    gender: str | None = "0"


class UserUpdate(User):
    """
    更新用户详细信息
    """
    name: str | None = None
    telephone: Telephone
    email: Email | None = None
    nickname: str | None = None
    avatar: str | None = None
    is_active: bool | None = True
    is_staff: bool | None = False
    gender: str | None = "0"
    role_ids: list[int] = []


class UserSimpleOut(User):
    model_config = ConfigDict(from_attributes=True)

    id: int
    update_datetime: DatetimeStr
    create_datetime: DatetimeStr

    is_reset_password: bool | None = None
    last_login: DatetimeStr | None = None
    last_ip: str | None = None


class UserOut(UserSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    roles: list[RoleSimpleOut] = []


class ResetPwd(BaseModel):
    password: str
    password_two: str

    @field_validator('password_two')
    def check_passwords_match(cls, v, info: FieldValidationInfo):
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('两次密码不一致!')
        return v
