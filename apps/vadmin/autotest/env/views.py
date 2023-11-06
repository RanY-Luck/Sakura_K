#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 11:39:42
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
#                     环境管理                             #
###########################################################

@app.get("/getenvlist", summary="获取环境列表")
async def get_env_list(p: params.EnvParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.EnvInfo
    options = [joinedload(model.create_user)]
    schema = schemas.EnvSimpleOut
    datas, count = await crud.EnvDal(auth.db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/createenv", summary="创建环境")
async def create_env(data: schemas.Env, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.EnvDal(auth.db).create_data(data=data))


@app.put("/env/{data_id}", summary="更新环境")
async def update_apinfo(
        data_id: int,
        data: schemas.Env,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.EnvDal(auth.db).put_data(data_id, data))


@app.delete("/delenv", summary="硬删除环境")
async def delete_env(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.EnvDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdelenv", summary="软删除环境")
async def delete_env(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.EnvDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")
