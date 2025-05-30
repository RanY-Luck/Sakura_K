#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-05-28 18:30:00
# @Author   : 冉勇
# @File     : text2sql_vo.py
# @Software : PyCharm
# @Desc     : Text2SQL模块的请求和响应模型

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from typing import Optional


class TrainRequest(BaseModel):
    """训练Text2SQL模型的请求模型"""
    model_config = ConfigDict(alias_generator=to_camel)
    
    supplier: str = ""
    question: str = ""
    sql: str = ""
    documentation: str = ""
    ddl: str = ""
    schema: bool = False


class AskRequest(BaseModel):
    """提问请求模型"""
    model_config = ConfigDict(alias_generator=to_camel)
    
    question: str
    auto_train: bool = True
    supplier: str = ""