#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/10 17:13
# @Author  : 冉勇
# @Site    : 
# @File    : production.py
# @Software: PyCharm
# @desc    : 生产环境数据生产配置文件

"""
Mysql 数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
"""
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://username:password@host:port/dbname"

"""
Redis 数据库配置项
连接Redis引擎官方文档：https://redis.io/docs/
Redis链接配置说明：redis://:密码@地址:端口/数据库
"""
REDIS_DB_ENABLE = True
REDIS_DB_URL = "redis://:123456@127.0.0.1:6379/0"

"""
MongoDB 数据库配置项
连接MongoDB引擎官方文档：https://www.mongodb.com/docs/drivers/pymongo/
MongoDB链接配置说明：mongodb://用户名:密码@地址:端口/?authSource={MONGO_DB_NAME}
"""
MONGO_DB_ENABLE = True
MONGO_DB_NAME = "sakura_k"
MONGO_DB_URL = f"mongodb://127.0.0.1:27017/?authSource={MONGO_DB_NAME}"

"""
阿里云对象存储OSS配置
阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
 *  [accessKeyId] {String}：通过阿里云控制台创建的AccessKey。
 *  [accessKeySecret] {String}：通过阿里云控制台创建的AccessSecret。
 *  [bucket] {String}：通过控制台或PutBucket创建的bucket。
 *  [endpoint] {String}：bucket所在的区域， 默认oss-cn-hangzhou。
"""
ALIYUN_OSS = {
    "accessKeyId": "通过阿里云控制台创建的AccessKey",
    "accessKeySecret": "通过阿里云控制台创建的AccessSecret",
    "endpoint": "https://oss-cn-shenzhen.aliyuncs.com",
    "bucket": "通过控制台或PutBucket创建的bucket",
    "baseUrl": "https://xxxx.oss-cn-shenzhen.aliyuncs.com/"
}

"""
获取IP地址归属地
文档：https://user.ip138.com/ip/doc
"""
IP_PARSE_ENABLE = True
IP_PARSE_TOKEN = ""
