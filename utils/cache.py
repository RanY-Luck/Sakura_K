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

from redis.asyncio.client import Redis
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload

from apps.vadmin.system.models import VadminSystemSettingsTab
from core.database import db_getter
from core.exception import CustomException
from core.logger import logger  # 注意：报错就在这里，如果只写 core.logger 会写入日志报错，很难排查
from utils import status


class Cache:
    DEFAULT_TAB_NAMES = ["wx_server", "aliyun_sms", "aliyun_oss", "web_email"]

    def __init__(self, rd: Redis):
        self.rd = rd

    async def __get_tab_name_values(self, tab_names: List[str]):
        """
        获取系统配置标签下的标签信息
        """
        async_session = db_getter()
        session = await async_session.__anext__()
        model = VadminSystemSettingsTab
        v_options = [joinedload(model.settings)]
        sql = select(model).where(
            model.is_delete == False,
            model.tab_name.in_(tab_names),
            model.disabled == False
        ).options(*[load for load in v_options])
        queryset = await session.execute(sql)
        datas = queryset.scalars().unique().all()
        return self.__generate_values(datas)

    @classmethod
    def __generate_values(cls, datas: List[VadminSystemSettingsTab]):
        """
        生成字典值
        """
        return {
            tab.tab_name: {
                item.config_key: item.config_value
                for item in tab.settings
                if not item.disabled
            }
            for tab in datas
        }

    async def cache_tab_names(self, tab_names: List[str] = None):
        """
        缓存系统配置
        如果手动修改了mysql数据库中的配置
        那么需要在redis中将对应的tab_name删除
        """

        if not tab_names:
            tab_names = self.DEFAULT_TAB_NAMES
        datas = await self.__get_tab_name_values(tab_names)

        for k, v in datas.items():
            await self.rd.client().set(k, json.dumps(v))

    async def get_tab_name(self, tab_name: str, retry: int = 3):
        """
        获取系统配置
        :params tab_name: 配置表标签名称
        :params retry_num: 重试次数
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
