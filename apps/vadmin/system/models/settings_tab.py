#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:18
# @Author  : 冉勇
# @Site    : 
# @File    : settings_tab.py
# @Software: PyCharm
# @desc    : 系统配置分类模型
from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean

"""
代码解释：
实现了一个系统配置分类表VadminSystemSettingsTab，并通过relationship方法定义了该表与VadminSystemSettings表的关联关系。
在VadminSystemSettingsTab表中，包含了title、classify、tab_label、tab_name、hidden和disabled等字段。其中，title表示标题；classify表示分类键，具有唯一性，不能为空；
tab_label表示tab标题；tab_name表示tab标识符，具有唯一性，不能为空；hidden表示该tab是否被隐藏；disabled表示该tab是否被禁用。
同时，也通过relationship方法定义了与VadminSystemSettings表的关联关系，back_populates参数表示在VadminSystemSettings表中与之关联的字段。
"""


class VadminSystemSettingsTab(BaseModel):
    __tablename__ = "vadmin_system_settings_tab"
    __table_args__ = ({"comment": "系统配置分类表"})
    title = Column(String(255), comment="标题")
    classify = Column(String(255), index=True, nullable=False, comment="分类键")
    tab_label = Column(String(255), comment="tab标题")
    tab_name = Column(String(255), index=True, nullable=False, unique=True, comment="tab标识符")
    hidden = Column(Boolean, default=False, comment="是否隐藏")
    disabled = Column(Boolean, default=False, comment="是否禁用")
    settings = relationship("VadminSystemSettings", back_populates="tab")
