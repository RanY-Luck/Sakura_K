#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    : 数据库 增删改查操作
"""
sqlalchemy 查询操作：https://segmentfault.com/a/1190000016767008
sqlalchemy 关联查询：https://www.jianshu.com/p/dfad7c08c57a
sqlalchemy 关联查询详细：https://blog.csdn.net/u012324798/article/details/103940527
"""
import json
import os
from enum import Enum
from typing import Any

from aioredis import Redis
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from application.settings import STATIC_ROOT, SUBSCRIBE
from core.crud import DalBase
from core.exception import CustomException
from core.mongo.mongo_manage import MongoManage
from utils import status
from utils.file.file_manage import FileManage
from . import models, schemas


class DictTypeDal(DalBase):
    """
    代码解释：
    定义了一个DictTypeDal类，该类继承自DalBase类。其中DalBase是一个基础数据访问层类，用于实现对数据库表的基本增删改查操作。
    DictTypeDal类重写了父类的__init__()方法，并在其中调用了父类的__init__()方法。
    该方法需要传入三个参数：db（AsyncSession对象）、models.VadminDictType（ORM模型类）和schemas.DictTypeSimpleOut（Pydantic模型类）。
    这意味着DictTypeDal类可以通过父类提供的方法，访问名为VadminDictType的数据表，并使用DictTypeSimpleOut模型类来映射数据表中的数据。
    """

    def __init__(self, db: AsyncSession):
        super(DictTypeDal, self).__init__(db, models.VadminDictType, schemas.DictTypeSimpleOut)

    async def get_dicts_details(self, dict_types: list[str]) -> dict:
        """
        获取多个字典类型下的字典元素列表
        :param dict_types:
        :return:
        代码解释：
        用于获取多个字典类型下的字典元素列表。
        该方法首先使用DictTypeDal类的get_datas()方法查询出指定字典类型的所有记录，同时设置v_options参数，使其能够关联查询出与字典类型相关联的所有字典详情数据。
        然后遍历查询结果，将每个字典类型对应的字典详情数据封装成字典格式返回。
        """
        data = {}
        options = [joinedload(self.model.details)]
        objs = await DictTypeDal(self.db).get_datas(
            limit=0,
            v_return_objs=True,
            v_options=options,
            dict_type=("in", dict_types)
        )
        for obj in objs:
            if not obj:
                data[obj.dict_type] = []
                continue
            else:
                data[obj.dict_type] = [schemas.DictDetailsSimpleOut.model_validate(i).model_dump() for i in obj.details]
        return data

    async def get_select_datas(self):
        """
        获取所有字典类型的选择数据
        :return:
        代码解释：
        用于获取所有字典类型的选择数据，返回值是一个由字典类型信息组成的列表。
        在该方法中，使用select()方法查询出所有字典类型记录，并使用from_orm()方法将查询结果转换为DictTypeSelectOut类的实例，最后使用dict()方法将实例转为字典格式并添加到列表中。
        """
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.DictTypeSelectOut.model_validate(i).model_dump() for i in queryset.scalars().all()]


class DictDetailsDal(DalBase):
    """
    代码解释：
    定义了一个DictDetailsDal类，该类继承自DalBase类。其中DalBase是一个基础数据访问层类，用于实现对数据库表的基本增删改查操作。
    DictDetailsDal类重写了父类的__init__()方法，并在其中调用了父类的__init__()方法。
    该方法需要传入三个参数：db（AsyncSession对象）、models.VadminDictDetails（ORM模型类）和schemas.DictDetailsSimpleOut（Pydantic模型类）。
    这意味着DictDetailsDal类可以通过父类提供的方法，访问名为VadminDictDetails的数据表，并使用DictDetailsSimpleOut模型类来映射数据表中的数据。
    """

    def __init__(self, db: AsyncSession):
        super(DictDetailsDal, self).__init__(db, models.VadminDictDetails, schemas.DictDetailsSimpleOut)


