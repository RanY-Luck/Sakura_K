#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/12/2 12:00
# @Author  : 冉勇
# @Site    : 
# @File    : demo_do.py
# @Software: PyCharm
# @desc    :
from config.db_base import BaseModel
from sqlalchemy import Column, Integer, String


class Demo(BaseModel):
    """
    接口表
    """
    __tablename__ = "demo"
    __table_args__ = ({'comment': '测试表'})

    demo_id = Column(Integer, primary_key=True, autoincrement=True, comment='接口ID')
    demo_name = Column(String(255), nullable=False, comment='接口名称', index=True)
    demo_name1 = Column(String(255), nullable=False, comment='接口名称', index=True)
    demo_name2 = Column(String(255), nullable=False, comment='接口名称', index=True)
