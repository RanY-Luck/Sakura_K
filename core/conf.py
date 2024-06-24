#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/24 12:03
# @Author  : 冉勇
# @Site    :
# @File    : conf.py
# @Software: PyCharm
# @desc    :
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Global Settings"""

    # Env Redis
    # todo:后续写入到.env中
    REDIS_HOST: str = '127.0.0.1'
    REDIS_PORT: int = '6379'
    REDIS_PASSWORD: str = ''
    REDIS_DATABASE: int = '11'

    # Redis
    REDIS_TIMEOUT: int = 5


@lru_cache
def get_settings() -> Settings:
    """获取全局配置"""
    return Settings()


# 创建配置实例
settings = get_settings()
