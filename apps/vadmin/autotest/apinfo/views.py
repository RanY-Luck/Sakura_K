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
from . import schemas, crud, params, models

app = APIRouter()


###########################################################
#                     接口管理                             #
###########################################################

@app.get("/getapinfolist", summary="获取接口信息详情")
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


@app.post("/addapinfo", summary="新增接口")
async def add_apinfo(data: schemas.ApiInfo, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.ApInfoDal(auth.db).create_data(data=data))
