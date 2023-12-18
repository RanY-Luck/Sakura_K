#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    : 数据库 增删改查操作
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from core.mongo_manage import MongoManage
from . import models, schemas


class LoginRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(LoginRecordDal, self).__init__()
        self.db = db
        self.model = models.VadminLoginRecord
        self.schema = schemas.LoginRecordSimpleOut


class SMSSendRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SMSSendRecordDal, self).__init__()
        self.db = db
        self.model = models.VadminSMSSendRecord
        self.schema = schemas.SMSSendRecordSimpleOut


class OperationRecordDal(MongoManage):

    def __init__(self, db: AsyncIOMotorDatabase):
        super(OperationRecordDal, self).__init__()
        self.db = db
        self.collection = db["operation_record"]
        self.schema = schemas.OperationRecordSimpleOut
        self.is_object_id = True
