#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:47
# @Author  : 冉勇
# @Site    :
# @File    : settings.py
# @Software: PyCharm
# @desc    : 系统设置模型，用于数据库序列化操作
"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
定义了两个类：Settings和SettingsSimpleOut，都是通过继承BaseModel类来实现的。
Settings类表示一个系统设置，包括了config_label（配置标签，可以为空）、config_key（配置键）、config_value（配置值，可以为空）、remark（备注信息，可以为空）、disabled（是否禁用，可以为空）、tab_id（所属模块ID）等属性。
SettingsSimpleOut类继承了Settings类，并增加了id（自增主键）、create_datetime（创建时间）、update_datetime（更新时间）等属性。
同时，这个类也使用了Config类的orm_mode配置，表示该类可以被用于ORM操作。
"""
from typing import Optional
from pydantic import BaseModel
from core.data_types import DatetimeStr


class Settings(BaseModel):
    config_label: Optional[str] = None
    config_key: str
    config_value: Optional[str] = None
    remark: Optional[str] = None
    disabled: Optional[bool] = None
    tab_id: int


class SettingsSimpleOut(Settings):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    class Config:
        orm_mode = True
