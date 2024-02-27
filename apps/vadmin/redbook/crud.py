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


class DeptDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(DeptDal, self).__init__()
        self.db = db
        self.model = models.RedBook
        self.schema = schemas.RedbookSimpleOut

    async def test_join_form(self):
        """
        join_form 使用示例：通过关联表的查询条件反查询出主表的数据
        官方描述：在当前 Select 的左侧不符合我们想要从中进行连接的情况下，可以使用 Select.join_from() 方法
        官方文档：https://docs.sqlalchemy.org/en/20/orm/queryguide/select.html#setting-the-leftmost-from-clause-in-a-join
        查询条件：获取指定用户所关联的所有部门列表数据，只返回关联的部门列表数据
        :return:
        """
        # SELECT * FROM red_book WHERE id = 1;
        red_book_id = 1
        sql = select(models.RedBook).where(models.RedBook.id == red_book_id)
        print("sql1:", sql)
        sql = sql.join_from(models.RedBook, models.URL).where(models.URL.red_book_id == red_book_id)
        print("sql2:", sql)
        queryset = await self.db.scalars(sql)
        result = queryset.unique().all()
        for dept in result:
            print(f"source：{dept.source} tags：{dept.tags} title：{dept.title}")
