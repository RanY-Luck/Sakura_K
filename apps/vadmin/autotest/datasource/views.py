#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 17:23:58
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
#                     数据源管理                            #
###########################################################

@app.get("/getdatasourcelist", summary="获取数据源列表")
async def get_datasource_list(p: params.DataSourceParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.DataSourceInfo
    options = [joinedload(model.create_user)]
    schema = schemas.DataSourceSimpleOut
    datas, count = await crud.DataSourceDal(auth.db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/adddatasource", summary="新增数据源")
async def add_datasource(data: schemas.DataSource, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.DataSourceDal(auth.db).create_data(data=data))


@app.put("/datasource/{data_id}", summary="更新数据源")
async def update_datasource(
        data_id: int,
        data: schemas.DataSource,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.DataSourceDal(auth.db).put_data(data_id, data))


@app.delete("/deldatasource", summary="硬删除数据源")
async def delete_datasource(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DataSourceDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdeldatasource", summary="软删除数据源")
async def delete_datasource(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DataSourceDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")
