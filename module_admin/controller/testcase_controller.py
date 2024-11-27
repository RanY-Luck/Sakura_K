#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/11/27 18:07
# @Author  : 冉勇
# @Site    : 
# @File    : testcase_controller.py
# @Software: PyCharm
# @desc    : 测试用例配置相关接口
import asyncio
import time
from typing import List
from fastapi import Depends, APIRouter, Request, Query, HTTPException
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.api_vo import BatchApiStats, BatchApi
from module_admin.entity.vo.testcase_vo import *
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.testcase_service import TestCaseService
from module_admin.service.login_service import LoginService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

testcaseController = APIRouter(prefix='/testcase/testcaseInfo', dependencies=[Depends(LoginService.get_current_user)])


@testcaseController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('testcase:testcaseInfo:list'))]
)
async def get_testcase_list(
        request: Request,
        api_page_query: TestCasePageQueryModel = Depends(TestCasePageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db)
):
    """
    获取测试用例列表
    """
    # 获取分页数据
    test_page_query_result = await TestCaseService.get_testcase_list_services(
        query_db,
        api_page_query,
        is_page=True
    )
    logger.info('测试用例获取成功')

    return ResponseUtil.success(model_content=test_page_query_result)


@testcaseController.post('', dependencies=[Depends(CheckUserInterfaceAuth('testcase:testcaseInfo:add'))])
@ValidateFields(validate_model='add_testcase')
@Log(title='测试用例', business_type=BusinessType.INSERT)
async def add_testcase(
        request: Request,
        add_testcase: TestCaseModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    新增测试用例
    """
    add_testcase.create_by = current_user.user.user_name
    add_testcase.create_time = datetime.now()
    add_testcase.update_by = current_user.user.user_name
    add_testcase.update_time = datetime.now()
    add_testcase_result = await TestCaseService.add_testcase_services(query_db, add_testcase)
    logger.info(add_testcase_result.message)

    return ResponseUtil.success(msg=add_testcase_result.message)


@testcaseController.put('', dependencies=[Depends(CheckUserInterfaceAuth('testcase:testcaseInfo:edit'))])
@ValidateFields(validate_model='edit_testcase')
@Log(title='测试用例', business_type=BusinessType.UPDATE)
async def edit_testcase(
        request: Request,
        edit_testcase: TestCaseModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    编辑测试用例
    """
    edit_testcase.update_by = current_user.user.user_name
    edit_testcase.update_time = datetime.now()
    edit_testcase_result = await TestCaseService.edit_testcase_services(query_db, edit_testcase)
    logger.info(edit_testcase_result.message)

    return ResponseUtil.success(msg=edit_testcase_result.message)


@testcaseController.delete(
    '/{testcase_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('testcase:testcaseInfo:remove'))]
)
@Log(title='测试用例', business_type=BusinessType.DELETE)
async def delete_testcase(request: Request, testcase_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除测试用例
    """
    delete_testcase = DeleteTestCaseModel(testcaseIds=testcase_ids)
    delete_testcase_result = await TestCaseService.delete_testcase_services(query_db, delete_testcase)
    logger.info(delete_testcase_result.message)

    return ResponseUtil.success(msg=delete_testcase_result.message)


@testcaseController.get(
    '/{testcase_id}',
    response_model=TestCaseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('testcase:testcaseInfo:query'))]
)
async def query_detail_testcase(request: Request, testcase_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    根据ID获取测试用例信息
    """
    testcase_detail_result = await TestCaseService.testcase_detail_services(query_db, testcase_id)
    logger.info(f'获取testcase_id为{testcase_id}的信息成功')

    return ResponseUtil.success(data=testcase_detail_result)


@testcaseController.post(
    '/batchTestCase',  # 修改路由名称以反映是测试用例批量运行
    response_model=BatchApiStats,
    dependencies=[Depends(CheckUserInterfaceAuth('testcase:testcaseInfo:batchtestcase'))]
)
async def testcase_batch_run(
        request: Request,
        testcase_ids: List[int],  # 修改参数名称
        env_id: int = Query(..., description='环境ID'),
        query_db: AsyncSession = Depends(get_db)
):
    """
    批量运行测试用例，返回执行统计信息
    """
    start_time = time.time()

    # 使用异步并发执行
    async def run_single_testcase(testcase_id: int):
        testcase_start = time.time()
        try:
            # 调用测试用例批量服务
            result = await TestCaseService.testcase_batch_services(query_db, [testcase_id], env_id=env_id)

            # 提取测试用例响应中的status
            testcase_status = result[0].get('response', {}).get('status', False)
            if isinstance(testcase_status, str):
                testcase_status = testcase_status.lower() == 'true'

            return BatchApi(
                id=testcase_id,
                status='success',
                response=result[0],
                execution_time=time.time() - testcase_start,
                api_status=testcase_status  # 添加测试用例响应状态
            )
        except asyncio.TimeoutError:
            execution_time = time.time() - testcase_start
            logger.error(f"测试用例 {testcase_id} 执行超时")
            return BatchApi(
                id=testcase_id,
                status='failed',
                error_message="执行超时",
                execution_time=execution_time,
                api_status=False
            )
        except Exception as e:
            execution_time = time.time() - testcase_start
            logger.error(f"测试用例编号为: {testcase_id} 执行失败: {str(e)}")
            return BatchApi(
                id=testcase_id,
                status='failed',
                error_message=str(e),
                execution_time=execution_time,
                api_status=False
            )

    try:
        # 使用asyncio.gather进行并发处理
        results = await asyncio.gather(
            *[run_single_testcase(testcase_id) for testcase_id in testcase_ids],
            return_exceptions=True
        )

        # 处理结果和统计
        processed_results = []
        testcase_success_count = 0  # 测试用例实际成功计数
        testcase_failure_count = 0  # 测试用例实际失败计数

        for result in results:
            if isinstance(result, Exception):
                testcase_failure_count += 1
                processed_results.append(
                    BatchApi(
                        id=-1,
                        status='failed',
                        error_message=str(result),
                        execution_time=0,
                        api_status=False
                    )
                )
            else:
                processed_results.append(result)
                if result.status == 'success':
                    # 根据测试用例响应状态统计
                    if result.api_status:
                        testcase_success_count += 1
                    else:
                        testcase_failure_count += 1
                else:
                    testcase_failure_count += 1

        total_time = time.time() - start_time
        total_count = len(testcase_ids)
        testcase_success_rate = (testcase_success_count / total_count * 100) if total_count > 0 else 0

        # 构建统计响应
        stats = BatchApiStats(
            total=total_count,
            api_success_count=testcase_success_count,
            api_failure_count=testcase_failure_count,
            api_success_rate=round(testcase_success_rate, 2),
            total_time=round(total_time, 3),
            results=processed_results
        )

        # 记录执行统计日志
        logger.info(
            f"批量执行测试用例完成: "
            f"总计={stats.total}个, "
            f"成功={stats.api_success_count}个, "
            f"失败={stats.api_failure_count}个, "
            f"成功率={stats.api_success_rate}%, "
            f"耗时={stats.total_time}s"
        )

        return stats

    except Exception as e:
        logger.error(f"批量执行测试用例失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"批量执行测试用例失败: {str(e)}"
        )
