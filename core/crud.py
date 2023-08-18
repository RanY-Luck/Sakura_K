#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 15:14
# @Author  : 冉勇
# @Site    : 
# @File    : crud.py
# @Software: PyCharm
# @desc    : 数据库增删改查操作
"""
首先你要了解SQLAlchemy 查询操作：https://segmentfault.com/a/1190000016767008
sqlalchemy 查询操作（官方文档）: https://www.osgeo.cn/sqlalchemy/orm/queryguide.html
sqlalchemy 增删改操作：https://www.osgeo.cn/sqlalchemy/tutorial/orm_data_manipulation.html#updating-orm-objects
sqlalchemy lazy load和eager load: https://www.jianshu.com/p/dfad7c08c57a
Mysql中内连接,左连接和右连接的区别总结:https://www.cnblogs.com/restartyang/articles/9080993.html
selectinload 官方文档：https://www.osgeo.cn/sqlalchemy/orm/loading_relationships.html?highlight=selectinload#sqlalchemy.orm.selectinload
joinedload 官方文档：https://www.osgeo.cn/sqlalchemy/orm/loading_relationships.html?highlight=selectinload#sqlalchemy.orm.joinedload
"""
import datetime
from typing import Any
from typing import Set

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, delete, update, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql.selectable import Select
from starlette import status

from core.exception import CustomException


