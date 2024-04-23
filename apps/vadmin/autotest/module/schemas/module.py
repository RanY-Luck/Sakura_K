#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 00:06
# @Author  : 冉勇
# @Site    : 
# @File    : module.py
# @Software: PyCharm
# @desc    :
from pydantic import BaseModel, ConfigDict, field_validator, PositiveInt

from core.data_types import DatetimeStr


class Module(BaseModel):
    module_name: str
    project_id: int
    test_user: str
    dev_user: str
    responsible_name: str
    priority: int = 4
    simple_desc: str | None = None
    remarks: str | None = None
    create_user_id: PositiveInt

    @field_validator('priority')
    def validate_priority(cls, value):
        if value < 1 or value > 4:
            raise ValueError("priority必须在1到4之间")
        return value

    @field_validator(
        'module_name', 'responsible_name', 'test_user', 'dev_user', 'simple_desc',
        'remarks'
    )
    def validate_string_fields(cls, value):
        if value is not None and len(value) > 100:
            raise ValueError("不能超过100个字符")
        return value

    @field_validator('create_user_id', 'project_id')
    def validate_positive_integer(cls, value):
        if value <= 0:
            raise ValueError("必须为正整数")
        return value


class ModuleSimpleOut(Module):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
