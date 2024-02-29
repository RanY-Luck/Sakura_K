#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 14:37
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from . import models, schemas


class RedbookDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RedbookDal, self).__init__()
        self.db = db
        self.model = models.RedBook
        self.schema = schemas.RedbookSimpleOut


class UrlsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(UrlsDal, self).__init__()
        self.db = db
        self.model = models.URL
        self.schema = schemas.UrlsSimpleOut


class RedBookUrlstDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RedBookUrlstDal, self).__init__()
        self.db = db
        self.model = models
        self.schema = schemas

    async def test_join_form(self):
        red_id = 1
        # sql: SELECT * FROM red_book JOIN red_book_urls ON red_book.id = red_book_urls.red_book_id WHERE red_book.id = 1;
        sql = select(models.RedBook, models.URL).join_from(
            models.RedBook, models.URL, models.RedBook.id == models.URL.red_book_id
        ).where(models.RedBook.id == red_id)
        print(sql)
        queryset = await self.db.scalars(sql)
        result = queryset.unique().all()
        for data in result:
            print(f"source：{data.source} tags：{data.tags} title：{data.title} {data}")
            print(f"{data}")
