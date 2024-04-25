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


class DataType(BaseModel):
    type_name: str | None = None
    type_id: int | None = None
    create_user_id: PositiveInt

    @field_validator('create_user_id', 'type_id')
    def validate_positive_integer(cls, value):
        if value <= 0:
            raise ValueError("必须为正整数")
        return value


class DataTypeInfo(BaseModel):
    type_name: str
    type_id: int


class DataSource(BaseModel):
    data_name: str
    type_id: PositiveInt = 1
    host: str
    port: int = 3306
    username: str
    password: str
    create_user_id: PositiveInt

    @field_validator('type_id')
    def validate_status_priority(cls, value):
        if value not in {1}:
            raise ValueError("type必须是1,目前只支持mysql类型")
        return value

    @field_validator('create_user_id', 'type_id', 'port')
    def validate_positive_integer(cls, value):
        if value <= 0:
            raise ValueError("必须为正整数")
        return value


class DataTypeSimpleOut(DataType):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_user_id: int
    create_user: UserLoginName
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class DataTypeNameSimpleOut(DataTypeInfo):
    model_config = ConfigDict(from_attributes=True)


class DataSourceSimpleOut(DataSource):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type_id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class DataSourceListOut(DataSource):
    model_config = ConfigDict(from_attributes=True)
    id: int
    type_id: int
    type: DataTypeNameSimpleOut
    create_user: UserLoginName
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
