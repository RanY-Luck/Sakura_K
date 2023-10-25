#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-23 15:51:21
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


# todo:更改有bug

###########################################################
#                     项目管理                             #
###########################################################

@app.get("/projectlist", summary="获取项目列表")
async def get_project_list(p: params.ProjectParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.ProjectInfo
    v_options = [joinedload(model.create_user)]
    v_schema = schemas.ProjectOut
    datas, count = await crud.ProjectDal(auth.db).get_datas(
        **p.dict(),
        v_options=v_options,
        v_schema=v_schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/createproject", summary="创建项目")
async def create_project(data: schemas.Project, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.ProjectDal(auth.db).create_data(data=data))


@app.put("/project/{data_id}", summary="更新项目")
async def update_project(data_id: int, data: schemas.Project, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.ProjectDal(auth.db).put_data(data_id, data))


@app.delete("/delproject", summary="删除项目")
async def delete_project(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.ProjectDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")
