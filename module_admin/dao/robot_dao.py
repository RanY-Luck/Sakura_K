#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Create Time    : 2024/09/15 12:42
# @Author         :
# @File           : robot_dao.py
# @Software       : PyCharm
# @desc           : 机器人配置模块数据库操作层
from datetime import datetime, time

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.entity.do.robot_do import Robot
from module_admin.entity.vo.robot_vo import *
from utils.page_util import PageUtil


class RobotDao:
    """
    机器人配置模块数据库操作层
    """

    @classmethod
    async def get_robot_detail_by_id(cls, db: AsyncSession, robot_id: int):
        """
        根据id获取机器人配置详细信息
        :param db: orm对象
        :param robot_id: 机器人id
        :return: 机器人信息对象
        """
        robot_info = (await db.execute(
            select(Robot)
                .where(Robot.robot_id == robot_id)
        )).scalars().first()

        return robot_info

    @classmethod
    async def get_robot_detail_by_info(cls, db: AsyncSession, robot: RobotModel):
        """
        根据机器人名称获取机器人配置详细信息
        :param db: orm对象
        :param robot:
        :return:
        """
        robot_info = (
            (
                await db.execute(
                    select(Robot).where(
                        Robot.robot_name == robot.robot_name if robot.robot_name else True
                    )
                )
            ).scalars().first())

        return robot_info

    @classmethod
    async def get_robot_list(cls, db: AsyncSession, query_object: RobotPageQueryModel, is_page: bool = False):
        """
        根据查询参数获取机器人列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 机器人信息对象
        """
        query = (
            select(Robot)
                .where(
                Robot.del_flag == '0',
                Robot.robot_id == query_object.robot_id if query_object.robot_id is not None else True,
                Robot.robot_name.like(f'%{query_object.robot_name}%') if query_object.robot_name else True,
                Robot.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
                Robot.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
                .distinct()
                .order_by(Robot.create_time.desc())
        )
        robot_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return robot_list

    @classmethod
    async def add_robot_dao(cls, db: AsyncSession, robot: RobotModel):
        """
        新增机器人数据库操作
        :param db: orm对象
        :param robot: 机器人对象
        :return:
        """
        db_robot = Robot(**robot.model_dump())
        db.add(db_robot)
        await db.flush()

        return db_robot

    @classmethod
    async def edit_robot_dao(cls, db: AsyncSession, robot: dict):
        """
        编辑机器人数据库操作
        :param db: orm对象
        :param robot: 需要更新的机器人
        :return:
        """
        await db.execute(
            update(Robot),
            [robot]
        )

    @classmethod
    async def delete_robot_dao(cls, db: AsyncSession, robot: RobotModel):
        """
        删除机器人数据库操作
        :param db: orm对象
        :param robot: 机器人对象
        :return:
        """
        await db.execute(
            update(Robot)
                .where(Robot.robot_id == robot.robot_id)
                .values(del_flag='1', update_by=robot.update_by, update_time=robot.update_time)
        )
