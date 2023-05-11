#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    : 帮助中心--增删改查
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession
from core.crud import DalBase
from . import models, schemas

"""
代码解释：
首先，通过导入AsyncSession类和DalBase基类，定义了IssueDal和IssueCategoryDal两个Dal类。
这些类分别对应了问题和问题分类两个数据表，在数据库操作时可以用作中间层，简化对数据库的操作。
在IssueDal类中，定义了一个add_view_number方法，用于更新指定问题的浏览次数。
该方法使用get_data方法获取指定问题的详细信息，并将浏览次数加一后重新保存到数据库中。
其中，使用了models和schemas模块中的相关类来表示数据库表结构和Pydantic模型结构。
在IssueCategoryDal类中，同样使用了models和schemas模块中的相关类来表示问题分类的数据库表结构和Pydantic模型结构。
在类的构造方法中，通过调用super()方法调用了基类的构造方法，实现了重复使用DalBase中已有的通用操作方法。
"""


class IssueDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(IssueDal, self).__init__(db, models.VadminIssue, schemas.IssueSimpleOut)

    async def add_view_number(self, data_id: int):
        """
        更新常见问题查看次数+1
        """
        obj = await self.get_data(data_id)
        obj.view_number = obj.view_number + 1 if obj.view_number else 1
        await self.flush(obj)
        return True


class IssueCategoryDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(IssueCategoryDal, self).__init__(db, models.VadminIssueCategory, schemas.IssueCategorySimpleOut)
