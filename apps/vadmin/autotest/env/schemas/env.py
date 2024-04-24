#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/6 15:46
# @Author   : 冉勇
# @File     : env.py
# @Software : PyCharm
# @Desc     :
from typing import List

from pydantic import BaseModel, ConfigDict

from apps.vadmin.auth.schemas import UserLoginName
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
    dns: str
    remarks: str | None = None
    headers: List[Header] = None
    env_variables: List[EnvVariable] = None
    create_user_id: int


class EnvSimpleOut(Env):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_user: UserLoginName
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
