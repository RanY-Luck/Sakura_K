#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/10/28 18:07
# @Author   : 冉勇
# @File     : env_controller.py
# @Software : PyCharm
# @Desc     : 环境配置相关接口
from datetime import datetime
from fastapi import Depends, APIRouter, Request, Form
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.env_vo import EnvPageQueryModel, EnvModel, DeleteEnvModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.env_service import EnvService
from module_admin.service.login_service import LoginService
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

envController = APIRouter(prefix='/env/envInfo', dependencies=[Depends(LoginService.get_current_user)])


@envController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('env:envInfo:list'))]
)
async def get_env_list(
        request: Request,
        env_page_query: EnvPageQueryModel = Depends(EnvPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db)
):
    """
    获取环境列表
    """
    # 获取分页数据
    env_page_query_result = await EnvService.get_env_list_services(
        query_db,
        env_page_query,
        is_page=True
    )
    logger.info('环境获取成功')

    return ResponseUtil.success(model_content=env_page_query_result)


@envController.post('', dependencies=[Depends(CheckUserInterfaceAuth('env:envInfo:add'))])
@ValidateFields(validate_model='add_env')
@Log(title='环境', business_type=BusinessType.INSERT)
async def add_env(
        request: Request,
        add_env: EnvModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    新增环境
    """
    add_env.create_by = current_user.user.user_name
    add_env.create_time = datetime.now()
    add_env.update_by = current_user.user.user_name
    add_env.update_time = datetime.now()
    add_env_result = await EnvService.add_env_services(query_db, add_env)
    logger.info(add_env_result.message)

    return ResponseUtil.success(msg=add_env_result.message)


@envController.put('', dependencies=[Depends(CheckUserInterfaceAuth('env:envInfo:edit'))])
@ValidateFields(validate_model='edit_api')
@Log(title='环境', business_type=BusinessType.UPDATE)
async def edit_env(
        request: Request,
        edit_env: EnvModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    编辑环境
    """
    edit_env.update_by = current_user.user.user_name
    edit_env.update_time = datetime.now()
    edit_env_result = await EnvService.edit_env_services(query_db, edit_env)
    logger.info(edit_env_result.message)

    return ResponseUtil.success(msg=edit_env_result.message)


@envController.delete('/{env_ids}', dependencies=[Depends(CheckUserInterfaceAuth('env:envInfo:remove'))])
@Log(title='环境', business_type=BusinessType.DELETE)
async def delete_env(request: Request, env_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除环境
    """
    delete_env = DeleteEnvModel(envIds=env_ids)
    delete_api_result = await EnvService.delete_env_services(query_db, delete_env)
    logger.info(delete_api_result.message)

    return ResponseUtil.success(msg=delete_api_result.message)


@envController.get(
    '/{env_id}', response_model=EnvModel, dependencies=[Depends(CheckUserInterfaceAuth('env:envInfo:query'))]
)
async def query_detail_env(request: Request, env_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    根据ID获取环境信息
    """
    env_detail_result = await EnvService.env_detail_services(query_db, env_id)
    logger.info(f'获取env_id为{env_id}的信息成功')

    return ResponseUtil.success(data=env_detail_result)


@envController.post('/copy/{env_id}', dependencies=[Depends(CheckUserInterfaceAuth('env:envInfo:copy'))])
@Log(title='服务器', business_type=BusinessType.INSERT)
async def copy_env(
        request: Request,
        env_id: int,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    复制环境
    """
    # 获取原环境的信息
    original_env = await EnvService.env_detail_services(query_db, env_id)
    if not original_env:
        return ResponseUtil.error(msg="要复制的环境不存在")
    # 创建新项目对象，基于原项目的所有字段
    new_env = original_env.copy(
        update={
            "env_name": f"{original_env.env_name}_copy",
            "create_by": current_user.user.user_name,
            "create_time": datetime.now(),
            "update_by": current_user.user.user_name,
            "update_time": datetime.now()
        }
    )

    # 保存原环境ID，用于在service中查找原环境
    new_env.env_id = env_id
    # 复制环境
    copy_env_result = await EnvService.copy_env_services(query_db, new_env)
    logger.info(copy_env_result.message)

    if copy_env_result.is_success:
        return ResponseUtil.success(msg=copy_env_result.message)
    else:
        return ResponseUtil.error(msg=copy_env_result.message)


@envController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('env:envInfo:export'))])
@Log(title='服务器', business_type=BusinessType.EXPORT)
async def export_ssh_list(
        request: Request,
        ssh_page_query: EnvPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    """
    导出服务器信息
    """
    # 获取全量数据
    env_query_result = await EnvService.get_env_list_services(query_db, ssh_page_query, is_page=False)
    env_export_result = await EnvService.export_env_list_services(env_query_result)
    logger.info('环境导出成功')
    return ResponseUtil.streaming(data=bytes2file_response(env_export_result))
