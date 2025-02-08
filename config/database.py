#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:54
# @Author  : 冉勇
# @Site    : 
# @File    : database.py
# @Software: PyCharm
# @desc    : mysql数据库
import datetime
from sqlalchemy import Column, Integer, DateTime, String, text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from urllib.parse import quote_plus
from config.env import DataBaseConfig

ASYNC_SQLALCHEMY_DATABASE_URL = f"mysql+asyncmy://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@" \
                                f"{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}"

if DataBaseConfig.db_type == 'postgresql':
    ASYNC_SQLALCHEMY_DATABASE_URL = (
        f'postgresql+asyncpg://{DataBaseConfig.db_username}:{quote_plus(DataBaseConfig.db_password)}@'
        f'{DataBaseConfig.db_host}:{DataBaseConfig.db_port}/{DataBaseConfig.db_database}'
    )

async_engine = create_async_engine(
    ASYNC_SQLALCHEMY_DATABASE_URL,
    echo=DataBaseConfig.db_echo,  # 为 True 输出所有 SQL 语句
    max_overflow=DataBaseConfig.db_max_overflow,  # 超过连接池大小外最多创建的连接数
    pool_size=DataBaseConfig.db_pool_size,  # 最大连接数
    pool_recycle=DataBaseConfig.db_pool_recycle,  # 连接被回收的时间
    pool_timeout=DataBaseConfig.db_pool_timeout  # 抛出超时异常之前等待返回连接的秒数
)
# 定义一个异步会话工厂，用于创建异步数据库会话
AsyncSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=async_engine)


class Base(AsyncAttrs, DeclarativeBase):
    """
    创建基本映射类
    稍后，我们将继承该类，创建每个 ORM 模型
    """
    pass


class BaseMixin:
    """model的基类,所有model都必须继承"""
    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    update_time = Column(
        DateTime, nullable=False, default=datetime.datetime.now,
        onupdate=datetime.datetime.now, index=True, comment='更新时间'
    )
    del_flag = Column(
        String(1), nullable=False, default='0', server_default=text("'0'"), comment='删除标志（0代表存在 2代表删除）'
    )
