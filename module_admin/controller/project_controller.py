#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/3 17:24
# @Author  : 冉勇
# @Site    : 
# @File    : project_controller.py
# @Software: PyCharm
# @desc    : 项目接口
from datetime import datetime
from fastapi import APIRouter, Depends, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.project_vo import DeleteProjectModel, ProjectModel, ProjectPageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.project_service import ProjectService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

projectController = APIRouter(prefix='/auto/project', dependencies=[Depends(LoginService.get_current_user)])


@projectController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('auto:project:list'))]
)
async def get_project_list(
        request: Request,
        project_page_query: ProjectPageQueryModel = Depends(ProjectPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db)
):
    """
    获取项目列表
    """
    # 获取分页数据
    project_page_query_result = await ProjectService.get_project_list_services(
        query_db,
        project_page_query,
        is_page=True
    )
    logger.info('项目获取成功')

    return ResponseUtil.success(model_content=project_page_query_result)


@projectController.post('', dependencies=[Depends(CheckUserInterfaceAuth('auto:project:add'))])
@ValidateFields(validate_model='add_project')
@Log(title='项目管理', business_type=BusinessType.INSERT)
async def add_project(
        request: Request,
        add_project: ProjectModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    新增项目
    """
    add_project.create_by = current_user.user.user_name
    add_project.create_time = datetime.now()
    add_project.update_by = current_user.user.user_name
    add_project.update_time = datetime.now()
    add_project_result = await ProjectService.add_project_services(query_db, add_project)
    logger.info(add_project_result.message)

    return ResponseUtil.success(msg=add_project_result.message)


@projectController.put('', dependencies=[Depends(CheckUserInterfaceAuth('auto:project:edit'))])
@ValidateFields(validate_model='edit_project')
@Log(title='项目管理', business_type=BusinessType.UPDATE)
async def edit_project(
        request: Request,
        edit_project: ProjectModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    编辑项目
    """
    edit_project.update_by = current_user.user.user_name
    edit_project.update_time = datetime.now()
    edit_project_result = await ProjectService.edit_project_services(query_db, edit_project)
    logger.info(edit_project_result.message)

    return ResponseUtil.success(msg=edit_project_result.message)


@projectController.delete('/{project_ids}', dependencies=[Depends(CheckUserInterfaceAuth('auto:project:remove'))])
@Log(title='项目管理', business_type=BusinessType.DELETE)
async def delete_project(request: Request, project_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除项目
    """
    delete_project = DeleteProjectModel(projectIds=project_ids)
    delete_project_result = await ProjectService.delete_project_services(query_db, delete_project)
    logger.info(delete_project_result.message)

    return ResponseUtil.success(msg=delete_project_result.message)


@projectController.get(
    '/{project_id}', response_model=ProjectModel, dependencies=[Depends(CheckUserInterfaceAuth('auto:project:query'))]
)
async def query_detail_system_post(request: Request, project_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    根据ID获取项目信息
    """
    project_detail_result = await ProjectService.project_detail_services(query_db, project_id)
    logger.info(f'获取notice_id为{project_id}的信息成功')

    return ResponseUtil.success(data=project_detail_result)
