#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 17:23:58
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    :
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from . import models, schemas


class DataSourceDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DataSourceDal, self).__init__(db, models.DataSourceInfo, schemas.DataSourceSimpleOut)


class DataTypeDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DataTypeDal, self).__init__(db, models.DataType, schemas.DataTypeSimpleOut)
