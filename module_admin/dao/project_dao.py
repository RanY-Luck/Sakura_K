#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/3 16:49
# @Author  : 冉勇
# @Site    : 
# @File    : project_dao.py
# @Software: PyCharm
# @desc    : 项目列表管理模块数据库操作层
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.project_do import Project
from module_admin.entity.vo.project_vo import *
from utils.page_util import PageUtil
from datetime import datetime, time


class ProjectDao:
    """
    项目列表管理模块数据库操作层
    """

    @classmethod
    async def get_project_detail_by_id(cls, db: AsyncSession, project_id: int):
        """
        根据项目列表id获取通知列表详细信息
        :param db: orm对象
        :param project_id: 项目列表id
        :return: 项目列表信息对象
        """
        project_info = (await db.execute(
            select(Project)
                .where(Project.project_id == project_id)
        )).scalars().first()

        return project_info

    @classmethod
    async def get_project_detail_by_info(cls, db: AsyncSession, project: ProjectModel):
        """
        根据项目列表参数获取通知公告信息
        :param db: orm对象
        :param project: 项目列表参数对象
        :return: 项目列表信息对象
        """
        project_info = (await db.execute(
            select(Project)
                .where(
                Project.project_name == project.project_name if project.project_name else True
            )
        )).scalars().first()

        return project_info

    @classmethod
    async def get_project_list(cls, db: AsyncSession, query_object: ProjectPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取项目列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目列表信息对象
        """
        query = (
            select(Project)
                .where(
                Project.project_id == query_object.project_id if query_object.project_id is not None else True,
                Project.project_name.like(f'%{query_object.project_name}%') if query_object.project_name else True,
                Project.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
                Project.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
                .distinct()
        )
        project_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return project_list

    @classmethod
    async def add_project_dao(cls, db: AsyncSession, project: ProjectModel):
        """
        新增项目列表数据库操作
        :param db: orm对象
        :param project: 项目列表对象
        :return:
        """
        db_project = Project(**project.model_dump())
        db.add(db_project)
        await db.flush()

        return db_project

    @classmethod
    async def edit_project_dao(cls, db: AsyncSession, project: dict):
        """
        编辑项目列表数据库操作
        :param db: orm对象
        :param project: 需要更新的项目列表
        :return:
        """
        await db.execute(
            update(Project),
            [project]
        )

    @classmethod
    async def delete_project_dao(cls, db: AsyncSession, project: ProjectModel):
        """
        删除通知公告数据库操作
        :param db: orm对象
        :param project: 通知公告对象
        :return:
        """
        await db.execute(
            delete(Project)
                .where(Project.project_id.in_([project.project_id]))
        )
