#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:30
# @Author   : 冉勇
# @File     : wx_user_dao.py
# @Software : PyCharm
# @Desc     :
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.user_do import UserWechat
from module_admin.entity.vo.user_vo import UserWechatModel


class WxUserDao:

    @classmethod
    async def get_wx_user_by_phone(cls, db: AsyncSession, phone: str) -> UserWechat:
        """
        根据用户名获取用户信息
        :return: 当前用户名的用户信息对象
        """
        query_user_info = (
            (
                await db.execute(
                    select(UserWechat)
                    .where(UserWechat.user_phone == phone)
                    .order_by(desc(UserWechat.create_time))
                )
            )
            .scalars()
            .first()
        )
        return query_user_info

    @classmethod
    async def add_wx_user_dao(cls, db: AsyncSession, user: UserWechatModel) -> UserWechat:
        db_wx_user = UserWechat(**user.model_dump())
        db.add(db_wx_user)
        await db.flush()

        return db_wx_user

    @classmethod
    async def get_wx_user_by_openid(cls, db: AsyncSession, openid: str) -> UserWechat:
        """
        根据用户名获取用户信息
        :return: 当前用户名的用户信息对象
        """
        query_user_info = (
            (
                await db.execute(
                    select(UserWechat)
                    .where(UserWechat.openid == openid)
                    .order_by(desc(UserWechat.create_time))
                )
            )
            .scalars()
            .first()
        )
        return query_user_info
