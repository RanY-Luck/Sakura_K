#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/10 17:13
# @Author  : 冉勇
# @Site    : 
# @File    : development.py
# @Software: PyCharm
# @desc    : 开发环境数据生产配置文件

"""
Mysql 数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
"""
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://root:123456@localhost:3306/Sakura_k"
SQLALCHEMY_DATABASE_TYPE = "mysql"

"""
Redis 数据库配置项
连接Redis引擎官方文档：https://redis.io/docs/
Redis链接配置说明：redis://:密码@地址:端口/数据库
"""
REDIS_DB_ENABLE = True
REDIS_DB_URL = "redis://:123456@localhost:6379/0"

"""
MongoDB 数据库配置项
连接MongoDB引擎官方文档：https://www.mongodb.com/docs/drivers/pymongo/
MongoDB链接配置说明：mongodb://用户名:密码@地址:端口/?authSource={MONGO_DB_NAME}
"""
MONGO_DB_ENABLE = True
MONGO_DB_NAME = "Sakura_k"
MONGO_DB_URL = f"mongodb://127.0.0.1:27017/?authSource={MONGO_DB_NAME}"
