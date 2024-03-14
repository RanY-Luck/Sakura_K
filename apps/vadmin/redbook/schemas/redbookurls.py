#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/2/27 16:18
# @Author   : 冉勇
# @File     : redbookurls.py
# @Software : PyCharm
# @Desc     : pydantic 模型，用于数据库序列化操作
from __future__ import annotations

from typing import List

from pydantic import BaseModel


class RedBookUrls(BaseModel):
    red_book_id: int
    source: str
    tags: str
    title: str
    describe: str
    type: str
    affiliation: str
    release_time: str
    auth_name: str
    urls: List[str]


class RedBookUrlsSimpleOut(BaseModel):
    data: RedBookUrls
