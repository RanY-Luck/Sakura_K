#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/7 15:26
# @Author   : 冉勇
# @File     : base.py
# @Software : PyCharm
# @Desc     :
import typing
from enum import Enum, IntEnum

from pydantic import HttpUrl

Name = str
Url = str
BaseUrl = typing.Union[HttpUrl, str]
Headers = typing.Dict[str, str]
Cookies = typing.Dict[str, str]
Env = typing.Dict[str, typing.Any]


class MethodEnum(str, Enum):
    """
    请求方法枚举
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class TStepTypeEnum(str, Enum):
    """
    步骤类型枚举
    """
    api = "api"
    case = "case"
    wait = "wait"
    script = "script"
    sql = "sql"


class TStepResultStatusEnum(str, Enum):
    """
    步骤数据状态
    """
    success = "SUCCESS"
    fail = "FAIL"
    skip = "SKIP"
    error = "ERROR"


class ExtractTypeEnum(str, Enum):
    """
    提取类型枚举
    """
    JsonPath = "JsonPath"
    jmespath = "jmespath"
    variable_or_func = "variable_or_func"
    RequestHeaders = "request_headers"
    ResponseHeaders = "response_headers"


class CheckModeEnum(str, Enum):
    """校验模式枚举"""
    JsonPath = "JsonPath"
    jmespath = "jmespath"
    variable_or_func = "variable_or_func"
    RequestHeaders = "request_headers"
    ResponseHeaders = "response_headers"


class BodyType(IntEnum):
    """body类型"""
    none = 0
    json = 1
    form = 2
    x_form = 3
    raw = 4
