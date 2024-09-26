#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/26 21:36
# @Author  : 冉勇
# @Site    : 
# @File    : api_vo.py
# @Software: PyCharm
# @desc    : 接口表类型-pydantic模型
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from typing import Any, Dict, List, Optional
from module_admin.annotation.pydantic_annotation import as_form, as_query, validate_string


class ApiModel(BaseModel):
    """
    接口表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    api_id: Optional[int] = Field(default=None, description='接口ID')
    api_name: Optional[str] = Field(default=None, description='接口名称')
    project_id: Optional[int] = Field(default=None, description='项目所属')
    api_method: Optional[str] = Field(default=None, description='接口方法')
    api_url: Optional[str] = Field(default=None, description='接口地址')
    api_status: Optional[int] = Field(default=None, description='接口状态')
    api_level: Optional[str] = Field(default=None, description='优先级')
    api_tags: Optional[str] = Field(default=None, description='接口标签')
    request_data_type: Optional[str] = Field(default=None, description='数据类型')
    request_data: Optional[str] = Field(default=None, description='请求体')
    request_headers: Optional[str] = Field(default=None, description='请求头')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    # 校验表单
    validate_api_name = field_validator('api_name')(validate_string('api_name', 10))
    validate_api_method = field_validator('api_method')(validate_string('api_method', 10))
    validate_api_url = field_validator('api_url')(validate_string('api_url', 512))
    validate_api_level = field_validator('api_level')(validate_string('api_level', 2))


class ApiQueryModel(ApiModel):
    """
    接口管理不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
@as_form
class ApiPageQueryModel(ApiQueryModel):
    """
    接口管理分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteApiModel(BaseModel):
    """
    删除接口模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    api_ids: str = Field(description='需要删除的接口主键')

# class Request(BaseModel):
#     data_type: str
#     data: List[Dict[str, Any]]
#     headers: List[Dict[str, Any]]
#     method: str
#     url: str
#
#
# class Model(BaseModel):
#     api_id: int
#     api_name: str
#     module_id: int
#     api_method: str
#     api_url: str
#     tags: List
#     remarks: str
#     request: Request
