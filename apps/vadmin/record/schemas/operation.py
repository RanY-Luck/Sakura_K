#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 19:21
# @Author  : 冉勇
# @Site    : 
# @File    : operation.py
# @Software: PyCharm
# @desc    : pydantic 模型，用于数据库序列化操作
"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
定义了两个 Pydantic 模型，OperationRecord 和 OperationRecordSimpleOut。
OperationRecord 是一个基础模型，它包含了一些操作记录的基本信息。
这些信息包括电话号码（telephone）、用户 ID（user_id）、用户名（user_name）、状态码（status_code）、客户端 IP 地址（client_ip）、
请求方法（request_method）、API 路径（api_path）、操作系统信息（system）、浏览器信息（browser）、操作摘要（summary）、
路由名称（route_name）、操作描述（description）、标签（tags）、处理时间（process_time）、参数（params）和创建时间（create_datetime）。其中，所有属性都是可选的。
OperationRecordSimpleOut 继承了 OperationRecord，并且没有添加任何新的属性。
它只是用于在需要返回 OperationRecord 数据时，确保数据符合 SQLAlchemy ORM 模型的属性要求。
OperationRecord 和 OperationRecordSimpleOut 都是 Pydantic 的 BaseModel 类的子类。
这意味着它们都具有 Pydantic 的基本功能，例如验证属性的类型、默认值等。
Config 类中的 orm_mode = True 表示该模型可以被用作 SQLAlchemy ORM 模型的返回类型，确保返回的数据符合 SQLAlchemy ORM 模型的属性要求。
"""

from typing import Optional, List
from pydantic import BaseModel


class OperationRecord(BaseModel):
    telephone: Optional[str] = None
    user_id: Optional[str] = None
    user_name: Optional[str] = None
    status_code: Optional[int] = None
    client_ip: Optional[str] = None
    request_method: Optional[str] = None
    api_path: Optional[str] = None
    system: Optional[str] = None
    browser: Optional[str] = None
    summary: Optional[str] = None
    route_name: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    process_time: Optional[str] = None
    params: Optional[str] = None
    create_datetime: Optional[str] = None


class OperationRecordSimpleOut(OperationRecord):
    class Config:
        orm_mode = True
