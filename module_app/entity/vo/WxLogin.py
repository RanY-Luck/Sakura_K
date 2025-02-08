#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/7 17:26
# @Author   : 冉勇
# @File     : WxLogin.py
# @Software : PyCharm
# @Desc     :
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel
from module_admin.entity.do.user_do import SysUser, UserWechat
from module_admin.entity.vo.user_vo import UserWechatModel, UserModel


class AppLoginModelResp(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    token: str = Field(description='token信息')
    expires_in: str = Field(description='过期时间')
    user: UserModel = Field(description="用户信息")
    wx_user: UserWechatModel = Field(description="微信用户信息")