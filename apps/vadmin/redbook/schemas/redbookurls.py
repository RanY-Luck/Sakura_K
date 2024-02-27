#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/2/27 16:18
# @Author   : 冉勇
# @File     : redbookurls.py
# @Software : PyCharm
# @Desc     : pydantic 模型，用于数据库序列化操作
from pydantic import ConfigDict

from apps.vadmin.redbook.schemas import RedbookSimpleOut, UrlsSimpleOut


class RedBookUrlsOut(RedbookSimpleOut):
    model_config = ConfigDict(from_attributes=True)

    urls: UrlsSimpleOut
