#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/26 22:12
# @Author  : 冉勇
# @Site    : 
# @File    : api_controller.py
# @Software: PyCharm
# @desc    : 接口配置相关接口
from datetime import datetime

from fastapi import Depends, APIRouter, Request, Query
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession

from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.api_vo import ApiPageQueryModel, DeleteApiModel, ApiModel
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
