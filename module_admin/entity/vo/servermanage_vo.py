#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/1 10:56
# @Author   : 冉勇
# @File     : servermanage_vo.py
# @Software : PyCharm
# @Desc     : 环境表类型-pydantic模型
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Xss, Size
from module_admin.annotation.pydantic_annotation import as_query, validate_string


class SshModel(BaseModel):
    """
    服务器表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    ssh_id: Optional[int] = Field(default=None, description='服务器ID')
    ssh_name: Optional[str] = Field(default=None, description='服务器名称')
    ssh_host: Optional[str] = Field(default=None, description='服务器地址')
    ssh_username: Optional[str] = Field(default=None, description='服务器用户名')
    ssh_password: Optional[str] = Field(default=None, description='服务器密码')
    ssh_port: Optional[int] = Field(default=None, description='服务器端口')

    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')
    del_flag: Optional[str] = Field(default=None, description='删除标志（0代表存在 1代表删除）')

    # 校验表单
    validate_env_name = field_validator('ssh_name')(validate_string('ssh_name', 10))
    validate_env_url = field_validator('ssh_host')(validate_string('ssh_host', 128))

    @Xss(field_name='ssh_name', message='服务器名称不能包含脚本字符')
    @NotBlank(field_name='ssh_name', message='服务器名称不能为空')
    @Size(field_name='ssh_name', max_length=10, message='服务器名称不能超过10个字符')
    def get_ssh_name(self):
        return self.ssh_name

    @Xss(field_name='ssh_host', message='服务器地址不能包含脚本字符')
    @NotBlank(field_name='ssh_host', message='服务器地址不能为空')
    @Size(field_name='ssh_host', max_length=128, message='服务器地址不能超过128个字符')
    def get_ssh_host(self):
        return self.ssh_host

    def validate_fields(self):
        self.get_ssh_name()
        self.get_ssh_host()


class SshQueryModel(SshModel):
    """
    服务器不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
class SshPageQueryModel(SshQueryModel):
    """
    服务器分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteSshModel(BaseModel):
    """
    删除服务器模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    ssh_ids: str = Field(description='需要删除的服务器主键')


# 服务器信息
class SshInfo(BaseModel):
    ssh_host: str
    ssh_username: str
    ssh_password: str
    ssh_port: int
