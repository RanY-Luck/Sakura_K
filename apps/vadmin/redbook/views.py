#!/usr/bin/python
# -*- coding: utf-8 -*-
# @version        : 1.0
# @Create Time    : 2024/02/01 14:37
# @File           : views.py
# @IDE            : PyCharm
# @desc           : 路由，视图文件
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import db_getter
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import schemas, crud, params

app = APIRouter()


###########################################################
#                       小红书素材表                        #
###########################################################
@app.get("/getredbook", summary="获取小红书素材表列表")
async def get_redbook_list(p: params.RedbookParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.RedbookDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.post("/createredbook", summary="创建小红书素材表")
async def create_redbook(data: schemas.Redbook, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.RedbookDal(auth.db).create_data(data=data))


@app.delete("/delredbook", summary="删除小红书素材表", description="硬删除")
async def delete_redbook_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.RedbookDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdelredbook", summary="删除小红书素材表", description="软删除")
async def delete_redbook_list(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.RedbookDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")


@app.put("/redbook/{data_id}", summary="更新小红书素材表")
async def put_redbook(data_id: int, data: schemas.Redbook, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.RedbookDal(auth.db).put_data(data_id, data))


@app.get("/redbook/{data_id}", summary="获取小红书素材表信息")
async def get_redbook(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.RedbookSimpleOut
    return SuccessResponse(await crud.RedbookDal(db).get_data(data_id, v_schema=schema))
