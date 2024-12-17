#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 11:40
# @Author  : 冉勇
# @Site    : 
# @File    : config_do.py
# @Software: PyCharm
# @desc    : 参数配置表
from sqlalchemy import Column, Integer, String
from config.db_base import BaseModel


class SysConfig(BaseModel):
    """
    参数配置表
    """
    __tablename__ = 'sys_config'
    __table_args__ = ({'comment': '参数配置表'})

    config_id = Column(Integer, primary_key=True, autoincrement=True, comment='参数主键')
    config_name = Column(String(100), nullable=True, default='', comment='参数名称')
    config_key = Column(String(100), nullable=True, default='', comment='参数键名')
    config_value = Column(String(500), nullable=True, default='', comment='参数键值')
    config_type = Column(String(1), nullable=True, default='N', comment='系统内置（Y是 N否）')