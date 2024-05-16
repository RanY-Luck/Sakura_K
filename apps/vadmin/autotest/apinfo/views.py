#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-28 14:37:30
# @Author  :
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    :

from fastapi import APIRouter, Depends
from sqlalchemy.orm import joinedload

from apps.vadmin.auth.utils.current import AllUserAuth, FullAdminAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.dependencies import IdList
from utils.response import SuccessResponse
from utils.sakurarunner.base.AsyncHttpClient import AsyncRequest
from . import schemas, crud, params, models

app = APIRouter()


###########################################################
#                     接口管理                             #
###########################################################

@app.get("/apilist", summary="获取接口信息详情")
async def get_apinfo_list(p: params.ApInfoParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.ApiInfo
    options = [joinedload(model.create_user)]
    schema = schemas.ApInfoSimpleOut
    datas, count = await crud.ApInfoDal(auth.db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/addapi", summary="新增接口")
async def add_apinfo(data: schemas.ApiInfo, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.ApInfoDal(auth.db).create_data(data=data))


@app.put("/{data_id}", summary="更新接口")
async def update_apinfo(
        data_id: int,
        data: schemas.ApiInfo,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.ApInfoDal(auth.db).put_data(data_id, data))


@app.delete("/delapi", summary="硬删除接口")
async def delete_apinfo(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.ApInfoDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdelapi", summary="软删除接口")
async def delete_apinfo(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.ApInfoDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")


@app.post("/http", summary="Http请求")
async def http_request(data: schemas.HttpRequest, auth: Auth = Depends(AllUserAuth())):
    r = await AsyncRequest(auth.db).client(data.url, data.body_type, headers=data.headers, body=data.body)
    response = await r.invoke(data.method)
    return SuccessResponse(data=response)


@app.post("/debugapi", summary="debug接口")
async def debug_api(data: schemas.HttpRequest, auth: Auth = Depends(AllUserAuth())):
    r = await AsyncRequest(auth.db).client(data.url, data.body_type, headers=data.headers, body=data.body)
    response = await r.invoke(data.method)
    return SuccessResponse(data=response)


@app.post("/runapi", summary="运行接口")
async def run_api(data: schemas.HttpRequest, auth: Auth = Depends(AllUserAuth())):
    r = await AsyncRequest(auth.db).client(data.url, data.body_type, headers=data.headers, body=data.body)
    response = await r.invoke(data.method)
    return SuccessResponse(data=response)
