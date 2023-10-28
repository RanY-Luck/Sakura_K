#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-28 14:37:30
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    :

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas


class ApInfoDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ApInfoDal, self).__init__(db, models.ApiInfo, schemas.ApInfoOut)
