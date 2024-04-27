# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2021/10/19 15:47
# @File           : production.py
# @IDE            : PyCharm
# @desc           : 数据库开发配置文件


"""
Redis 数据库配置

与接口是同一个数据库

格式："redis://:密码@地址:端口/数据库名称"
"""
REDIS_DB_ENABLE = True
REDIS_DB_URL = "redis://:@127.0.0.1:6379/11"

"""
MongoDB 数据库配置

与接口是同一个数据库

格式：mongodb://用户名:密码@地址:端口/?authSource=数据库名称
"""
MONGO_DB_ENABLE = True
MONGO_DB_NAME = "sakura_k"
MONGO_DB_URL = f"mongodb://127.0.0.1:27017/?authSource={MONGO_DB_NAME}"

