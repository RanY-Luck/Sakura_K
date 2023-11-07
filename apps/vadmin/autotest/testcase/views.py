#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 11:09:09
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
#                   测试用例管理                            #
###########################################################

@app.get("/gettestcaselist", summary="获取测试用例列表")
async def get_testcase_list(p: params.TestCaseParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.TestCaseInfo
    options = [joinedload(model.create_user)]
    schema = schemas.TestCaseSimpleOut
    datas, count = await crud.TestCaseDal(auth.db).get_datas(
        **p.dict(),
        v_options=options,
        v_schema=schema,
        v_return_count=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/createtestcase", summary="创建测试用例")
async def create_testcase(data: schemas.TestCase, auth: Auth = Depends(AllUserAuth())):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.TestCaseDal(auth.db).create_data(data=data))


@app.put("/env/{data_id}", summary="更新测试用例")
async def update_testcase(
        data_id: int,
        data: schemas.TestCase,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.TestCaseDal(auth.db).put_data(data_id, data))


@app.delete("/deltestcase", summary="硬删除测试用例")
async def delete_env(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.TestCaseDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.delete("/softdeltestcase", summary="软删除测试用例")
async def delete_env(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.TestCaseDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")