class SettingsDal(DalBase):
    """
    代码解释：
    定义了一个SettingsDal类，该类继承自DalBase类。其中DalBase是一个基础数据访问层类，用于实现对数据库表的基本增删改查操作。
    SettingsDal类重写了父类的__init__()方法，并在其中调用了父类的__init__()方法。
    该方法需要传入三个参数：db（AsyncSession对象）、models.VadminSystemSettings（ORM模型类）和schemas.SettingsSimpleOut（Pydantic模型类）。
    这意味着SettingsDal类可以通过父类提供的方法，访问名为VadminSystemSettings的数据表，并使用SettingsSimpleOut模型类来映射数据表中的数据。
    还定义了一个异步方法get_tab_values()，用于获取系统配置标签下的信息。
    该方法接受一个整型参数tab_id，指定要查询的系统配置标签ID。
    首先，该方法调用父类的get_datas()方法查询指定标签下的所有记录，并设置v_return_objs参数为True以返回ORM对象列表。
    然后遍历查询结果列表，将每一条记录的config_key字段作为字典的键，config_value字段作为字典的值，组成一个字典。
    注意到在遍历过程中，只有当disabled字段值为False时，对应记录的键值才会被添加到字典中。最后，将组成的字典返回给调用方。
    此外，还提供了其他的方法，如 update_datas() 和 get_base_config()。
    update_datas() 方法用于更新系统配置信息，该方法的输入参数 datas 是一个字典类型，存储了需要更新的配置项及其对应的值。
    通过遍历 datas 字典，将每一个配置项的值写入系统配置表中。
    如果更新的配置项是 web_ico_local_path，则对应的配置值需要将上传的 ico 文件路径替换到 static/system/favicon.ico 文件中。
    get_base_config() 方法用于获取系统基本信息（不包含敏感信息），忽略了wx_server_app_id和wx_server_app_secret两个配置项，并返回结果字典给调用方。
    """

    def __init__(self, db: AsyncSession):
        super(SettingsDal, self).__init__(db, models.VadminSystemSettings, schemas.SettingsSimpleOut)

    async def get_tab_values(self, tab_id: int) -> dict:
        """
        获取系统配置标签下的信息
        :param tab_id:
        :return:
        """
        datas = await self.get_datas(limit=0, tab_id=tab_id, v_return_objs=True)
        result = {}
        for data in datas:
            if not data.disabled:
                result[data.config_key] = data.config_value
        return result

    async def update_datas(self, datas: dict, rd: Redis):
        """
        更新系统配置信息
        :param datas:
        :param rd:
        :return:
        """
        for key, value in datas.items():
            if key == "web_ico":
                continue
            elif key == "web_ico_local_path":
                if not value:
                    continue
                ico = await self.get_data(config_key="web_ico", tab_id=1)
                web_ico = datas.get("web_ico")
                if ico.config_value == web_ico:
                    continue
                # 将上传的ico路径替换到static/system/favicon.ico文件
                await FileManage.async_copy(value, os.path.join(STATIC_ROOT, "system/favicon.ico"))
                sql = update(self.model).where(self.model.config_key == "web_ico").values(config_value=web_ico)
                await self.db.execute(sql)
            else:
                sql = update(self.model).where(self.model.config_key == key).values(config_value=value)
                await self.db.execute(sql)
        if "wx_server_app_id" in datas:
            await rd.client().set("wx_server", json.dumps(datas))

    async def get_base_config(self):
        """
        获取系统基本信息
        :return:
        """
        ignore_configs = ["wx_server_app_id", "wx_server_app_secret"]
        datas = await self.get_datas(limit=0, tab_id=("in", ["1", "9"]), disabled=False, v_return_objs=True)
        result = {}
        for config in datas:
            if config.config_key not in ignore_configs:
                result[config.config_key] = config.config_value
        return result


