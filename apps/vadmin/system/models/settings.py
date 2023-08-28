#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/19 11:03
# @Author  : 冉勇
# @Site    :
# @File    : settings.py
# @Software: PyCharm
# @desc    : 系统字典模型
from sqlalchemy import String, Integer, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

from db.db_base import BaseModel

"""
代码解释：
实现了一个系统配置表VadminSystemSettings，通过relationship方法定义了该表与VadminSystemSettingsTab表的关联关系。
在VadminSystemSettings表中，包含了config_label、config_key、config_value、remark、disabled和tab_id等字段。
其中，config_label表示配置表标签；config_key表示配置表键，具有唯一性，不能为空；
config_value表示配置表内容；remark表示备注信息；disabled表示该配置是否被禁用；tab_id是用来关联VadminSystemSettingsTab表的外键。
同时，也通过relationship方法定义了与VadminSystemSettingsTab表的关联关系，
foreign_keys参数表示VadminSystemSettings表中的外键，back_populates参数表示在VadminSystemSettingsTab表中与之关联的字段。
"""


class VadminSystemSettingsTab(BaseModel):
    __tablename__ = "vadmin_system_settings_tab"
    __table_args__ = ({'comment': '系统配置分类表'})

    title: Mapped[str] = mapped_column(String(255), comment="标题")
    classify: Mapped[str] = mapped_column(String(255), index=True, nullable=False, comment="分类键")
    tab_label: Mapped[str] = mapped_column(String(255), comment="tab标题")
    tab_name: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True, comment="tab标识符")
    hidden: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否隐藏")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    settings: Mapped[list["VadminSystemSettings"]] = relationship(back_populates="tab")


class VadminSystemSettings(BaseModel):
    __tablename__ = "vadmin_system_settings"
    __table_args__ = ({'comment': '系统配置表'})

    config_label: Mapped[str] = mapped_column(String(255), comment="配置表标签")
    config_key: Mapped[str] = mapped_column(String(255), index=True, nullable=False, unique=True, comment="配置表键")
    config_value: Mapped[str | None] = mapped_column(Text, comment="配置表内容")
    remark: Mapped[str | None] = mapped_column(String(255), comment="备注信息")
    disabled: Mapped[bool] = mapped_column(Boolean, default=False, comment="是否禁用")
    tab_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("vadmin_system_settings_tab.id", ondelete='CASCADE'),
        comment="关联tab标签"
    )
    tab: Mapped[VadminSystemSettingsTab] = relationship(foreign_keys=tab_id, back_populates="settings")
