#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 17:56:40
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    : 自定义函数增删改查
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from . import models, schemas


class FunctionsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(FunctionsDal, self).__init__(db, models.FunctionsInfo, schemas.FunctionsSimpleOut)
