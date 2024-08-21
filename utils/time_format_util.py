#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 11:03
# @Author  : 冉勇
# @Site    : 
# @File    : time_format_util.py
# @Software: PyCharm
# @desc    : 时间格式化
import datetime


def object_format_datetime(obj):
    """
    :param obj: 输入一个对象
    :return:对目标对象所有datetime类型的属性格式化
    """
    # 遍历目标对象的所有属性
    for attr in dir(obj):
        # 获取属性的值
        value = getattr(obj, attr)
        # 如果属性值是datetime类型，则格式化为字符串
        if isinstance(value, datetime.datetime):
            # 格式化为字符串
            setattr(obj, attr, value.strftime('%Y-%m-%d %H:%M:%S'))
    return obj


def list_format_datetime(lst):
    """
    :param lst: 输入一个嵌套对象的列表
    :return: 对目标列表中所有对象的datetime类型的属性格式化
    """
    # 遍历目标列表中的所有对象
    for obj in lst:
        # 遍历对象中的所有属性
        for attr in dir(obj):
            # 获取属性的值
            value = getattr(obj, attr)
            # 如果属性值是datetime类型，则格式化为字符串
            if isinstance(value, datetime.datetime):
                # 格式化为字符串
                setattr(obj, attr, value.strftime('%Y-%m-%d %H:%M:%S'))
    return lst


def format_datetime_dict_list(dicts):
    """
    递归遍历嵌套字典，并将 datetime 值转换为字符串格式
    :param dicts: 输入一个嵌套字典的列表
    :return: 对目标列表中所有字典的datetime类型的属性格式化
    """
    result = []
    # 遍历目标列表中的所有字典
    for item in dicts:
        # 遍历字典中的所有键值对
        new_item = {}
        # 遍历键值对
        for k, v in item.items():
            # 如果值是字典，则递归处理
            if isinstance(v, dict):
                # 递归遍历子字典
                new_item[k] = format_datetime_dict_list([v])[0]
            elif isinstance(v, datetime.datetime):
                # 如果值是 datetime 类型，则格式化为字符串
                new_item[k] = v.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # 否则保留原始值
                new_item[k] = v
        result.append(new_item)

    return result
