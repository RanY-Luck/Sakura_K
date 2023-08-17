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
代码解释：
定义了两个数据访问层（DAL）的类，LoginRecordDal 和 SMSSendRecordDal，它们都继承了一个名为 DalBase 的基础类。
这里的 DAL 类提供了对于数据库的访问和操作。其中，LoginRecordDal 类提供了获取用户登录分布情况的方法
get_user_distribute，SMSSendRecordDal 类没有提供任何其他方法。
在初始化 LoginRecordDal 和 SMSSendRecordDal 实例时，它们都需要传入一个 AsyncSession 类型的参数 db，表示当前的异步数据库会话。
这个 db 参数会被传递给基础类 DalBase 的构造函数，用于构造 DAL 实例中的查询和操作。
LoginRecordDal 和 SMSSendRecordDal 类中的 super() 调用都会调用基础类 DalBase 的构造函数，
并传递三个参数：db、对应的 SQLAlchemy 模型类（models.VadminLoginRecord 和 models.VadminSMSSendRecord）
和对应的 Pydantic 模型类（schemas.LoginRecordSimpleOut 和 schemas.SMSSendRecordSimpleOut）。这些参数会在基础类中用于构造查询和操作。
在 LoginRecordDal 中，get_user_distribute 方法会返回一个包含了用户登录分布情况的列表。
这个列表中每个元素都是一个字典，包含了城市的名称（name）、中心点经纬度坐标（center）和登录总数（total）。
其中，登录总数是使用 random.randint() 方法随机生成的一个整数。
"""
import random

# sqlalchemy 查询操作：https://segmentfault.com/a/1190000016767008
# sqlalchemy 关联查询：https://www.jianshu.com/p/dfad7c08c57a
# sqlalchemy 关联查询详细：https://blog.csdn.net/u012324798/article/details/103940527
from motor.motor_asyncio import AsyncIOMotorDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from core.mongo_manage import MongoManage
from . import models, schemas


class LoginRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(LoginRecordDal, self).__init__(db, models.VadminLoginRecord, schemas.LoginRecordSimpleOut)

    async def get_user_distribute(self) -> list[dict]:
        """
        获取用户登录分布情况
        高德经纬度查询：https://lbs.amap.com/tools/picker

        {
            name: '北京',
            center: [116.407394, 39.904211],
            total: 20
        }

        :return: List[dict]
        """
        result = [{
            "name": '北京',
            "center": [116.407394, 39.904211],
        },
            {
                "name": '重庆',
                "center": [106.551643, 29.562849],
            },
            {
                "name": '郑州',
                "center": [113.778584, 34.759197],
            },
            {
                "name": '南京',
                "center": [118.796624, 32.059344],
            },
            {
                "name": '武汉',
                "center": [114.304569, 30.593354],
            },
            {
                "name": '乌鲁木齐',
                "center": [87.616824, 43.825377],
            },
            {
                "name": '新乡',
                "center": [113.92679, 35.303589],
            }]
        for data in result:
            assert isinstance(data, dict)
            data["total"] = random.randint(2, 80)
        return result


class SMSSendRecordDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(SMSSendRecordDal, self).__init__(db, models.VadminSMSSendRecord, schemas.SMSSendRecordSimpleOut)


class OperationRecordDal(MongoManage):

    def __init__(self, db: AsyncIOMotorDatabase):
        super(OperationRecordDal, self).__init__(db, "operation_record", schemas.OperationRecordSimpleOut)
