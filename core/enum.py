#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 19:07
# @Author  : 冉勇
# @Site    : 
# @File    : enum.py
# @Software: PyCharm
# @desc    : 枚举类方法
from enum import Enum


class SuperEnum(Enum):
    """
    代码解释：
    这些方法都是通过对原有 Enum 类中的特殊属性和方法进行封装实现的。
    例如，to_dict() 方法中使用了 _member_names_ 和 _value2member_map_ 这两个原有属性，分别表示所有成员名称的列表和成员名称到成员对象的映射。
    """

    @classmethod
    def to_dict(cls):
        """
        返回枚举的字典表示形式
        代码解释：
        例如，如果枚举类中有一个成员 FOO，其值为 1，则 to_dict() 方法返回的字典为 {'FOO': 1}。
        :return:
        """
        return {e.name: e.value for e in cls}

    @classmethod
    def keys(cls):
        """
        返回所有的枚举键（即成员名称）组成的列表。
        :return:
        """
        return cls._member_names_

    @classmethod
    def values(cls):
        """
        方法返回所有的枚举值组成的列表，它并不是返回枚举成员本身，而是返回成员的值
        代码解释：
        例如，如果枚举类中有两个成员 BAR 和 BAZ，它们的值分别为 2 和 3，则 values() 方法返回的列表为 [2, 3]。
        :return:
        """
        return list(cls._value2member_map_.keys())
