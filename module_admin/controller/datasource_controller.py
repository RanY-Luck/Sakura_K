#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/17 16:44
# @Author  : 冉勇
# @Site    : 
# @File    : datasource_controller.py
# @Software: PyCharm
# @desc    : 数据源接口
from datetime import datetime
from fastapi import APIRouter, Depends, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.datasource_vo import DeleteDataSourceModel, DataSourceModel, DataSourcePageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.datasource_service import DataSourceService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

dataSourceController = APIRouter(
    prefix='/commonConfig/dataSource',
    dependencies=[Depends(LoginService.get_current_user)]
)


@dataSourceController.get(
    '/list',
    response_model=PageResponseModel,
    dependencies=[Depends(CheckUserInterfaceAuth('commonConfig:dataSource:list'))]
)
async def get_dataSource_list(
        request: Request,
        datasource_page_query: DataSourcePageQueryModel = Depends(DataSourcePageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db)
):
    """
    获取数据源列表
    """
    # 获取分页数据
    datasource_page_query_result = await DataSourceService.get_datasource_list_services(
        query_db,
        datasource_page_query,
        is_page=True
    )
    logger.info('数据源获取成功')

    return ResponseUtil.success(model_content=datasource_page_query_result)


@dataSourceController.post('', dependencies=[Depends(CheckUserInterfaceAuth('commonConfig:dataSource:add'))])
@ValidateFields(validate_model='add_datasource')
@Log(title='数据源', business_type=BusinessType.INSERT)
async def add_datasource(
        request: Request,
        add_datasource: DataSourceModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    新增数据源
    """
    add_datasource.create_by = current_user.user.user_name
    add_datasource.create_time = datetime.now()
    add_datasource.update_by = current_user.user.user_name
    add_datasource.update_time = datetime.now()
    add_datasource_result = await DataSourceService.add_datasource_services(query_db, add_datasource)
    logger.info(add_datasource_result.message)

    return ResponseUtil.success(msg=add_datasource_result.message)


@dataSourceController.put('', dependencies=[Depends(CheckUserInterfaceAuth('commonConfig:dataSource:edit'))])
@ValidateFields(validate_model='edit_datasource')
@Log(title='数据源', business_type=BusinessType.UPDATE)
async def edit_datasource(
        request: Request,
        edit_datasource: DataSourceModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    编辑数据源
    """
    edit_datasource.update_by = current_user.user.user_name
    edit_datasource.update_time = datetime.now()
    edit_datasource_result = await DataSourceService.edit_datasource_services(query_db, edit_datasource)
    logger.info(edit_datasource_result.message)

    return ResponseUtil.success(msg=edit_datasource_result.message)


@dataSourceController.delete(
    '/{datasource_ids}',
    dependencies=[Depends(CheckUserInterfaceAuth('commonConfig:dataSource:remove'))]
)
@Log(title='数据源', business_type=BusinessType.DELETE)
async def delete_datasource(request: Request, datasource_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除数据源
    """
    delete_datasource = DeleteDataSourceModel(datasourceIds=datasource_ids)
    delete_datasource_result = await DataSourceService.delete_datasource_services(query_db, delete_datasource)
    logger.info(delete_datasource_result.message)

    return ResponseUtil.success(msg=delete_datasource_result.message)


@dataSourceController.get(
    '/{datasource_id}',
    response_model=DataSourceModel,
    dependencies=[Depends(CheckUserInterfaceAuth('commonConfig:dataSource:query'))]
)
async def query_detail_datasource(request: Request, datasource_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    根据ID获取数据源
    """
    datasource_detail_result = await DataSourceService.datasource_detail_services(query_db, datasource_id)
    logger.info(f'获取datasource_id为{datasource_id}的信息成功')

    return ResponseUtil.success(data=datasource_detail_result)
