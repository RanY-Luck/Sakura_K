#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:11
# @Author  : 冉勇
# @Site    : 
# @File    : login_dao.py
# @Software: PyCharm
# @desc    : 登录管理模块数据库操作层
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.user_do import SysUser
from module_admin.entity.do.dept_do import SysDept


async def login_by_account(db: AsyncSession, user_name: str):
    """
    根据用户名查询用户信息
    :param db: orm对象
    :param user_name: 用户名
    :return: 用户对象
    """
    user = (await db.execute(
        select(SysUser, SysDept)
            .where(SysUser.user_name == user_name, SysUser.del_flag == '0')
            .join(
            SysDept,
            and_(SysUser.dept_id == SysDept.dept_id, SysDept.status == 0, SysDept.del_flag == 0),
            isouter=True
        )
            .distinct()
    )).first()
    return user
