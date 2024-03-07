#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 14:37
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from typing import Any

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

    async def get_redbook_urls(self, red_id: int) -> list[dict[str, Any]]:
        # sql: SELECT * FROM red_book JOIN red_book_urls ON red_book.id = red_book_urls.red_book_id WHERE red_book.id = 1;
        sql = select(models.RedBook, models.URL)
        sql = sql.join_from(models.RedBook, models.URL).where(models.RedBook.id == red_id)
        queryset = await self.db.execute(sql)
        result = queryset.fetchall()
        # 将结果转换为 JoinResultSchema 的实例列表
        serialized_result = []
        for red_book, url in result:
            serialized_result.append(
                {
                    'url': url.url,
                    'red_book_id': url.red_book_id,
                    'source': red_book.source,
                    'tags': red_book.tags,
                    'title': red_book.title,
                    'describe': red_book.describe,
                    'type': red_book.type,
                    'affiliation': red_book.affiliation,
                    'release_time': red_book.release_time,
                    'auth_name': red_book.auth_name,
                }
            )
        return serialized_result
