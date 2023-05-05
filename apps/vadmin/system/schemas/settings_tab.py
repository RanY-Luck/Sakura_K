#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 16:27
# @Author  : 冉勇
# @Site    : 
# @File    : settings_tab.py
# @Software: PyCharm
# @desc    : 系统设置选项卡模型，用于数据库序列化操作
"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
定义了两个类：SettingsTab和SettingsTabSimpleOut，两个类都是通过继承BaseModel类来实现的。
SettingsTab类表示一个系统设置选项卡，包括了title（选项卡标题）、classify（选项卡分类）、tab_label（选项卡标签）、tab_name（选项卡名称）和hidden（是否隐藏）等属性。
SettingsTabSimpleOut类继承了SettingsTab类，并增加了id（自增主键）、create_datetime（创建时间）和update_datetime（更新时间）等属性。
同时，这个类也使用了Config类的orm_mode配置，表示该类可以被用于ORM操作。
这些数据模型类都采用了pydantic库实现，利用了其内置的输入数据验证、类型转换等功能，可以在运行前对数据进行预处理和校验。
而使用继承方式构建数据模型类，可以方便地进行属性的复用和继承。
"""
from pydantic import BaseModel
from core.data_types import DatetimeStr


class SettingsTab(BaseModel):
    """
    系统设置选项卡
    """
    title: str
    classify: str
    tab_label: str
    tab_name: str
    hidden: bool


class SettingsTabSimpleOut(SettingsTab):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    class Config:
        orm_mode = True
