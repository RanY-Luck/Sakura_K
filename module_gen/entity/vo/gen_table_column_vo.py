#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:53
# @Author   : 冉勇
# @File     : gen_table_column_vo.py
# @Software : PyCharm
# @Desc     :
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing import List, Literal, Optional, Union
from module_admin.annotation.pydantic_annotation import as_query


class GenTableColumnModel(BaseModel):
    """
    表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    column_id: Optional[int] = Field(default=None, description='编号')

    table_id: Optional[int] = Field(default=None, description='归属表编号')

    column_name: Optional[str] = Field(default=None, description='列名称')

    column_comment: Optional[str] = Field(default=None, description='列描述')

    column_type: Optional[str] = Field(default=None, description='列类型')

    python_type: Optional[str] = Field(default=None, description='python类型')

    python_field: Optional[str] = Field(default=None, description='python字段名')

    is_pk: Optional[str] = Field(default=None, description='是否主键（1是）')

    is_increment: Optional[str] = Field(default=None, description='是否自增（1是）')

    is_required: Optional[str] = Field(default=None, description='是否必填（1是）')

    is_insert: Optional[str] = Field(default=None, description='是否为插入字段（1是）')

    is_edit: Optional[str] = Field(default=None, description='是否编辑字段（1是）')

    is_list: Optional[str] = Field(default=None, description='是否列表字段（1是）')

    is_query: Optional[str] = Field(default=None, description='是否查询字段（1是）')

    query_type: Optional[str] = Field(default=None, description='查询方式（等于、不等于、大于、小于、范围）')

    html_type: Optional[str] = Field(default=None, description='显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）')

    dict_type: Optional[str] = Field(default=None, description='字典类型')

    sort: Optional[int] = Field(default=None, description='排序')

    create_by: Optional[str] = Field(default=None, description='创建者')

    create_time: Optional[datetime] = Field(default=None, description='创建时间')

    update_by: Optional[str] = Field(default=None, description='更新者')

    update_time: Optional[datetime] = Field(default=None, description='更新时间')


@as_query
class GenTableColumnPageModel(GenTableColumnModel):
    """
    分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')
