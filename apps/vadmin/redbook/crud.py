"""
@Project : Sakura_K
@File    : crud.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/10/13 10:45
@Desc    : 增删改查逻辑1
"""
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from . import models, schemas


class RedBookDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(RedBookDal, self).__init__(db, models.VadminRedBook, schemas.RedBookImagesOut)
