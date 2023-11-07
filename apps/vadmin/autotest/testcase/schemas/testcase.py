#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/7 15:16
# @Author   : 冉勇
# @File     : testcase.py
# @Software : PyCharm
# @Desc     :
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator

from core.data_types import DatetimeStr


class Variable(BaseModel):
    key: str
    value: str
    remarks: str


class TestCase(BaseModel):
    case_name: str
    project_id: int
    remarks: str
    step_rely: int
    step_data: int | None = 0
    headers: List[Variable]
    variables: List[Variable]
    version: int
    create_user_id: int

    @field_validator('step_rely')
    def validate_step_rely_priority(cls, value):
        if value not in {0, 1}:
            raise ValueError("step_rely必须是0或1")
        return value


class TestCaseSimpleOut(TestCase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
