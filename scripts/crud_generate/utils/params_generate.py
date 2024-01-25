#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/1/25 9:56
# @Author   : 冉勇
# @File     : params_generate.py
# @Software : PyCharm
# @Desc     : params层代码生成

import inspect
import sys
from pathlib import Path
from typing import Type

from core.database import Base
from .generate_base import GenerateBase


class ParamsGenerate(GenerateBase):

    def __init__(
            self,
            model: Type[Base],
            zh_name: str,
            en_name: str,
            params_dir_path: Path,
            param_file_path: Path,
            param_class_name: str
    ):
        """
        初始化工作
        :param model: 提前定义好的 ORM 模型
        :param zh_name: 功能中文名称，主要用于描述、注释
        :param en_name: 功能英文名称，主要用于 param、param 文件命名，以及它们的 class 命名，dal、url 命名，默认使用 model class
        :param params_dir_path:
        :param param_file_path:
        :param param_class_name:
        en_name 例子：
            如果 en_name 由多个单词组成那么请使用 _ 下划线拼接
            在命名文件名称时，会执行使用 _ 下划线名称
            在命名 class 名称时，会将下划线名称转换为大驼峰命名（CamelCase）
            在命名 url 时，会将下划线转换为 /
        """
        self.model = model
        self.param_class_name = param_class_name
        self.zh_name = zh_name
        self.en_name = en_name
        # model文件的地址
        self.model_file_path = Path(inspect.getfile(sys.modules[model.__module__]))
        # model文件app路径
        self.app_dir_path = self.model_file_path.parent.parent
        # params目录地址
        self.params_dir_path = params_dir_path
        self.param_file_path = param_file_path

    def write_generate_code(self):
        """
        生成 params 文件，以及代码内容
        :return:
        """
        params_init_file_path = self.params_dir_path / "__init__.py"
        self.param_file_path.parent.mkdir(parents=True, exist_ok=True)
        if self.param_file_path.exists():
            self.param_file_path.unlink()
        self.param_file_path.touch()
        params_init_file_path.touch()

    def generate_code(self) -> str:
        """
        生成 schema 代码内容
        :return:
        """
        code = self.generate_file_desc(self.param_file_path.name, "1.0", self.zh_name)
        modules = {
            "fastapi": ['Depends'],
            "core.dependencies": ['Paging', "QueryParams"],
        }
        code += self.generate_modules_code(modules)
        base_code = f"\n\nclass {self.param_class_name}(QueryParams):"
        base_code += f"\n\tdef __init__(self, params: Paging = Depends()):"
        base_code += f"\n\t\tsuper().__init__(params)"
        base_code += "\n"
        code += base_code
        return code.replace("\t", "    ")
