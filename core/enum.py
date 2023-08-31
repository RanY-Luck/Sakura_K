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

    @classmethod
    def to_dict(cls):
        """Returns a dictionary representation of the enum."""
        return {e.name: e.value for e in cls}

    @classmethod
    def keys(cls):
        """Returns a list of all the enum keys."""
        return cls._member_names_

    @classmethod
    def values(cls):
        """Returns a list of all the enum values."""
        return list(cls._value2member_map_.keys())
