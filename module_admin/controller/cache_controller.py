#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/17 17:23
# @Author  : 冉勇
# @Site    : 
# @File    : cache_controller.py
# @Software: PyCharm
# @desc    : 缓存监控相关接口
from fastapi import APIRouter, Depends, Request
from typing import List
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.cache_vo import CacheInfoModel, CacheMonitorModel
from module_admin.service.cache_service import CacheService
from module_admin.service.login_service import LoginService
from utils.log_util import logger
from utils.response_util import ResponseUtil

cacheController = APIRouter(prefix='/monitor/cache', dependencies=[Depends(LoginService.get_current_user)])


@cacheController.get(
    '', response_model=CacheMonitorModel, dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))]
)
async def get_monitor_cache_info(request: Request):
    """
    获取缓存信息
    """
    cache_info_query_result = await CacheService.get_cache_monitor_statistical_info_services(request)
    logger.info('缓存信息获取成功')

    return ResponseUtil.success(data=cache_info_query_result)


@cacheController.get(
    '/getNames',
    response_model=List[CacheInfoModel],
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))],
)
async def get_monitor_cache_name(request: Request):
    """
    获取缓存名称
    """
    cache_name_list_result = await CacheService.get_cache_monitor_cache_name_services()
    logger.info('缓存名称获取成功')

    return ResponseUtil.success(data=cache_name_list_result)


@cacheController.get(
    '/getKeys/{cache_name}',
    response_model=List[str],
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))],
)
async def get_monitor_cache_key(request: Request, cache_name: str):
    """
    根据缓存名称获取信息
    """
    cache_key_list_result = await CacheService.get_cache_monitor_cache_key_services(request, cache_name)
    logger.info(f'缓存名称:{cache_name} 获取成功')

    return ResponseUtil.success(data=cache_key_list_result)


@cacheController.get(
    '/getValue/{cache_name}/{cache_key}',
    response_model=CacheInfoModel,
    dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))],
)
async def get_monitor_cache_value(request: Request, cache_name: str, cache_key: str):
    """
     获取缓存密钥
     """
    cache_value_list_result = await CacheService.get_cache_monitor_cache_value_services(request, cache_name, cache_key)
    logger.info('缓存密钥获取成功')

    return ResponseUtil.success(data=cache_value_list_result)


@cacheController.delete(
    '/clearCacheName/{cache_name}', dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))]
)
async def clear_monitor_cache_name(request: Request, cache_name: str):
    """
    删除缓存
    """
    clear_cache_name_result = await CacheService.clear_cache_monitor_cache_name_services(request, cache_name)
    logger.info(clear_cache_name_result.message)

    return ResponseUtil.success(msg=clear_cache_name_result.message)


@cacheController.delete(
    '/clearCacheKey/{cache_key}', dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))]
)
async def clear_monitor_cache_key(request: Request, cache_key: str):
    """
    删除缓存密钥
    """
    clear_cache_key_result = await CacheService.clear_cache_monitor_cache_key_services(request, cache_key)
    logger.info(clear_cache_key_result.message)

    return ResponseUtil.success(msg=clear_cache_key_result.message)


@cacheController.delete('/clearCacheAll', dependencies=[Depends(CheckUserInterfaceAuth('monitor:cache:list'))])
async def clear_monitor_cache_all(request: Request):
    """
    清除所有缓存
    """
    clear_cache_all_result = await CacheService.clear_cache_monitor_all_services(request)
    logger.info(clear_cache_all_result.message)

    return ResponseUtil.success(msg=clear_cache_all_result.message)
