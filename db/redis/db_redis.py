#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/24 11:56
# @Author  : 冉勇
# @Site    : 
# @File    : db_redis.py
# @Software: PyCharm
# @desc    : redis客户端链接
import sys
from redis.asyncio.client import Redis
from redis.exceptions import AuthenticationError, TimeoutError
from core import logger
from core.conf import settings


class RedisCli(Redis):
    def __init__(self):
        super(RedisCli, self).__init__(
            host=settings.REDIS_HOST,
            port=settings.REDIS_PORT,
            password=settings.REDIS_PASSWORD,
            db=settings.REDIS_DATABASE,
            socket_timeout=settings.REDIS_TIMEOUT,
            decode_responses=True,  # 转码 utf-8
        )

    async def open(self):
        """
        触发初始化连接

        :return:
        """
        try:
            await self.ping()
        except TimeoutError:
            logger.error('❌ 数据库 redis 连接超时')
            sys.exit()
        except AuthenticationError:
            logger.error('❌ 数据库 redis 连接认证失败')
            sys.exit()
        except Exception as e:
            logger.error('❌ 数据库 redis 连接异常 {}', e)
            sys.exit()

    async def delete_prefix(self, prefix: str, exclude: str | list = None):
        """
        删除指定前缀的所有key

        :param prefix:
        :param exclude:
        :return:
        """
        keys = []
        async for key in self.scan_iter(match=f'{prefix}*'):
            if isinstance(exclude, str):
                if key != exclude:
                    keys.append(key)
            elif isinstance(exclude, list):
                if key not in exclude:
                    keys.append(key)
            else:
                keys.append(key)
        for key in keys:
            await self.delete(key)


# 创建 redis 客户端实例
redis_client = RedisCli()
