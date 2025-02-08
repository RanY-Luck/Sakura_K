#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:06
# @Author  : 冉勇
# @Site    : 
# @File    : user_do.py
# @Software: PyCharm
# @desc    : 用户信息表
from sqlalchemy import Column, Integer, String, DateTime
from config.database import Base, BaseMixin
from datetime import datetime


class SysUser(Base):
    """
    用户信息表
    """
    __tablename__ = 'sys_user'
    __table_args__ = ({'comment': '用户信息表'})

    user_id = Column(Integer, primary_key=True, autoincrement=True, comment='用户ID')
    dept_id = Column(Integer, default=None, comment='部门ID')
    user_name = Column(String(30), nullable=False, comment='用户账号')
    nick_name = Column(String(30), nullable=False, comment='用户昵称')
    user_type = Column(String(2), default='00', comment='用户类型（00系统用户）')
    email = Column(String(50), default='', comment='用户邮箱')
    phonenumber = Column(String(11), default='', comment='手机号码')
    sex = Column(String(1), default='0', comment='用户性别（0男 1女 2未知）')
    avatar = Column(String(100), default='', comment='头像地址')
    password = Column(String(100), default='', comment='密码')
    status = Column(String(1), default='0', comment='帐号状态（0正常 1停用）')
    del_flag = Column(String(1), default='0', comment='删除标志（0代表存在 2代表删除）')
    login_ip = Column(String(128), default='', comment='最后登录IP')
    login_date = Column(DateTime, comment='最后登录时间')
    create_by = Column(String(64), default='', comment='创建者')
    create_time = Column(DateTime, comment='创建时间', default=datetime.now())
    update_by = Column(String(64), default='', comment='更新者')
    update_time = Column(DateTime, comment='更新时间', default=datetime.now())
    remark = Column(String(500), default=None, comment='备注')


class SysUserRole(Base):
    """
    用户和角色关联表
    """
    __tablename__ = 'sys_user_role'

    user_id = Column(Integer, primary_key=True, nullable=False, comment='用户ID')
    role_id = Column(Integer, primary_key=True, nullable=False, comment='角色ID')


class SysUserPost(Base):
    """
    用户与岗位关联表
    """
    __tablename__ = 'sys_user_post'

    user_id = Column(Integer, primary_key=True, nullable=False, comment='用户ID')
    post_id = Column(Integer, primary_key=True, nullable=False, comment='岗位ID')


class UserWechat(Base, BaseMixin):
    """
    用户微信信息
    """

    __tablename__ = 'user_wechat'

    user_id = Column(Integer, nullable=False, comment='用户ID')
    city = Column(String(100), nullable=True, comment='城市')
    country = Column(String(100), nullable=True, comment='国家')
    head_img_url = Column(String(255), nullable=True, comment='微信头像')
    nickname = Column(String(255), nullable=True, comment='微信昵称')
    openid = Column(String(255), unique=True, nullable=False, comment='openid')
    union_id = Column(String(255), nullable=False, comment='union_id')
    user_phone = Column(String(15), unique=True, nullable=False, comment='手机号')
    province = Column(String(255), nullable=True, comment='省份')
    sex = Column(Integer, nullable=True, comment='性别')
