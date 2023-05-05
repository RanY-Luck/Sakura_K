#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    : 主要接口文件
from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import crud, schemas
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.mongo import get_database, DatabaseManage
from .params import LoginParams, OperationParams, SMSParams

app = APIRouter()


###########################################################
#                      日志管理                            #
###########################################################

@app.get("/logins/", summary="获取登录日志列表")
async def get_record_login(
        p: LoginParams = Depends(),  # 请求中解析出来，并传递给数据访问层（DAL）的 get_datas 方法。
        auth: Auth = Depends(AllUserAuth())  # 用户认证，并获取对应的异步数据库会话（auth.db）。
):
    # 创建一个 LoginRecordDal 实例，传入异步数据库会话（auth.db），然后调用该实例的 get_datas 方法，传入 p.dict() 方法的返回值，
    # 获取符合条件的登录日志数据列表（datas）。
    datas = await crud.LoginRecordDal(auth.db).get_datas(**p.dict())
    # 创建一个 LoginRecordDal 实例，并调用该实例的 get_count 方法，传入 p.to_count() 方法的返回值，获取符合条件的登录日志记录总数（count）。
    count = await crud.LoginRecordDal(auth.db).get_count(**p.to_count())
    # 最后，处理器返回一个 SuccessResponse 类型的响应，其中 datas 是获取到的登录日志数据列表，count 是获取到的登录日志记录总数。
    return SuccessResponse(datas, count=count)


@app.get("/operations/", summary="获取操作日志列表")
async def get_record_operation(
        p: OperationParams = Depends(),  # 一个OperationParams类型的参数，这是一个Pydantic模型类的实例，用于解析请求中的参数。
        db: DatabaseManage = Depends(get_database)  # 一个DatabaseManage类型的参数，这是一个自定义的类的实例，用于操作数据库。
):
    # 首先调用了db.get_count方法，该方法会根据传入的参数查询数据库中符合条件的记录数量。
    count = await db.get_count("operation_record", **p.to_count())
    # 接下来，调用了db.get_datas方法，该方法会根据传入的参数查询数据库中符合条件的记录，并使用schemas.OperationRecordSimpleOut对查询结果进行序列化。
    datas = await db.get_datas("operation_record", v_schema=schemas.OperationRecordSimpleOut, **p.dict())
    # 使用SuccessResponse类将查询到的记录列表和记录数量封装成一个JSON格式的响应返回给客户端。
    return SuccessResponse(datas, count=count)


@app.get("/sms/send/list/", summary="获取短信发送列表")
async def get_sms_send_list(
        p: SMSParams = Depends(),  # 一个SMSParams类型的参数，这是一个Pydantic模型类的实例，用于解析请求中的参数。
        auth: Auth = Depends(AllUserAuth)  # 一个Auth类型的参数，这是一个自定义的类的实例，用于进行用户身份验证。
):
    # crud.SMSSendRecordDal(auth.db).get_datas方法，该方法会根据传入的参数查询数据库中符合条件的短信发送记录，并使用默认的序列化方式对查询结果进行序列化。
    datas = await crud.SMSSendRecordDal(auth.db).get_datas(**p.dict())
    # crud.SMSSendRecordDal(auth.db).get_count方法，该方法会根据传入的参数查询数据库中符合条件的短信发送记录数量。
    count = await crud.SMSSendRecordDal(auth.db).get_count(**p.to_count())
    # 使用SuccessResponse类将查询到的短信发送记录列表和记录数量封装成一个JSON格式的响应返回给客户端。
    return SuccessResponse(datas, count=count)


###########################################################
#                      日志分析                            #
###########################################################
@app.get("/analysis/user/login/distribute/", summary="获取用户登录分布情况列表")
async def get_user_login_distribute(
        auth: Auth = Depends(AllUserAuth())  # 一个Auth类型的参数，这是一个自定义的类的实例，用于进行用户身份验证。
):
    # crud.LoginRecordDal(auth.db).get_user_distribute方法，该方法会查询数据库中所有用户的登录分布情况，并将结果封装成一个JSON格式的响应返回给客户端。
    return SuccessResponse(await crud.LoginRecordDal(auth.db).get_user_distribute())
