#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-23 15:51:14
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
#                     模块管理                             #
###########################################################

@app.get("/getmodulelist", summary="获取模块列表")
async def get_project_list(p: params.ModuleParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.ModuleInfo,
    schema = schemas.ModuleSimpleOut
    datas, count = await crud.ModuleDal(auth.db).get_datas(
        **p.dict(),
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)
