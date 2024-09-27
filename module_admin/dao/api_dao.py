#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/26 21:57
# @Author  : 冉勇
# @Site    : 
# @File    : api_dao.py
# @Software: PyCharm
# @desc    : 接口配置模块数据库操作层
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.api_do import Api
from module_admin.entity.vo.api_vo import *
from utils.page_util import PageUtil
from datetime import datetime, time


class ApiDao:
    """
    接口配置模块数据库操作层
    """

    @classmethod
    async def get_api_detail_by_id(cls, db: AsyncSession, api_id: int):
        """
        根据id获取接口配置详细信息
        :param db: orm对象
        :param api_id: 接口id
        :return: 接口信息对象
        """
        api_info = (await db.execute(select(Api).where(Api.api_id == api_id))).scalars().first()

        return api_info

    @classmethod
    async def get_api_detail_by_info(cls, db: AsyncSession, api: ApiModel):
        """
        根据接口名称获取接口配置详细信息
        :param db: orm对象
        :param api:
        :return:
        """
        api_info = ((await db.execute(
            select(Api).where(
                Api.api_name == api.api_name if api.api_name else True
            )
        )).scalars().first())

        return api_info

    @classmethod
    async def get_api_list(cls, db: AsyncSession, query_object: ApiPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取接口列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口信息对象
        """
        query = (
            select(Api).where(
                Api.api_id == query_object.api_id if query_object.api_id is not None else True,
                Api.api_name.like(f'%{query_object.api_name}%') if query_object.api_name else True,
                Api.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
                Api.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            ).distinct()
        )
        api_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return api_list

    @classmethod
    async def add_api_dao(cls, db: AsyncSession, api: ApiModel):
        """
        新增接口数据库操作
        :param db: orm对象
        :param api: 接口对象
        :return:
        """
        try:
            db_api = Api(**api.model_dump())
            db.add(db_api)
            await db.flush()
            return db_api
        except Exception as e:
            await db.rollback()
            raise

    @classmethod
    async def edit_api_dao(cls, db: AsyncSession, api: dict):
        """
        编辑接口数据库操作
        :param db: orm对象
        :param api: 需要更新的接口
        :return:
        """
        await db.execute(
            update(Api),
            [api]
        )

    @classmethod
    async def delete_api_dao(cls, db: AsyncSession, api: ApiModel):
        """
        删除接口数据库操作
        :param db: orm对象
        :param api: 接口对象
        :return:
        """
        await db.execute(delete(Api).where(Api.api_id.in_([api.api_id])))
