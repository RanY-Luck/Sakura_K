#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/17 16:03
# @Author  : 冉勇
# @Site    : 
# @File    : datasource_do.py
# @Software: PyCharm
# @desc    : 数据源配置表
from config.db_base import BaseModel
from sqlalchemy import Column, String, Integer


class DataSource(BaseModel):
    """
    数据源配置表
    """
    __tablename__ = "data_source"
    __table_args__ = ({'comment': '数据源配置表'})

    datasource_id = Column(Integer, primary_key=True, autoincrement=True, comment='数据源ID')
    datasource_name = Column(String(10), nullable=False, default='', comment='数据源名称', index=True)
    datasource_type = Column(String(10), nullable=False, default='', comment='数据源类型')
    datasource_host = Column(String(255), nullable=False, default='', comment='数据源地址')
    datasource_port = Column(String(10), nullable=False, default='', comment='数据源端口')
    datasource_user = Column(String(64), nullable=False, default='', comment='数据源用户名')
    datasource_pwd = Column(String(255), nullable=False, default='', comment='数据源密码')
