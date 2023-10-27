#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-23 15:51:14
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    : 模块列表增删改查

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models,schemas

class ModuleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ModuleDal, self).__init__(db, models.ModuleInfo, schemas.ModuleSimpleOut)
