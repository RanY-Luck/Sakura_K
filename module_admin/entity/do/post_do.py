#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:07
# @Author  : 冉勇
# @Site    : 
# @File    : post_do.py
# @Software: PyCharm
# @desc    : 岗位信息表
from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base
from datetime import datetime


class SysPost(Base):
    """
    岗位信息表
    """
    __tablename__ = 'sys_post'
    __table_args__ = ({'comment': '岗位信息表'})

    post_id = Column(Integer, primary_key=True, autoincrement=True, comment='岗位ID')
    post_code = Column(String(64), nullable=False, comment='岗位编码')
    post_name = Column(String(50), nullable=False, comment='岗位名称')
    post_sort = Column(Integer, nullable=False, comment='显示顺序')
    status = Column(String(1), nullable=False, default='0', comment='状态（0正常 1停用）')
    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, nullable=True, default=datetime.now(), comment='创建时间')
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, nullable=True, default=datetime.now(), comment='更新时间')
    remark = Column(String(500), nullable=True, default=None, comment='备注')