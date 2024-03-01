#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 14:37
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.dependencies import IdList
from utils.response import SuccessResponse
from utils.xhs.source import XHS
from . import schemas, crud, params, models
from .schemas import Links, RedBookConfig

app = APIRouter()


###########################################################
#                     小红书作品下载                        #
###########################################################

@app.post("/redbookdown", summary="获取小红书作品信息,支持单个下载")
async def getredbookdown(
        link: str = Query(..., description="小红书链接"),
        config: RedBookConfig = RedBookConfig(),
        auth: Auth = Depends(AllUserAuth())
):
    """获取小红书无水印文件,支持单个下载"""
    async with XHS(
            **config.model_dump()
    ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        data = await xhs.extract(link, download)
    return SuccessResponse(data=data)


@app.post("/redbookdownmultiple", summary="获取小红书作品信息,支持批量下载")
async def getredbookdownmultiple(
        links: Links,
        auth: Auth = Depends(AllUserAuth())
):
    """获取小红书无水印文件,支持批量下载"""
    multiple_links = " ".join(links.link or [])
    # 实例对象
    work_path = ""  # 作品数据/文件保存根路径，默认值：项目根路径
    folder_name = "Download"  # 作品文件储存文件夹名称（自动创建），默认值：Download
    user_agent = ""  # 请求头 User-Agent
    cookie = ""  # 小红书网页版 Cookie，无需登录
    proxy = None  # 网络代理
    timeout = 5  # 请求数据超时限制，单位：秒，默认值：10
    chunk = 1024 * 1024 * 10  # 下载文件时，每次从服务器获取的数据块大小，单位：字节
    max_retry = 5  # 请求数据失败时，重试的最大次数，单位：秒，默认值：5
    record_data = True  # 是否记录作品数据至文件
    image_format = "PNG"  # 图文作品文件下载格式，支持：PNG、WEBP
    folder_mode = True  # 是否将每个作品的文件储存至单独的文件夹
    async with XHS(
            work_path=work_path,
            folder_name=folder_name,
            user_agent=user_agent,
            cookie=cookie,
            proxy=proxy,
            timeout=timeout,
            chunk=chunk,
            max_retry=max_retry,
            record_data=record_data,
            image_format=image_format,
            folder_mode=folder_mode,
    ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        data = await xhs.extract(multiple_links, download)
    return SuccessResponse(data=data)


###########################################################
#                      小红书无水印表                       #
###########################################################
@app.get("/geturls", summary="获取小红书无水印原链接")
async def get_urls_list(p: params.UrlsParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.UrlsDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/createurls", summary="创建小红书无水印原链接")
async def create_urls(data: schemas.Urls, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.UrlsDal(auth.db).create_data(data=data))


@app.put("/urls/{data_id}", summary="更新小红书无水印原链接")
async def put_urls(data_id: int, data: schemas.Urls, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.UrlsDal(auth.db).put_data(data_id, data))


@app.delete("/delurls", summary="删除小红书无水印原链接", description="硬删除")
async def delete_urls_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.UrlsDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdelurls", summary="删除小红书无水印原链接", description="软删除")
async def delete_urls_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.UrlsDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")


###########################################################
#                       小红书素材表                        #
###########################################################
@app.get("/getredbook", summary="获取小红书素材表列表")
async def get_redbook_list(p: params.RedbookParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    v_options = [joinedload(models.RedBook.create_user)]
    datas, count = await crud.RedbookDal(auth.db).get_datas(
        **p.dict(),
        v_options=v_options,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/createredbook", summary="创建小红书素材表")
async def create_redbook(data: schemas.Redbook, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.RedbookDal(auth.db).create_data(data=data))


@app.put("/redbook/{data_id}", summary="更新小红书素材表")
async def put_redbook(data_id: int, data: schemas.Redbook, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.RedbookDal(auth.db).put_data(data_id, data))


@app.delete("/delredbook", summary="删除小红书素材表", description="硬删除")
async def delete_redbook_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.RedbookDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdelredbook", summary="删除小红书素材表", description="软删除")
async def delete_redbook_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.RedbookDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")


# @app.get("/urls/{id}", summary="获取小红书信息+无水印链接")
# async def get_urls(id: int, auth: Auth = Depends(AllUserAuth())):
#     schema = schemas.RedbookSimpleOut
#     return SuccessResponse(await crud.RedbookDal(auth.db).get_data(id, v_schema=schema))

@app.get("/urls/{id}", summary="获取小红书信息+无水印链接")
async def get_urls(id: int, auth: Auth = Depends(AllUserAuth())):
    schema = schemas.RedBookUrlsOut
    return SuccessResponse(
        await crud.RedBookUrlstDal(auth.db).get_datas(
            v_start_sql=select(models.RedBook, models.URL).join_from(models.RedBook, models.URL).where(
                models.RedBook.id == id
            ),
            v_schema=schema
        )
    )


@app.get("/test", summary="接口测试")
async def test(auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.RedBookUrlstDal(auth.db).test_join_form())
