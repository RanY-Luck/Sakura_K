#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Create Time    : 2024/09/15 12:42
# @Author         :
# @File           : robot_vo.py
# @Software       : PyCharm
# @desc           : 机器人配置表类型--pydantic模型
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic import BaseModel, field_validator
from module_admin.annotation.pydantic_annotation import as_form, as_query, validate_string


class RobotModel(BaseModel):
    """
    项目表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    robot_id: Optional[int] = Field(default=None, description='机器人ID')
    robot_name: Optional[str] = Field(default=None, description='机器人名称')
    robot_webhook: Optional[str] = Field(default=None, description='机器人WebHook')
    robot_type: Optional[str] = Field(default=None, description='类型')
    robot_template: Optional[str] = Field(default=None, description='通知模板')
    robot_status: Optional[str] = Field(default='0', description='状态（0正常 1停用）')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    # 校验表单
    validate_robot_name = field_validator('robot_name')(validate_string('robot_name', 10))
    validate_robot_type = field_validator('robot_type')(validate_string('robot_type', 10))
    validate_robot_webhook = field_validator('robot_webhook')(validate_string('robot_webhook', 255))
    validate_robot_template = field_validator('robot_template')(validate_string('robot_template', 255))

    @field_validator('robot_status')
    def validate_status_priority(cls, value):
        if value not in {'0', '1'}:
            raise ValueError("robot_status必须是'1'或'0'")
        return value


class RobotQueryModel(RobotModel):
    """
    机器人不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
@as_form
class RobotPageQueryModel(RobotQueryModel):
    """
    机器人分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteRobotModel(BaseModel):
    """
    删除机器人模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    robot_ids: str = Field(description='需要删除的机器人主键')
