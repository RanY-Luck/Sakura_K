#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 17:29
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_dao.py
# @Software: PyCharm
# @desc    : 测试用例模块数据库操作层
from datetime import time
from typing import Union

from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from module_admin.dao.api_dao import ApiDao
from module_admin.entity.do.testcase_do import TestCase
from module_admin.entity.do.project_do import Project
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.testcase_vo import *
from utils.common_util import CamelCaseUtil
from utils.page_util import PageUtil


class TestCaseDao:
    """
    测试用例模块数据库操作层
    """

    @classmethod
    async def get_testcase_detail_by_id(cls, db: AsyncSession, testcase_id: int):
        """
        根据id获取测试用例配置详细信息
        :param db: orm对象
        :param testcase_id: 测试用例id
        :return: 接口信息对象
        """
        testcase_info = (
            await db.execute(select(TestCase).where(TestCase.testcase_id == testcase_id))).scalars().first()

        return testcase_info

    @classmethod
    async def get_testcase_detail_by_info(cls, db: AsyncSession, testcase: TestCaseModel):
        """
        根据接口名称获取接口配置详细信息
        :param db: orm对象
        :param testcase:
        :return:
        """
        testcase_info = ((await db.execute(
            select(TestCase).where(
                TestCase.testcase_name == testcase.testcase_name if testcase.testcase_name else True
            )
        )).scalars().first())

        return testcase_info

    @classmethod
    async def get_testcase_list(
            cls, db: AsyncSession, query_object: TestCaseQueryModel, is_page: bool = False
    ):
        """
        根据查询参数获取测试用例信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 测试用例对象
        """
        query = (
            select(TestCase, Project)
                .join(Project, TestCase.project_id == Project.project_id)
                .where(
                TestCase.del_flag == '0',
                TestCase.testcase_id == query_object.testcase_id if query_object.testcase_id is not None else True,
                TestCase.testcase_name.like(f'%{query_object.testcase_name}%') if query_object.testcase_name else True,
                TestCase.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
                TestCase.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59))
                )
                if query_object.begin_time and query_object.end_time else True
            )
                .distinct()
                .order_by(TestCase.create_time.desc())
        )
        api_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return api_list

    @classmethod
    async def add_testcase_dao(cls, db: AsyncSession, testcase: TestCaseModel):
        """
        新增测试用例数据库操作
        :param db: orm对象
        :param testcase: 测试用例对象
        :return:
        """
        try:
            testcase_api = TestCase(**testcase.model_dump())
            db.add(testcase_api)
            await db.flush()
            return testcase_api
        except Exception as e:
            await db.rollback()
            raise

    @classmethod
    async def edit_testcase_dao(cls, db: AsyncSession, testcase: dict):
        """
        编辑测试用例数据库操作
        :param db: orm对象
        :param testcase: 需要更新的测试用例
        :return:
        """
        await db.execute(
            update(TestCase),
            [testcase]
        )

    @classmethod
    async def delete_testcase_dao(cls, db: AsyncSession, testcase: TestCaseModel):
        """
        删除测试用例数据库操作
        :param db: orm对象
        :param testcase: 测试用例对象
        :return:
        """
        await db.execute(
            update(TestCase)
                .where(TestCase.testcase_id == testcase.testcase_id)
                .values(del_flag='1', update_by=testcase.update_by, update_time=testcase.update_time)
        )

    @classmethod
    async def get_testcase_and_api_list(
            cls,
            query_db: AsyncSession,
            testcase_id: int
    ) -> Union[List[ApiModel], CrudResponseModel]:
        """
        根据测试用例ID获取对应的接口列表
        :param query_db: 数据库会话
        :param testcase_id: 测试用例ID
        :return: 接口列表或错误响应
        """
        # 先获取测试用例详情
        testcase = await TestCaseDao.get_testcase_detail_by_id(query_db, testcase_id=testcase_id)
        if testcase is None:
            return CrudResponseModel(is_success=False, message=f'测试用例{testcase_id}不存在')
        # 获取测试用例中的接口ID列表
        api_ids = testcase.testcase_list if hasattr(testcase, 'testcase_list') else []
        if not api_ids:
            return CrudResponseModel(is_success=False, message='该测试用例没有关联接口')
        # 轮询接口详情
        api_list = []
        for api_id in api_ids:
            api = await ApiDao.get_api_detail_by_id(query_db, api_id=api_id)
            if api:
                # 转换为ApiModel
                api_model = ApiModel(**CamelCaseUtil.transform_result(api))
                api_list.append(api_model)

        return api_list
