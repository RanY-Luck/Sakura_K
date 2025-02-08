#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:55
# @Author   : 冉勇
# @File     : gen_table_service.py
# @Software : PyCharm
# @Desc     :
import io
import json
import zipfile
from io import BytesIO
from math import trunc
from typing import List, Optional, Dict
from watchfiles import awatch
from module_gen.dao.gen_table_dao import GenTableDao
from module_gen.dao.gen_table_column_dao import GenTableColumnDao
from module_gen.entity.do.gen_table_column_do import GenTableColumn
from module_gen.entity.do.gen_table_do import GenTable
from module_gen.entity.vo.gen_table_options_vo import GenTableOptionModel
from module_gen.entity.vo.gen_table_vo import GenTablePageModel, GenTableModel
from module_gen.utils.gen_utils import GenUtils
from module_gen.utils.velocity_utils import VelocityUtils
from module_gen.entity.vo.gen_table_column_vo import GenTableColumnModel, GenTableColumnPageModel
from utils.common_util import CamelCaseUtil, SnakeCaseUtil
from utils.page_util import PageResponseModel


class GenTableService:
    """代码生成 服务层实现"""

    @classmethod
    async def select_gen_table_list(cls, gen_table: GenTablePageModel, query_db, data_scope_sql) -> PageResponseModel:
        """查询业务信息"""
        return await GenTableDao.get_gen_table_list(query_db, gen_table, data_scope_sql, is_page=True)

    @classmethod
    async def select_all_gen_table_list(cls, query_db, data_scope_sql) -> PageResponseModel:
        """查询业务信息"""
        return await GenTableDao.get_gen_table_list(query_db, GenTablePageModel(), data_scope_sql, is_page=False)

    @classmethod
    async def select_gen_table_by_id(cls, table_id: int, query_db, data_scope_sql) -> Optional[GenTableModel]:
        """查询业务信息"""
        gen_table = await GenTableDao.get_by_id(query_db, table_id)

        columns = await GenTableColumnDao.get_gen_table_column_list(
            query_db,
            GenTableColumnPageModel(tableId=table_id),
            data_scope_sql
        )
        result = GenTableModel(**CamelCaseUtil.transform_result(gen_table))
        if result.options:
            table_options = GenTableOptionModel(**json.loads(result.options))
            result.parent_menu_id = table_options.parent_menu_id
        result.columns = columns
        return result

    @classmethod
    async def select_gen_table_by_name(cls, table_name: str, query_db) -> Optional[GenTableModel]:
        """查询表名称业务信息"""
        gen_table = await GenTableDao.get_by_table_name(query_db, table_name)
        columns = await GenTableColumnDao.get_gen_table_column_list(
            query_db,
            GenTableColumnPageModel(
                tableId=gen_table.table_id
            )
        )
        result = GenTableModel(**CamelCaseUtil.transform_result(gen_table))
        if result.options:
            table_options = GenTableOptionModel(**json.loads(result.options))
            result.parent_menu_id = table_options.parent_menu_id
        result.columns = columns
        return result

    @classmethod
    async def select_db_table_list(cls, gen_table: GenTablePageModel, query_db, data_scope_sql) -> PageResponseModel:
        """查询数据库列表"""
        return await GenTableDao.select_db_table_list(query_db, gen_table, is_page=True)

    @classmethod
    async def select_db_table_list_by_names(cls, table_names: List[str], query_db) -> List[GenTableModel]:
        """查询数据库列表"""
        return await GenTableDao.select_db_table_list_by_names(query_db, table_names)

    @classmethod
    async def import_gen_table(cls, table_list: List[str], query_db) -> None:
        """导入表结构"""
        tables = await GenTableService.select_db_table_list_by_names(table_list, query_db)
        for table in tables:
            gen_table = GenTableModel()
            gen_table.table_name = table.table_name
            gen_table.table_comment = table.table_comment

            # 查询表列信息
            columns = await GenTableColumnDao.select_db_table_columns_by_name(query_db, table.table_name)

            GenUtils.init_table(gen_table, columns)
            # 添加表信息
            gen_table_result = await GenTableDao.add_gen_table(query_db, gen_table)
            # 添加列信息
            for i, column in enumerate(columns):
                column.table_id = gen_table_result.table_id
                await GenTableColumnDao.add_gen_table_column(query_db, column)
        await query_db.commit()

    @classmethod
    async def validate_edit(cls, gen_table: GenTableModel) -> None:
        """验证编辑"""
        if gen_table.tpl_category == "tree":
            if not all([gen_table.tree_code, gen_table.tree_parent_code, gen_table.tree_name]):
                raise ValueError("树表配置必须填写树编码字段、树父编码字段和树名称字段")

    @classmethod
    async def update_gen_table(cls, query_db, gen_table: GenTableModel) -> None:
        """业务信息"""
        columns_dicts = gen_table.columns
        columns = [GenTableColumnModel(**columns_dict) for columns_dict in columns_dicts]

        gen_table.options = json.dumps(gen_table.params)
        await GenTableDao.edit_gen_table(query_db, gen_table)
        if columns:
            for column in columns:
                column.table_id = gen_table.table_id
                await GenTableColumnDao.edit_gen_table_column(query_db, column)

    @classmethod
    async def delete_gen_table_by_ids(cls, query_db, ids: List[int]) -> None:
        """删除业务对象"""
        await GenTableDao.del_gen_table_by_ids(query_db, ids, soft_del=False)
        await GenTableColumnDao.del_gen_table_column_by_table_ids(query_db, ids, soft_del=False)

    # @classmethod
    # async def generate_code(cls, table_name: str, query_db) -> None:
    #     """生成代码（自定义路径）"""
    #     # 查询表信息
    #     table = await GenTableService.select_gen_table_by_name(table_name, query_db)
    #     # 生成代码
    #     if table:
    #         # 获取模板列表
    #         templates = GenUtils.get_template_path(table.tpl_category)
    #         context = await VelocityUtils.get_render_params(table, query_db)
    #         # 生成代码
    #         for template_name, template_path in templates.items():
    #             # 渲染模板
    #
    #
    #             # 获取生成路径
    #             file_name = GenUtils.get_file_name(template_name, table)
    #             if file_name:
    #                 try:
    #                     file_path = table.gen_path + "/" + file_name
    #                     # 写入文件
    #                     VelocityUtils.write_file(template_path, context, file_path)
    #                 except Exception as e:
    #                     raise RuntimeError(f"渲染模板失败，表名：{table.table_name}")

    @classmethod
    async def sync_db(cls, query_db, table_name: str, data_scope_sql) -> None:

        table = await GenTableDao.get_by_table_name(query_db, table_name)
        table_columns_dicts = await GenTableColumnDao.get_gen_table_column_list(
            query_db,
            GenTableColumnPageModel(tableName=table_name),
            data_scope_sql
        )
        table_columns = [GenTableColumnModel(**tcd) for tcd in table_columns_dicts]
        db_table_columns = await GenTableColumnDao.select_db_table_columns_by_name(query_db, table_name)
        if not db_table_columns or len(db_table_columns) == 0:
            return None

        for i, db_table_column in enumerate(db_table_columns):
            GenUtils.init_column_field(db_table_column, GenTableModel(**CamelCaseUtil.transform_result(table)))
            prev_column = next(
                (table_column for table_column in table_columns if
                 table_column.column_name == db_table_column.column_name), None
            )
            if prev_column:
                db_table_column.column_id = prev_column.column_id
                if db_table_column.is_list:
                    db_table_column.dict_type = prev_column.dict_type
                    db_table_column.query_type = prev_column.query_type
                db_table_column.is_required = prev_column.is_required
                db_table_column.html_type = prev_column.html_type
                await GenTableColumnDao.edit_gen_table_column(query_db, db_table_column, auto_commit=False)
            else:
                await GenTableColumnDao.add_gen_table_column(query_db, db_table_column)

        dbc_names = {dbc.column_name for dbc in db_table_columns}
        del_columns = [t_column for t_column in table_columns if t_column.column_name not in dbc_names]
        for i, del_column in enumerate(del_columns):
            await GenTableColumnDao.del_gen_table_column(query_db, del_column, auto_commit=False, soft_del=False)
        await query_db.commit()

    @classmethod
    async def preview_code(cls, query_db, table_id: int, data_scope_sql) -> (Dict[str, str], GenTableModel):
        """预览模板代码"""
        table = await cls.select_gen_table_by_id(table_id, query_db, data_scope_sql)
        render_params = await VelocityUtils.get_render_params(table, query_db)
        templates = GenUtils.get_template_path(table.tpl_category)
        preview_result = {}
        for template_name, template_path in templates.items():
            template = VelocityUtils.get_template(template_path)
            content = template.render(**render_params)
            preview_result[template_name] = content
        return preview_result, table

    @classmethod
    async def batch_generate_code(cls, query_db, data_scope_sql, table_id_array: List[str]) -> BytesIO:
        """批量下载生成代码"""
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for i, table_id in enumerate(table_id_array):
                preview_result, table = await cls.preview_code(query_db, int(table_id), data_scope_sql)
                for filename, content in preview_result.items():
                    target_file_name = GenUtils.get_file_name(filename, table)
                    zip_file.writestr(target_file_name, content)
        zip_buffer.seek(0)
        return zip_buffer

    @classmethod
    async def create_table(cls, query_db, sql) -> bool:
        """数据库表创建"""
        return await GenTableDao.create_table(query_db, sql)