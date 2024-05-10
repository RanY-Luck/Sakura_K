#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 15:20
# @Author  : 冉勇
# @Site    : 
# @File    : apinfo.py
# @Software: PyCharm
# @desc    :

from typing import Dict, List

from pydantic import BaseModel, ConfigDict, field_validator

from core.data_types import DatetimeStr
from utils.sakurarunner.models.base import BodyType


class ApiInfo(BaseModel):
    api_name: str
    project_id: int
    module_id: int
    status: int = 1
    priority: int = 3
    tags: List[str]
    url: str
    method: str
    remarks: str
    headers: List[Dict]
    create_user_id: int

    @field_validator('status')
    def validate_status_priority(cls, value):
        if value not in {1, 0}:
            raise ValueError("status必须是1或0")
        return value

    @field_validator('method')
    def validate_method_priority(cls, value):
        valid_methods = ["GET", "POST", "PUT", "DELETE"]
        if value not in valid_methods:
            raise ValueError("method是无效的HTTP方法")
        return value


class HttpRequest(BaseModel):
    method: str
    url: str
    body: str = ''
    body_type: BodyType = BodyType.none
    headers: List[str] = []

    @field_validator('method', 'url')
    def name_not_empty(cls, v):
        if isinstance(v, str) and len(v.strip()) == 0:
            raise ValueError("不能为空")
        return v


class ApInfoSimpleOut(ApiInfo):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
