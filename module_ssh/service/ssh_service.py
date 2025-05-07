#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/7 10:03
# @Author   : 冉勇
# @File     : ssh_service.py
# @Software : PyCharm
# @Desc     : 服务器操作模块服务层
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.service.servermanage_service import SshService
from utils.pwd_util import PwdUtil, hash_key


async def get_ssh_connection_details(query_db: AsyncSession, ssh_id: int):
    """
    通过ssh_id获取SSH连接详情
    :param query_db: 数据库会话
    :param ssh_id: SSH服务器ID
    :return:
    """
    try:
        # 获取SSH服务器详情
        ssh_info = await SshService.ssh_detail_services(query_db, ssh_id)
        if not ssh_info:
            return None
        # 解密密码
        password = None
        if ssh_info.ssh_password:
            password = PwdUtil.decrypt(hash_key=hash_key, hashed_password=ssh_info.ssh_password)
        return ssh_info.ssh_host, ssh_info.ssh_username, password, ssh_info.ssh_port
    except Exception as e:
        return None
