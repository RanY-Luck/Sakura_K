#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/23 17:12
# @Author   : 冉勇
# @File     : project.py
# @Software : PyCharm
# @Desc     :

from pydantic import BaseModel, ConfigDict, field_validator, PositiveInt

from apps.vadmin.auth.schemas import UserLoginName
from core.data_types import DatetimeStr


class Project(BaseModel):
    project_name: str
    responsible_name: str
    test_user: str
    dev_user: str
    publish_app: str
    simple_desc: str | None = None
    remarks: str | None = None
    create_user_id: PositiveInt

    @field_validator(
        'project_name', 'responsible_name', 'test_user', 'dev_user', 'publish_app', 'simple_desc', 'remarks'
    )
    def validate_string_fields(cls, value):
        if value is not None and len(value) > 100:
            raise ValueError("不能超过100个字符")
        return value

    @field_validator('create_user_id')
    def validate_positive_integer(cls, value):
        if value <= 0:
            raise ValueError("必须为正整数")
        return value


class ProjectSimpleOut(Project):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_user: UserLoginName
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class Project_Name(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    project_name: str


class ProjectListOut(Project_Name):
    model_config = ConfigDict(from_attributes=True)
