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
from typing import List, Set
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy import func, delete, update, or_
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from core.exception import CustomException
from sqlalchemy.sql.selectable import Select
from typing import Any


class DalBase:
    # 倒序
    ORDER_FIELD = ['desc', 'descending']

    def __init__(
            self,
            db: AsyncSession,
            model: Any,
            schema: Any,
            key_models: dict = None
    ):
        """
        :param db: 数据库的会话对象
        :param model: ORM模型对象
        :param schema: Pydantic模型对象
        :param key_models: 关键词模型字典
        """
        self.db = db
        self.model = model
        self.schema = schema
        self.key_models = key_models

    async def get_data(
            self,
            data_id: int = None,
            v_options: list = None,
            v_join_query: dict = None,
            v_or: List[tuple] = None,
            v_order: str = None,
            v_return_none: bool = False,
            v_schema: Any = None,
            **kwargs
    ):
        """
        根据指定条件查询单个数据库记录，并返回该记录的ORM模型对象
        :param data_id: 要查询的ORM模型对象的主键ID
        :param v_options: 列表类型，表示使用select在预加载中加载给定的属性。
        :param v_join_query: 字典类型，表示外键字段查询，内连接。
        :param v_or: 列表类型，表示或查询。
        :param v_order: 字符串类型，表示排序，默认正序，可以传入desc表示倒序。
        :param v_return_none: 布尔类型，表示是否返回空None，如果为假则抛出异常。
        :param v_schema: 表示要使用的序列化对象。
        :param kwargs: 查询参数
        :return:
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
        if v_order and (v_order in self.ORDER_FIELD):
            sql = sql.order_by(self.model.create_datetime.desc())
        queryset = await self.db.execute(sql)
        data = queryset.scalars().unique().first()
        if not data and v_return_none:
            return None
        if data and v_schema:
            return v_schema.from_orm(data).dict()
        if data:
            return data
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="未找到此数据")

    async def get_datas(
            self,
            page: int = 1,
            limit: int = 10,
            v_options: list = None,
            v_join_query: dict = None,
            v_or: List[tuple] = None,
            v_order: str = None,
            v_order_field: str = None,
            v_return_objs: bool = False,
            v_start_sql: Any = None,
            v_schema: Any = None,
            **kwargs
    ):
        """
        查询指定模型数据库表的多条记录
        :param page: 表示页面编号，默认为1。
        :param limit: 表示每个页面的数量限制，默认为10。
        :param v_options: 列表类型，表示使用select在预加载中加载给定的属性。
        :param v_join_query: 字典类型，表示外键字段查询，内连接。
        :param v_or: 列表类型，表示或查询。
        :param v_order: 字符串类型，表示排序，默认正序，可以传入desc表示倒序。
        :param v_order_field: 字符串类型，表示排序字段。
        :param v_return_objs: 布尔类型，表示是否返回对象。
        :param v_start_sql: 表示要使用的起始SQL语句，如果没有指定将使用默认的select语句。
        :param v_schema: 表示要使用的序列化对象。
        :param kwargs: 查询参数
        :return:
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
            v_or: List[tuple] = None,
            **kwargs
    ):
        """
        获取指定模型数据库表的记录总数
        :param v_options: 列表类型，表示使用select在预加载中加载给定的属性。
        :param v_join_query: 字典类型，表示外键字段查询，内连接。
        :param v_or: 列表类型，表示或查询。
        :param kwargs: 查询参数。
        :return:
        代码解释：
        该方法首先使用select函数构造一个SQL语句，使用func.count()方法计算符合条件的记录个数，并将其命名为total。
        然后使用where()方法添加过滤条件，将is_delete属性为False的记录作为目标记录。
        接着使用add_filter_condition()方法添加过滤条件和查询条件。
        然后执行异步查询，并返回结果集中的唯一元素的total属性值，即查询结果的总条数。
        """
        sql = select(func.count(self.model.id).label('total')).where(self.model.is_delete == False)
        sql = self.add_filter_condition(sql, v_options, v_join_query, v_or, **kwargs)
        queryset = await self.db.execute(sql)
        return queryset.one()['total']

    async def create_data(
            self,
            data,
            v_options: list = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ):
        """
        创建数据
        :param data: 要插入的数据，可以是字典或数据模型对象。
        :param v_options: 列表类型，表示使用select在预加载中加载给定的属性。
        :param v_return_obj: 布尔类型，表示是否返回对象。
        :param v_schema: 指定使用的序列化对象。
        :return:
        代码解释：
        首先，该方法判断传入的data参数是否为字典类型，
        如果是则直接将其作为模型的构造函数的参数创建数据模型对象，
        否则通过调用dict()方法将数据模型对象转换为字典类型，并使用该字典作为参数创建数据模型对象。
        """
        if isinstance(data, dict):
            obj = self.model(**data)
        else:
            obj = self.model(**data.dict())
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
        :param data_id: 要更新的记录的ID。
        :param data: 包含新数据的对象。
        :param v_options: 列表类型，表示使用select在预加载中加载给定的属性。
        :param v_return_obj: 布尔类型，表示是否返回对象。
        :param v_schema: 指定使用的序列化对象。
        :return:
        代码解释：
        首先，该方法调用get_data()方法获取指定ID的记录对象。
        然后将传入的新数据对象转换为可序列化的JSON格式，并通过循环遍历将其所有属性值都赋值给旧记录对象的对应属性。
        接着调用flush()方法将修改后的对象提交到数据仓库进行更新，并等待操作完成。
        最后使用out_dict()方法将修改后的对象转换为字典类型，如果传入参数v_return_obj为真，则直接返回修改后的对象；
        否则，返回转换后的字典。
        """
        obj = await self.get_data(data_id, v_options=v_options)
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def delete_datas(
            self,
            ids: List[int],
            v_soft: bool = False,
            **kwargs
    ):
        """
        删除多条数据
        :param ids: 记录的id列表
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        :return:
        代码解释：
        在该方法中，首先判断是否启用软删除。如果启用，将使用update()函数更新ORM模型对象，将delete_datetime和is_delete字段分别设置为当前日期和时间和True。
        如果未启用软删除，则使用delete()函数直接从数据库中删除记录。
        最后通过异步执行的方式将修改操作提交到数据库中，完成删除操作。
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

    def add_filter_condition(
            self,
            sql: select,
            v_options: list = None,
            v_join_query: dict = None,
            v_or: List[tuple] = None,
            **kwargs
    ) -> select:
        """
        添加过滤条件，以及内连接过滤条件
        :param sql:
        :param v_options: 使用select在预加载中加载给定的属性
        :param v_join_query: 外键字段查询，内连接
        :param v_or: 或 逻辑查询
        :param kwargs: 关键字参数
        :return:
        """
        v_join: Set[str] = set()
        v_join_left: Set[str] = set()
        if v_join_query:
            for key, value in v_join_query.items():
                foreign_key = self.key_models.get(key)
                conditions = []
                self.__dict_filter(conditions, foreign_key.get("model"), **value)
                if conditions:
                    sql = sql.where(*conditions)
                    v_join.add(key)
        if v_or:
            sql = self.__or_filter(sql, v_or, v_join_left, v_join)
        for item in v_join:
            foreign_key = self.key_models.get(item)
            # 当外键模型在查询模型中存在多个外键时，则需要添加onclause属性
            sql = sql.join(foreign_key.get("model"), onclause=foreign_key.get("onclause"))
        for item in v_join_left:
            foreign_key = self.key_models.get(item)
            # 当外键模型在查询模型中存在多个外键时，则需要添加onclause属性
            sql = sql.outerjoin(foreign_key.get("model"), onclause=foreign_key.get("onclause"))
        conditions = []
        self.__dict_filter(conditions, self.model, **kwargs)
        if conditions:
            sql = sql.where(*conditions)
        if v_options:
            sql = sql.options(*[load for load in v_options])
        return sql

    def __or_filter(
            self,
            sql: select,
            v_or: List[tuple],
            v_join_left: Set[str],
            v_join: Set[str]
    ):
        """
        或 逻辑操作
        :param sql:
        :param v_or: 或 逻辑查询
        :param v_join_left: 左连接
        :param v_join: 内连接
        :return:
        """
        or_list = []
        for item in v_or:
            if len(item) == 2:
                model = self.model
                condition = {item[0]: item[1]}
                self.__dict_filter(or_list, model, **condition)
            elif len(item) == 4 and item[0] == "fk":
                model = self.key_models.get(item[1]).get("model")
                condition = {item[2]: item[3]}
                conditions = []
                self.__dict_filter(conditions, model, **condition)
                if conditions:
                    or_list = or_list + conditions
                    v_join_left.add(item[1])
                    if item[1] in v_join:
                        v_join.remove(item[1])
            else:
                raise CustomException(msg="v_or 获取查询属性失败，语法错误！")
        if or_list:
            sql = sql.where(or_(i for i in or_list))
        return sql

    def __dict_filter(
            self,
            conditions: list,
            model,
            **kwargs
    ):
        """
        字典过滤
        :param conditions: 列表类型，表示待构造的查询条件列表。
        :param model: ORM模型对象，表示要查询的数据表对应的ORM模型对象。
        :param kwargs: 表示以字段名为键，查询条件为值的关键字参数。
        :return:
        代码解释：
        定义了一个私有方法__dict_filter()，用于根据输入的关键字参数kwargs生成ORM查询条件列表。
        首先遍历关键字参数kwargs，依次处理每个键值对。
        如果该值不为空并且非空字符串，则通过ORM模型对象以属性名获取查询字段，并在检查元组是否为单元素元组（即只有一个查询条件）的前提下对查询条件进行解析：
        如果元组的第一个元素为"None"，则调用is_()方法将其与该字段进行比较，判断其是否为None；
        如果元组的第一个元素为"not None"，则调用isnoe()方法将其与该字段进行比较，判断其是否不为None；

        如果元组的长度为2且第二个元素不为空、非空列表或非空字符串，
        则根据第一个元素指定的查询条件类型构造查询条件，
        比如"date"表示按日期查询，"like"表示模糊匹配查询，"in"表示在指定列表中查询，"between"表示指定区间查询等等；
        否则，将该字段设为指定的值。
        最后将构造好的查询条件加入conditions列表中，并返回该列表。
        注意：该方法只能对"="、"!="、">"等简单的查询条件进行处理
        """
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
                        else:
                            raise CustomException("SQL查询语法错误")
                else:
                    conditions.append(attr == value)

    async def flush(
            self,
            obj: Any = None
    ):
        """
        将ORM模型对象或所有待刷新的对象刷新到数据库中
        :param obj:
        :return:
        代码解释：
        首先判断传入的参数是否为空，如果不为空，则调用self.db.add()方法将该ORM模型对象添加到会话中；否则表示要刷新所有待刷新的ORM模型对象，无需执行该步骤
        接下来，通过调用异步方法self.db.flush()将所有待刷新的ORM模型对象进行刷新，即将其同步到数据库中。
        最后，如果传入参数obj不为空，则使用self.db.refresh()方法从数据库重新加载该ORM模型对象的数据，并将其返回。
        """
        if obj:
            self.db.add(obj)
        await self.db.flush()
        if obj:
            await self.db.refresh(obj)

    async def out_dict(
            self,
            obj: Any,
            v_options: List = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ):
        """
        序列化
        :param obj: 序列化的ORM模型对象
        :param v_options: 列表类型，使用select在预加载中加载给定的属性
        :param v_return_obj: 布尔类型，是否返回对象本身，而不是将其序列化为字典
        :param v_schema: 使用的序列化对象
        :return:
        代码解释：
        方法内部首先根据传入的参数v_options，通过调用get_data()方法来预加载指定属性。
        在此之后，如果传入参数v_return_obj为真，则直接返回原始的ORM模型对象。否则，通过判断是否传入了v_schema参数来选择要使用的序列化对象。
        如果有指定序列化对象，则调用其from_orm()方法将ORM模型对象转换为对应的Pydantic模型对象，并使用dict()方法将其转换为Python字典；
        否则使用默认的self.schema进行序列化，并同样使用dict()方法将其转换为Python字典。
        """
        if v_options:
            obj = await self.get_data(obj.id, v_options=v_options)
        if v_return_obj:
            return obj
        if v_schema:
            return v_schema.from_orm(obj).dict()
        return self.schema.from_orm(obj).dict()