class SettingsTabDal(DalBase):
    """
    代码解释：
    定义了一个SettingsTabDal类，该类是一个数据访问层（DAL）类，用于操作名为VadminSystemSettingsTab的数据表，实现了对该数据表的增、删、改、查等基本操作。
    在__init__()方法中，该类继承自基类DalBase，并在初始化时传入了三个参数：db、models.VadminSystemSettingsTab和schemas.SettingsTabSimpleOut。
    其中，db参数是AsyncSession对象（异步数据库会话对象），models.VadminSystemSettingsTab是ORM模型类（定义了数据表的结构），schemas.SettingsTabSimpleOut是Pydantic模型类（定义了数据表的字段类型）。
    该类通过get_classify_tab_values()方法实现了获取系统配置分类下所有标签信息的功能。
    该方法接收两个参数：classify（字符串列表类型）和hidden（布尔类型或None）。
    在查询时根据这两个参数来指定要查询的系统配置分类和是否包含隐藏的标签。
    首先，通过调用父类DalBase中封装的get_datas()方法来获取指定分类下的所有数据记录（注意到该方法设置了参数limit=0表示获取所有数据记录，参数v_return_objs=True表示返回ORM对象列表）。
    然后，利用for循环遍历每一条数据记录，将disabled字段值为False的数据记录的config_key作为键，config_value作为值，组成一个字典并返回给调用方。
    另外，该类还提供了get_tab_name_value()方法，其作用和get_classify_tab_values()类似，只是根据标签名获取相应的标签信息，而不是根据分类。
    该方法也接收两个参数：tab_names（字符串列表类型）和hidden（布尔类型或None）。
    同样地，该方法调用了父类DalBase中的get_datas()方法来获取指定标签名下的所有数据记录，然后调用generate_values()方法将数据转化为一个字典并返回给调用方。
    最后，generate_values()是一个静态方法，作用是将包含标签信息的ORM对象列表转化为一个嵌套字典结构，其中每个键代表一个标签名，对应的值是该标签下的所有配置项及其对应的值（如果该配置项被禁用，则不包含在字典中）。
    """

    def __init__(self, db: AsyncSession):
        super(SettingsTabDal, self).__init__(db, models.VadminSystemSettingsTab, schemas.SettingsTabSimpleOut)

    async def get_classify_tab_values(self, classify: list[str], hidden: bool | None = False):
        """
        获取系统配置分类下的标签信息
        :param classify:
        :param hidden:
        :return:
        """
        model = models.VadminSystemSettingsTab
        options = [joinedload(model.settings)]
        datas = await self.get_datas(
            limit=0,
            v_options=options,
            classify=("in", classify),
            disabled=False,
            v_return_objs=True,
            hidden=hidden
        )
        return self.generate_values(datas)

    async def get_tab_name_values(self, tab_names: list[str], hidden: bool | None = False):
        """
        获取系统配置标签下的标签信息
        :param tab_names:
        :param hidden:
        :return:
        """
        model = models.VadminSystemSettingsTab
        options = [joinedload(model.settings)]
        datas = await self.get_datas(
            limit=0,
            v_options=options,
            tab_name=("in", tab_names),
            disabled=False,
            v_return_objs=True,
            hidden=hidden
        )
        return self.generate_values(datas)

    @classmethod
    def __generate_values(cls, datas: list[models.VadminSystemSettingsTab]):
        """
        生成字典值
        """
        return {
            tab.tab_name: {
                item.config_key: item.config_value
                for item in tab.settings
                if not item.disabled
            }
            for tab in datas
        }


