#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 15:20
# @Author  : 冉勇
# @Site    : 
# @File    : apinfo.py
# @Software: PyCharm
# @desc    :

from typing import Dict, List
from typing import Union
from pydantic import BaseModel, ConfigDict, field_validator

from core.data_types import DatetimeStr
from utils.sakurarunner.models.base import BodyType


class RequestHeader(BaseModel):
    key: str
    value: str
    remarks: str = ''


class RequestData(BaseModel):
    key: str
    type: str
    value: Union[str, dict]


class Request(BaseModel):
    url: str
    data: List[RequestData] = []
    method: str
    params: List = []
    upload: Dict = {}
    verify: bool = False
    cookies: Dict = {}
    headers: List[RequestHeader] = []
    timeout: int = 0
    req_json: Dict = None
    data_type: str = ''
    allow_redirects: bool = True


class ApiInfo(BaseModel):
    api_name: str
    project_id: int
    module_id: int
    status: int = 1
    priority: int = 3
    method: str
    tags: List[str]
    url: str
    description: str
    request: Request
    variables: List[Dict]
    validators: List[Dict]
    extracts: List[Dict]
    setup_hooks: List[Dict]
    teardown_hooks: List[Dict]
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
    headers: Dict = {}

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
