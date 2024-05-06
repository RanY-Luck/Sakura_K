#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/4/29 14:24
# @Author   : 冉勇
# @File     : mysql_manage.py
# @Software : PyCharm
# @Desc     :
import aiomysql

from apps.vadmin.autotest.datasource.schemas import SourceInfo
from core.logger import logger


class DatabaseHelper:
    def __init__(self, source_info: SourceInfo):
        self.db_config = {
            'host': source_info.get('host'),
            'port': source_info.get('port'),
            'user': source_info.get('user'),
            'password': source_info.get('password')
        }

    async def test_db_connection(self):
        """
        测试连接
        :return:
        """
        try:
            # 连接数据库
            conn = await aiomysql.connect(**self.db_config)
            await conn.ensure_closed()
            logger.info("MySQL服务器连接成功")
            return {"message": "MySQL服务器连接成功!"}
        except aiomysql.Error as e:
            logger.error(f"MySQL服务器连接失败：{self.db_config}，报错：{e}")
            return {"message": f"MySQL服务器连接失败!"}

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
            return {"databases": databases}
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
            return {"tables": tables}
        except aiomysql.Error as e:
            logger.error(f"获取数据库 {database} 中的表名失败: {e}")
            return {"message": f"获取数据库 {database} 中的表名失败: {e}"}

    async def get_all_tables_and_columns(self):
        """
        获取所有数据库及其表和列信息
        :return: 字典形式的数据库信息
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
                    all_info[database] = {}
                    for table in tables:
                        # 获取表结构
                        await cursor.execute(f"DESCRIBE {table}")
                        columns = [column[0] async for column in cursor]
                        all_info[database][table] = columns
                    logger.info(f"数据库 {database} 中的表有: {all_info}")
            await conn.ensure_closed()
            return all_info
        except aiomysql.Error as e:
            logger.error(f"获取所有数据库及其表和列信息失败: {e}")
            return {"message": f"获取所有数据库及其表和列信息失败: {e}"}

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
        'host': '127.0.0.1',
        'port': 3306,
        'user': 'root',
        'password': '123456',
    }
    source_info = SourceInfo(**db_config)
    db_helper = DatabaseHelper(source_info)

    # 测试连接
    result = await db_helper.test_db_connection()
    print(result)
    # 获取所有数据库
    result = await db_helper.get_database()
    print(result)
    # 获取指定库的所有表
    result = await db_helper.get_tables("sakura_k")
    print(result)
    # 执行查询
    query = "SELECT * FROM red_book LIMIT 10;"
    result = await db_helper.execute_query('sakura_k', query)
    print(result)
    # 获取所有数据库及其表和列信息
    result = await db_helper.get_all_tables_and_columns()
    print(result)
    # 执行操作
    # query = "INSERT INTO data_source(data_name,`host`,`port`,username,`password`,create_user_id,id,create_datetime," \
    #         "update_datetime,is_delete,type_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    # params = (
    #     'demo', '127.0.0.1', '3306', 'ranyong', '123456', '1', '4', '2024-04-28 16:02:58', '2024-04-28 16:02:58', '0',
    #     '1')
    # result = await db_helper.execute_query('sakura_k', query, params)
    # print(result)


# asyncio.run(main())
