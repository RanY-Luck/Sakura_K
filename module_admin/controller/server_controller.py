#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 17:02
# @Author  : 冉勇
# @Site    : 
# @File    : server_controller.py
# @Software: PyCharm
# @desc    : 服务监控相关接口
from fastapi import APIRouter, Request
from fastapi import Depends
from module_admin.service.login_service import LoginService
from module_admin.service.server_service import *
from utils.response_util import *
from utils.log_util import *
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth

serverController = APIRouter(prefix='/monitor/server', dependencies=[Depends(LoginService.get_current_user)])


@serverController.get(
    "",
    response_model=ServerMonitorModel,
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:server:list'))]
)
async def get_monitor_server_info(request: Request):
    """
    获取服务监控信息
    """
    try:
        # 获取全量数据
        server_info_query_result = await ServerService.get_server_monitor_info()
        logger.info('服务监控信息获取成功')
        return ResponseUtil.success(data=server_info_query_result)
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=str(e))
