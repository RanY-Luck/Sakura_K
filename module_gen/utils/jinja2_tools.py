#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 10:00
# @Author   : 冉勇
# @File     : jinja2_tools.py
# @Software : PyCharm
# @Desc     :
import re
from module_gen.constants.gen_constants import GenConstants


def snake_to_pascal_case(value):
    """将下划线命名 (snake_case) 转换大驼峰"""
    return ''.join(word.capitalize() for word in value.split('_'))


def snake_to_camel(snake_str):
    """将下划线命名 (snake_case) 转换小驼峰"""
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def snake_2_colon(snake_str: str) -> str:
    """将下划线命名 (snake_case) 转换冒号分隔"""
    return snake_str.replace('_', ':')


def is_base_column(column_name: str) -> bool:
    """判断是否是基础字段"""
    return column_name in ('id', 'create_time', 'update_time', 'del_flag')


def get_sqlalchemy_type(mysql_field_type: str) -> str:
    """mysql_field_type 转sqlalchemy类型"""
    if mysql_field_type:
        base_type = mysql_field_type.split("(", 1)[0]
        if base_type.upper() in GenConstants.MYSQL_TO_SQLALCHEMY.keys():
            sqlalchemy_type = GenConstants.MYSQL_TO_SQLALCHEMY[base_type.upper()]
            if sqlalchemy_type == 'String':
                match = re.search(r'\((.*?)\)', mysql_field_type)
                if match:
                    return f'{sqlalchemy_type}({match.group(1)})'
                else:
                    return f'{sqlalchemy_type}'
            else:
                return f'{sqlalchemy_type}'
    return "String"


def get_column_options(col) -> str:
    options = []
    # 主键
    if col['isPk'] == "1":
        options.append("primary_key=True")
    # 是否允许为空
    if col['isRequired'] == "1":
        options.append("nullable=False")
    # 自增
    if col["isIncrement"] == "1":
        options.append("autoincrement=True")
    # 注释
    options.append(f"comment='{col['columnComment']}'")
    return ", ".join(options)
