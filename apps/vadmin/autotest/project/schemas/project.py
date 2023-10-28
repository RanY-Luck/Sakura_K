#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/23 17:12
# @Author   : 冉勇
# @File     : project.py
# @Software : PyCharm
# @Desc     :

from pydantic import BaseModel, ConfigDict, validator

from apps.vadmin.auth.schemas import UserSimpleOut
from core.data_types import DatetimeStr


class Project(BaseModel):
    project_name: str
    responsible_name: str
    test_user: str
    dev_user: str
    publish_app: str
    simple_desc: str
    remarks: str
    config_id: int
    product_id: int
    create_user_id: int
    create_user: str  # 如果报错 改成int

    @validator(
        'project_name', 'responsible_name', 'test_user', 'dev_user', 'publish_app', 'simple_desc', 'remarks',
        'create_user', pre=True, always=True
    )
    def validate_string_fields(cls, value):
        if len(value) > 100:
            raise ValueError("不能超过100个字符")
        return value

    @validator('config_id', 'product_id', 'create_user_id', pre=True, always=True)
    def validate_positive_integer(cls, value):
        if value < 0:
            raise ValueError("必须为正整数")
        return value


class ProjectSimpleOut(Project):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class ProjectOut(ProjectSimpleOut):
    model_config = ConfigDict(from_attributes=True)
    create_user: UserSimpleOut


class ProjectDel(Project):
    model_config = ConfigDict(from_attributes=True)
    is_delete: bool
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
