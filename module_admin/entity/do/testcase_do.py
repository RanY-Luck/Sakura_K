#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 17:15
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_do.py
# @Software: PyCharm
# @desc    : 测试用例表
from config.db_base import BaseModel
from sqlalchemy import Column, Integer, String, JSON


class TestCase(BaseModel):
    """
    测试用例表
    """
    __tablename__ = "testcase_info"
    __table_args__ = ({'comment': '测试用例表'})

    testcase_id = Column(Integer, primary_key=True, autoincrement=True, comment='测试用例ID')
    testcase_name = Column(String(50), nullable=False, comment='测试用例名称', index=True)
    project_id = Column(Integer, nullable=False, comment='项目ID')
    testcase_list = Column(JSON, nullable=False, comment='测试用例数组')
