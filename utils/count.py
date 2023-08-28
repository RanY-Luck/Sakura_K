#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 14:27
# @Author  : 冉勇
# @Site    : 
# @File    : count.py
# @Software: PyCharm
# @desc    : 计数
from redis.asyncio.client import Redis

"""
代码解释：
定义了一个Count类，这个类里面封装了Redis对象的相关操作方法。在初始化 Count 类时，需要传入一个 Redis 对象 rd 和一个 key 值，用于指定在Redis中的存储位置。
类中包含以下方法：
- add：用于增加计数器，将当前计数器+1后设置到redis的指定位置，并返回当前计数器的值
- subtract：用于减少计数器，将当前计数器-1后设置到redis的指定位置，并返回当前计数器的值
- get_count：获取当前计数器的值，主要从redis中获取指定位置的值
- reset：将计数器的值重置为0，将0设置到redis的指定位置中
- delete：删除redis中指定位置的值
"""


class Count:
    """
    计数
    """

    def __init__(self, rd: Redis, key):
        self.rd = rd
        self.key = key

    async def add(self, ex: int = None) -> int:
        await self.rd.set(self.key, await self.get_count() + 1, ex=ex)
        return await self.get_count()

    async def subtract(self, ex: int = None) -> int:
        await self.rd.set(self.key, await self.get_count() - 1, ex=ex)
        return await self.get_count()

    async def get_count(self) -> int:
        number = await self.rd.get(self.key)
        if number:
            return int(number)
        return 0

    async def reset(self) -> None:
        await self.rd.set(self.key, 0)

    async def delete(self) -> None:
        await self.rd.delete(self.key)
