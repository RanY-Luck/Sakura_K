#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/2 19:23
# @Author   : 冉勇
# @File     : servermanage_controller.py
# @Software : PyCharm
# @Desc     : 环境配置相关接口
from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.servermanage_service import SshService
from module_admin.entity.vo.servermanage_vo import DeleteSshModel, SshModel, SshPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

serverManageController = APIRouter(prefix='/ssh/sshInfo', dependencies=[Depends(LoginService.get_current_user)])


@serverManageController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('ssh:sshInfo:list'))]
)
async def get_ssh_list(
        request: Request,
        ssh_page_query: SshPageQueryModel = Depends(SshPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    """
    获取服务器列表
    :param request:
    :param ssh_page_query:
    :param query_db:
    :return:
    """
    # 获取分页数据
    ssh_page_query_result = await SshService.get_ssh_list_services(
        query_db,
        ssh_page_query,
        is_page=True
    )
    logger.info('服务器获取成功')

    return ResponseUtil.success(model_content=ssh_page_query_result)


@serverManageController.post('', dependencies=[Depends(CheckUserInterfaceAuth('ssh:sshInfo:add'))])
@ValidateFields(validate_model='add_ssh')
@Log(title='服务器', business_type=BusinessType.INSERT)
async def add_ssh(
        request: Request,
        add_ssh: SshModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    新增服务器
    :param request:
    :param add_ssh:
    :param query_db:
    :param current_user:
    :return:·
    """
    add_ssh.create_by = current_user.user.user_name
    add_ssh.create_time = datetime.now()
    add_ssh.update_by = current_user.user.user_name
    add_ssh.update_time = datetime.now()
    add_ssh_result = await SshService.add_ssh_services(query_db, add_ssh)
    logger.info(add_ssh_result.message)

    return ResponseUtil.success(msg=add_ssh_result.message)


@serverManageController.put('', dependencies=[Depends(CheckUserInterfaceAuth('ssh:sshInfo:edit'))])
@ValidateFields(validate_model='edit_ssh')
@Log(title='服务器', business_type=BusinessType.UPDATE)
async def edit_ssh(
        request: Request,
        edit_ssh: SshModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    编辑服务器
    :param request:
    :param edit_ssh:
    :param query_db:
    :param current_user:
    :return:
    """
    edit_ssh.update_by = current_user.user.user_name
    edit_ssh.update_time = datetime.now()
    edit_ssh_result = await SshService.edit_ssh_services(query_db, edit_ssh)
    logger.info(edit_ssh_result.message)

    return ResponseUtil.success(msg=edit_ssh_result.message)


@serverManageController.delete('/{ssh_ids}', dependencies=[Depends(CheckUserInterfaceAuth('ssh:sshInfo:remove'))])
@Log(title='服务器', business_type=BusinessType.DELETE)
async def delete_ssh(request: Request, ssh_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除服务器
    :param request:
    :param ssh_ids:
    :param query_db:
    :return:
    """
    delete_ssh = DeleteSshModel(sshIds=ssh_ids)
    delete_ssh_result = await SshService.delete_ssh_services(query_db, delete_ssh)
    logger.info(delete_ssh_result.message)

    return ResponseUtil.success(msg=delete_ssh_result.message)


@serverManageController.get(
    '/{ssh_id}', response_model=SshModel, dependencies=[Depends(CheckUserInterfaceAuth('ssh:sshInfo:query'))]
)
async def query_detail_ssh(request: Request, ssh_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    根据ID获取服务器信息
    :param request:
    :param ssh_id:
    :param query_db:
    :return:
    """
    ssh_detail_result = await SshService.ssh_detail_services(query_db, ssh_id)
    logger.info(f'获取ssh_id为{ssh_id}的信息成功')

    return ResponseUtil.success(data=ssh_detail_result)


@serverManageController.post('/copy/{ssh_id}', dependencies=[Depends(CheckUserInterfaceAuth('ssh:sshInfo:copy'))])
@Log(title='服务器', business_type=BusinessType.INSERT)
async def copy_ssh(
        request: Request,
        ssh_id: int,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    复制服务器
    """
    # 获取原项目的信息
    original_ssh = await SshService.ssh_detail_services(query_db, ssh_id)
    if not original_ssh:
        return ResponseUtil.error(msg="要复制的服务器不存在")
    # 创建新项目对象，基于原项目的所有字段
    new_ssh = original_ssh.copy(
        update={
            "ssh_name": f"{original_ssh.ssh_name}_copy",
            "create_by": current_user.user.user_name,
            "create_time": datetime.now(),
            "update_by": current_user.user.user_name,
            "update_time": datetime.now()
        }
    )

    # 保存原服务器ID，用于在service中查找原项目
    new_ssh.ssh_id = ssh_id

    # 复制服务器
    copy_ssh_result = await SshService.copy_ssh_services(query_db, new_ssh)
    logger.info(copy_ssh_result.message)

    if copy_ssh_result.is_success:
        return ResponseUtil.success(msg=copy_ssh_result.message)
    else:
        return ResponseUtil.error(msg=copy_ssh_result.message)


@serverManageController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('ssh:sshInfo:export'))])
@Log(title='服务器', business_type=BusinessType.EXPORT)
async def export_ssh_list(
        request: Request,
        ssh_page_query: SshPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    """
    导出服务器信息
    :param request:
    :param ssh_page_query:
    :param query_db:
    :return:
    """
    # 获取全量数据
    ssh_query_result = await SshService.get_ssh_list_services(query_db, ssh_page_query, is_page=False)
    ssh_export_result = await SshService.export_ssh_list_services(ssh_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(ssh_export_result))


@serverManageController.get(
    '/test/{ssh_id}', dependencies=[Depends(CheckUserInterfaceAuth('ssh:sshInfo:query'))]
)
async def test_ssh_connection(request: Request, ssh_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    测试SSH连接并获取服务器信息
    :param request: 请求对象
    :param ssh_id: 服务器ID
    :param query_db: 数据库会话
    :return: 连接测试结果和服务器信息
    """
    test_result = await SshService.ssh_client_services(query_db, ssh_id)
    if test_result.is_success:
        logger.info(f'服务器{ssh_id}连接测试成功')
    else:
        logger.error(f'服务器{ssh_id}连接测试失败: {test_result.message}')
    
    return ResponseUtil.success(data=test_result)
