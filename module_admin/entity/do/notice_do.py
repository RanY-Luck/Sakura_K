#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/15 10:25
# @Author  : 冉勇
# @Site    : 
# @File    : notice_do.py
# @Software: PyCharm
# @desc    : 通知公告表
from sqlalchemy import Column, Integer, String, LargeBinary
from config.db_base import BaseModel
from datetime import datetime


class SysNotice(BaseModel):
    """
    通知公告表
    """
    __tablename__ = 'sys_notice'
    __table_args__ = ({'comment': '通知公告表'})

    notice_id = Column(Integer, primary_key=True, autoincrement=True, comment='公告ID')
    notice_title = Column(String(50), nullable=False, comment='公告标题')
    notice_type = Column(String(1), nullable=False, comment='公告类型（1通知 2公告）')
    notice_content = Column(LargeBinary, comment='公告内容')
    status = Column(String(1), default='0', comment='公告状态（0正常 1关闭）')
