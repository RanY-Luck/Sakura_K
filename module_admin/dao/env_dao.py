#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/10/28 17:28
# @Author   : 冉勇
# @File     : env_dao.py
# @Software : PyCharm
# @Desc     : 环境配置模块数据库操作层
from datetime import time

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.env_do import Env
from module_admin.entity.vo.env_vo import *
from utils.page_util import PageUtil


class EnvDao:
    """
    环境配置模块数据库操作层
    """

    @classmethod
    async def get_env_detail_by_id(cls, db: AsyncSession, env_id: int):
        """
        根据id获取环境配置详细信息
        :param db: orm对象
        :param env_id: 环境id
        :return: 环境信息对象
        """
        env_info = (await db.execute(select(Env).where(Env.env_id == env_id))).scalars().first()

        return env_info

    @classmethod
    async def get_env_detail_by_info(cls, db: AsyncSession, env: EnvModel):
        """
        根据环境名称获取环境配置详细信息
        :param db: orm对象
        :param env:
        :return:
        """
        env_info = ((await db.execute(
            select(Env).where(
                Env.env_name == env.env_name if env.env_name else True
            )
        )).scalars().first())

        return env_info

    @classmethod
    async def get_env_list(
            cls, db: AsyncSession, query_object: EnvPageQueryModel, is_page: bool = False
    ):
        """
        根据查询参数获取环境列表信息
        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境信息对象
        """
        query = (
            select(Env)
            .where(
                Env.env_id == query_object.env_id if query_object.env_id is not None else True,
                Env.env_name.like(f'%{query_object.env_name}%') if query_object.env_name else True,
                Env.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
                Env.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
            .distinct()
            .order_by(Env.create_time.desc())
        )
        env_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return env_list

    @classmethod
    async def add_env_dao(cls, db: AsyncSession, env: EnvModel):
        """
        新增环境数据库操作
        :param db: orm对象
        :param env: 环境对象
        :return:
        """
        try:
            db_env = Env(**env.model_dump())
            db.add(db_env)
            await db.flush()
            return db_env
        except Exception as e:
            await db.rollback()
            raise

    @classmethod
    async def edit_env_dao(cls, db: AsyncSession, env: dict):
        """
        编辑环境数据库操作
        :param db: orm对象
        :param env: 需要更新的接口
        :return:
        """
        await db.execute(
            update(Env),
            [env]
        )

    @classmethod
    async def delete_env_dao(cls, db: AsyncSession, env: EnvModel):
        """
        删除环境数据库操作
        :param db: orm对象
        :param env: 接口对象
        :return:
        """
        await db.execute(delete(Env).where(Env.env_id.in_([env.env_id])))
