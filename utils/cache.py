#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 19:45
# @Author  : 冉勇
# @Site    : 
# @File    : cache.py
# @Software: PyCharm
# @desc    : 缓存
import json
from typing import List
from core import logger
from core.database import db_getter
from apps.vadmin.system.crud import SettingsTabDal
from aioredis.client import Redis
from core.exception import CustomException
from utils import status

"""
代码解释：
定义了一个名为Cache的类，实现了两个方法：cache_tab_names和get_tab_name。
Cache类的构造函数接收一个Redis对象rd作为参数，用于连接Redis数据库。
方法cache_tab_names用于缓存系统配置信息。它接受参数tab_names，用于指定要缓存的配置项名称。
如果参数tab_names没有提供，则会缓存DEFAULT_TABLE_NAMES属性中指定的默认配置项。
在方法内部，它首先通过调用db_getter函数获取数据库访问Session对象，然后使用SettingsTabDal类从数据库中获取指定的配置项数据。
然后它遍历获取到的配置项数据，使用Redis的set方法将其写入缓存中，其中键为配置项名称，值为对应的配置项数据的JSON序列化表示。

方法get_tab_name用于检索系统配置信息。它接受一个参数tab_name，用于指定要检索的配置项名称。
它还包括一个可选参数retry，表示在从Redis中获取配置数据失败时的重试次数。方法的实现如下：
- 首先，它尝试从Redis中获取指定的配置数据。
- 如果成功获取到数据，则返回其JSON解析表示。
- 如果未能获取到数据，并且还有剩余的重试次数，则它将重新更新配置数据（通过调用cache_tab_names方法），并递归调用自身，减少重试次数。
- 如果无法在重试次数用尽时获得数据，则它引发CustomException异常。
"""


class Cache:
    DEFAULT_TAB_NAMES = ["wx_server", "aliyun_sms", "aliyun_oss"]

    def __init__(self, rd: Redis):
        self.rd = rd

    async def cache_tab_names(self, tab_names: List[str] = None):
        """
        缓存系统配置
        :param tab_names:
        :return:
        """
        async_session = db_getter()
        session = await async_session.__anext__()
        if tab_names:
            datas = await SettingsTabDal(session).get_tab_name_values(tab_names, hidden=None)
        else:
            datas = await SettingsTabDal(session).get_tab_name_values(self.DEFAULT_TAB_NAMES, hidden=None)
        for k, v in datas.items():
            await self.rd.client().set(k, json.dumps(v))

    async def get_tab_name(self, tab_name: str, retry: int = 3):
        """
        获取系统配置
        :param tab_name: 配置标签名称
        :param retry: 重试次数
        :return:
        """
        result = await self.rd.get(tab_name)
        if not result and retry > 0:
            logger.error(f"未从Redis中获取到{tab_name}配置信息，正在重新更新配置信息，重试次数：{retry}。")
            await self.cache_tab_names([tab_name])
            return await self.get_tab_name(tab_name, retry - 1)
        elif not result and retry == 0:
            raise CustomException(f"获取{tab_name}配置信息失败，请联系管理员！", code=status.HTTP_ERROR)
        else:
            return json.loads(result)
