#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/3 12:06
# @Author  : 冉勇
# @Site    : 
# @File    : project_vo.py
# @Software: PyCharm
# @desc    : 项目表类型-pydantic模型
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_form, as_query, validate_string


class ProjectModel(BaseModel):
    """
    项目表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    project_id: Optional[int] = Field(default=None, description='项目ID')
    project_name: Optional[str] = Field(default=None, description='项目名称')
    responsible_name: Optional[str] = Field(default=None, description='负责人')
    test_user: Optional[str] = Field(default=None, description='测试人员')
    dev_user: Optional[str] = Field(default=None, description='开发人员')
    publish_app: Optional[str] = Field(default=None, description='发布应用')
    simple_desc: Optional[str] = Field(default=None, description='简要描述')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    validate_project_name = field_validator('project_name')(validate_string('project_name', 10))
    validate_responsible_name = field_validator('responsible_name')(validate_string('responsible_name', 10))
    validate_test_user = field_validator('test_user')(validate_string('test_user', 10))
    validate_dev_user = field_validator('dev_user')(validate_string('dev_user', 10))
    validate_publish_app = field_validator('publish_app')(validate_string('publish_app', 10))


class ProjectQueryModel(ProjectModel):
    """
    项目管理不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
@as_form
class ProjectPageQueryModel(ProjectQueryModel):
    """
    项目管理分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteProjectModel(BaseModel):
    """
    删除项目模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    project_ids: str = Field(description='需要删除的项目主键')
