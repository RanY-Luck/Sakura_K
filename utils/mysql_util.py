#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/20 16:08
# @Author  : 冉勇
# @Site    : 
# @File    : mysql_util.py
# @Software: PyCharm
# @desc    : 数据库测试、连接、执行SQL
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
        测试数据库连接并处理不同类型的错误
        :return: dict 包含连接状态和消息
        """
        try:
            conn = await aiomysql.connect(**self.db_config)
            await conn.ensure_closed()
            logger.info(f"连接成功: {self.db_config}")
            return {"status": "success", "message": "MySQL服务器连接成功!"}
        except aiomysql.OperationalError as e:
            error_code, error_message = e.args
            if error_code == 1045:
                logger.error(f"认证失败: {self.db_config}")
                return {"status": "error", "message": "MySQL认证失败: 用户名或密码错误"}
            elif error_code == 2003:
                logger.error(f"无法连接到服务器: {self.db_config}")
                return {"status": "error", "message": "无法连接到MySQL服务器: 请检查主机名和端口"}
            else:
                logger.error(f"操作错误: {self.db_config}, 错误: {e}")
                return {"status": "error", "message": f"MySQL操作错误: {error_message}"}
        except aiomysql.InterfaceError as e:
            logger.error(f"接口错误: {self.db_config}, 错误: {e}")
            return {"status": "error", "message": "MySQL接口错误: 可能是连接参数不正确"}
        except Exception as e:
            logger.error(f"未知错误: {self.db_config}, 错误: {e}")
            return {"status": "error", "message": f"未知错误: {str(e)}"}

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

    async def execute_query(self, database, query):
        """
        在指定的数据库中执行 SQL 语句
        :param database: 要操作的数据库名称
        :param query: SQL 语句
        :return: 包含操作结果的字典
        """
        try:
            conn = await aiomysql.connect(**self.db_config)
            async with conn.cursor() as cursor:
                await cursor.execute(f"USE {database}")
                logger.info(f"你选择的数据库为:{database}")
                affected_rows = await cursor.execute(query)
                logger.info(f"执行的SQL语句:{query}")
                # 检查是否是 SELECT 语句
                if query.strip().upper().startswith("SELECT"):
                    # 获取字段名
                    field_names = [d[0] for d in cursor.description]
                    # 获取结果数据
                    result = await cursor.fetchall()
                    logger.info(f"查询结果:{result}")
                    await conn.commit()
                    return {
                        "type": "SELECT",
                        "fields": field_names,
                        "data": result
                    }
                else:
                    # 非 SELECT 语句，返回影响的行数
                    await conn.commit()
                    return {
                        "type": "NON-SELECT",
                        "affected_rows": affected_rows
                    }
        except aiomysql.Error as e:
            logger.error(f"操作数据库失败：{self.db_config}，报错：{e}")
            return {"type": "ERROR", "message": f"操作失败: {e}"}
        finally:
            await conn.ensure_closed()


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
    # 执行sql语句
    query = "INSERT INTO data_source (`datasource_id`, `datasource_name`, `datasource_type`, `datasource_host`, `datasource_port`, `datasource_user`, `datasource_pwd`, `create_by`, `create_time`, `update_by`, `update_time`, `remark`) VALUES (7, '12323', 'mysql', '127.0.0.1', '3306', 'root', 'gAAAAABm74I5oiYNpBlxdDiJM5TfI6m-G5h7_mrVYY99Zl31PZAzarKDTGmDLxWnOB2gNZVgmcN9pVbBdwfJDRsZ2AYVlKzdSw==', 'admin', '2024-09-22 10:34:33', 'admin', '2024-09-22 10:34:33', '');"
    await db_helper.execute_query('skf', query)
    # 获取所有数据库及其表和列信息
    await db_helper.get_all_databases_and_tables()

# asyncio.run(main())
