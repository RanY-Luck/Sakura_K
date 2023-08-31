#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 19:14
# @Author  : 冉勇
# @Site    :
# @File    : login.py
# @Software: PyCharm
# @desc    : pydantic 模型，用于数据库序列化操作

"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
定义了两个 Pydantic 模型， LoginRecord 和 LoginRecordSimpleOut。
LoginRecord 是一个基础模型，它包含了一些登录记录的基本信息。
这些信息包括电话号码（telephone）、登录状态（status）、登录 IP 地址（ip）、登录地址（address）、浏览器信息（browser）、
操作系统信息（system）、响应信息（response）、请求信息（request）、邮政编码（postal_code）、区号（area_code）、
国家（country）、省份（province）、城市（city）、县/区（county）、运营商（operator）和登录方式（login_method）。
其中，telephone 和 status 属性是必需的，其他属性都是可选的。
LoginRecordSimpleOut 继承了 LoginRecord，并扩展了三个属性：id、create_datetime 和 update_datetime。
其中，id 属性表示登录记录的唯一标识，create_datetime 属性表示登录记录的创建时间，update_datetime 属性表示登录记录的更新时间。这三个属性都是必需的。
LoginRecordSimpleOut 的 Config 类中设置了 orm_mode = True，这表示该模型可以被用作 SQLAlchemy ORM 模型的返回类型。
这样可以确保返回的数据符合 SQLAlchemy ORM 模型的属性要求。
"""

from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class LoginRecord(BaseModel):
    telephone: str
    status: bool
    ip: str | None = None
    address: str | None = None
    browser: str | None = None
    system: str | None = None
    response: str | None = None
    request: str | None = None
    postal_code: str | None = None
    area_code: str | None = None
    country: str | None = None
    province: str | None = None
    city: str | None = None
    county: str | None = None
    operator: str | None = None
    platform: str | None = None
    login_method: str | None = None


class LoginRecordSimpleOut(LoginRecord):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr