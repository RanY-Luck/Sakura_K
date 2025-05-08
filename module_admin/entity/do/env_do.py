#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/10/28 16:27
# @Author   : 冉勇
# @File     : env_do.py
# @Software : PyCharm
# @Desc     : 环境表
from sqlalchemy import Column, Integer, String, JSON
from config.db_base import BaseModel


class Env(BaseModel):
    """
    接口表
    """
    __tablename__ = "env_info"
    __table_args__ = ({'comment': '环境表'})

    env_id = Column(Integer, primary_key=True, autoincrement=True, comment='环境ID')
    env_name = Column(String(20), nullable=False, comment='环境名称', index=True)
    env_url = Column(String(512), nullable=False, comment='环境地址')
    env_variables = Column(JSON, nullable=True, comment='环境变量')
    env_headers = Column(JSON, nullable=True, comment='环境请求头')
