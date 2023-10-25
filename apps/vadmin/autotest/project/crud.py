#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-23 15:51:21
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    :

from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from . import models, schemas


class ProjectDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(ProjectDal, self).__init__(db, models.ProjectInfo, schemas.ProjectSimpleOut)
