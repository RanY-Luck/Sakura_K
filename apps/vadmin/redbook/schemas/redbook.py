"""
@Project : Sakura_K
@File    : redbook.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/10/13 11:00
@Desc    : 
"""
from pydantic import BaseModel, ConfigDict


class RedBookImages(BaseModel):
    noteurl: str
    notetype: str | None = None
    notetitle: str
    notedescription: str | None = None
    notetags: str | None = None
    filename: str | None = None
    image_url: str | None = None


class RedBookImagesOut(RedBookImages):
    model_config = ConfigDict(from_attributes=True)
