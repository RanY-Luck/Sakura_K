#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/10/23 17:12
# @Author   : 冉勇
# @File     : project.py
# @Software : PyCharm
# @Desc     :

from pydantic import BaseModel, ConfigDict

from apps.vadmin.auth.schemas import UserSimpleOut
from core.data_types import DatetimeStr


class Project(BaseModel):
    project_name: str
    test_user: str = None
    responsible_name: str = None
    dev_user: str = None
    publish_app: str = None
    simple_desc: str = None
    remarks: str = None
    config_id: int = None
    product_id: int = None

    create_user_id: int


class ProjectSimpleOut(Project):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class ProjectOut(ProjectSimpleOut):
    model_config = ConfigDict(from_attributes=True)
    create_user: UserSimpleOut
