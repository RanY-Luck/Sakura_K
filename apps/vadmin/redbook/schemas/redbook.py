#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 10:24
# @File           : redbook.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作

from datetime import datetime
from typing import Optional, List

from fastapi import Query
from pydantic import BaseModel, ConfigDict, Field

from core.data_types import DatetimeStr


class Redbook(BaseModel):
    tags: str = Field(..., title="标签")
    title: str = Field(..., title="作品标题")
    describe: str = Field(..., title="作品描述")
    type: str = Field(..., title="作品类型")
    affiliation: str = Field(..., title="ID归属地")
    release_time: datetime = Field(..., title="发布时间")
    auth_name: str = Field(..., title="作者昵称")
    url: str = Field(..., title="下载地址")
    is_active: bool = Field(True, title="是否可见")
    create_user_id: int = Field(..., title="创建人")


class RedbookSimpleOut(Redbook):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class Links(BaseModel):
    link: Optional[List[str]] = Query(None, description="多个链接，逗号分隔")
