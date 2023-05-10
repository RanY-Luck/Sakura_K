# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2023/4/11 14:32
# # @Author  : 冉勇
# # @Site    :
# # @File    : mongo_manage.py
# # @Software: PyCharm
# # @desc    : Mongo管理
# import json
# from typing import Any
# from bson.json_util import dumps
# from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
# from core.mongo import DatabaseManage
# from pymongo.results import InsertManyResult
#
#
# class MongoManage(DatabaseManage):
#     """
#     ./database_manage.py 从这里调用类
#     """
#     client: AsyncIOMotorClient = None
#     db: AsyncIOMotorDatabase = None
#
#     async def connect_to_database(self, path: str, db_name: str):
#         self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
#         self.db = self.client[db_name]
#
#     async def close_database_connection(self):
#         self.client.close()
#
#     async def create_data(self, collection: str, data: dict) -> InsertManyResult:
#         return await self.db[collection].insert_ont(data)
#
#     async def get_datas(
#             self, collection: str, page: int = 1, limit: int = 10, v_schema: Any = None, v_order: str = None,
#             v_order_field: str = None, **kwargs
#     ):
#         """
#         用于查询MongoDB数据库中的数据集合，并返回符合条件的数据。具体实现逻辑如下：
#         首先，根据传入的参数，构造出查询条件params，通过filter_condition方法实现。然后，使用collection指定要查询的数据集合，在该集合上执行find操作，得到一个游标对象cursor。
#         接着，对查询结果应用排序、跳过和限制等限制条件。其中sort方法表示排序方式，这里按照create_datetime字段进行降序排列，即最新的在前面；skip方法表示跳过多少条数据，即从当前查询结果的第(page - 1) * limit条开始查询；limit方法表示查询的数据条数，即查询limit条数据。
#         随后，使用async for迭代游标对象cursor，将每条查询结果追加到列表datas中，并使用json.loads和dumps方法转换成字典类型数据。
#         最后，如果指定了v_schema参数，则调用parse_obj方法将数据解析为v_schema指定的模型，并使用dict()方法将模型解析成字典格式返回。如果未指定v_schema参数，则直接将查询结果字典放入datas列表中返回。
#         :param collection:
#         :param page:
#         :param limit:
#         :param v_schema:
#         :param v_order:
#         :param v_order_field:
#         :param kwargs:
#         :return:
#         """
#         params = self.filter_condition(**kwargs)
#         cursor = self.db[collection].find(params)
#         # 对查询应用排序(sort)，跳过(skip)，限制(limit)
#         cursor.sort("create_datetime", -1).skip((page - 1) * limit).limit(limit)
#         datas = []
#         async for row in cursor:
#             del row['_id']
#             data = json.loads(dumps(row))
#             if v_schema:
#                 data = v_schema.parse_obj(data).dict()
#             datas.append(data)
#         return datas
#
#     async def get_count(self, collection: str, **kwargs) -> int:
#         params = self.filter_condition(**kwargs)
#         return await self.db[collection].count_documents(params)
#
#     @classmethod
#     def filter_condition(cls, **kwargs):
#         """
#         过滤条件
#         解释代码：
#         首先定义一个空字典params，用于存储查询参数。然后对传入的参数进行遍历，判断是否满足特定条件，并将符合要求的参数加入到params中。
#         在循环中，首先判断传入的值v是否存在，如果不存在，则继续下一个循环；如果存在，则判断v的数据类型是否为元组。如果是元组类型，则根据元组的第一个值确定查询方式。
#         若是like方式，则构造正则表达式，将该正则表达式作为查询条件加入到params中；
#         若是between方式，则按照区间筛选方式，将区间范围条件添加到params中。
#         如果传入的值不是元组类型，则直接将该参数及其值添加到params中即可。
#         最后返回完成后的查询参数params。
#         """
#         params = {}
#         for k, v in kwargs.items():
#             if not v:
#                 continue
#             elif isinstance(v, tuple):
#                 if v[0] == 'like' and v[1]:
#                     params[k] = {'$regex': v[1]}
#                 elif v[0] == 'between' and len(v[1]) == 2:
#                     params[k] = {'$gte': v[1][0], '$lt': v[1][0]}
#             else:
#                 params[k] = v
#         return params

import json
from typing import Any

from bson.json_util import dumps
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from core.mongo import DatabaseManage
from pymongo.results import InsertOneResult


class MongoManage(DatabaseManage):
    """
    This class extends from ./database_manage.py
    which have the abstract methods to be re-used here.
    博客：https://www.cnblogs.com/aduner/p/13532504.html
    mongodb 官网：https://www.mongodb.com/docs/drivers/motor/
    motor 文档：https://motor.readthedocs.io/en/stable/
    """

    client: AsyncIOMotorClient = None
    db: AsyncIOMotorDatabase = None

    async def connect_to_database(self, path: str, db_name: str):
        self.client = AsyncIOMotorClient(path, maxPoolSize=10, minPoolSize=10)
        self.db = self.client[db_name]

    async def close_database_connection(self):
        self.client.close()

    async def create_data(self, collection: str, data: dict) -> InsertOneResult:
        return await self.db[collection].insert_one(data)

    async def get_datas(
            self,
            collection: str,
            page: int = 1,
            limit: int = 10,
            v_schema: Any = None,
            v_order: str = None,
            v_order_field: str = None,
            **kwargs
    ):
        """
        使用 find() 要查询的一组文档。 find() 没有I / O，也不需要 await 表达式。它只是创建一个 AsyncIOMotorCursor 实例
        当您调用 to_list() 或为循环执行异步时 (async for) ，查询实际上是在服务器上执行的。
        """

        params = self.filter_condition(**kwargs)
        cursor = self.db[collection].find(params)

        # 对查询应用排序(sort)，跳过(skip)或限制(limit)
        cursor.sort("create_datetime", -1).skip((page - 1) * limit).limit(limit)

        datas = []
        async for row in cursor:
            del row['_id']
            data = json.loads(dumps(row))
            if v_schema:
                data = v_schema.parse_obj(data).dict()
            datas.append(data)
        return datas

    async def get_count(self, collection: str, **kwargs) -> int:
        params = self.filter_condition(**kwargs)
        return await self.db[collection].count_documents(params)

    @classmethod
    def filter_condition(cls, **kwargs):
        """
        过滤条件
        """
        params = {}
        for k, v in kwargs.items():
            if not v:
                continue
            elif isinstance(v, tuple):
                if v[0] == "like" and v[1]:
                    params[k] = {'$regex': v[1]}
                elif v[0] == "between" and len(v[1]) == 2:
                    params[k] = {'$gte': f"{v[1][0]} 00:00:00", '$lt': f"{v[1][1]} 23:59:59"}
            else:
                params[k] = v
        return params
