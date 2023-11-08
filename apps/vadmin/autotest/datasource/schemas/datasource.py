#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/8 11:35
# @Author   : 冉勇
# @File     : datasource.py
# @Software : PyCharm
# @Desc     : 数据源增删改查
from pydantic import BaseModel, ConfigDict, field_validator

from core.data_types import DatetimeStr


class DataSource(BaseModel):
    data_name: str
    type: int
    host: str
    port: int
    user: str
    password: str
    create_user_id: int

    @field_validator('type')
    def validate_status_priority(cls, value):
        if value not in {1}:
            raise ValueError("type必须是1,目前只支持mysql类型")
        return value


class DataSourceSimpleOut(DataSource):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
