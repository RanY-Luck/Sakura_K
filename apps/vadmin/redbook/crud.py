#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 14:37
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.crud import DalBase
from . import models, schemas
from ..system.crud import DictTypeDal


class RedbookDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RedbookDal, self).__init__()
        self.db = db
        self.model = models.RedBook
        self.schema = schemas.RedbookSimpleOut

    async def get_url_details(self, redbook_id: list[int]) -> dict:
        """
        获取url详细信息
        """
        data = {}
        options = [joinedload(self.model.urls)]
        objs = await DictTypeDal(self.db).get_datas(
            limit=0,
            v_return_objs=True,
            v_options=options,
            dict_type=("in", redbook_id)
        )
        for obj in objs:
            if not obj:
                data[obj.dict_type] = []
                continue
            else:
                data[obj.dict_type] = [schemas.RedbookSimpleOut.model_validate(i).model_dump() for i in obj.details]
        return data


class UrlsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(UrlsDal, self).__init__()
        self.db = db
        self.model = models.URL
        self.schema = schemas.UrlsSimpleOut
