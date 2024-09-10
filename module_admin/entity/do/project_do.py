#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/3 11:52
# @Author  : 冉勇
# @Site    : 
# @File    : project_do.py
# @Software: PyCharm
# @desc    : 项目表
from config.db_base import BaseModel
from sqlalchemy import Column, String, Integer


class Project(BaseModel):
    """
    项目表
    """
    __tablename__ = "project_info"
    __table_args__ = ({'comment': '项目表'})

    project_id = Column(Integer, primary_key=True, autoincrement=True, comment='项目ID')
    project_name = Column(String(10), nullable=False, default='', comment='项目名称', index=True)
    responsible_name = Column(String(10), nullable=False, default='', comment='负责人')
    test_user = Column(String(10), nullable=False, default='', comment='测试人员')
    dev_user = Column(String(10), nullable=False, default='', comment='开发人员')
    publish_app = Column(String(10), nullable=False, default='', comment='发布应用')
    simple_desc = Column(String(100), nullable=True, default='', comment='简要描述')
