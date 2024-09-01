#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 11:40
# @Author  : 冉勇
# @Site    : 
# @File    : config_do.py
# @Software: PyCharm
# @desc    : Demo表
from sqlalchemy import Column, Integer, String, DateTime, LargeBinary
from config.database import Base
from datetime import datetime


# 参考 dept_do
class Demo(Base):
    """
    参数配置表
    """
    __tablename__ = 'demo'
    __table_args__ = ({'comment': '测试生成表'})

    dept_id = Column(Integer, primary_key=True, autoincrement=True, comment='部门id')
    parent_id = Column(Integer, default=0, comment='父部门id')
    ancestors = Column(String(50), nullable=True, default='', comment='祖级列表')
    dept_name = Column(String(30), nullable=True, default='', comment='部门名称')
    order_num = Column(Integer, default=0, comment='显示顺序')
    leader = Column(String(20), nullable=True, default=None, comment='负责人')
    phone = Column(String(11), nullable=True, default=None, comment='联系电话')
    email = Column(String(50), nullable=True, default=None, comment='邮箱')
    status = Column(String(1), nullable=True, default=0, comment='部门状态（0正常 1停用）')
    del_flag = Column(String(1), nullable=True, default=0, comment='删除标志（0代表存在 2代表删除）')
    create_by = Column(String(64), nullable=True, default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), nullable=True, default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')