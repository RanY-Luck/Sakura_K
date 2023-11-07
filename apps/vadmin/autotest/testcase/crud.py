#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 11:09:09
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    :
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from . import models, schemas


class TestCaseDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(TestCaseDal, self).__init__(db, models.TestCaseInfo, schemas.TestCaseSimpleOut)
