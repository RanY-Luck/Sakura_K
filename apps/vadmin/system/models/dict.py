#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 19:57
# @Author  : 冉勇
# @Site    :
# @File    : dict.py
# @Software: PyCharm
# @desc    : 系统字典模型
from sqlalchemy import Column, String, Boolean, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.db_base import BaseModel

"""
代码解释：
实现了一个字典类型表VadminDictType和字典详情表VadminDictDetails，通过relationship方法定义了两个表之间的关系。
在VadminDictType表中，包含了dict_name、dict_type、disabled和remark等字段。
其中，dict_name和dict_type分别对应字典名称和类型，具有唯一性，不能为空；
disabled表示该字典状态是否被禁用；remark表示备注信息。
同时，通过relationship方法定义了与VadminDictDetails表的关联关系，back_populates参数表示在VadminDictDetails表中与之关联的字段。
在VadminDictDetails表中，则包含了label、value、disabled、is_delete、order、dict_type_id和remark等字段。
其中，label和value分别对应字典标签和键值，具有唯一性，不能为空；
disabled表示该字典状态是否被禁用；is_delete表示该字典是否为默认值；order表示该字典在字典类型中的排序；
dict_type_id是用来关联字典类型表VadminDictType的外键。
同时，也通过relationship方法定义了与VadminDictType表的关联关系，foreign_keys参数表示VadminDictDetails表中的外键，
back_populates参数表示在VadminDictType表中与之关联的字段。
"""


class VadminDictType(BaseModel):
    __tablename__ = "vadmin_system_dict_type"
    __table_args__ = ({'comment': '字典类型表'})

    dict_name = Column(String(50), index=True, nullable=False, comment="字典名称")
    dict_type = Column(String(50), index=True, nullable=False, comment="字典类型")
    disabled = Column(Boolean, default=False, comment="字典状态，是否禁用")
    remark = Column(String(255), comment="备注")
    details = relationship("VadminDictDetails", back_populates="dict_type")


class VadminDictDetails(BaseModel):
    __tablename__ = "vadmin_system_dict_details"
    __table_args__ = ({'comment': '字典详情表'})

    label = Column(String(50), index=True, nullable=False, comment="字典标签")
    value = Column(String(50), index=True, nullable=False, comment="字典键值")
    disabled = Column(Boolean, default=False, comment="字典状态，是否禁用")
    is_default = Column(Boolean, default=False, comment="是否默认")
    order = Column(Integer, comment="字典排序")
    dict_type_id = Column(Integer, ForeignKey("vadmin_system_dict_type.id", ondelete='CASCADE'), comment="关联字典类型")
    dict_type = relationship("VadminDictType", foreign_keys=dict_type_id, back_populates="details")
    remark = Column(String(255), comment="备注")
