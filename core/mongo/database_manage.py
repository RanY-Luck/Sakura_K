# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2023/4/11 11:24
# # @Author  : 冉勇
# # @Site    :
# # @File    : database_manage.py
# # @Software: PyCharm
# # @desc    : 数据库管理
# from abc import abstractmethod  # 用于定义抽象方法
# from typing import Any
#
#
# class DatabaseManage:
#     """
#     ./mongo_manage.py 这将是到mongodb的实际连接。
#     """
#
#     @property
#     def client(self):
#         raise NotImplementedError
#
#     @property
#     def db(self):
#         raise NotImplementedError
#
#     # 数据库连接和关闭连接
#     @abstractmethod
#     async def connect_to_database(self, path: str, db_name: str):
#         pass
#
#     @abstractmethod
#     async def close_database_connection(self):
#         pass
#
#     @abstractmethod
#     async def create_data(self, collection: str, data: dict):
#         pass
#
#     @abstractmethod
#     async def get_datas(
#             self, collection: str, page: int = 1, limit: int = 10, v_schema: Any = None, v_order: str = None,
#             v_order_field: str = None, **kwargs
#     ):
#         """
#         即查询数据库数据的方法，并且根据该方法的传入参数限定了查询的范围和方式。
#         :param collection: 指定要操作的数据集合；
#         :param page: 指定数据查询的页数，默认为1；
#         :param limit: 指定每页查询的数据条数，默认为10；
#         :param v_schema: 指定查询的条件筛选器；
#         :param v_order: 指定排序方式；
#         :param v_order_field: 指定排序字段；
#         :param kwargs: 其他可选参数。
#         :return:
#         """
#         pass
#
#     @abstractmethod
#     async def get_count(self, collection: str, **kwargs) -> int:
#         pass
from abc import abstractmethod
from typing import Any


class DatabaseManage:
    """
    This class is meant to be extended from
    ./mongo_manage.py which will be the actual connection to mongodb.
    """

    @property
    def client(self):
        raise NotImplementedError

    @property
    def db(self):
        raise NotImplementedError

    # database connect and close connections
    @abstractmethod
    async def connect_to_database(self, path: str, db_name: str):
        pass

    @abstractmethod
    async def close_database_connection(self):
        pass

    @abstractmethod
    async def create_data(self, collection: str, data: dict):
        pass

    @abstractmethod
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
        pass

    @abstractmethod
    async def get_count(self, collection: str, **kwargs) -> int:
        pass
