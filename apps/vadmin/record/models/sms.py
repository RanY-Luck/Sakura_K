#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/24 15:43
# @Author  : 冉勇
# @Site    : 
# @File    : sms.py
# @Software: PyCharm
# @desc    : 短信发送记录模型
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, ForeignKey


class VadminSMSSendRecord(BaseModel):
    __tablename__ = "vadmin_record_sms_send"
    __table_args__ = ({"comment": "短信发送记录表"})

    user_id = Column(ForeignKey("vadmin_auth_user.id", ondelete="CASCADE"), comment="操作人")
    status = Column(Boolean, default=True, comment="发送状态")
    content = Column(String(255), comment="发送内容")
    telephone = Column(String(11), comment="目标手机号")
    desc = Column(String(255), comment="失败描述")
    scene = Column(String(50), comment="发送场景")
