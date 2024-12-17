#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:58
# @Author  : 冉勇
# @Site    : 
# @File    : dict_do.py
# @Software: PyCharm
# @desc    : 字典类型表
from sqlalchemy import Column, Integer, String, UniqueConstraint
from config.db_base import BaseModel


class SysDictType(BaseModel):
    """
    字典类型表
    """
    __tablename__ = 'sys_dict_type'
    __table_args__ = ({'comment': '字典类型表'})

    dict_id = Column(Integer, primary_key=True, autoincrement=True, comment='字典主键')
    dict_name = Column(String(100), nullable=True, default='', comment='字典名称')
    dict_type = Column(String(100), nullable=True, default='', comment='字典类型')
    status = Column(String(1), nullable=True, default='0', comment='状态（0正常 1停用）')

    __table_args__ = (
        UniqueConstraint('dict_type', name='uq_sys_dict_type_dict_type'),
    )


class SysDictData(BaseModel):
    """
    字典数据表
    """
    __tablename__ = 'sys_dict_data'

    dict_code = Column(Integer, primary_key=True, autoincrement=True, comment='字典编码')
    dict_sort = Column(Integer, nullable=True, default=0, comment='字典排序')
    dict_label = Column(String(100), nullable=True, default='', comment='字典标签')
    dict_value = Column(String(100), nullable=True, default='', comment='字典键值')
    dict_type = Column(String(100), nullable=True, default='', comment='字典类型')
    css_class = Column(String(100), nullable=True, default=None, comment='样式属性（其他样式扩展）')
    list_class = Column(String(100), nullable=True, default=None, comment='表格回显样式')
    is_default = Column(String(1), nullable=True, default='N', comment='是否默认（Y是 N否）')
    status = Column(String(1), nullable=True, default='0', comment='状态（0正常 1停用）')
