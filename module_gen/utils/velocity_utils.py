#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:59
# @Author   : 冉勇
# @File     : velocity_utils.py
# @Software : PyCharm
# @Desc     :
import os
from typing import Dict, Any, List
from jinja2 import Template
from module_gen.constants.gen_constants import GenConstants
from module_gen.dao.gen_table_column_dao import GenTableColumnDao
from module_gen.dao.gen_table_dao import GenTableDao
from module_gen.entity.do.gen_table_column_do import GenTableColumn
from module_gen.entity.do.gen_table_do import GenTable
from module_gen.entity.vo.gen_table_column_vo import GenTableColumnPageModel, GenTableColumnModel
from module_gen.entity.vo.gen_table_vo import GenTableModel
from module_gen.utils.velocity_initializer import VelocityInitializer


class VelocityUtils:
    """模板处理工具类"""

    # 默认上级菜单，系统工具
    DEFAULT_PARENT_MENU_ID = "3"

    # 环境对象
    _env = None

    @classmethod
    def get_env(cls):
        """获取模板环境对象"""
        if cls._env is None:
            cls._env = VelocityInitializer.init_velocity()
        return cls._env

    @classmethod
    def get_template(cls, template_path: str) -> Template:
        """获取模板"""
        return cls.get_env().get_template(template_path)

    @classmethod
    async def get_render_params(cls, gen_table: GenTableModel, query_db) -> Dict[str, Any]:
        """设置模板变量信息"""
        # 设置python文件路径
        sub_table = None
        if gen_table.sub_table_name:
            # 子表信息
            sub_table = await GenTableDao.get_by_table_name(query_db, gen_table.sub_table_name)
            # 设置主子表信息
            # await cls.set_sub_table_value(query_db, gen_table, sub_table)

        # 设置主键列信息
        table_columns_dicts = await GenTableColumnDao.get_gen_table_column_list(
            query_db, GenTableColumnPageModel(tableId=gen_table.table_id)
        )
        table_columns = [GenTableColumnModel(**tcd) for tcd in table_columns_dicts]
        pk_column = None
        for column in table_columns:
            if column.is_pk == "1":
                pk_column = column
                break

        context = {
            # 文件名称
            "tableName": gen_table.table_name,
            # 小写类名
            "className": gen_table.class_name.lower(),
            # 大写类名
            "ClassName": gen_table.class_name,
            # 包路径
            "packageName": gen_table.package_name,
            # 模块名
            "moduleName": gen_table.module_name,
            # 业务名
            "businessName": gen_table.business_name,
            # 业务名(首字母大写)
            "BusinessName": gen_table.business_name.capitalize(),
            # 功能名称
            "functionName": gen_table.function_name,
            # 作者
            "author": gen_table.function_author,
            # 主键字段
            "pkColumn": pk_column.model_dump(by_alias=True) if pk_column else None,
            # 导入sqlalchemy需要导入的类型字段
            "importList": cls.get_import_list(table_columns),
            # 列集合
            "columns": [tcn.model_dump(by_alias=True) for tcn in table_columns],
            # 生成路径
            "genPath": gen_table.gen_path,
            # 表描述
            "tableComment": gen_table.table_comment,
            # 权限前缀
            "permissionPrefix": cls.get_permission_prefix(gen_table.module_name, gen_table.business_name),
            # 是否包含主键
            "hasPk": cls.has_pk_column(table_columns),
            # 是否包含Bigdecimal
            "hasBigDecimal": cls.has_column_big_decimal(table_columns),
            # 是否包含时间类型
            "hasDateTime": cls.has_column_datetime(table_columns),
            # 主键是否自增
            "auto": cls.is_pk_auto(table_columns),
            # 父级菜单ID
            "parentMenuId": gen_table.parent_menu_id,
            # 字段关联的字典名
            "dicts": cls.get_column_related_dicts(table_columns),
        }

        # if gen_table.tpl_category == "tree":
        #     context.update({
        #         "treeCode": gen_table.tree_code,
        #         "treeParentCode": gen_table.tree_parent_code,
        #         "treeName": gen_table.tree_name,
        #         "expandColumn": gen_table.tree_name,
        #         "tree_parent_code": gen_table.tree_parent_code,
        #         "tree_name": gen_table.tree_name
        #     })

        # if gen_table.tpl_category == "sub":
        #     context.update({
        #         "subTable": sub_table,
        #         "subTableName": gen_table.sub_table_name,
        #         "subTableFkName": gen_table.sub_table_fk_name,
        #         "subClassName": sub_table.class_name,
        #         "subclassName": sub_table.class_name.lower(),
        #         "subImportList": cls.get_import_list(sub_table, table_columns)
        #     })

        return context

    @classmethod
    def get_permission_prefix(cls, module_name: str, business_name: str) -> str:
        """获取权限前缀"""
        return f"{module_name}:{business_name}"

    # @classmethod
    # async def set_sub_table_value(cls, query_db, gen_table: GenTable, sub_table: GenTable):
    #     """设置主子表信息"""
    #     table_columns = await GenTableColumnDao.get_gen_table_column_list(query_db, GenTableColumnPageModel(
    #         tableId=sub_table.table_id))
    #     for column in table_columns:
    #         if column.is_pk == "1":
    #             gen_table.pk_column = column
    #             break

    @classmethod
    def get_import_list(cls, table_columns: List[GenTableColumnModel]) -> str:
        """获取需要导入的包列表"""
        sqlalchemy_types = []
        for i, table_column in enumerate(table_columns):
            if table_column.column_type:
                mysql_type = table_column.column_type.split("(")[0]
                if mysql_type.upper() in GenConstants.MYSQL_TO_SQLALCHEMY.keys():
                    temp_type = GenConstants.MYSQL_TO_SQLALCHEMY[mysql_type.upper()]
                    if temp_type not in sqlalchemy_types:
                        sqlalchemy_types.append(temp_type)
        return ", ".join(sqlalchemy_types)

    @staticmethod
    def has_column_datetime(columns: List[GenTableColumnModel]) -> bool:
        """判断是否包含datetime"""
        return any(column.python_type == "Date" for column in columns)

    @staticmethod
    def has_column_big_decimal(columns: List[GenTableColumnModel]) -> bool:
        """判断是否包含BigDecimal"""
        return any(column.python_type == "BigDecimal" for column in columns)

    @staticmethod
    def has_pk_column(columns: List[GenTableColumnModel]) -> bool:
        """判断是否包含主键"""
        return any(column.is_pk == "1" for column in columns)

    @staticmethod
    def is_pk_auto(columns: List[GenTableColumnModel]) -> bool:
        """判断主键是否自增"""
        return any(column.is_pk == "1" and column.is_increment == "1" for column in columns)

    @classmethod
    def write_file(cls, template_path: str, context: Dict[str, Any], file_path: str) -> None:
        """渲染模板并写入文件"""
        try:
            # 获取生成文件的目录
            out_dir = os.path.dirname(file_path)
            if not os.path.exists(out_dir):
                os.makedirs(out_dir)

            # 渲染模板
            template = cls.get_template(template_path)
            content = template.render(**context)

            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        except Exception as e:
            raise RuntimeError(f"渲染模板失败，模板路径：{template_path}") from e

    @classmethod
    def get_column_related_dicts(cls, table_columns) -> str:
        dicts = []
        for table_column in table_columns:
            if table_column.dict_type:
                dicts.append(f"'{table_column.dict_type}'")
        return ", ".join(dicts)
