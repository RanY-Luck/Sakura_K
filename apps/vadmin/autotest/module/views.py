#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-23 15:51:14
# @Author  :
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    :

from fastapi import APIRouter, Depends
from sqlalchemy.orm import joinedload, contains_eager

from apps.vadmin.auth.utils.current import AllUserAuth, FullAdminAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.dependencies import IdList
from utils.response import SuccessResponse
from . import schemas, crud, params, models

app = APIRouter()


###########################################################
#                     模块管理                             #
###########################################################

@app.get("/getmodulelist", summary="获取模块列表")
async def get_project_list(p: params.ModuleParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.ModuleInfo
    options = [joinedload(model.create_user), contains_eager(model.project)]
    schema = schemas.ModuleSimpleOut
    datas, count = await crud.ModuleDal(auth.db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True
    )
    for data in datas:
        data.project_name = data.project.project_name
    print(datas)
    return SuccessResponse(datas, count=count)


@app.post("/createmodule", summary="创建模块")
async def create_module(data: schemas.Module, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.ModuleDal(auth.db).create_data(data=data))


@app.put("/module/{data_id}", summary="更新模块")
async def update_module(
        data_id: int,
        data: schemas.Module,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.ModuleDal(auth.db).put_data(data_id, data))


@app.delete("/delmodule", summary="硬删除模块")
async def delete_module(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.ModuleDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdelmodule", summary="软删除模块")
async def delete_module(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.ModuleDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")
