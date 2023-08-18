#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:03
# @Author  : 冉勇
# @Site    :
# @File    : settings.py
# @Software: PyCharm
# @desc    : 系统字典模型
from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, TEXT, Integer, ForeignKey, Boolean

"""
代码解释：
实现了一个系统配置表VadminSystemSettings，通过relationship方法定义了该表与VadminSystemSettingsTab表的关联关系。
在VadminSystemSettings表中，包含了config_label、config_key、config_value、remark、disabled和tab_id等字段。
其中，config_label表示配置表标签；config_key表示配置表键，具有唯一性，不能为空；
config_value表示配置表内容；remark表示备注信息；disabled表示该配置是否被禁用；tab_id是用来关联VadminSystemSettingsTab表的外键。
同时，也通过relationship方法定义了与VadminSystemSettingsTab表的关联关系，
foreign_keys参数表示VadminSystemSettings表中的外键，back_populates参数表示在VadminSystemSettingsTab表中与之关联的字段。
"""


class VadminSystemSettings(BaseModel):
    __tablename__ = "vadmin_system_settings"
    __table_args__ = ({'comment': '系统配置表'})

    config_label = Column(String(255), comment="配置表标签")
    config_key = Column(String(255), index=True, nullable=False, unique=True, comment="配置表键")
    config_value = Column(TEXT, comment="配置表内容")
    remark = Column(String(255), comment="备注信息")
    disabled = Column(Boolean, default=False, comment="是否禁用")

    tab_id = Column(Integer, ForeignKey("vadmin_system_settings_tab.id", ondelete='CASCADE'), comment="关联tab标签")
    tab = relationship("VadminSystemSettingsTab", foreign_keys=tab_id, back_populates="settings")
