'''
Descripttion: 
version: 
Author: 冉勇
Date: 2025-05-13 14:03:06
LastEditTime: 2025-05-13 14:24:42
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/13 14:00
# @Author  : 冉勇
# @Site    : 
# @File    : plugin_service.py
# @Software: PyCharm
# @desc    : 插件管理服务层
import asyncio
from concurrent.futures import ThreadPoolExecutor
from plugin.tools import download_github_repo
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.log_util import logger


class PluginService:
    """
    插件管理服务层
    """

    @classmethod
    async def download_plugin_service(cls, repo_url: str):
        """
        下载插件服务
        :param repo_url: GitHub仓库地址，例如：https://github.com/ranyong1997/Sakura_K_plugin
        :return: 下载结果
        """
        try:
            # 在线程池中运行下载函数，避免阻塞事件循环，同时保留进度条显示
            loop = asyncio.get_event_loop()
            with ThreadPoolExecutor() as pool:
                download_success = await loop.run_in_executor(
                    pool, download_github_repo, repo_url
                )
            
            if download_success:
                result = dict(
                    is_success=True,
                    message='插件下载成功并已安装',
                    result=None
                )
            else:
                result = dict(
                    is_success=False,
                    message='插件下载或安装失败',
                    result=None
                )
            
            return CrudResponseModel(**result)
        except Exception as e:
            logger.exception(f"插件下载异常: {str(e)}")
            return CrudResponseModel(
                is_success=False,
                message=f"插件下载异常: {str(e)}",
                result=None
            ) 