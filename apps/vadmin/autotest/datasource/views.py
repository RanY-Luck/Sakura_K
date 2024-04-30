#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-10-31 17:23:58
# @Author  :
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    :
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import joinedload

from apps.vadmin.auth.utils.current import AllUserAuth, FullAdminAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.dependencies import IdList
from core.mysql_manage import DatabaseHelper
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
    schema = schemas.DataSourceListOut
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


@app.put("/{data_id}", summary="更新数据源")
async def update_datasource(
        data_id: int,
        data: schemas.DataSource,
        auth: Auth = Depends(AllUserAuth())
):
    return SuccessResponse(await crud.DataSourceDal(auth.db).put_data(data_id, data))


@app.delete("/deldatasource", summary="硬删除数据源")
async def delete_datasource(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DataSourceDal(auth.db).delete_datas(ids=ids.ids)
    return SuccessResponse("删除成功")


@app.delete("/softdeldatasource", summary="软删除数据源")
async def delete_datasource(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.DataSourceDal(auth.db).delete_datas(ids=ids.ids, v_soft=True)
    return SuccessResponse("删除成功")


###########################################################
#                     数据源获取                            #
###########################################################

@app.post("/testconnect", summary="测试连接")
async def test_connect(data: schemas.SourceInfo, auth: Auth = Depends(FullAdminAuth())):
    db_helper = DatabaseHelper(source_info=data)
    datas = await db_helper.test_db_connection()
    return SuccessResponse(datas)


@app.post("/dbList", summary="获取数据库中的所有库")
async def test_connect(data: schemas.SourceInfo, auth: Auth = Depends(FullAdminAuth())):
    db_helper = DatabaseHelper(source_info=data)
    datas = await db_helper.get_database()
    return SuccessResponse(datas)


@app.post("/tableList", summary="获取指定数据库中的所有表名")
async def test_connect(
        data: schemas.SourceInfo,
        databases: str = Query(..., description="数据库库名"),
        auth: Auth = Depends(FullAdminAuth())
):
    db_helper = DatabaseHelper(source_info=data)
    datas = await db_helper.get_tables(database=databases)
    return SuccessResponse(datas)


@app.post("/mysqlexecute", summary="在指定的数据库中执行 SQL 查询语句")
async def test_connect(
        data: schemas.SourceInfo,
        databases: str = Query(..., description="数据库库名"),
        sql: str = Query(..., description="SQL 查询语句"),
        auth: Auth = Depends(FullAdminAuth())
):
    db_helper = DatabaseHelper(source_info=data)
    datas = await db_helper.execute_query(database=databases, query=sql)
    return SuccessResponse(datas)


@app.post("/getalltablesandcolumns", summary="获取所有数据库及其表和列信息")
async def test_connect(data: schemas.SourceInfo, auth: Auth = Depends(FullAdminAuth())):
    db_helper = DatabaseHelper(source_info=data)
    datas = await db_helper.get_all_tables_and_columns()
    return SuccessResponse(datas)
