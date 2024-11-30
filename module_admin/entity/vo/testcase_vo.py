#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 17:20
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_vo.py
# @Software: PyCharm
# @desc    : 测试用例表类型-pydantic模型
import json
from datetime import datetime
from typing import Optional, Literal, Any, List, Union, Dict

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import Xss, NotBlank, Size

from module_admin.annotation.pydantic_annotation import as_query, validate_string


class ApiModel(BaseModel):
    apiId: int
    apiName: str
    apiUrl: str
    apiMethod: str
    requestDataType: Optional[Union[str, int]] = Field(default=None)
    requestData: Optional[Union[Dict[str, Any], str, int, None]] = None
    requestHeaders: Optional[Dict[str, Any]] = None
    createBy: Optional[str] = None
    createTime: Optional[datetime] = None
    updateBy: Optional[str] = None
    updateTime: Optional[datetime] = None
    remark: Optional[str] = None

    class Config:
        # 允许从字符串或其他类型转换
        arbitrary_types_allowed = True

        # 当遇到类型不匹配时尝试强制转换
        @classmethod
        def validate_field(cls, field, value):
            if field.type_ is str and not isinstance(value, str):
                return str(value)
            return value


class TestCaseModel(BaseModel):
    """
    测试用例表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    testcase_id: Optional[int] = Field(default=None, description='测试用例ID')
    testcase_name: Optional[str] = Field(default=None, description='测试用例名称')
    project_id: Optional[int] = Field(default=None, description='项目ID')
    testcase_list: Optional[List] = Field(default=[], description='测试用例数组')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    # 校验表单
    validate_testcase_name = field_validator('testcase_name')(validate_string('testcase_name', 50))

    @Xss(field_name='testcase_name', message='测试用例名称不能包含脚本字符')
    @NotBlank(field_name='testcase_name', message='测试用例名称不能为空')
    @Size(field_name='testcase_name', max_length=50, message='测试用例名称不能超过50个字符')
    def get_testcase_name(self):
        return self.get_testcase_name

    def validate_fields(self):
        self.get_testcase_name()


class TestCaseQueryModel(TestCaseModel):
    """
    测试用例不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
class TestCasePageQueryModel(TestCaseQueryModel):
    """
    测试用例分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteTestCaseModel(BaseModel):
    """
    删除测试用例模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    testcase_ids: str = Field(description='需要删除的测试用例主键')
