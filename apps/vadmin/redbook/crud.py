#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 14:37
# @File           : crud.py
# @IDE            : PyCharm
# @desc           : 数据访问层
from typing import Any, Dict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute
from sqlalchemy.orm.base import _T_co

from core.crud import DalBase
from . import models, schemas


class RedbookDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RedbookDal, self).__init__()
        self.db = db
        self.model = models.RedBook
        self.schema = schemas.RedbookSimpleOut

    async def create_data_info(self, data: Dict, create_user_id: int) -> models.RedBook:
        """
        创建小红书图文信息(非链接)
        :param data: 返回的图文信息
        :return:
        """
        redbook_data = data[0]
        redbook = models.RedBook(
            source=redbook_data['作品ID'],
            tags=' '.join(redbook_data['作品标签']),
            title=redbook_data['作品标题'],
            describe=redbook_data['作品描述'],
            type=redbook_data['作品类型'],
            affiliation=redbook_data['IP归属地'],
            release_time=redbook_data['发布时间'],
            auth_name=redbook_data['作者昵称'],
            create_user_id=create_user_id,
        )
        self.db.add(redbook)
        await self.db.flush()
        redbook_id = redbook.id
        return redbook

    async def create_batch_data_info(self, data_list: Dict, create_user_id: int) -> list[
        InstrumentedAttribute[_T_co] | _T_co]:
        """
        批量创建小红书图文信息(非链接)
        :param data_list:
        :param create_user_id:
        :return:
        """
        redbook_ids = []
        for item in data_list:
            redbook = models.RedBook(
                source=item.get('作品ID'),
                tags=' '.join(item.get('作品标签')),
                title=item.get('作品标题'),
                describe=item.get('作品描述'),
                type=item.get('作品类型'),
                affiliation=item.get('IP归属地'),
                release_time=item.get('发布时间'),
                auth_name=item.get('作者昵称'),
                create_user_id=create_user_id
            )
            self.db.add(redbook)
            await self.db.flush()
            redbook_ids.append(redbook.id)
        return redbook_ids


class UrlsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(UrlsDal, self).__init__()
        self.db = db
        self.model = models.URL
        self.schema = schemas.UrlsSimpleOut

    async def create_data_urls(self, red_book_id: int, url: str) -> models.URL:
        """
        创建小红书链接(非图文)
        :param url: 无水印源链接
        :param red_book_id: 对应返回的图文信息的id
        :return:
        """
        urls = models.URL(
            red_book_id=red_book_id,
            url=url,
        )
        self.db.add(urls)
        await self.db.flush()
        return urls

    async def create_batch_data_urls(self, red_book_id: int, url: str) -> models.URL:
        """
        批量创建小红书链接(非图文)
        :param url: 无水印源链接
        :param red_book_id: 对应返回的图文信息的id
        :return:
        """
        urls = models.URL(
            red_book_id=red_book_id,
            url=url
        )
        self.db.add(urls)
        await self.db.flush()
        return urls


class RedBookUrlsDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RedBookUrlsDal, self).__init__()
        self.db = db
        self.model = models
        self.schema = schemas

    async def get_redbook_urls(self, red_id: int) -> dict[str, list[Any] | list[dict[str, Any]]] | None:
        """
        获取小红书信息+无水印链接
        :param red_id: 小红书id
        :return:
        """
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
        return {"info": unique_data, "urls": url_list} if unique_data else None
