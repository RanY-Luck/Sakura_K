#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/1 20:44
# @Author   : 冉勇
# @File     : servermanage_do.py
# @Software : PyCharm
# @Desc     : 服务器表
from sqlalchemy import Column, Integer, String
from config.db_base import BaseModel


class Ssh(BaseModel):
    """
    服务器表
    """
    __tablename__ = 'ssh_info'
    __table_args__ = ({'comment': '服务器表'})

    ssh_id = Column(Integer, primary_key=True, autoincrement=True, comment='服务器ID')
    ssh_name = Column(String(10), nullable=False, comment='服务器名称')
    ssh_host = Column(String(128), nullable=False, comment='服务器地址')
    ssh_username = Column(String(128), nullable=True, comment='服务器用户名')
    ssh_password = Column(String(128), nullable=True, comment='服务器密码')
    ssh_port = Column(Integer, nullable=True, comment='服务器端口')



