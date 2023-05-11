#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/12 19:23
# @Author  : 冉勇
# @Site    : 
# @File    : data_types.py
# @Software: PyCharm
# @desc    : 自定义数据类型
"""
自定义数据类型 - 官方文档：https://pydantic-docs.helpmanual.io/usage/types/#custom-data-types
"""
from .validator import *


class DatetimeStr(str):
    """
    代码解释：
    定义了一个继承自 Python 标准库中的字符串类 str 的新类 DatetimeStr，并给该类添加了两个方法：__get_validators__() 和 validate()。
    DatetimeStr 类通过重写 __get_validators__() 方法，将 validate() 方法注册为类型验证器，使得在使用 Pydantic 进行数据验证时，可以将 DatetimeStr 当作一个数据类型来使用。
    validate() 方法接收一个参数 v，用于对数据进行验证和转换。如果传入的数据类型为 str，则直接返回该字符串；
    否则将其转换为字符串类型，格式为 %Y-%m-%d %H:%M:%S 的日期时间字符串。其中，v.strftime() 表示将时间对象 v 转换为指定格式的字符串。
    例如，如果传入 datetime.datetime(2023, 4, 12, 19, 38, 14) （即一个日期时间对象），则调用 DatetimeStr.validate() 方法后会返回字符串 '2023-04-12 19:38:14'。
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return v
        return v.strftime("%Y-%m-%d %H:%M:%S")


class Telephone(str):
    """
    代码解释：
    定义了一个继承自 Python 标准库中的字符串类 str 的新类 Telephone，并给该类添加了两个方法：__get_validators__() 和 validate()。
    Telephone 类通过重写 __get_validators__() 方法，将 validate() 方法注册为类型验证器，使得在使用 Pydantic 进行数据验证时，可以将 Telephone 当作一个数据类型来使用。
    validate() 方法接收一个参数 v，用于对数据进行验证。在该方法中，它调用了 vali_telephone(v) 函数来判断参数 v 是否符合 Telephone 号码的格式要求，并将结果返回。
    例如，如果传入 '12345678901' 字符串，则调用 Telephone.validate() 方法后会返回原始字符串，表明该字符串是一个合法的 Telephone 号码。
    如果传入的字符串不符合 Telephone 号码的格式要求，则会引发异常。
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return vali_telephone(v)


class Email(str):
    """
    代码解释：
    定义了一个继承自 Python 标准库中的字符串类 str 的新类 Email，并给该类添加了两个方法：__get_validators__() 和 validate()。
    Email 类通过重写 __get_validators__() 方法，将 validate() 方法注册为类型验证器，使得在使用 Pydantic 进行数据验证时，可以将 Email 当作一个数据类型来使用。
    validate() 方法接收一个参数 v，用于对数据进行验证。在该方法中，它调用了 vali_email(v) 函数来判断参数 v 是否符合 Email 地址的格式要求，并将结果返回。
    例如，如果传入 'user@example.com' 字符串，则调用 Email.validate() 方法后会返回原始字符串，表明该字符串是一个合法的 Email 地址。
    如果传入的字符串不符合 Email 地址的格式要求，则会引发异常。
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        return vali_email(v)


class DateStr(str):
    """
    代码解释：
    定义一个继承自 Python 标准库中的字符串类 str 的新类 DateStr，并给该类添加了两个方法：__get_validators__() 和 validate()。
    DateStr 类通过重写 __get_validators__() 方法，将 validate() 方法注册为类型验证器，使得在使用 Pydantic 进行数据验证时，可以将 DateStr 当作一个数据类型来使用。
    validate() 方法接收一个参数 v，用于对数据进行验证和转换。如果传入的数据类型为 str，则直接返回该字符串；
    否则将其转换为字符串类型，格式为 %Y-%m-%d 的日期字符串。其中，v.strftime() 表示将时间对象 v 转换为指定格式的字符串。
    例如，如果传入 datetime.date(2023, 4, 12) （即一个日期对象），则调用 DateStr.validate() 方法后会返回字符串 '2023-04-12'。
    """

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, str):
            return v
        return v.strftime("%Y-%m-%d")
