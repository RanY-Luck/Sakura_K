#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/19 10:00
# @Author  : 冉勇
# @Site    : 
# @File    : plugin_controller.py
# @Software: PyCharm
# @desc    : 插件管理相关接口

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from module_admin.service.login_service import LoginService
from module_admin.service.plugin_service import PluginService
from utils.response_util import ResponseUtil
from utils.log_util import logger


class PluginDownloadRequest(BaseModel):
    repo_url: str


pluginController = APIRouter(prefix='/plugin', dependencies=[Depends(LoginService.get_current_user)])


@pluginController.post("/download")
async def download_plugin(request: PluginDownloadRequest):
    """
    下载并安装插件
    """
    try:
        download_result = await PluginService.download_plugin_service(request.repo_url)
        if download_result.is_success:
            logger.info('插件下载安装成功')
            return ResponseUtil.success(msg=download_result.message)
        else:
            logger.warning(f'插件下载安装失败: {download_result.message}')
            return ResponseUtil.failure(msg=download_result.message)
    except Exception as e:
        logger.exception(e)
        return ResponseUtil.error(msg=str(e)) 