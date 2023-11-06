#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 11:39:42
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    : 环境管理增删改查

from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from . import models, schemas


class EnvDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(EnvDal, self).__init__(db, models.EnvInfo, schemas.EnvSimpleOut)