class TaskDal(MongoManage):
    class JobOperation(Enum):
        add = "add_job"

    def __init__(self, db: AsyncIOMotorDatabase):
        super(TaskDal, self).__init__(db, "vadmin_system_task", schemas.TaskSimpleOut)

    async def get_task(
            self, _id: str = None,
            v_return_none: bool = False,
            v_schema: Any = None,
            **kwargs
    ) -> dict | None:
        """
        获取单个数据，默认使用ID查询，否则使用关键词查询
       包括临时字段 last_run_datetime，is_active
        is_active: 只有在 scheduler_task_jobs 任务运行表中存在相同 _id 才表示任务添加成功，任务状态才为 True
        last_run_datetime: 在 scheduler_task_record 中获取该任务最近一次执行完成的时间
        :param _id: 数据ID
        :param v_return_none: 是否返回空None，否则抛出异常，默认抛出异常
        :param v_schema: 指定使用序列化对象
        :param kwargs:
        :return:
        """
        if _id:
            kwargs["_id"] = ("objectId", _id)
        params = self.filter_condition(**kwargs)
        pipeline = [
            {
                '$addFields': {
                    'str_id': {'$toString': '$_id'}
                }
            },
            {
                '$lookup': {
                    'from': 'scheduler_task_jobs',
                    'localField': 'str_id',
                    'foreignField': '_id',
                    'as': 'matched_jobs'
                }
            },
            {
                '$lookup': {
                    'from': 'scheduler_task_record',
                    'localField': 'str_id',
                    'foreignField': 'job_id',
                    'as': 'matched_records'
                }
            },
            {
                '$addFields': {
                    'is_active': {
                        '$cond': {
                            'if': {'$ne': ['$matched_jobs', []]},
                            'then': True,
                            'else': False
                        }
                    },
                    'last_run_datetime': {
                        '$ifNull': [
                            {'$arrayElemAt': ['$matched_records.create_datetime', -1]},
                            None
                        ]
                    }
                }
            },
            {
                '$project': {
                    'matched_records': 0,
                    'matched_jobs': 0
                }
            },
            {
                '$match': params
            },
            {
                '$facet': {
                    'documents': [
                        {'$limit': 1},
                    ]
                }
            }
        ]
        # 执行聚合查询
        cursor = self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
        data = result[0]['documents']
        if not data and v_return_none:
            return None
        elif not data:
            raise CustomException("未查到对应数据", code=status.HTTP_404_NOT_FOUND)
        data = data[0]
        if data and v_schema:
            return jsonable_encoder(v_schema(**data))
        return data

    async def get_tasks(
            self, page: int = 1, limit: int = 10, v_schema: Any = None, v_order: str = None, v_order_field: str = None,
            **kwargs
    ):
        """
        获取任务信息列表
       添加了两个临时字段
         is_active: 只有在 scheduler_task_jobs 任务运行表中存在相同 _id 才表示任务添加成功，任务状态才为 True
         last_run_datetime: 在 scheduler_task_record 中获取该任务最近一次执行完成的时间
        :param page:
        :param limit:
        :param v_schema:
        :param v_order:
        :param v_order_field:
        :param kwargs:
        :return:
        """
        v_order_field = v_order_field if v_order_field else "create_datetime"
        v_order = -1 if v_order in self.ORDER_FIELD else 1
        params = self.filter_condition(**kwargs)
        pipeline = [
            {
                '$addFields': {
                    'str_id': {'$toString': '$_id'}
                }
            },
            {
                '$lookup': {
                    'from': 'scheduler_task_jobs',
                    'localField': 'str_id',
                    'foreignField': '_id',
                    'as': 'matched_jobs'
                }
            },
            {
                '$lookup': {
                    'from': 'scheduler_task_record',
                    'localField': 'str_id',
                    'foreignField': 'job_id',
                    'as': 'matched_records'
                }
            },
            {
                '$addFields': {
                    'is_active': {
                        '$cond': {
                            'if': {'$ne': ['$matched_jobs', []]},
                            'then': True,
                            'else': False
                        }
                    },
                    'last_run_datetime': {
                        '$ifNull': [
                            {'$arrayElemAt': ['$matched_records.create_datetime', -1]},
                            None
                        ]
                    }
                }
            },
            {
                '$project': {
                    'matched_records': 0,
                    'matched_jobs': 0
                }
            },
            {
                '$match': params
            },
            {
                '$facet': {
                    'documents': [
                        {'$sort': {v_order_field: v_order}},
                        {'$limit': limit},
                        {'$skip': (page - 1) * limit}
                    ],
                    'count': [{'$count': 'total'}]
                }
            }
        ]
        # 执行聚合查询
        cursor = self.collection.aggregate(pipeline)
        result = await cursor.to_list(length=None)
        datas = result[0]['documents']
        count = result[0]['count'][0]['total'] if result[0]['count'] else 0
        if count == 0:
            return [], 0
        elif v_schema:
            datas = [jsonable_encoder(v_schema(**datas)) for data in datas]
        elif self.schema:
            datas = [jsonable_encoder(self.schema(**data)) for data in datas]
        return datas, count

    async def add_task(self, rd: Redis, data: dict) -> int:
        """
        添加任务到消息队列
        使用消息无保留策略：无保留是指当发送者向某个频道发送消息时，如果没有订阅该频道的调用方，就直接将该消息丢弃。
        :param rd: redis对象
        :param data: 行数据字典
        :return: 接收到消息的订阅者数量
        """
        exec_strategy = data.get("exec_strategy")
        job_params = {
            "name": data.get("_id"),
            "job_class": data.get("job_class"),
            "expression": data.get("expression")
        }
        if exec_strategy == "interval" or exec_strategy == "cron":
            job_params["start_data"] = data.get("start_data")
            job_params["end_data"] = data.get("end_data")
        message = {
            "operation": self.get("exec_strategy"),
            "task": {
                "exec_strategy": data.get("exec_strategy"),
                "job_params": job_params
            }
        }
        return await rd.publish(SUBSCRIBE, json.dumps(message).encode("utf-8"))

    async def create_task(self, rd: Redis, data: schemas.Task) -> dict:
        """
        创建任务
        :param rd:
        :param data:
        :return:
        """
        data_dict = data.model_dump()
        is_active = data_dict.pop("is_active")
        insert_result = await super().create_data(data_dict)
        obj = await self.get_task(insert_result.inserted_id, v_schema=schemas.TaskSimpleOut)
        # 如果分组不存在则新增分组
        group = await TaskGroupDal(self.db).get_data(value=data.group, v_return_none=True)
        if not group:
            await TaskGroupDal(self.db).create_data({"value": data.group})
        result = {
            "subscribe_number": 0,
            "is_active": is_active
        }
        if is_active:
            # 创建任务成功后，如果任务状态为True，则向消息队列中发送任务
            result['subscribe_number'] = await self.add_task(rd, obj)
        return result

    async def put_task(self, rd: Redis, _id: str, data: schemas.Task) -> dict:
        """
        更新任务
        :param rd:
        :param _id:
        :param data:
        :return:
        """
        data_dict = data.model_dump()
        is_active = data_dict.pop(_id, data)
        await super(TaskDal, self).put_data(_id, data)
        obj: dict = await self.get_task(_id, v_schema=schemas.TaskSimpleOut)
        # 如果分组不存在则新增分组
        group = await TaskGroupDal(self.db).get_data(value=data.group, v_return_none=True)
        if not group:
            await TaskGroupDal(self.db).create_data({"value": data.group})
        try:
            # 删除正在运行的Job
            await SchedulerTaskJobsDal(self.db).delete_data(_id)
        except CustomException as e:
            pass
        result = {
            "subscribe_number": 0,
            "is_active": is_active
        }
        if is_active:
            # 更新任务成功后, 如果任务状态为 True，则向消息队列中发送任务
            result["subscribe_number"] = await self.add_task(rd, obj)
        return result

    async def delete_task(self, _id: str) -> bool:
        """
        删除任务
        :param _id:
        :return:
        """
        result = await super(TaskDal, self).delete_data(_id)
        try:
            # 删除正在运行的Job
            await SchedulerTaskJobsDal(self.db).delete_data(_id)
        except CustomException as e:
            pass
        return result

    async def run_once_task(self, rd: Redis, _id: str) -> int:
        """
        执行一次任务
        :param rd:
        :param _id:
        :return:
        """
        obj: dict = await self.get_data(_id, v_schema=schemas.TaskSimpleOut)
        message = {
            "operation": self.JobOperation.add.value,
            "task": {
                "exec_strategy": "once",
                "job_params": {
                    "name": obj.get("_id"),
                    "job_class": obj.get("job_class")
                }
            }
        }
        return await rd.publish(SUBSCRIBE, json.dumps(message).encode("utf-8"))


class TaskGroupDal(MongoManage):
    def __init__(self, db: AsyncIOMotorDatabase):
        super(TaskGroupDal, self).__init__(db, "vadmin_system_task_group")


class TaskRecordDal(MongoManage):
    def __init__(self, db: AsyncIOMotorDatabase):
        super(TaskRecordDal, self).__init__(db, "scheduler_task_record")


class SchedulerTaskJobsDal(MongoManage):
    def __init__(self, db: AsyncIOMotorDatabase):
        super(SchedulerTaskJobsDal, self).__init__(db, "scheduler_task_jobs", is_object_id=False)
