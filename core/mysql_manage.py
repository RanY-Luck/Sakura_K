#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/4/29 14:24
# @Author   : 冉勇
# @File     : mysql_manage.py
# @Software : PyCharm
# @Desc     :
import pymysql

from core.logger import logger


class DatabaseHelper:
    def __init__(self, db_config):
        self.db_config = db_config

    def test_db_connection(self):
        try:
            # 连接数据库
            conn = pymysql.connect(**self.db_config)
            conn.close()
            logger.info("MySQL服务器连接成功")
            return {"message": "MySQL服务器连接成功!"}
        except pymysql.Error as e:
            # 如果连接失败,打印错误信息
            print(f"MySQL服务器连接失败: {e}")
            logger.error(f"MySQL服务器连接失败：{self.db_config}，报错：{e}")
            return {"message": f"MySQL服务器连接失败: {e}"}

    def get_database(self):
        """
        获取已连接的所有库
        :return:
        """
        try:
            # 连接MySQL服务器
            conn = pymysql.connect(**self.db_config)
            # 获取游标
            cursor = conn.cursor()
            # 执行查询所有数据库的SQL语句
            cursor.execute("SHOW DATABASES")
            # 获取查询结果
            databases = [db[0] for db in cursor.fetchall()]
            logger.info(f"该连接的数据库有表有以下:{databases}")
            # 关闭游标和连接
            cursor.close()
            conn.close()
            return {"databases": databases}
        except pymysql.Error as e:
            # 如果发生错误,打印错误信息
            logger.error(f"获取数据库名称失败：{self.db_config}，报错：{e}")
            return {"message": f"获取数据库名称失败: {e}"}

    def execute_query(self, database, query, params=None):
        """
        在指定的数据库中执行 SQL 查询语句。

        Args:
            database (str): 要操作的数据库名称。
            query (str): SQL 查询语句。
            params (tuple, optional): 查询参数,如果有则传递,否则传递 None。

        Returns:
            dict: 包含查询结果的字典,格式为 {"data": query_result}。若发生异常,则返回错误信息。
        """
        try:
            # 连接数据库
            conn = pymysql.connect(**self.db_config)
            # 选择数据库
            conn.select_db(database)
            logger.info(f"你选择的数据库为:{database}")
            # 获取游标
            with conn.cursor() as cursor:
                # 执行 SQL 语句
                cursor.execute(query, params)
                logger.info(f"执行的SQL语句:{query, params}")
                # 获取结果数据
                result = cursor.fetchall()
                logger.info(f"查询结果:{result}")
                # 提交更改(如果是写入操作)
                conn.commit()
            return {"data": result}
        except pymysql.Error as e:
            # 如果发生错误,打印错误信息并回滚
            logger.error(f"操作数据库失败：{self.db_config}，报错：{e}")
            conn.rollback()
            return {"message": f"操作失败: {e}"}


# 数据库配置
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '123456'
}

db_helper = DatabaseHelper(db_config)
# 测试连接
db_helper.test_db_connection()
# 获取所有数据库
db_helper.get_database()

# 执行查询
query = "SELECT * FROM red_book LIMIT 10;"
db_helper.execute_query('sakura_k', query)

# 执行操作
query = "INSERT INTO data_source(data_name,`host`,`port`,username,`password`,create_user_id,id,create_datetime," \
        "update_datetime,is_delete,type_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
params = (
    'demo', '127.0.0.1', '3306', 'ranyong', '123456', '1', '4', '2024-04-28 16:02:58', '2024-04-28 16:02:58', '0', '1')
db_helper.execute_query('sakura_k', query, params)
