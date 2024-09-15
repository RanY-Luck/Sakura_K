#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/15 12:32
# @Author  : 冉勇
# @Site    : 
# @File    : robot_do.py
# @Software: PyCharm
# @desc    : 机器人配置表
from config.db_base import BaseModel
from sqlalchemy import Column, String, Integer


class Robot(BaseModel):
    """
    机器人配置表
    """
    __tablename__ = "robot_conf"
    __table_args__ = ({'comment': '机器人配置表'})

    robot_id = Column(Integer, primary_key=True, autoincrement=True, comment='机器人ID')
    robot_name = Column(String(10), nullable=False, default='', comment='机器人名称', index=True)
    robot_webhook = Column(String(255), nullable=False, default='', comment='机器人WebHook')
    robot_type = Column(String(10), nullable=False, default='', comment='类型')
    robot_template = Column(String(255), nullable=False, default='', comment='通知模板')
    robot_status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
