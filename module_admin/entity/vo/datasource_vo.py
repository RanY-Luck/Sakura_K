#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/17 16:08
# @Author  : 冉勇
# @Site    : 
# @File    : datasource_vo.py
# @Software: PyCharm
# @desc    : 数据源配置表类型--pydantic模型
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic import BaseModel, field_validator
from pydantic_validation_decorator import NotBlank, Size
from module_admin.annotation.pydantic_annotation import as_form, as_query, validate_string


class DataSourceModel(BaseModel):
    """
    数据源表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    datasource_id: Optional[int] = Field(default=None, description='数据源ID')
    datasource_name: Optional[str] = Field(default=None, description='数据源名称')
    datasource_type: Optional[str] = Field(default=None, description='数据源类型')
    datasource_host: Optional[str] = Field(default=None, description='数据源地址')
    datasource_port: Optional[str] = Field(default=None, description='数据源端口')
    datasource_user: Optional[str] = Field(default=None, description='数据源用户名')
    datasource_pwd: Optional[str] = Field(default=None, description='数据源密码')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    # 校验表单
    validate_datasource_name = field_validator('datasource_name')(validate_string('datasource_name', 20))
    validate_datasource_type = field_validator('datasource_type')(validate_string('datasource_type', 10))
    validate_datasource_host = field_validator('datasource_host')(validate_string('datasource_host', 255))
    validate_datasource_port = field_validator('datasource_port')(validate_string('datasource_port', 10))
    validate_datasource_user = field_validator('datasource_user')(validate_string('datasource_user', 64))

    @NotBlank(field_name='datasource_name', message='数据源名称不能为空')
    @Size(field_name='datasource_name', min_length=0, max_length=20, message='数据源名称字符串长度不能超过20个字符')
    def get_datasource_name(self):
        return self.datasource_name

    @NotBlank(field_name='datasource_type', message='数据源类型不能为空')
    @Size(field_name='datasource_type', min_length=0, max_length=10, message='数据源类型字符串长度不能超过10个字符')
    def get_datasource_type(self):
        return self.datasource_type

    @NotBlank(field_name='datasource_host', message='数据源地址不能为空')
    @Size(field_name='datasource_host', min_length=0, max_length=255, message='数据源地址字符串长度不能超过255个字符')
    def get_datasource_host(self):
        return self.datasource_host

    @NotBlank(field_name='datasource_port', message='数据源端口不能为空')
    @Size(field_name='datasource_port', min_length=0, max_length=10, message='数据源端口字符串长度不能超过10个字符')
    def get_datasource_port(self):
        return self.datasource_port

    @NotBlank(field_name='datasource_user', message='数据源用户名不能为空')
    @Size(field_name='datasource_user', min_length=0, max_length=64, message='数据源用户名字符串长度不能超过64个字符')
    def get_datasource_user(self):
        return self.datasource_user

    def validate_fields(self):
        self.get_datasource_name()
        self.get_datasource_type()
        self.get_datasource_host()
        self.get_datasource_port()
        self.get_datasource_user()


class DataSourceQueryModel(DataSourceModel):
    """
    数据源不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
@as_form
class DataSourcePageQueryModel(DataSourceQueryModel):
    """
    数据源分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteDataSourceModel(BaseModel):
    """
    删除数据源模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    datasource_ids: str = Field(description='需要删除的数据源主键')


# 数据源信息
class SourceInfo(BaseModel):
    datasource_host: str
    datasource_port: int
    datasource_user: str
    datasource_pwd: str


# 数据源排除密码
class SourceExcludePasswords(BaseModel):
    datasourceId: int
    datasourceName: str
    datasourceType: str
    datasourceHost: str
    datasourcePort: str
    datasourceUser: str
    datasourcePwd: str
    createBy: Optional[str] = None
    createTime: Optional[datetime] = None
    updateBy: Optional[str] = None
    updateTime: Optional[datetime] = None
    remark: Optional[str] = None
