#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/10/28 00:06
# @Author  : 冉勇
# @Site    : 
# @File    : module.py
# @Software: PyCharm
# @desc    :

from pydantic import BaseModel, ConfigDict
from apps.vadmin.auth.schemas import UserSimpleOut
from core.data_types import DatetimeStr


class Module(BaseModel):
    module_name: str
    project_id: int
    config_id: int
    test_user: str = None
    simple_desc: str = None
    remark: str = None
    module_packages: str = None
    leader_user: str = None
    priority: int = None


class ModuleSimpleOut(Module):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
