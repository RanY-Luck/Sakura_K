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


class RedBookUrlsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RedBookUrlsDal, self).__init__()
        self.db = db
        self.model = models
        self.schema = schemas

    async def get_redbook_urls(self, red_id: int) -> list[dict[str, Any]]:
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
        url_list = []
        unique_data = []
        red_book_ids = set()
        for item in serialized_result:
            url = item['url']
            red_book_id = item['red_book_id']
            if red_book_id not in red_book_ids:
                red_book_ids.add(red_book_id)
                unique_data.append(item)
            url_list.append(url)
        # 判断为空则返回 null
        return {"data": unique_data, "urls": url_list} if unique_data else None
