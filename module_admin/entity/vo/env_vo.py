#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/10/28 17:16
# @Author   : 冉勇
# @File     : env_vo.py
# @Software : PyCharm
# @Desc     : 环境表类型-pydantic模型
from datetime import datetime
from typing import Optional, Any

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import Xss, NotBlank, Size

from module_admin.annotation.pydantic_annotation import as_query, validate_string


class EnvModel(BaseModel):
    """
    环境表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    env_id: Optional[int] = Field(default=None, description='环境ID')
    env_name: Optional[str] = Field(default=None, description='环境名称')
    env_url: Optional[str] = Field(default=None, description='环境地址')
    env_variables: Optional[Any] = Field(default={}, description='环境变量')
    env_headers: Optional[Any] = Field(default={}, description='环境请求头')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    # 校验表单
    validate_env_name = field_validator('env_name')(validate_string('env_name', 10))
    validate_env_url = field_validator('env_url')(validate_string('env_url', 512))

    @Xss(field_name='env_name', message='环境名称不能包含脚本字符')
    @NotBlank(field_name='env_name', message='环境名称不能为空')
    @Size(field_name='env_name', max_length=10, message='环境名称不能超过10个字符')
    def get_env_name(self):
        return self.get_env_name

    @Xss(field_name='env_url', message='环境地址不能包含脚本字符')
    @NotBlank(field_name='env_url', message='环境地址不能为空')
    @Size(field_name='env_url', max_length=512, message='环境地址不能超过512个字符')
    def get_env_url(self):
        return self.get_env_url

    def validate_fields(self):
        self.get_env_name()
        self.get_env_url()


class EnvQueryModel(EnvModel):
    """
    环境管理不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
class EnvPageQueryModel(EnvQueryModel):
    """
    环境管理分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteEnvModel(BaseModel):
    """
    删除环境模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    env_ids: str = Field(description='需要删除的环境主键')
