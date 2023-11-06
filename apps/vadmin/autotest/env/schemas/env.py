#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/6 15:46
# @Author   : 冉勇
# @File     : env.py
# @Software : PyCharm
# @Desc     :
from typing import Any, List, Optional

from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class Header(BaseModel):
    key: str
    value: str
    remarks: str


class EnvVariable(BaseModel):
    key: str
    value: str
    remarks: str


class Env(BaseModel):
    env_name: str
    dns: Optional[str] = None
    remarks: Optional[str] = None
    headers: List[Header]
    env_variables: List[EnvVariable]
    data_sources: Any
    create_user_id: int


class EnvSimpleOut(Env):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
