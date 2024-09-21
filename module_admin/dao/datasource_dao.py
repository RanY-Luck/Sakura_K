#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/17 16:22
# @Author  : 冉勇
# @Site    : 
# @File    : datasource_dao.py
# @Software: PyCharm
# @desc    : 数据源配置模块数据库操作层
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.datasource_do import DataSource
from module_admin.entity.vo.datasource_vo import *
from utils.page_util import PageUtil
from datetime import datetime, time


class DataSourceDao:
    """
    数据源配置模块数据库操作层
    """

    @classmethod
    async def get_datasource_detail_by_id(cls, db: AsyncSession, datasource_id: int):
        """
        根据id获取数据源配置详细信息
        :param db: orm对象
        :param datasource_id: 数据源id
        :return: 数据源信息对象
        """
        datasource_info = (await db.execute(
            select(DataSource)
                .where(DataSource.datasource_id == datasource_id)
        )).scalars().first()
        return datasource_info

    @classmethod
    async def get_datasource_detail_by_info(cls, db: AsyncSession, datasource: DataSourceModel):
        """
        根据数据源名称获取机器人配置详细信息
        :param db: orm对象
        :param datasource:
        :return:
        """
        datasource_info = (
            (
                await db.execute(
                    select(DataSource).where(
                        DataSource.datasource_name == datasource.datasource_name if datasource.datasource_name else True
                    )
                )
            ).scalars().first())

        return datasource_info

    @classmethod
    async def get_datasource_list(cls, db: AsyncSession, query_object: DataSourcePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取数据源列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据源信息对象
        """
        query = (
            select(DataSource).where(
                DataSource.datasource_id == query_object.datasource_id if query_object.datasource_id is not None else True,
                DataSource.datasource_name.like(
                    f'%{query_object.datasource_name}%'
                ) if query_object.datasource_name else True,
                DataSource.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
                DataSource.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time else True
            ).distinct()
        )
        datasource_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return datasource_list

    @classmethod
    async def add_datasource_dao(cls, db: AsyncSession, datasource: DataSourceModel):
        """
        新增数据源数据库操作
        :param db: orm对象
        :param datasource: 数据源对象
        :return:
        """
        db_datasource = DataSource(**datasource.model_dump())
        db.add(db_datasource)
        await db.flush()

        return db_datasource

    @classmethod
    async def edit_datasource_dao(cls, db: AsyncSession, datasource: dict):
        """
        编辑数据源数据库操作
        :param db: orm对象
        :param datasource: 需要更新的数据源
        :return:
        """
        await db.execute(
            update(DataSource),
            [datasource]
        )

    @classmethod
    async def delete_datasource_dao(cls, db: AsyncSession, datasource: DataSourceModel):
        """
        删除数据源数据库操作
        :param db: orm对象
        :param datasource: 数据源对象
        :return:
        """
        await db.execute(
            delete(DataSource)
                .where(DataSource.datasource_id.in_([datasource.datasource_id]))
        )
