#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    : 主要接口文件
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase

from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.database import mongo_getter
from utils.response import SuccessResponse
from . import crud
from .params import LoginParams, OperationParams, SMSParams

app = APIRouter()


###########################################################
#                      日志管理                            #
###########################################################
@app.get("/logins", summary="获取登录日志列表")
async def get_record_login(
        p: LoginParams = Depends(),
        auth: Auth = Depends(AllUserAuth())
):
    datas, count = await crud.LoginRecordDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)


@app.get("/operations", summary="获取操作日志列表")
async def get_record_operation(
        p: OperationParams = Depends(),
        db: AsyncIOMotorDatabase = Depends(mongo_getter),
        auth: Auth = Depends(AllUserAuth())
):
    count = await crud.OperationRecordDal(db).get_count(**p.to_count())
    datas = await crud.OperationRecordDal(db).get_datas(**p.dict())
    return SuccessResponse(datas, count=count)


@app.get("/sms/send/list", summary="获取短信发送列表")
async def get_sms_send_list(p: SMSParams = Depends(), auth: Auth = Depends(AllUserAuth())):
    datas, count = await crud.SMSSendRecordDal(auth.db).get_datas(**p.dict(), v_return_count=True)
    return SuccessResponse(datas, count=count)
