#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/29 10:53
# @Author  : 冉勇
# @Site    : 
# @File    : dao_generate.py
# @Software: PyCharm
# @desc    : 生成 xx_dao.py
import inspect
import sys
from pathlib import Path
from typing import Type
from config.database import Base
from .generate_base import GenerateBase


class DaoGenerate(GenerateBase):

    def __init__(
            self,
            model: Type[Base],
            zh_name: str,
            en_name: str,
            dao_dir_path: Path,
            dao_file_path: Path,
            dao_base_class_name: str,
            vo_model_class_name: str
    ):
        """
        初始化工作
        :param model: 提前定义好的 ORM 模型
        :param zh_name: 功能中文名称，主要用于描述、注释
        :param en_name: 功能英文名称，主要用于 param、param 文件命名，以及它们的 class 命名，dal、url 命名，默认使用 model class
        en_name 例子：
            如果 en_name 由多个单词组成那么请使用 _ 下划线拼接
            在命名文件名称时，会执行使用 _ 下划线名称
            在命名 class 名称时，会将下划线名称转换为大驼峰命名（CamelCase）
            在命名 url 时，会将下划线转换为 /
        :param dao_file_path:
        :param dao_dir_path:
        :param dao_base_class_name:
        :param vo_model_class_name:
        """
        self.model = model
        self.zh_name = zh_name
        self.en_name = en_name
        self.dao_dir_path = dao_dir_path
        self.dao_file_path = dao_file_path
        self.dao_base_class_name = dao_base_class_name
        self.vo_model_class_name = vo_model_class_name

    def write_generate_code(self):
        """
        生成 params 文件，以及代码内容
        :return:
        """
        self.dao_file_path.parent.mkdir(parents=True, exist_ok=True)
        if self.dao_file_path.exists():
            self.dao_file_path.unlink()
        self.dao_file_path.touch()

        code = self.generate_code()
        self.dao_file_path.write_text(code, "utf-8")
        print(f"===========================dao 代码创建完成=================================")

    def generate_code(self) -> str:
        """
        生成 schema 代码内容
        :return:
        """
        code = self.generate_file_desc(self.dao_file_path.name, self.zh_name)
        # 导入模块
        modules = {
            "typing": ['List'],
            "sqlalchemy": ['select', 'update', 'delete', 'and_', 'func', 'bindparam', 'or_', 'asc', 'desc'],
            "sqlalchemy.ext.asyncio": ['AsyncSession'],
            "sqlalchemy.orm": ['Session'],
            f"module_admin.entity.do.{self.en_name}_do": ['*'],
            f"module_admin.entity.vo.{self.en_name}_vo": ['*'],
            "utils.page_util": ['PageUtil'],
            "datetime": ['datetime', 'time'],
        }
        code += self.generate_modules_code(modules)

        # 根据 id 获取信息 已改好
        base_code = f'''
"""
需要自己写 dao 逻辑代码
"""
            '''
        base_code += f"\n\nclass {self.dao_base_class_name}:"
        base_code += f'''
    """
    {self.zh_name}管理模块数据库操作层
    """
        '''
        base_code += f"\n\t@classmethod"
        base_code += f"\n\tasync def get_{self.en_name}_detail_by_id(cls, db: AsyncSession, {self.en_name}_id: int):"
        base_code += f'''
        """
        根据id获取{self.zh_name}详细信息
        :param db: orm对象
        :param {self.en_name}_id: 
        :return: 
        """
        '''
        base_code += f"{self.en_name}_info = (await db.execute(select({self.snake_to_camel(self.en_name)})" \
                     f".where({self.snake_to_camel(self.en_name)}.{self.en_name}_id == {self.en_name}_id)))" \
                     f".scalars().first()"
        base_code += f"\n\n\t\treturn {self.en_name}_info"
        base_code += f"\n"

        # 根据参数获取信息
        base_code += f"\n\t@classmethod"
        base_code += f"\n\tasync def get_{self.en_name}_detail_by_info(cls, db: AsyncSession," \
                     f" {self.en_name}: {self.vo_model_class_name}):"
        base_code += f'''
        """
        根据配置id获取{self.zh_name}详细信息
        :param db: orm对象
        :param {self.en_name}:
        :return:
        """
        '''
        base_code += f"{self.en_name}_info = (" \
                     f"\n\t\t\t(" \
                     f"\n\t\t\t\tawait db.execute(" \
                     f"\n\t\t\t\t\tselect({self.snake_to_camel(self.en_name)}).where(" \
                     f"\n\t\t\t\t\t\t{self.snake_to_camel(self.en_name)}.xxx == {self.en_name}.xxx " \
                     f"if {self.en_name}.xxx else True" \
                     f"\n\t\t\t\t\t)" \
                     f"\n\t\t\t\t)" \
                     f"\n\t\t\t).scalars().first())"
        base_code += f"\n\n\t\treturn {self.en_name}_info"
        base_code += f"\n"

        code += base_code
        return code.replace("\t", "    ")
