"""
@Project : Sakura_K
@File    : crud.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/8/25 17:36
@Desc    : 
"""
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import DalBase
from . import models, schemas


class ImagesDal(DalBase):
    def __init__(self, db: AsyncSession):
        super(ImagesDal, self).__init__(db, models.VadminImages, schemas.ImagesSimpleOut)
