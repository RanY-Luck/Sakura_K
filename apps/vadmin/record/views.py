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
        p: LoginParams = Depends(),  # 请求中解析出来，并传递给数据访问层（DAL）的 get_datas 方法。
        auth: Auth = Depends(AllUserAuth())  # 用户认证，并获取对应的异步数据库会话（auth.db）。
):
    datas, count = await crud.LoginRecordDal(auth.db).get_datas(**p.dict(), v_return_objs=True)
    return SuccessResponse(datas, count=count)


@app.get("/operations", summary="获取操作日志列表")
async def get_record_operation(
        p: OperationParams = Depends(),  # 一个OperationParams类型的参数，这是一个Pydantic模型类的实例，用于解析请求中的参数。
        db: AsyncIOMotorDatabase = Depends(mongo_getter),  # 一个DatabaseManage类型的参数，这是一个自定义的类的实例，用于操作数据库。
        auth: Auth = Depends(AllUserAuth())
):
    # 首先调用了db.get_count方法，该方法会根据传入的参数查询数据库中符合条件的记录数量。
    count = await crud.OperationRecordDal(db).get_count(**p.to_count())
    # 接下来，调用了db.get_datas方法，该方法会根据传入的参数查询数据库中符合条件的记录，并使用schemas.OperationRecordSimpleOut对查询结果进行序列化。
    datas = await crud.OperationRecordDal(db).get_datas(**p.dict())
    # 使用SuccessResponse类将查询到的记录列表和记录数量封装成一个JSON格式的响应返回给客户端。
    return SuccessResponse(datas, count=count)


@app.get("/sms/send/list", summary="获取短信发送列表")
async def get_sms_send_list(
        p: SMSParams = Depends(),  # 一个SMSParams类型的参数，这是一个Pydantic模型类的实例，用于解析请求中的参数。
        auth: Auth = Depends(AllUserAuth())  # 一个Auth类型的参数，这是一个自定义的类的实例，用于进行用户身份验证。
):
    datas, count = await crud.SMSSendRecordDal(auth.db).get_datas(**p.dict(), v_return_objs=True)
    return SuccessResponse(datas, count=count)
