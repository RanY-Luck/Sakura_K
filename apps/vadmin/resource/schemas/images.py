"""
@Project : Sakura_K
@File    : images.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/8/28 16:23
@Desc    : 
"""
from pydantic import BaseModel, ConfigDict

from apps.vadmin.auth.schemas import UserSimpleOut
from core.data_types import DatetimeStr


class Images(BaseModel):
    filename: str
    image_url: str
    create_user_id: int


class ImagesSimpleOut(Images):
    model_config = ConfigDict(from_attributes=True)
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr


class ImagesOut(ImagesSimpleOut):
    model_config = ConfigDict(from_attributes=True)
    create_user: UserSimpleOut
