#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 14:37
# @File           : redbook.py
# @IDE            : PyCharm
# @desc           : pydantic 模型，用于数据库序列化操作
from typing import Optional, List

from pydantic import BaseModel, ConfigDict, Field

from core.data_types import DatetimeStr


class Redbook(BaseModel):
    source: str = Field(..., title="原文地址")
    tags: str = Field(..., title="标签")
    title: str = Field(..., title="作品标题")
    describe: str = Field(..., title="作品描述")
    type: str = Field(..., title="作品类型")
    affiliation: str = Field(..., title="ID归属地")
    release_time: DatetimeStr = Field(..., title="发布时间")
    auth_name: str = Field(..., title="作者昵称")
    is_active: bool = Field(True, title="是否可见")
    create_user_id: int = Field(..., title="创建人")


class RedbookSimpleOut(Redbook):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


class Urls(BaseModel):
    red_book_id: int = Field(..., title="关联表red_book.id")
    url: str = Field(..., title="下载地址")


class UrlsSimpleOut(Urls):
    model_config = ConfigDict(from_attributes=True)

    id: int = Field(..., title="编号")
    create_datetime: DatetimeStr = Field(..., title="创建时间")
    update_datetime: DatetimeStr = Field(..., title="更新时间")


# 需要写pydantic类型


class Links(BaseModel):
    """多个URL"""
    link: Optional[List[str]] = Field(..., description="多个链接，逗号分隔")


class RedBookConfig(BaseModel):
    work_path: str = ""  # 作品数据/文件保存根路径，默认值：项目根路径
    folder_name: str = "Download"  # 作品文件储存文件夹名称（自动创建），默认值：Download
    user_agent: str = ""  # 请求头 User-Agent
    cookie: str = ""  # 小红书网页版 Cookie，无需登录
    proxy: Optional[str] = None  # 网络代理
    timeout: int = 5  # 请求数据超时限制，单位：秒，默认值：10
    chunk: int = 1024 * 1024 * 10  # 下载文件时，每次从服务器获取的数据块大小，单位：字节
    max_retry: int = 5  # 请求数据失败时，重试的最大次数，单位：秒，默认值：5
    record_data: bool = True  # 是否记录作品数据至文件
    image_format: str = "PNG"  # 图文作品文件下载格式，支持：PNG、WEBP
    folder_mode: bool = True  # 是否将每个作品的文件储存至单独的文件夹
