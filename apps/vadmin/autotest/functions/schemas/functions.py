#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2023/11/8 11:11
# @Author   : 冉勇
# @File     : functions.py
# @Software : PyCharm
# @Desc     :
from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class Functions(BaseModel):
    function_name: str
    remarks: str
    project_id: int | None = None
    content: str
    func_type: str | None = None
    func_tags: str | None = None
    create_user_id: int


class FunctionsSimpleOut(Functions):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
