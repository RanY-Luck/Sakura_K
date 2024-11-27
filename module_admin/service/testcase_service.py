#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 17:28
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_service.py
# @Software: PyCharm
# @desc    : 测试用例模块服务层
import asyncio
from typing import List
from module_admin.dao.testcase_dao import *
from module_admin.entity.vo.common_vo import CrudResponseModel
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
    async def testcase_batch_services(cls, query_db: AsyncSession, testcase_ids: List[int], env_id: int):
        """
        批量运行测试用例service
        :param query_db: orm对象
        :param testcase_ids: 测试用例id列表
        :param env_id: 环境id
        :return: 批量测试用例响应结果
        """

        # 并发执行多个测试用例的调试
        async def debug_single_testcase(testcase_id: int):
            start_time = round(datetime.now().timestamp(), 3)
            try:
                # 查询测试用例列表，获取对应的接口信息
                query_object = TestCasePageQueryModel(testcase_ids=[testcase_id])
                testcase_list_result = await TestCaseDao.get_testcase_list(query_db, query_object, is_page=False)

                # 如果没有找到测试用例，返回错误
                if not testcase_list_result or len(testcase_list_result) == 0:
                    return {
                        'testcase_id': testcase_id,
                        'is_success': False,
                        'error': f'未找到测试用例 {testcase_id} 的相关信息'
                    }

                # 取第一个测试用例
                testcase_info = testcase_list_result[0]

                # 调试对应的接口
                result = await ApiService.api_debug_services(query_db, testcase_info.api_id, env_id)

                end_time = round(datetime.now().timestamp(), 3)
                return {
                    'testcase_id': testcase_id,
                    'api_id': testcase_info.api_id,
                    'testcase_name': testcase_info.testcase_name,
                    'is_success': True,
                    'response': result,
                    'duration': end_time - start_time
                }
            except Exception as e:
                return {
                    'testcase_id': testcase_id,
                    'is_success': False,
                    'error': str(e)
                }

        # 使用asyncio.gather并发执行所有测试用例调试
        results = await asyncio.gather(
            *[debug_single_testcase(testcase_id) for testcase_id in testcase_ids]
        )

        return results
