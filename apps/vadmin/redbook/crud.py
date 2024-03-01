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
        red_id = 2
        # sql: SELECT * FROM red_book JOIN red_book_urls ON red_book.id = red_book_urls.red_book_id WHERE red_book.id = 1;
        sql = select(models.RedBook, models.URL)
        sql = sql.join_from(models.RedBook, models.URL).where(models.RedBook.id == red_id)
        print(sql)
        queryset = await self.db.execute(sql)
        result = queryset.fetchall()
        for red_book, url in result:
            print(
                f"url: {url.url} red_book_id: {url.red_book_id} "
                f"Source: {red_book.source} tags: {red_book.tags} title: {red_book.title} describe: {red_book.describe}"
            )
