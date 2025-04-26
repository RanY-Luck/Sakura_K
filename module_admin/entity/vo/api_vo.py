#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/26 21:36
# @Author  : 冉勇
# @Site    : 
# @File    : api_vo.py
# @Software: PyCharm
# @desc    : 接口表类型-pydantic模型
from datetime import datetime
from typing import List, Optional, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import Xss, NotBlank, Size

from module_admin.annotation.pydantic_annotation import as_form, as_query, validate_string


class BatchApi(BaseModel):
    id: Optional[int] = None
    status: Optional[str] = None
    response: Optional[dict] = None
    error_message: Optional[str] = None
    execution_time: Optional[float] = 0
    api_status: Optional[bool] = False  # API响应状态


class BatchApiStats(BaseModel):
    """批量执行统计信息"""
    total: Optional[int]
    api_success_count: Optional[int]  # API实际成功数
    api_failure_count: Optional[int]  # API实际失败数
    api_success_rate: Optional[float]  # API实际成功率
    total_time: Optional[float]
    results: List[BatchApi]


class ApiQueryModel(BaseModel):
    """
    接口表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    api_id: Optional[int] = Field(default=None, description='接口ID')
    api_name: Optional[str] = Field(default=None, description='接口名称')
    project_id: Optional[int] = Field(default=None, description='项目所属')
    api_method: Optional[str] = Field(default=None, description='接口方法')
    api_url: Optional[str] = Field(default=None, description='接口地址')
    api_status: Optional[str] = Field(default=None, description='接口状态(0正常 1停用)')
    api_level: Optional[str] = Field(default=None, description='优先级')
    api_tags: Optional[str] = Field(default=None, description='接口标签')
    request_data_type: Optional[int] = Field(
        default=None, description='数据类型:0[none] 1[json] 2[form] 3[x_form] 4[raw]'
    )
    request_data: Optional[Any] = Field(default=None, description='请求体')
    request_headers: Optional[Any] = Field(default=None, description='请求头')
    variable: Optional[Any] = Field(default=None, description='变量')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')


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
    api_status: Optional[str] = Field(default='0', description='接口状态(0正常 1停用)')
    api_level: Optional[str] = Field(default=None, description='优先级')
    api_tags: Optional[List[str]] = Field(default=[], description='接口标签')
    request_data_type: Optional[int] = Field(
        default=None, description='数据类型:0[none] 1[json] 2[form] 3[x_form] 4[raw]'
    )
    request_params: Optional[Any] = Field(default=[], description='请求参数')
    request_data: Optional[Any] = Field(default={}, description='请求体')
    request_headers: Optional[Any] = Field(default={}, description='请求头')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    # 校验表单
    validate_api_name = field_validator('api_name')(validate_string('api_name', 10))
    validate_api_method = field_validator('api_method')(validate_string('api_method', 10))
    validate_api_url = field_validator('api_url')(validate_string('api_url', 512))
    validate_api_status = field_validator('api_status')(validate_string('api_status', 1))
    validate_api_level = field_validator('api_level')(validate_string('api_level', 2))

    @Xss(field_name='api_name', message='接口名称不能包含脚本字符')
    @NotBlank(field_name='api_name', message='接口名称不能为空')
    @Size(field_name='api_name', min_length=0, max_length=10, message='接口名称不能超过10个字符')
    def get_api_name(self):
        return self.get_api_name

    @Xss(field_name='api_url', message='接口地址不能包含脚本字符')
    @NotBlank(field_name='api_url', message='接口地址不能为空')
    @Size(field_name='api_url', min_length=0, max_length=512, message='接口地址不能超过512个字符')
    def get_api_url(self):
        return self.get_api_url

    @Xss(field_name='api_method', message='接口方法不能包含脚本字符')
    @NotBlank(field_name='api_method', message='接口方法不能为空')
    @Size(field_name='api_method', min_length=0, max_length=10, message='接口方法不能超过10个字符')
    def get_api_method(self):
        return self.get_api_method

    @Xss(field_name='api_level', message='接口优先级不能包含脚本字符')
    @NotBlank(field_name='api_level', message='接口优先级不能为空')
    @Size(field_name='api_level', min_length=0, max_length=2, message='接口优先级不能超过2个字符')
    def get_api_level(self):
        return self.get_api_level

    @Xss(field_name='api_status', message='接口状态不能包含脚本字符')
    @NotBlank(field_name='api_status', message='接口状态不能为空')
    @Size(field_name='api_status', min_length=0, max_length=1, message='接口状态不能超过1个字符')
    def get_api_status(self):
        return self.get_api_status

    def validate_fields(self):
        self.get_api_name()
        self.get_api_url()
        self.get_api_method()
        self.get_api_level()
        self.get_api_status()

    @field_validator('api_status')
    def validate_api_status_priority(cls, value):
        if value not in {'0', '1'}:
            raise ValueError("api_status必须是'0'或'1'")
        return value

    @field_validator('api_level')
    def validate_api_level_priority(cls, value):
        if value not in {'P0', 'P1', 'P2', 'P3'}:
            raise ValueError("api_method必须是'P0'或'P1'或'P2'或'P3'")
        return value

    @field_validator('api_method')
    def validate_api_method_priority(cls, value):
        if value not in {'GET', 'POST', 'DELETE', 'PUT'}:
            raise ValueError("api_method必须是'GET'或'POST'或'DELETE'或'PUT'")
        return value

    @field_validator('request_data_type')
    def validate_request_data_type_priority(cls, value):
        if value not in {0, 1, 2, 3, 4}:
            raise ValueError("request_data_type必须是'0'或'1'或'2'或'3'或'4'")
        return value


class ApiQueryModel(ApiQueryModel):
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
