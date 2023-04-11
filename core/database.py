#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 19:09
# @Author  : 冉勇
# @Site    : 
# @File    : database.py
# @Software: PyCharm
# @desc    : SQLAlchemy 部分

"""
导入SQLAlchemy 部分
安装： pip3 install sqlalchemy
中文文档：https://www.osgeo.cn/sqlalchemy/
"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from application.settings import SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_TYPE


def create_async_engine_session(database_url: str, database_type: str = "mysql"):
    """
    创建数据库会话
    相关配置文档：https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
    max_overflow 超过连接池大小外最多创建的连接
    pool_size=5,     # 连接池大小
    pool_timeout=20, # 池中没有连接最多等待的时间，否则报错
    pool_recycle=-1  # 多久之后对线程池中的线程进行一次连接的回收（重置）
    :param database_url: dialect+driver://username:password@host:port/database
    :param database_type:
    :return:
    代码解释：
    该方法使用create_async_engine()方法创建SQLAlchemy引擎对象，
    传入的参数包括数据库URL、是否显示SQL语句、是否在连接池中检查空闲连接的有效性、空闲连接回收的时间间隔、启用异步引擎等配置。
    其中，connect_args参数表示连接数据库时的附加参数，如果数据库类型为sqlite3，则还需要添加check_same_thread参数确保线程安全。
    最后，使用工厂函数sessionmaker()创建一个与数据库连接绑定的异步会话对象，用于进行数据访问和事务管理操作。
    """
    engine = create_async_engine(
        database_url,
        echo=False,
        pool_pre_ping=True,
        pool_recycle=3600,
        future=True,
        max_overflow=5,
        connect_args={'check_same_thread': False, "timeout": 30} if database_type == 'sqlite3' else {}
    )
    return sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=True, class_=AsyncSession)


class Base:
    """
    将表名改为小写
    """

    @declared_attr
    def __tablename__(self):
        # 如果有自定义表名就取自定义，没有就取小写类名
        table_name = self.__tablename__
        if not table_name:
            model_name = self.__name__
            ls = []
            for index, char in enumerate(model_name):
                if char.isupper() and index != 0:
                    ls.append("_")
                ls.append(char)
            table_name = "".join(ls).lower()
        return table_name


"""
创建基本映射类
"""
Model = declarative_base(name="Model", cls=Base)


async def db_getter():
    """
    获取主数据库
    数据库依赖项，它将在单个请求中使用，然后在请求完成后将其关闭
    :return:
    """
    async with create_async_engine_session(SQLALCHEMY_DATABASE_URL, SQLALCHEMY_DATABASE_TYPE)() as session:
        async with session.begin():
            yield session
