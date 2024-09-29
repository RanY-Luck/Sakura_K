#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/26 21:20
# @Author  : 冉勇
# @Site    : 
# @File    : api_do.py
# @Software: PyCharm
# @desc    : 接口表
from config.db_base import BaseModel
from sqlalchemy import Column, Integer, String, JSON


class Api(BaseModel):
    """
    接口表
    """
    __tablename__ = "api_info"
    __table_args__ = ({'comment': '接口表'})

    api_id = Column(Integer, primary_key=True, autoincrement=True, comment='接口ID')
    api_name = Column(String(255), nullable=False, comment='接口名称', index=True)
    project_id = Column(Integer, nullable=False, comment='项目ID')
    api_method = Column(String(10), nullable=False, comment='接口方法')
    api_url = Column(String(512), nullable=False, comment='接口地址')
    api_status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    api_level = Column(String(2), nullable=False, default='P3', comment='优先级（P0、P1、P2、P3）')
    api_tags = Column(JSON, nullable=True, comment='标签')
    request_data_type = Column(String(25), nullable=True, comment='请求数据类型')
    request_data = Column(JSON, nullable=True, comment='请求数据')
    request_headers = Column(JSON, nullable=True, comment='请求头')
