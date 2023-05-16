#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 15:11
# @Author  : 冉勇
# @Site    :
# @File    : issue.py
# @Software: PyCharm
# @desc    : 常见问题
from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, Text


class VadminIssueCategory(BaseModel):
    """
    代码解释：
    定义了一个名为VadminIssueCategory的Pydantic模型类，用于表示常见问题的类别。
    在该类中，__tablename__属性指定了此模型类对应的数据库表名，__table_args__属性指定了表名的注释信息。
    该类中还包含了四个属性，分别为name、platform、is_active和user_id。这些属性通过Column函数映射到数据库表结构中，包括了数据类型、索引、非空约束、注释等信息。
    其中，name属性指定了类别名称，属于50个字符长度的字符串类型，被定义为不允许为空且需要建立索引的列；
    platform属性指定了展示平台，属于8个字符长度的字符串类型，被定义为不允许为空且需要建立索引的列；
    is_active属性指定了是否可见，属于布尔类型，在表中默认值为True；
    user_id属性指定了创建人，属于整数类型，是vadmin_auth_user表中某一行的ID。
    此外，该模型类中还定义了一个名为user的关系属性，表示Category模型与User模型之间的关联关系。
    关联关系通过ForeignKey和relationship函数建立，在数据库中通过外键进行关联查询。
    """
    __tablename__ = "vadmin_help_issue_category"
    __table_args__ = ({'comment': '常见问题类别表'})
    name = Column(String(50), index=True, nullable=False, comment="类别名称")
    platform = Column(String(8), index=True, nullable=False, comment="展示平台")
    is_active = Column(Boolean, default=True, comment="是否可见")
    issues = relationship("VadminIssue", back_populates='category')
    create_user_id = Column(ForeignKey("vadmin_auth_user.id", ondelete='SET NULL'), comment="创建人")
    create_user = relationship("VadminUser", foreign_keys=create_user_id)


class VadminIssue(BaseModel):
    __tablename__ = "vadmin_help_issue"
    __table_args__ = ({'comment': '常见问题记录表'})
    category_id = Column(ForeignKey("vadmin_help_issue_category.id", ondelete='CASCADE'), comment="类别")
    category = relationship("VadminIssueCategory", foreign_keys=category_id, back_populates='issues')
    title = Column(String(255), index=True, nullable=False, comment="标题")
    content = Column(Text, comment="内容")
    view_number = Column(Integer, default=0, comment="查看次数")
    is_active = Column(Boolean, default=True, comment="是否可见")
    create_user_id = Column(ForeignKey("vadmin_auth_user.id", ondelete='SET NULL'), comment="创建人")
    create_user = relationship("VadminUser", foreign_keys=create_user_id)
