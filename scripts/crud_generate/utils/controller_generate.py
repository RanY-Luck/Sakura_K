#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/29 10:54
# @Author  : 冉勇
# @Site    : 
# @File    : controller_generate.py
# @Software: PyCharm
# @desc    : 生成 xx_controller.py
import inspect
import sys
from pathlib import Path
from typing import Type
from config.database import Base
from .generate_base import GenerateBase


class ControllerGenerate(GenerateBase):

    def __init__(
            self,
            model: Type[Base],
            zh_name: str,
            en_name: str,
            controller_dir_path: Path,
            controller_file_path: Path,
            vo_page_query_class_name: str,
            service_base_class_name: str,
    ):
        """
        初始化工作
        :param model: 提前定义好的 ORM 模型
        :param zh_name: 功能中文名称，主要用于描述、注释
        :param en_name: 功能英文名称，主要用于 schema、param 文件命名，以及它们的 class 命名，dal、url 命名，默认使用 model class
        en_name 例子：
            如果 en_name 由多个单词组成那么请使用 _ 下划线拼接
            在命名文件名称时，会执行使用 _ 下划线名称
            在命名 class 名称时，会将下划线名称转换为大驼峰命名（CamelCase）
            在命名 url 时，会将下划线转换为 /
        :param controller_dir_path:
        :param controller_file_path:
        :param vo_page_query_class_name:
        :param service_base_class_name:

        """
        self.model = model
        self.zh_name = zh_name
        self.en_name = en_name
        self.controller_dir_path = controller_dir_path
        self.controller_file_path = controller_file_path
        self.vo_page_query_class_name = vo_page_query_class_name
        self.service_base_class_name = service_base_class_name

    def write_generate_code(self):
        """
        生成 controller 文件，以及代码内容
        :return:
        """
        if self.controller_file_path.exists():
            codes = self.file_code_split_module(self.controller_file_path)
            if codes:
                print(f"==========controller 文件已存在并已有代码内容，正在追加新代码============")
                if not codes[0]:
                    # 无文件注释则添加文件注释
                    codes[0] = self.generate_file_desc(self.controller_file_path.name, "视图层")
                codes[1] = self.merge_dictionaries(codes[1], self.get_base_module_config())
                codes[2] += self.get_base_code_content()
                code = ''
                code += codes[0]
                code += self.generate_modules_code(codes[1])
                if "app = APIRouter()" not in codes[2]:
                    code += "\n\napp = APIRouter()"
                code += codes[2]
                self.controller_file_path.write_text(code, "utf-8")
                print(f"=================controller 代码已创建完成=====================")
                return
        else:
            self.controller_file_path.touch()
            code = self.generate_code()
            self.controller_file_path.write_text(code, encoding="utf-8")
            print(f"===============controller 代码创建完成==================")

    def generate_code(self) -> str:
        """
        生成代码
        :return:
        """
        code = self.generate_file_desc(self.controller_file_path.name, f"{self.zh_name}相关接口")
        code += self.generate_modules_code(self.get_base_module_config())
        code += f"\n{self.en_name}Controller = APIRouter(prefix='/{self.en_name}', dependencies=[Depends(" \
                f"LoginService.get_current_user)]) "
        code += self.get_base_code_content()

        return code.replace("\t", "    ")

    @staticmethod
    def get_base_module_config():
        """
        获取基础模块导入配置
        :return:
        """
        modules = {
            "fastapi": ["APIRouter", "Depends", "Request"],
            "module_admin.aspect.interface_auth": ["CheckUserInterfaceAuth"],
            "module_admin.service.login_service": ["LoginService"],
            "datetime": ["datetime"],
            "utils.log_util": ["logger"],
            "pydantic_validation_decorator": ["ValidateFields"],
            "sqlalchemy.ext.asyncio": ["AsyncSession"],
            "config.enums": ["BusinessType"],
            "config.get_db": ["get_db"],
            "module_admin.annotation.log_annotation": ["Log"],
            "module_admin.aspect.data_scope": ["GetDataScope"],
            "module_admin.entity.vo.user_vo": ["CurrentUserModel"],
            "utils.response_util": ["ResponseUtil"],
            "utils.page_util": ["PageResponseModel"],
        }
        return modules

    def get_base_code_content(self):
        """
        获取基础代码内容
        :return:
        """

        router = self.en_name.replace("_", "/")
        base_code = f"\n\n\n@{self.en_name}Controller.get(" \
                    f"\n\t\'/{router}/list\', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('{self.en_name}:{self.en_name}:list'))]" \
                    f"\n)"
        base_code += f"\nasync def get_{self.en_name}_list(" \
                     f"\n\t\trequest: Request," \
                     f"\n\t\t{self.en_name}_page_query: {self.vo_page_query_class_name} = Depends({self.vo_page_query_class_name}.as_query),"
        base_code += f"\n\t\tquery_db: AsyncSession = Depends(get_db)" \
                     f"\n):"
        base_code += f'''
    """
     获取{self.zh_name}列表
    """
            '''
        base_code += f"\n\t{self.en_name}_page_query_result = await {self.service_base_class_name}.get_{self.en_name}_list_services("
        base_code += f"\n\t\tquery_db, {self.en_name}_page_query, is_page=True" \
                     f"\n\t)"
        base_code += f"\n\tlogger.info('{self.en_name}列表获取成功')"
        base_code += "\n"
        base_code += f"\n\treturn ResponseUtil.success(model_content={self.en_name}_page_query_result)"

        base_code += "\n"
        return base_code.replace("\t", "    ")
