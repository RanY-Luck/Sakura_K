#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Create Time    : 2024/09/15 12:42
# @Author         :
# @File           : robot_vo.py
# @Software       : PyCharm
# @desc           : 机器人配置表类型--pydantic模型
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size
from typing import Optional
from module_admin.annotation.pydantic_annotation import as_form, as_query


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

    @NotBlank(field_name='robot_name', message='机器人名称不能为空')
    @Size(field_name='robot_name', min_length=0, max_length=10, message='机器人名称长度不能超过10个字符')
    def get_robot_name(self):
        return self.robot_name

    @NotBlank(field_name='robot_webhook', message='机器人WebHook不能为空')
    @Size(field_name='robot_webhook', min_length=0, max_length=255, message='机器人WebHook长度不能超过255个字符')
    def get_robot_webhook(self):
        return self.robot_webhook

    @NotBlank(field_name='robot_type', message='类型不能为空')
    @Size(field_name='robot_type', min_length=0, max_length=10, message='类型长度不能超过10个字符')
    def get_robot_type(self):
        return self.robot_type

    def validate_fields(self):
        self.get_robot_name()
        self.get_robot_webhook()
        self.get_robot_type()


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
