#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/15 10:24
# @Author  : 冉勇
# @Site    : 
# @File    : notice_controller.py
# @Software: PyCharm
# @desc    : 通知公告接口
from fastapi import APIRouter, Request, Depends
from pydantic_validation_decorator import ValidateFields
from datetime import datetime
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.service.login_service import LoginService, CurrentUserModel
from module_admin.service.notice_service import *
from utils.response_util import *
from utils.log_util import *
from utils.page_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth

noticeController = APIRouter(prefix='/system/notice', dependencies=[Depends(LoginService.get_current_user)])


@noticeController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:list'))]
)
async def get_system_notice_list(
        request: Request,
        notice_page_query: NoticePageQueryModel = Depends(NoticePageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    """
    获取系统通知公告列表
    """
    # 获取分页数据
    notice_page_query_result = await NoticeService.get_notice_list_services(query_db, notice_page_query, is_page=True)
    logger.info('系统通知公告获取成功')

    return ResponseUtil.success(model_content=notice_page_query_result)


@noticeController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:notice:add'))])
@ValidateFields(validate_model='add_notice')
@Log(title='通知公告', business_type=BusinessType.INSERT)
async def add_system_notice(
        request: Request,
        add_notice: NoticeModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    新增系统通知公告
    """
    add_notice.create_by = current_user.user.user_name
    add_notice.create_time = datetime.datetime.now()
    add_notice.update_by = current_user.user.user_name
    add_notice.update_time = datetime.datetime.now()
    add_notice_result = await NoticeService.add_notice_services(query_db, add_notice)
    logger.info(add_notice_result.message)

    return ResponseUtil.success(msg=add_notice_result.message)


@noticeController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:notice:edit'))])
@ValidateFields(validate_model='edit_notice')
@Log(title='通知公告', business_type=BusinessType.UPDATE)
async def edit_system_notice(
        request: Request,
        edit_notice: NoticeModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    编辑系统通知公告
    """
    edit_notice.update_by = current_user.user.user_name
    edit_notice.update_time = datetime.datetime.now()
    edit_notice_result = await NoticeService.edit_notice_services(query_db, edit_notice)
    logger.info(edit_notice_result.message)

    return ResponseUtil.success(msg=edit_notice_result.message)


@noticeController.delete('/{notice_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:notice:remove'))])
@Log(title='通知公告', business_type=BusinessType.DELETE)
async def delete_system_notice(request: Request, notice_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除系统通知公告
    """
    delete_notice = DeleteNoticeModel(noticeIds=notice_ids)
    delete_notice_result = await NoticeService.delete_notice_services(query_db, delete_notice)
    logger.info(delete_notice_result.message)

    return ResponseUtil.success(msg=delete_notice_result.message)


@noticeController.get(
    '/{notice_id}', response_model=NoticeModel, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:query'))]
)
async def query_detail_system_post(request: Request, notice_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    获取系统通知公告信息
    """
    notice_detail_result = await NoticeService.notice_detail_services(query_db, notice_id)
    logger.info(f'获取notice_id为{notice_id}的信息成功')

    return ResponseUtil.success(data=notice_detail_result)
