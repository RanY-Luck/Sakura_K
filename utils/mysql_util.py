#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/20 16:08
# @Author  : 冉勇
# @Site    : 
# @File    : mysql_util.py
# @Software: PyCharm
# @desc    : 数据库测试连接
import asyncio
import aiomysql
from module_admin.entity.vo.datasource_vo import SourceInfo
from utils.log_util import logger


class DatabaseHelper:
    def __init__(self, source_info: SourceInfo):
        self.db_config = {
            'host': source_info.datasource_host,
            'port': source_info.datasource_port,
            'user': source_info.datasource_user,
            'password': source_info.datasource_pwd
        }

    async def test_db_connection(self):
        """
        测试连接
        :return:
        """
        try:
            # 连接MySQL服务器
            conn = await aiomysql.connect(**self.db_config)
            await conn.ensure_closed()
            logger.info(f"连接成功: {self.db_config}")
            return {"message": "MySQL服务器连接成功!"}
        except aiomysql.Error as e:
            logger.error(f"连接失败: {self.db_config}，报错：{e}")
            return {"message": f"MySQL服务器连接失败!: {e}"}

    async def get_database(self):
        """
        获取已连接的所有库
        :return:
        """
        try:
            # 连接MySQL服务器
            conn = await aiomysql.connect(**self.db_config)
            async with conn.cursor() as cursor:
                # 执行查询所有数据库的SQL语句
                await cursor.execute("SHOW DATABASES")
                # 获取查询结果
                databases = [db[0] async for db in cursor]
            await conn.ensure_closed()
            logger.info(f"该连接的数据库有表有以下:{databases}")
            return {"databases": databases, "type": "database"}
        except aiomysql.Error as e:
            logger.error(f"获取数据库名称失败：{self.db_config}，报错：{e}")
            return {"message": f"获取数据库名称失败: {e}"}

    async def get_tables(self, database):
        """
        获取指定数据库中的所有表名
        :param database: 数据库名
        :return: 表名列表
        """
        try:
            conn = await aiomysql.connect(**self.db_config)
            async with conn.cursor() as cursor:
                # 选择数据库
                await cursor.execute(f"USE {database}")
                # 查询表名
                await cursor.execute("SHOW TABLES")
                # 获取结果
                tables = [table[0] async for table in cursor]
            await conn.ensure_closed()
            logger.info(f"数据库 {database} 中的表有: {tables}")
            return {"tables": tables, "type": "tables"}
        except aiomysql.Error as e:
            logger.error(f"获取数据库 {database} 中的表名失败: {e}")
            return {"message": f"获取数据库 {database} 中的表名失败: {e}"}

    async def get_all_databases_and_tables(self):
        """
        获取所有数据库及其表信息
        :return: 字典形式的数据库和表信息
        """
        try:
            conn = await aiomysql.connect(**self.db_config)
            databases_dict = await self.get_database()  # 使用 await 获取返回值
            databases = databases_dict['databases']  # 提取数据库列表
            all_info = {}
            for database in databases:
                async with conn.cursor() as cursor:
                    # 选择数据库
                    await cursor.execute(f"USE {database}")
                    # 获取表名
                    await cursor.execute("SHOW TABLES")
                    tables = [table[0] async for table in cursor]
                    all_info[database] = tables
            logger.info(f"获取到的数据库及其表信息: {all_info}")
            await conn.ensure_closed()
            return all_info
        except aiomysql.Error as e:
            logger.error(f"获取所有数据库及其表信息失败: {e}")
            return {"message": f"获取所有数据库及其表信息失败: {e}"}

    async def execute_query(self, database, query, params=None):
        """
        在指定的数据库中执行 SQL 查询语句
        :param database: 要操作的数据库名称
        :param query: SQL 查询语句
        :param params: 查询参数,如果有则传递,否则传递 None
        :return:
        """
        try:
            # 连接数据库
            conn = await aiomysql.connect(**self.db_config)
            async with conn.cursor() as cursor:
                # 选择数据库
                await cursor.execute(f"USE {database}")
                logger.info(f"你选择的数据库为:{database}")
                # 执行 SQL 语句
                await cursor.execute(query, params)
                logger.info(f"执行的SQL语句:{query, params}")
                # 获取结果数据
                result = await cursor.fetchall()
                logger.info(f"查询结果:{result}")
            # 提交更改(如果是写入操作)
            await conn.commit()
            await conn.ensure_closed()
            return {"data": result}
        except aiomysql.Error as e:
            # 如果发生错误,打印错误信息并回滚
            logger.error(f"操作数据库失败：{self.db_config}，报错：{e}")
            return {"message": f"操作失败: {e}"}


async def main():
    # 数据库配置
    db_config = {
        'datasource_host': '127.0.0.1',
        'datasource_port': 3306,
        'datasource_user': 'root',
        'datasource_pwd': '123456',
    }
    source_info = SourceInfo(**db_config)
    db_helper = DatabaseHelper(source_info)

    # 测试连接
    await db_helper.test_db_connection()
    # 获取所有数据库
    await db_helper.get_database()
    # 获取指定库的所有表
    await db_helper.get_tables("skf")
    # 执行查询
    query = "SELECT * FROM data_source LIMIT 10;"
    await db_helper.execute_query('skf', query)
    # 获取所有数据库及其表和列信息
    # await db_helper.get_all_databases_and_tables()
    # 执行操作
    # query = "INSERT INTO data_source(data_name,`host`,`port`,username,`password`,create_user_id,id,create_datetime," \
    #         "update_datetime,is_delete,type_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # params = (
    #     'demo', '127.0.0.1', '3306', 'ranyong', '123456', '1', '4', '2024-04-28 16:02:58', '2024-04-28 16:02:58', '0',
    #     '1')
    # result = await db_helper.execute_query('sakura_k', query, params)
    # print(result)


asyncio.run(main())
