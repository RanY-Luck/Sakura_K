#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 11:24
# @Author  : 冉勇
# @Site    : 
# @File    : __init__.py.py
# @Software: PyCharm
# @desc    :
from application.config.development import MONGO_DB_ENABLE
from utils import status
from .database_manage import DatabaseManage
from .mongo_manage import MongoManage
from core.exception import CustomException

db = MongoManage()


async def get_database() -> DatabaseManage:
    if not MONGO_DB_ENABLE:
        raise CustomException(msg="请先开启 MongoDB 数据库连接！", code=status.HTTP_ERROR)
    return db
