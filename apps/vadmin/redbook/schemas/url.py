#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/2/27 11:31
# @Author   : 冉勇
# @File     : url.py
# @Software : PyCharm
# @Desc     : pydantic 模型，用于数据库序列化操作

from pydantic import BaseModel, ConfigDict, Field

from core.data_types import DatetimeStr


class Urls(BaseModel):
    red_book_id: int = Field(..., title="关联表red_book.id")
    url: str = Field(..., title="下载地址")


class UrlsSimpleOut(Urls):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")
