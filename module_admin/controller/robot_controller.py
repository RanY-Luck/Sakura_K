#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Create Time    : 2024/09/15 12:42
# @Author         : 
# @File           : robot_controller.py
# @Software       : PyCharm
# @desc           : 机器人配置相关接口
from module_admin.service.robot_service import RobotService
from module_admin.entity.vo.robot_vo import RobotPageQueryModel, DeleteRobotModel, RobotModel
from utils.response_util import ResponseUtil
from module_admin.annotation.log_annotation import Log
from utils.page_util import PageResponseModel
from module_admin.service.login_service import LoginService
from fastapi import Depends, APIRouter, Request
from config.enums import BusinessType
from utils.log_util import logger
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from pydantic_validation_decorator import ValidateFields
from datetime import datetime
from module_admin.entity.vo.user_vo import CurrentUserModel
from config.get_db import get_db
from sqlalchemy.ext.asyncio import AsyncSession

robotController = APIRouter(prefix='/notify/robots', dependencies=[Depends(LoginService.get_current_user)])


@robotController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('notify:robots:list'))]
)
async def get_robot_list(
        request: Request,
        robot_page_query: RobotPageQueryModel = Depends(RobotPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db)
):
    """
    获取机器人列表
    """
    # 获取分页数据
    robot_page_query_result = await RobotService.get_robot_list_services(
        query_db,
        robot_page_query,
        is_page=True
    )
    logger.info('机器人获取成功')

    return ResponseUtil.success(model_content=robot_page_query_result)


@robotController.post('', dependencies=[Depends(CheckUserInterfaceAuth('notify:robots:add'))])
@ValidateFields(validate_model='add_robot')
@Log(title='机器人', business_type=BusinessType.INSERT)
async def add_robot(
        request: Request,
        add_robot: RobotModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    新增机器人
    """
    add_robot.create_by = current_user.user.user_name
    add_robot.create_time = datetime.now()
    add_robot.update_by = current_user.user.user_name
    add_robot.update_time = datetime.now()
    add_robot_result = await RobotService.add_robot_services(query_db, add_robot)
    logger.info(add_robot_result.message)

    return ResponseUtil.success(msg=add_robot_result.message)


@robotController.put('', dependencies=[Depends(CheckUserInterfaceAuth('notify:robots:edit'))])
@ValidateFields(validate_model='edit_robot')
@Log(title='机器人', business_type=BusinessType.UPDATE)
async def edit_robot(
        request: Request,
        edit_robot: RobotModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    编辑机器人
    """
    edit_robot.update_by = current_user.user.user_name
    edit_robot.update_time = datetime.now()
    edit_robot_result = await RobotService.edit_robot_services(query_db, edit_robot)
    logger.info(edit_robot_result.message)

    return ResponseUtil.success(msg=edit_robot_result.message)


@robotController.delete('/{robot_ids}', dependencies=[Depends(CheckUserInterfaceAuth('notify:robots:remove'))])
@Log(title='机器人', business_type=BusinessType.DELETE)
async def delete_robot(request: Request, robot_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除项目
    """
    delete_robot = DeleteRobotModel(robotIds=robot_ids)
    delete_robot_result = await RobotService.delete_robot_services(query_db, delete_robot)
    logger.info(delete_robot_result.message)

    return ResponseUtil.success(msg=delete_robot_result.message)


@robotController.get(
    '/{robot_id}', response_model=RobotModel, dependencies=[Depends(CheckUserInterfaceAuth('notify:robots:query'))]
)
async def query_detail_robot(request: Request, robot_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    根据ID获取机器人信息
    """
    robot_detail_result = await RobotService.robot_detail_services(query_db, robot_id)
    logger.info(f'获取robot_id为{robot_id}的信息成功')

    return ResponseUtil.success(data=robot_detail_result)
