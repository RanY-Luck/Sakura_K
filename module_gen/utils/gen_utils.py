#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:58
# @Author   : 冉勇
# @File     : gen_utils.py
# @Software : PyCharm
# @Desc     :
import os
from typing import List, Dict, Any
from click.types import convert_type
from sqlalchemy import Boolean
from module_gen.constants.gen_constants import GenConstants
from module_gen.entity.do.gen_table_column_do import GenTableColumn
from module_gen.entity.do.gen_table_do import GenTable
from module_gen.entity.vo.gen_table_vo import GenTableModel
from module_gen.entity.vo.gen_table_column_vo import GenTableColumnModel


class GenUtils:
    """代码生成器 工具类"""

    @classmethod
    def init_table(cls, table: GenTableModel, columns: List[GenTableColumnModel]) -> None:
        """初始化表信息"""
        table.class_name = cls.convert_class_name(table.table_name)
        table.package_name = cls.get_package_name(table.table_name)
        table.module_name = cls.get_module_name(table.table_name)
        table.business_name = cls.get_business_name(table.table_name)
        table.function_name = table.table_comment
        table.function_author = "FluxAdmin"

        # 初始化列属性字段
        for column in columns:
            cls.init_column_field(column, table)

        # 设置主键列信息
        # for column in columns:
        #     if column.is_pk == "1":
        #         table.pk_column = column
        #         break

    @classmethod
    def init_column_field(cls, column: GenTableColumnModel, table: GenTableModel):
        data_type = cls.get_db_type(column.column_type)
        column_name = column.column_name
        column.table_id = table.table_id
        # 设置python字段名
        column.python_field = column_name
        # 设置默认类型
        column.python_type = GenConstants.MYSQL_TO_PYTHON.get(data_type.upper(), "Any")
        column.query_type = GenConstants.QUERY_EQ

        if data_type in GenConstants.TYPE_STRING or data_type in GenConstants.TYPE_TEXT:
            # 字符串长度超过500设置为文本域
            column_length = cls.get_column_length(column.column_type)
            html_type = GenConstants.HTML_TEXTAREA if column_length >= 500 or (data_type in GenConstants.TYPE_TEXT) \
                else GenConstants.HTML_INPUT
            column.html_type = html_type
        elif data_type in GenConstants.TYPE_DATE_TIME:
            column.html_type = GenConstants.HTML_DATETIME
        elif data_type in GenConstants.TYPE_NUMBER:
            column.html_type = GenConstants.HTML_INPUT
        # 插入字段
        if column.column_name not in GenConstants.COLUMN_NAME_NOT_EDIT and not column.is_pk == '1':
            column.is_insert = GenConstants.REQUIRE
        # 编辑字段
        if column.column_name not in GenConstants.COLUMN_NAME_NOT_EDIT and not column.is_pk == '1':
            column.is_edit = GenConstants.REQUIRE
        # 列表字段
        if column.column_name not in GenConstants.COLUMN_NAME_NOT_LIST and not column.is_pk == '1':
            column.is_list = GenConstants.REQUIRE
        # 查询字段
        if column.column_name not in GenConstants.COLUMN_NAME_NOT_QUERY and not column.is_pk == '1':
            column.is_query = GenConstants.REQUIRE

    @classmethod
    def convert_html_type(cls, column_name: str) -> str:

        # 状态字段初始化
        if column_name.lower().endswith('_status'):
            return GenConstants.HTML_RADIO
        # 类型字段初始化
        elif column_name.lower().endswith('_type'):
            return GenConstants.HTML_SELECT
        # 内容字段初始化
        elif column_name.lower().endswith('_content'):
            return GenConstants.HTML_EDITOR
        # 文件字段初始化
        elif column_name.lower().endswith('_file'):
            return GenConstants.HTML_FILE_UPLOAD
        # 图片字段初始化
        elif column_name.lower().endswith('_image'):
            return GenConstants.HTML_IMAGE_UPLOAD
        else:
            return GenConstants.HTML_INPUT

    @classmethod
    def get_db_type(cls, column_type):
        # 解析数据库类型逻辑，示例返回列的类型
        return column_type.split('(')[0]

    @classmethod
    def get_column_length(cls, column_type):
        # 获取列的长度逻辑，这里简化为返回一个默认值
        if '(' in column_type:
            return int(column_type.split('(')[1].split(')')[0])
        return 0

    @classmethod
    def convert_class_name(cls, table_name: str) -> str:
        """表名转换成Java类名"""
        return ''.join(word.title() for word in table_name.lower().split('_'))

    @classmethod
    def convert_python_field(cls, column_name: str) -> str:
        """列名转换成Python属性名"""
        # words = column_name.lower().split('_')
        # return words[0] + ''.join(word.title() for word in words[1:])
        return column_name.lower()

    @classmethod
    def get_package_name(cls, table_name: str) -> str:
        """获取包名"""
        return "module_admin"  # 可配置的包名

    @classmethod
    def get_module_name(cls, table_name: str) -> str:
        """获取模块名"""
        return table_name.split('_')[0]

    @classmethod
    def get_business_name(cls, table_name: str) -> str:
        """获取业务名"""
        words = table_name.split('_')
        return words[1] if len(words) > 1 else words[0]

    @classmethod
    def get_template_path(cls, tpl_category: str) -> Dict[str, str]:
        """获取模板信息"""
        templates = {
            # Python相关模板
            'controller.py': 'python/controller_template.j2',
            'do.py': 'python/model_do_template.j2',
            'vo.py': 'python/model_vo_template.j2',
            'service.py': 'python/service_template.j2',
            'dao.py': 'python/dao_template.j2',
            # Vue相关模板
            'index.vue': 'vue/index.vue.j2',
            'api.js': 'vue/api.js.j2',
            # SQL脚本模板
            'sql': 'sql/sql.j2',

        }

        # 树表特殊处理
        # if tpl_category == "tree":
        #     templates.update({
        #         'entity': 'java/tree_entity.java.vm',
        #         'mapper': 'java/tree_mapper.java.vm',
        #         'service': 'java/tree_service.java.vm',
        #         'service_impl': 'java/tree_service_impl.java.vm',
        #         'controller': 'java/tree_controller.java.vm'
        #     })

        return templates

    @classmethod
    def get_file_name(cls, template_name: str, table) -> str:
        """获取文件名"""
        target_file_name = "unknown_file_name"
        if template_name.endswith("controller.py"):
            target_file_name = f"python/controller/{table.table_name}_{template_name}"
        elif template_name.endswith("do.py"):
            target_file_name = f"python/entity/do/{table.table_name}_{template_name}"
        elif template_name.endswith("vo.py"):
            target_file_name = f"python/entity/vo/{table.table_name}_{template_name}"
        elif template_name.endswith("service.py"):
            target_file_name = f"python/service/{table.table_name}_{template_name}"
        elif template_name.endswith("dao.py"):
            target_file_name = f"python/dao/{table.table_name}_{template_name}"
        elif template_name.endswith('index.vue'):
            target_file_name = f'vue/views/{table.module_name}/{table.business_name}/index.vue'
        if template_name.endswith('api.js'):
            target_file_name = f'vue/api/{table.module_name}/{table.business_name}.js'

        if template_name.endswith('sql'):
            target_file_name = f'sql/{table.business_name}.sql'
        return target_file_name