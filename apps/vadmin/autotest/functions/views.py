#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 17:56:40
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
from . import schemas, crud, params, models

app = APIRouter()


###########################################################
#                   自定义函数管理                          #
###########################################################

@app.get("/getfunctionslist", summary="获取自定义函数列表")
async def get_functions_list(p: params.FunctionsParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.FunctionsInfo
    options = [joinedload(model.create_user)]
    schema = schemas.FunctionsSimpleOut
    datas, count = await crud.FunctionsDal(auth.db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/creatfunctions", summary="创建自定义函数")
async def create_functions(data: schemas.Functions, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.FunctionsDal(auth.db).create_data(data=data))


@app.put("/env/{data_id}", summary="更新自定义函数")
async def update_functions(
        data_id: int,
        data: schemas.Functions,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.FunctionsDal(auth.db).put_data(data_id, data))


@app.delete("/delfunctions", summary="硬删除自定义函数")
async def delete_functions(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.FunctionsDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdelfunctions", summary="软删除自定义函数")
async def delete_env(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.FunctionsDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")
