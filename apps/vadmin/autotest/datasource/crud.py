#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 17:23:58
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    :
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.expression import select

from core.crud import DalBase
from . import models, schemas


class DataSourceDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DataSourceDal, self).__init__(db, models.DataSourceInfo, schemas.DataSourceSimpleOut)


# 通过data_source的id来查询数据库的账号、密码、端口
class DataSourceInfoDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DataSourceInfoDal, self).__init__()
        self.db = db
        self.model = models
        self.schema = schemas

    async def get_datasource_info(self, source_id: int) -> List[schemas.DataSourceSimpleOut]:
        """
        获取数据源信息
        :param self:
        :param source_id: 数据源id
        :return:
        """
        sql = select(models.DataSourceInfo).where(models.DataSourceInfo.id == source_id)
        queryset = await self.db.execute(sql)
        result = queryset.scalars().all()
        return [schemas.DataSourceSimpleOut.from_orm(item) for item in result]
