#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:50
# @Author   : 冉勇
# @File     : gen_controller.py
# @Software : PyCharm
# @Desc     : 代码生成操作处理
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from config.get_db import get_db
from module_admin.aspect.data_scope import GetDataScope
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.service.login_service import LoginService
from module_gen.entity.vo.gen_table_vo import GenTableModel, GenTablePageModel, GenTableIdsModel
from module_gen.service.gen_table_service import GenTableService
from utils.response_util import ResponseUtil

gen1Controller = APIRouter(prefix="/tool/gen",  dependencies=[Depends(LoginService.get_current_user)])

"""代码生成操作处理"""


@gen1Controller.get('/list', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:list'))])
async def gen_list(
        request: Request,
        gen_table: GenTablePageModel = Depends(GenTablePageModel.as_query),
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept')), ):
    """查询代码生成列表"""
    table_list = await GenTableService.select_gen_table_list(gen_table, query_db, data_scope_sql)
    return ResponseUtil.success(model_content=table_list)


@gen1Controller.get('/db/list', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:list'))])
async def gen_db_list(
        request: Request,
        gen_table: GenTablePageModel = Depends(GenTablePageModel.as_query),
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """查询数据库列表"""
    db_list = await GenTableService.select_db_table_list(gen_table, query_db, data_scope_sql)
    return ResponseUtil.success(model_content=db_list)


@gen1Controller.post('/importTable', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:import'))])
async def import_table(
        request: Request, tables: str = Query(None),
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """导入表结构"""
    tables_array = tables.split(',') if tables else []
    operate_log = "导入表" + ",".join(tables_array)
    await GenTableService.import_gen_table(tables_array, query_db)
    return ResponseUtil.success(operate_log)


@gen1Controller.get('/getById/{tableId}', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:query'))])
async def get_info(
        request: Request, tableId: int,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """查询表详细信息"""
    table_info = await GenTableService.select_gen_table_by_id(tableId, query_db, data_scope_sql)
    all_gen_tables = await GenTableService.select_all_gen_table_list(query_db, data_scope_sql)
    result = {
        "info": table_info,
        "rows": table_info.columns,
        "tables": all_gen_tables
    }
    return ResponseUtil.success(data=result)


@gen1Controller.get('/tableInfo/{tableName}')
async def get_table_info(
        request: Request, tableName: str,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """获取表详细信息"""
    table_info = GenTableService.select_gen_table_by_name(tableName, query_db)
    return ResponseUtil.success(data=table_info)


@gen1Controller.put('', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:edit'))])
async def update_save(
        request: Request, gen_table: GenTableModel,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """修改保存代码生成业务"""
    await GenTableService.validate_edit(gen_table)
    await GenTableService.update_gen_table(query_db, gen_table)
    return ResponseUtil.success()


@gen1Controller.delete('/{tableIds}', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:remove'))])
async def delete(
        request: Request, tableIds: str,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """删除代码生成"""
    tableIdsArray = tableIds.split(',') if tableIds else []
    await GenTableService.delete_gen_table_by_ids(query_db, tableIdsArray)
    return ResponseUtil.success()


@gen1Controller.get('/preview/{tableId}', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:preview'))])
async def preview(
        request: Request, tableId: int,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """预览代码"""
    result, table = await GenTableService.preview_code(query_db, tableId, data_scope_sql)
    return ResponseUtil.success(data=result)


# @gen1Controller.get('/download/{tableName}', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:code'))])
# async def download(request: Request, table_name: str,
#                        query_db: AsyncSession = Depends(get_db),
#                        data_scope_sql: str = Depends(GetDataScope('SysDept'))):
#     """生成代码（下载方式）"""
#     # 查询表信息
#     table_info = await GenTableService.select_gen_table_by_name(table_name, query_db)
#     #生成代码
#     byte_data = await GenTableService.download_code(table_info)
#
#     # 生成zip文件
#     return create_zip_file(byte_data, f"{table_info.table_comment}.zip")

# @gen1Controller.get('/genCode/{tableName}', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:code'))])
# async def generate_code(request: Request, table_name: str,
#                        query_db: AsyncSession = Depends(get_db),
#                        data_scope_sql: str = Depends(GetDataScope('SysDept'))):
#     """生成代码（自定义路径）"""
#     # 生成代码
#     await GenTableService.generate_code(table_name, query_db)
#     return ResponseUtil.success()

@gen1Controller.get('/synchDb/{tableName}', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:edit'))])
async def sync_db(
        request: Request, tableName: str,
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """同步数据库"""
    await GenTableService.sync_db(query_db, tableName, data_scope_sql)
    return ResponseUtil.success()


@gen1Controller.get('/batchGenCode', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:code'))])
async def batch_generate_code(
        request: Request, ids_model: GenTableIdsModel = Depends(GenTableIdsModel.as_query),
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """批量生成代码"""
    # 查询表信息
    table_id_array = ids_model.tb_ids.split(',') if ids_model.tb_ids else []
    # 生成zip包
    byte_data = await GenTableService.batch_generate_code(query_db, data_scope_sql, table_id_array)
    return ResponseUtil.streaming(data=byte_data)


@gen1Controller.post('/createTable', dependencies=[Depends(CheckUserInterfaceAuth('tool:gen:import'))])
async def import_table(
        request: Request, sql: str = Query(None),
        query_db: AsyncSession = Depends(get_db),
        data_scope_sql: str = Depends(GetDataScope('SysDept'))
):
    """创建表结构"""
    success = await GenTableService.create_table(query_db, sql)
    if success:
        return ResponseUtil.success()
    else:
        return ResponseUtil.failure(msg="创建失败，请检查语法是否符合mysql标准，并检查后端日志")
