#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/1 21:03
# @Author   : 冉勇
# @File     : servermanage_dao.py
# @Software : PyCharm
# @Desc     : 环境配置模块数据库操作层
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.servermanage_do import Ssh
from module_admin.entity.vo.servermanage_vo import *
from utils.page_util import PageUtil
from datetime import datetime, time


class SshDao:
    """
    服务器模块数据库操作层
    """

    @classmethod
    async def get_ssh_detail_by_id(cls, db: AsyncSession, ssh_id: int):
        """
        根据id获取服务器配置详细信息
        :param db: orm对象
        :param ssh_id: 服务器id
        :return: 服务器信息对象
        """
        ssh_info = (await db.execute(select(Ssh).where(Ssh.ssh_id == ssh_id))).scalars().first()

        return ssh_info

    @classmethod
    async def get_ssh_detail_by_info(cls, db: AsyncSession, ssh: SshModel):
        """
        根据服务器名称获取服务器配置详细信息
        :param db: orm对象
        :param ssh: 服务器参数对象
        :return: 服务器信息对象
        """
        ssh_info = ((await db.execute(
            select(Ssh).where(
                Ssh.ssh_name == ssh.ssh_name if ssh.ssh_name else True
            )
        )).scalars().first())

        return ssh_info

    @classmethod
    async def get_ssh_list(
            cls, db: AsyncSession, query_object: SshPageQueryModel, is_page: bool = False
    ):
        """
        根据查询参数获取服务器列表信息
        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 服务器信息对象
        """
        query = (
            select(Ssh)
                .where(
                Ssh.del_flag == '0',
                Ssh.ssh_id == query_object.ssh_id if query_object.ssh_id is not None else True,
                Ssh.ssh_name.like(f'%{query_object.ssh_name}%') if query_object.ssh_name else True,
                Ssh.ssh_host.like(f'%{query_object.ssh_host}%') if query_object.ssh_host else True,
                Ssh.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
                Ssh.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
                .order_by(Ssh.create_time.desc())
                .distinct()
        )
        ssh_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return ssh_list

    # @classmethod
    # async def get_ssh_list(cls, db: AsyncSession, query_object: SshPageQueryModel, is_page: bool = False):
    #     """
    #     根据查询参数获取环境列表信息
    #
    #     :param db: orm对象
    #     :param query_object: 查询参数对象
    #     :param is_page: 是否开启分页
    #     :return: 环境列表信息对象
    #     """
    #     query = (
    #         select(Ssh)
    #         .where(
    #         )
    #         .order_by(Ssh.ssh_id)
    #         .distinct()
    #     )
    #     info_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
    #
    #     return info_list

    @classmethod
    async def add_ssh_dao(cls, db: AsyncSession, ssh: SshModel):
        """
        新增服务器数据库操作
        :param db: orm对象
        :param ssh: 服务器对象
        :return:
        """
        try:
            db_ssh = Ssh(**ssh.model_dump())
            db.add(db_ssh)
            await db.flush()
            return db_ssh
        except Exception as e:
            await db.rollback()
            raise

    @classmethod
    async def edit_ssh_dao(cls, db: AsyncSession, ssh: dict):
        """
        编辑服务器数据库操作
        :param db: orm对象
        :param ssh: 需要更新的接口
        :return:
        """
        await db.execute(
            update(Ssh),
            [ssh]
        )

    @classmethod
    async def delete_ssh_dao(cls, db: AsyncSession, ssh: SshModel):
        """
        删除服务器数据库操作
        :param db: orm对象
        :param ssh: 服务器对象
        :return:
        """
        await db.execute(
            update(Ssh)
                .where(Ssh.ssh_id == ssh.ssh_id)
                .values(del_flag='1', update_by=ssh.update_by, update_time=ssh.update_time)
        )
