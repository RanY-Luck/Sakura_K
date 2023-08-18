#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:40
# @Author  : 冉勇
# @Site    :
# @File    : dict.py
# @Software: PyCharm
# @desc    : pydantic 模型，用于数据库序列化操作
"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
DictType类：表示一个字典类型，包括dict_name（字典名称）、dict_type（字典类型）、disabled（是否禁用，默认为False）和remark（备注信息）等属性。
DictTypeSimpleOut类：继承自DictType类，同时增加了id（自增主键）、create_datetime（创建时间）和update_datetime（更新时间）等属性。这个类也使用了Config类的orm_mode配置。
DictTypeSelectOut类：表示以选择框形式展现的字典类型，包括id（自增主键）、dict_name（字典名称）和disabled（是否禁用）等属性。同样，这个类也使用了Config类的orm_mode配置。
DictDatails类：表示一个字典详情，包括label（标签）、value（值）、disabled（是否禁用，默认为False）、is_default（是否默认，默认为False）、remark（备注信息）、order（排序）和dict_type_id（字典类型id）等属性。
DictDetailsSimpleOut类：继承自DictDatails类，同时增加了id（自增主键）、create_datetime（创建时间）和update_datetime（更新时间）等属性。同样，这个类也使用了Config类的orm_mode配置。
"""
from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class DictType(BaseModel):
    dict_name: str
    dict_type: str
    disabled: bool | None = False
    remark: str | None = None


class DictTypeSimpleOut(DictType):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class DictTypeSelectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    dict_name: str
    disabled: bool


class DictDetails(BaseModel):
    label: str
    value: str
    disabled: bool | None = False
    is_default: bool | None = False
    remark: str | None = None
    order: int | None = None
    dict_type_id: int


class DictDetailsSimpleOut(DictDetails):
    model_config = ConfigDict(from_attributes=True)

    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr
