#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 15:20
# @Author  : 冉勇
# @Site    : 
# @File    : apinfo.py
# @Software: PyCharm
# @desc    :

from pydantic import BaseModel, ConfigDict, validator
from apps.vadmin.auth.schemas import UserSimpleOut
from core.data_types import DatetimeStr
from typing import Any, Dict, List


class RequestModel(BaseModel):
    url: str
    data: str
    mode: str
    method: str
    params: Dict[str, Any]
    upload: Dict[str, Any]
    verify: bool
    cookies: Dict[str, Any]
    headers: List[str]
    timeout: int
    language: str
    req_json: Dict[str, Any]
    allow_redirects: bool


class ApiInfo(BaseModel):
    api_name: str
    project_id: int
    module_id: int
    status: int
    code_id: int
    code: str
    priority: int
    tags: List[str]
    url: str
    method: str
    remarks: str
    step_type: str
    pre_steps: Dict[str, Any]
    post_steps: Dict[str, Any]
    setup_code: str
    teardown_code: str
    setup_hooks: List
    teardown_hooks: List
    headers: List
    variables: List
    validators: List
    extracts: List
    export: List
    request: RequestModel
    sql_request: Dict[str, Any]
    loop_data: Dict[str, Any]
    if_data: Dict[str, Any]
    wait_data: Dict[str, Any]
    create_user_id: int

    @validator('status', pre=True, always=True)
    def validate_status_priority(cls, value):
        if value not in {10, 20}:
            raise ValueError("status必须是10或20")
        return value

    @validator('method', pre=True, always=True)
    def validate_method(cls, value):
        valid_methods = ["GET", "POST", "PUT", "DELETE"]
        if value not in valid_methods:
            raise ValueError("无效的HTTP方法")
        return value


class ApInfoSimpleOut(ApiInfo):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class ApInfoOut(ApInfoSimpleOut):
    model_config = ConfigDict(from_attributes=True)
    create_user: UserSimpleOut


class ApInfoDel(ApiInfo):
    model_config = ConfigDict(from_attributes=True)
    is_delete: bool
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
