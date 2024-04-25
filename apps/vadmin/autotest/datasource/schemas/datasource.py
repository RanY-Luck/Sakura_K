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
    type: PositiveInt = 1
    host: str
    port: int = 3306
    username: str
    password: str
    create_user_id: PositiveInt

    @field_validator('type')
    def validate_status_priority(cls, value):
        if value not in {1}:
            raise ValueError("type必须是1,目前只支持mysql类型")
        return value

    @field_validator('create_user_id', 'type', 'port')
    def validate_positive_integer(cls, value):
        if value <= 0:
            raise ValueError("必须为正整数")
        return value


class DataSourceSimpleOut(DataSource):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_user: UserLoginName
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
