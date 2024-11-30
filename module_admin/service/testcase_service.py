#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 17:28
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_service.py
# @Software: PyCharm
# @desc    : 测试用例模块服务层
import asyncio
from typing import List, Union

from module_admin.dao.api_dao import ApiDao
from module_admin.dao.env_dao import EnvDao
from module_admin.dao.testcase_dao import *
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.env_vo import EnvModel
from utils.common_util import CamelCaseUtil
from module_admin.service.api_service import ApiService


class TestCaseService:
    """
    测试用例模块服务层
    """

    @classmethod
    async def get_testcase_list_services(
            cls,
            query_db: AsyncSession,
            query_object: TestCasePageQueryModel,
            is_page: bool = True
    ):
        """
        获取测试用例列表service
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 测试用例列表信息对象
        """
        testcase_list_result = await TestCaseDao.get_testcase_list(query_db, query_object, is_page)

        return testcase_list_result

    @classmethod
    async def add_testcase_services(cls, query_db: AsyncSession, page_object: TestCaseModel):
        """
        新增测试用例列表service
        :param query_db: orm对象
        :param page_object: 新增测试用例对象
        :return: 新增测试用例校验结果
        """
        testcase = await TestCaseDao.get_testcase_detail_by_info(query_db, page_object)
        if testcase:
            result = dict(is_success=False, message=f'测试用例:{testcase.testcase_name} 已存在')
        else:
            try:
                await TestCaseDao.add_testcase_dao(query_db, page_object)
                await query_db.commit()
                result = dict(is_success=True, message=f'新增测试用例成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        return CrudResponseModel(**result)

    @classmethod
    async def edit_testcase_services(cls, query_db: AsyncSession, page_object: TestCaseModel):
        """
        编辑测试用例service
        :param query_db: orm对象
        :param page_object: 编辑测试用例对象
        :return: 编辑测试用例校验结果
        """
        edit_testcase = page_object.model_dump(exclude_unset=True)
        testcase_info = await cls.testcase_detail_services(query_db, edit_testcase.get('testcase_id'))
        if testcase_info:
            if testcase_info.testcase_name != page_object.testcase_name:
                testcase = await TestCaseDao.get_testcase_detail_by_info(query_db, page_object)
                if testcase:
                    result = dict(is_success=False, message=f'测试用例:{testcase.testcase_name} 已存在')
                    return CrudResponseModel(**result)
            try:
                await TestCaseDao.edit_testcase_dao(query_db, edit_testcase)
                await query_db.commit()
                result = dict(is_success=True, message=f'测试用例:{testcase_info.testcase_name} 更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='测试用例不存在')

        return CrudResponseModel(**result)

    @classmethod
    async def delete_testcase_services(cls, query_db: AsyncSession, page_object: DeleteTestCaseModel):
        """
        删除测试用例service
        :param query_db: orm对象
        :param page_object: 删除测试用例对象
        :return: 删除测试用例校验结果
        """
        if page_object.testcase_ids.split(','):
            testcase_id_list = page_object.testcase_ids.split(',')
            try:
                for testcase_id in testcase_id_list:
                    await TestCaseDao.delete_testcase_dao(query_db, TestCaseModel(testcaseId=testcase_id))
                await query_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='传入测试用例id为空')
        return CrudResponseModel(**result)

    @classmethod
    async def testcase_detail_services(cls, query_db: AsyncSession, testcase_id: int):
        """
        获取测试用例详细信息service
        :param query_db: orm对象
        :param testcase_id: 测试用例id
        :return: 测试用例id对应的信息
        """
        testcase = await TestCaseDao.get_testcase_detail_by_id(query_db, testcase_id=testcase_id)
        if testcase is None:
            return CrudResponseModel(is_success=False, message=f'接口{testcase_id}不存在')
        result = TestCaseModel(**CamelCaseUtil.transform_result(testcase))

        return result

    @classmethod
    async def testcase_batch_services(cls, query_db: AsyncSession, testcase_id: int, env_id: int):
        """
        运行测试用例service
        :param query_db: 数据库会话
        :param testcase_id: 测试用例ID
        :param env_id: 环境ID
        :return: 接口列表和环境信息，或错误响应
        """
        # 并行获取测试用例接口列表和环境信息
        api_list, env = await asyncio.gather(
            TestCaseDao.get_testcase_and_api_list(query_db, testcase_id),
            EnvDao.get_env_detail_by_id(query_db, env_id=env_id)
        )

        # 检查测试用例接口列表是否存在错误
        if isinstance(api_list, CrudResponseModel):
            return api_list

        # 检查环境是否存在
        if env is None:
            return CrudResponseModel(is_success=False, message=f'环境{env_id}不存在')

        return api_list, env
