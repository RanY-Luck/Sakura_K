#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/8 11:35
# @Author   : 冉勇
# @File     : datasource.py
# @Software : PyCharm
# @Desc     : 数据源增删改查
from pydantic import BaseModel, ConfigDict, field_validator, PositiveInt

from apps.vadmin.auth.schemas import UserLoginName
from core.data_types import DatetimeStr


class DataSource(BaseModel):
    data_name: str
    type_id: str
    host: str
    port: int = 3306
    user: str
    password: str
    create_user_id: PositiveInt

    @field_validator('create_user_id', 'port')
    def validate_positive_integer(cls, value):
        if value <= 0:
            raise ValueError("必须为正整数")
        return value


# 数据源信息
class SourceInfo(BaseModel):
    host: str
    port: int
    user: str
    password: str


# 查询时将密码排除
class DataSourceInfo(BaseModel):
    data_name: str
    type_id: str
    host: str
    port: int = 3306
    user: str
    create_user_id: PositiveInt


class DataSourceSimpleOut(DataSource):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type_id: str
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class DataSourceListOut(DataSourceInfo):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_user: UserLoginName
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