class DalBase:
    # 倒叙
    ORDER_FIELD = ["desc", "descending"]

    def __init__(self, db: AsyncSession, model: Any, schema: Any, key_models: dict = None):
        self.db = db
        self.model = model
        self.schema = schema
        self.key_models = key_models

    async def get_data(
            self,
            data_id: int = None,
            v_options: list = None,
            v_join_query: dict = None,
            v_or: list[tuple] = None,
            v_order: str = None,
            v_order_field: str = None,
            v_return_none: bool = False,
            v_schema: Any = None,
            **kwargs
    ):
        """
          获取单个数据，默认使用 ID 查询，否则使用关键词查询
          :param data_id: 数据 ID
          :param v_options: 指示应使用select在预加载中加载给定的属性。
          :param v_join_query: 外键字段查询，内连接
          :param v_or: 或逻辑查询
          :param v_order: 排序，默认正序，为 desc 是倒叙
          :param v_order_field: 排序字段
          :param v_return_none: 是否返回空 None，否认 抛出异常，默认抛出异常
          :param v_schema: 指定使用的序列化对象
          :param kwargs: 查询参数
        代码解释：
        首先，该方法会根据传入的参数构造查询语句，添加过滤条件和查询条件；
        如果传入的参数是数据ID，则使用where子句构造查询条件；
        否则使用add_filter_condition()方法添加过滤条件。
        如果传入的参数v_order不为空，则使用order_by子句添加排序条件，以查询结果的创建时间倒序排列。
        接着，该方法执行查询语句，并将结果转换为查询集。
        如果查询集不存在，且传入参数v_return_none为真，则直接返回空None；否则抛出HTTP异常，提示未找到此数据。
        如果查询集存在，并且传入了v_schema参数，则使用该参数指定的序列化对象，将ORM模型对象转换为对应的Pydantic模型对象，并使用dict()方法将其转换为Python字典返回；
        否则直接返回ORM模型对象。
        """
        sql = select(self.model).where(self.model.is_delete == False)
        if data_id:
            sql = sql.where(self.model.id == data_id)
        sql = self.add_filter_condition(sql, v_options, v_join_query, v_or, **kwargs)
        if v_order_field and (v_order in self.ORDER_FIELD):
            sql = sql.order_by(getattr(self.model, v_order_field).desc(), self.model.id.desc())
        elif v_order_field:
            sql = sql.order_by(getattr(self.model, v_order_field), self.model.id)
        elif v_order and (v_order in self.ORDER_FIELD):
            sql = sql.order_by(self.model.create_datetime.desc())
        queryset = await self.db.execute(sql)
        data = queryset.scalars().unique().first()
        if not data and v_return_none:
            return None
        if data and v_schema:
            return v_schema.model_validate(data).model_dump()
        if data:
            return data
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到此数据")

    async def get_datas(
            self,
            page: int = 1,
            limit: int = 10,
            v_options: list = None,
            v_join_query: dict = None,
            v_or: list[tuple] = None,
            v_order: str = None,
            v_order_field: str = None,
            v_return_objs: bool = False,
            v_start_sql: Any = None,
            v_schema: Any = None,
            **kwargs
    ) -> list:
        """
        获取数据列表
        :param page: 页码
        :param limit: 当前页数据量
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_join_query: 外键字段查询
        :param v_or: 或逻辑查询
        :param v_order: 排序，默认正序，为 desc 是倒叙
        :param v_order_field: 排序字段
        :param v_return_objs: 是否返回对象
        :param v_start_sql: 初始 sql
        :param v_schema: 指定使用的序列化对象
        :param kwargs: 查询参数
        代码解释：
        首先，该方法判断传入的v_start_sql参数是否为Select类型，如果不是则使用默认的select语句并添加过滤条件；
        然后使用add_filter_condition()方法添加过滤条件和查询条件。
        如果传入的参数v_order_field不为空且v_order为desc，则按照指定字段倒序排列，并将每页结果按照记录ID倒序排列；
        否则按照指定字段正序排序，并将每页结果按照记录ID正序排列；如果既没有指定排序字段也没有指定排序方式，则将每页结果按照记录ID倒序排列。
        接着，该方法根据页面编号和限制数量计算查询语句的偏移量和限制数量，并使用offset()和limit()方法添加限制条件。
        然后执行异步查询，并将查询结果转换为查询集。
        如果传入参数v_return_objs为真，则直接返回查询集；
        否则，遍历查询集并使用out_dict()方法将查询结果转换为字典类型，放入列表中返回。
        """
        if not isinstance(v_start_sql, Select):
            v_start_sql = select(self.model).where(self.model.is_delete == False)
        sql = self.add_filter_condition(v_start_sql, v_options, v_join_query, v_or, **kwargs)
        if v_order_field and (v_order in self.ORDER_FIELD):
            sql = sql.order_by(getattr(self.model, v_order_field).desc(), self.model.id.desc())
        elif v_order_field:
            sql = sql.order_by(getattr(self.model, v_order_field), self.model.id)
        elif v_order in self.ORDER_FIELD:
            sql = sql.order_by(self.model.id.desc())
        if limit != 0:
            sql = sql.offset((page - 1) * limit).limit(limit)
        queryset = await self.db.execute(sql)
        if v_return_objs:
            return queryset.scalars().unique().all()
        return [await self.out_dict(i, v_schema=v_schema) for i in queryset.scalars().unique().all()]

    async def get_count(
            self,
            v_options: list = None,
            v_join_query: dict = None,
            v_or: list[tuple] = None,
            **kwargs
    ) -> int:
        """
        获取数据总数
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_join_query: 外键字段查询
        :param v_or: 或逻辑查询
        :param kwargs: 查询参数
        """
        sql = select(func.count(self.model.id).label('total')).where(self.model.is_delete == False)
        sql = self.add_filter_condition(sql, v_options, v_join_query, v_or, **kwargs)
        queryset = await self.db.execute(sql)
        return queryset.one()['total']

    async def create_data(self, data, v_options: list = None, v_return_obj: bool = False, v_schema: Any = None):
        """
        创建数据
        :param data: 创建数据
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_schema: ，指定使用的序列化对象
        :param v_return_obj: ，是否返回对象
        """
        if isinstance(data, dict):
            obj = self.model(**data)
        else:
            obj = self.model(**data.model_dump())
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: Any,
            v_options: list = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ):
        """
        更新单个数据
        :param data_id: 修改行数据的 ID
        :param data: 数据内容
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_return_obj: ，是否返回对象
        :param v_schema: ，指定使用的序列化对象
        """
        obj = await self.get_data(data_id, v_options=v_options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs):
        """
        删除多条数据
        :param ids: 数据集
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        """
        if v_soft:
            await self.db.execute(
                update(self.model).where(self.model.id.in_(ids)).values(
                    delete_datetime=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    is_delete=True,
                    **kwargs
                )
            )
        else:
            await self.db.execute(delete(self.model).where(self.model.id.in_(ids)))
        await self.flush()

    def add_filter_condition(
            self,
            sql: select,
            v_options: list = None,
            v_join_query: dict = None,
            v_or: list[tuple] = None,
            **kwargs
    ) -> select:
        """
        添加过滤条件，以及内连接过滤条件
        :param sql:
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_join_query: 外键字段查询，内连接
        :param v_or: 或逻辑
        :param kwargs: 关键词参数
        """
        v_select_from: Set[str] = set()
        v_join: Set[str] = set()
        v_join_left: Set[str] = set()
        if v_join_query:
            for key, value in v_join_query.items():
                foreign_key = self.key_models.get(key)
                conditions = self.__dict_filter(foreign_key.get("model"), **value)
                if conditions:
                    sql = sql.where(*conditions)
                    v_join.add(key)
        if v_or:
            sql = self.__or_filter(sql, v_or, v_join_left, v_join)
        sql = self.__generate_join_conditions(sql, v_join, "join", v_select_from)
        sql = self.__generate_join_conditions(sql, v_join_left, "outerjoin", v_select_from)
        # 多对多关系查询使用
        for item in v_select_from:
            sql = sql.select_from(item)
        conditions = self.__dict_filter(self.model, **kwargs)
        if conditions:
            sql = sql.where(*conditions)
        if v_options:
            sql = sql.options(*[load for load in v_options])
        return sql

    def __generate_join_conditions(self, sql, model_keys: Set[str], join_type: str, v_select_from: []):
        """
        生成 join 条件
        """
        for item in model_keys:
            foreign_key = self.key_models.get(item)
            join = foreign_key.get("join", None)
            model = foreign_key.get("model")
            if join:
                v_select_from.add(model)
                model = join
            if join_type == "join":
                sql = sql.join(model, onclause=foreign_key.get("onclause"))
            elif join_type == "outerjoin":
                sql = sql.outerjoin(model, onclause=foreign_key.get("onclause"))
        return sql

    def __or_filter(self, sql: select, v_or: list[tuple], v_join_left: Set[str], v_join: Set[str]):
        """
        或逻辑操作
        :param sql:
        :param v_or: 或逻辑
        :param v_join_left: 左连接
        :param v_join: 内连接
        """
        or_list = []
        for item in v_or:
            if len(item) == 2:
                model = self.model
                condition = {item[0]: item[1]}
                or_list.extend(self.__dict_filter(model, **condition))
            elif len(item) == 4 and item[0] == "fk":
                model = self.key_models.get(item[1]).get("model")
                condition = {item[2]: item[3]}
                conditions = self.__dict_filter(model, **condition)
                if conditions:
                    or_list.extend(conditions)
                    v_join_left.add(item[1])
                    if item[1] in v_join:
                        v_join.remove(item[1])
            else:
                raise CustomException(msg="v_or 获取查询属性失败，语法错误！")
        if or_list:
            sql = sql.where(or_(i for i in or_list))
        return sql

    @staticmethod
    def __dict_filter(model, **kwargs):
        """
        字典过滤
        :param model:
        :param kwargs:
        """
        conditions = []
        for field, value in kwargs.items():
            if value is not None and value != "":
                attr = getattr(model, field)
                if isinstance(value, tuple):
                    if len(value) == 1:
                        if value[0] == "None":
                            conditions.append(attr.is_(None))
                        elif value[0] == "not None":
                            conditions.append(attr.isnot(None))
                        else:
                            raise CustomException("SQL查询语法错误")
                    elif len(value) == 2 and value[1] not in [None, [], ""]:
                        if value[0] == "date":
                            # 根据日期查询， 关键函数是：func.time_format和func.date_format
                            conditions.append(func.date_format(attr, "%Y-%m-%d") == value[1])
                        elif value[0] == "like":
                            conditions.append(attr.like(f"%{value[1]}%"))
                        elif value[0] == "in":
                            conditions.append(attr.in_(value[1]))
                        elif value[0] == "between" and len(value[1]) == 2:
                            conditions.append(attr.between(value[1][0], value[1][1]))
                        elif value[0] == "month":
                            conditions.append(func.date_format(attr, "%Y-%m") == value[1])
                        elif value[0] == "!=":
                            conditions.append(attr != value[1])
                        elif value[0] == ">":
                            conditions.append(attr > value[1])
                        elif value[0] == "<=":
                            conditions.append(attr <= value[1])
                        else:
                            raise CustomException("SQL查询语法错误")
                else:
                    conditions.append(attr == value)
        return conditions

    async def flush(self, obj: Any = None):
        """
        刷新到数据库
        """
        if obj:
            self.db.add(obj)
        await self.db.flush()
        if obj:
            await self.db.refresh(obj)
        return obj

    async def out_dict(self, obj: Any, v_options: list = None, v_return_obj: bool = False, v_schema: Any = None):
        """
        序列化
        :param obj:
        :param v_options: 指示应使用select在预加载中加载给定的属性。
        :param v_return_obj: ，是否返回对象
        :param v_schema: ，指定使用的序列化对象
        :return:
        """
        if v_options:
            obj = await self.get_data(obj.id, v_options=v_options)
        if v_return_obj:
            return obj
        if v_schema:
            return v_schema.model_validate(obj).model_dump()
        return self.schema.model_validate(obj).model_dump()
