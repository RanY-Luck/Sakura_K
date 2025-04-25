#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/26 22:12
# @Author  : 冉勇
# @Site    : 
# @File    : api_controller.py
# @Software: PyCharm
# @desc    : 接口配置相关接口
import time
import asyncio
from typing import List
from datetime import datetime
from fastapi import Depends, APIRouter, Request, Query, HTTPException
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.api_vo import ApiPageQueryModel, DeleteApiModel, ApiModel, BatchApi, BatchApiStats
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.api_service import ApiService
from module_admin.service.login_service import LoginService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

apiController = APIRouter(prefix='/apitest/apiInfo', dependencies=[Depends(LoginService.get_current_user)])


@apiController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('apitest:apiInfo:list'))]
)
async def get_api_list(
        request: Request,
        api_page_query: ApiPageQueryModel = Depends(ApiPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db)
):
    """
    获取接口列表
    """
    # 获取分页数据
    api_page_query_result = await ApiService.get_api_list_services(
        query_db,
        api_page_query,
        is_page=True
    )
    logger.info('接口获取成功')

    return ResponseUtil.success(model_content=api_page_query_result)


@apiController.post('', dependencies=[Depends(CheckUserInterfaceAuth('apitest:apiInfo:add'))])
@ValidateFields(validate_model='add_api')
@Log(title='接口', business_type=BusinessType.INSERT)
async def add_api(
        request: Request,
        add_api: ApiModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    新增接口
    """
    add_api.create_by = current_user.user.user_name
    add_api.create_time = datetime.now()
    add_api.update_by = current_user.user.user_name
    add_api.update_time = datetime.now()
    add_api_result = await ApiService.add_api_services(query_db, add_api)
    logger.info(add_api_result.message)

    return ResponseUtil.success(msg=add_api_result.message)


@apiController.put('', dependencies=[Depends(CheckUserInterfaceAuth('apitest:apiInfo:edit'))])
@ValidateFields(validate_model='edit_api')
@Log(title='接口', business_type=BusinessType.UPDATE)
async def edit_api(
        request: Request,
        edit_api: ApiModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    编辑接口
    """
    edit_api.update_by = current_user.user.user_name
    edit_api.update_time = datetime.now()
    edit_api_result = await ApiService.edit_api_services(query_db, edit_api)
    logger.info(edit_api_result.message)

    return ResponseUtil.success(msg=edit_api_result.message)


@apiController.delete('/{api_ids}', dependencies=[Depends(CheckUserInterfaceAuth('apitest:apiInfo:remove'))])
@Log(title='接口', business_type=BusinessType.DELETE)
async def delete_api(request: Request, api_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除接口
    """
    delete_api = DeleteApiModel(apiIds=api_ids)
    delete_api_result = await ApiService.delete_api_services(query_db, delete_api)
    logger.info(delete_api_result.message)

    return ResponseUtil.success(msg=delete_api_result.message)


@apiController.get(
    '/{api_id}', response_model=ApiModel, dependencies=[Depends(CheckUserInterfaceAuth('apitest:apiInfo:query'))]
)
async def query_detail_api(request: Request, api_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    根据ID获取接口信息
    """
    api_detail_result = await ApiService.api_detail_services(query_db, api_id)
    logger.info(f'获取api_id为{api_id}的信息成功')

    return ResponseUtil.success(data=api_detail_result)


@apiController.post(
    '/debugApi',
    response_model=ApiModel,
    dependencies=[Depends(CheckUserInterfaceAuth('apitest:apiInfo:debug'))]
)
async def api_test_client(
        request: Request,
        api_id: int = Query(..., description='接口ID'),
        env_id: int = Query(..., description='环境ID'),
        query_db: AsyncSession = Depends(get_db)
):
    """
    调试接口
    """
    api_debug_result = await ApiService.api_debug_services(query_db, api_id, env_id)
    return ResponseUtil.success(data=api_debug_result)


@apiController.post(
    '/batchApi',
    response_model=BatchApiStats,  # 注意返回类型应为列表
    dependencies=[Depends(CheckUserInterfaceAuth('apitest:apiInfo:batchapi'))]
)
async def api_batch_run(
        request: Request,
        api_id_list: List[int],
        env_id: int = Query(..., description='环境ID'),
        query_db: AsyncSession = Depends(get_db)
):
    """
    批量运行接口，返回执行统计信息
    """
    start_time = time.time()

    # 使用异步并发执行
    async def run_single_api(api_id: int):
        api_start = time.time()
        try:
            result = await ApiService.api_batch_services(query_db, [api_id], env_id)
            # 提取API响应中的status
            api_status = result[0].get('response', {}).get('status', False)
            if isinstance(api_status, str):
                api_status = api_status.lower() == 'true'

            return BatchApi(
                id=api_id,
                status='success',
                response=result[0],
                execution_time=time.time() - api_start,
                api_status=api_status  # 添加API响应状态
            )
        except asyncio.TimeoutError:
            execution_time = time.time() - api_start
            logger.error(f"API {api_id} execution timed out")
            return BatchApi(
                id=api_id,
                status='failed',
                error_message="Execution timed out",
                execution_time=execution_time,
                api_status=False
            )
        except Exception as e:
            execution_time = time.time() - api_start
            logger.error(f"API编号为: {api_id} 执行失败: {str(e)}")
            return BatchApi(
                id=api_id,
                status='failed',
                error_message=str(e),
                execution_time=execution_time,
                api_status=False
            )

    try:
        # 使用asyncio.gather进行并发处理
        results = await asyncio.gather(
            *[run_single_api(api_id) for api_id in api_id_list],
            return_exceptions=True
        )
        # 处理结果和统计
        processed_results = []
        api_success_count = 0  # API实际成功计数
        api_failure_count = 0  # API实际失败计数

        for result in results:
            if isinstance(result, Exception):
                api_failure_count += 1
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
                    # 根据API响应状态统计
                    if result.api_status:
                        api_success_count += 1
                    else:
                        api_failure_count += 1
                else:
                    api_failure_count += 1

        total_time = time.time() - start_time
        total_count = len(api_id_list)
        api_success_rate = (api_success_count / total_count * 100) if total_count > 0 else 0

        # 构建统计响应
        stats = BatchApiStats(
            total=total_count,
            api_success_count=api_success_count,
            api_failure_count=api_failure_count,
            api_success_rate=round(api_success_rate, 2),
            total_time=round(total_time, 3),
            results=processed_results
        )

        # 记录执行统计日志
        logger.info(
            f"批量执行API完成: "
            f"总计={stats.total}个, "
            f"成功={stats.api_success_count}个, "
            f"失败={stats.api_failure_count}个, "
            f"成功率={stats.api_success_rate}%, "
            f"耗时={stats.total_time}s"
        )

        return stats

    except Exception as e:
        logger.error(f"Batch execution failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch execution failed: {str(e)}"
        )
