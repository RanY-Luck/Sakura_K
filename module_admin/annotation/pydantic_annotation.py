#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 11:00
# @Author  : 冉勇
# @Site    : 
# @File    : pydantic_annotation.py
# @Software: PyCharm
# @desc    : pydantic 接受查询参数(高级用法)
import inspect
from fastapi import Form, Query
from typing import Optional, Callable
from pydantic import BaseModel
from pydantic.fields import FieldInfo
from typing import Type


def as_query(cls: Type[BaseModel]):
    """
    用于将 Pydantic 模型转换为查询参数
    """
    # 创建新参数列表
    new_parameters = []
    # 遍历模型字段 循环遍历 Pydantic 模型的所有字段
    for field_name, model_field in cls.model_fields.items():
        model_field: FieldInfo  # type: ignore
        if not model_field.is_required():
            new_parameters.append(
                inspect.Parameter(
                    model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Query(default=model_field.default, description=model_field.description),
                    annotation=model_field.annotation
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    field_name,
                    # model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Query(..., description=model_field.description),
                    annotation=model_field.annotation
                )
            )

    # 定义内部函数
    async def as_query_func(**data):
        """
        将传入的数据转换为 Pydantic 模型实例
        """
        return cls(**data)

    sig = inspect.signature(as_query_func)
    sig = sig.replace(parameters=new_parameters)
    as_query_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_query', as_query_func)
    return cls


def as_form(cls: Type[BaseModel]):
    """
    用于将将 Pydantic 模型用于接收表单参数
    """
    new_parameters = []
    for field_name, model_field in cls.model_fields.items():
        model_field: FieldInfo  # type: ignore
        if not model_field.is_required():
            new_parameters.append(
                inspect.Parameter(
                    field_name,
                    # model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(default=model_field.default, description=model_field.description),
                    annotation=model_field.annotation
                )
            )
        else:
            new_parameters.append(
                inspect.Parameter(
                    field_name,
                    # model_field.alias,
                    inspect.Parameter.POSITIONAL_ONLY,
                    default=Form(..., description=model_field.description),
                    annotation=model_field.annotation
                )
            )

    async def as_form_func(**data):
        return cls(**data)

    sig = inspect.signature(as_form_func)
    sig = sig.replace(parameters=new_parameters)
    as_form_func.__signature__ = sig  # type: ignore
    setattr(cls, 'as_form', as_form_func)
    return cls


# def validate_string(field_name: str, max_length: int):
#     """
#     用于将将 Pydantic 模型用于校验表单参数
#     """
#     def validator(cls, value: Optional[str]):
#         if value is None:
#             return value  # 允许值为 None，但如果提供了值，则不能为空字符串
#         value = value.strip()
#         if value == '':
#             raise ValueError(f"{field_name}不能为空")
#         if len(value) > max_length:
#             raise ValueError(f"{field_name}不能超过{max_length}个字符")
#         return value
#
#     return validator


def validate_string(field_name: str, max_length: int) -> Callable:
    def validator(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value  # 允许值为 None，但如果提供了值，则不能为空字符串
        value = value.strip()
        if value == '':
            raise ValueError(f"{field_name}不能为空")
        if len(value) > max_length:
            raise ValueError(f"{field_name}不能超过{max_length}个字符（包括{max_length}个字符）")
        return value

    return validator