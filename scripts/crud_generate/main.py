#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/29 10:54
# @Author  : 冉勇
# @Site    : 
# @File    : main.py
# @Software: PyCharm
# @desc    :
import sys
import os.path
import inspect
from typing import Type
from pathlib import Path
from config.database import Base
from config.settings import BASE_DIR
from scripts.crud_generate.utils.vo_generate import VoGenerate
from scripts.crud_generate.utils.dao_generate import DaoGenerate
from scripts.crud_generate.utils.generate_base import GenerateBase
from scripts.crud_generate.utils.service_generate import ServiceGenerate
from scripts.crud_generate.utils.controller_generate import ControllerGenerate


class CrudGenerate(GenerateBase):
    APPS_ROOT = os.path.join(BASE_DIR, "apps")
    SCRIPT_DIR = os.path.join(BASE_DIR, 'scripts', 'crud_generate')

    def __init__(self, model: Type[Base], zh_name: str, en_name: str = None):
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
        """
        self.model = model
        self.zh_name = zh_name
        # model 文件的地址
        self.model_file_path = Path(inspect.getfile(sys.modules[model.__module__]))
        # model 文件 app 路径
        self.app_dir_path = self.model_file_path.parent.parent
        # vo 目录地址:Sakura_K/module_admin/entity/vo
        self.vo_dir_path = self.app_dir_path / "vo"  # 已改好
        # dao 文件地址 目录地址:Sakura_K/module_admin/dao
        self.dao_dir_path = self.app_dir_path.parent / "dao"  # 已改好
        # service 目录地址 目录地址:Sakura_K/module_admin/service
        self.service_dir_path = self.app_dir_path.parent / "service"  # 已改好
        # controller 目录地址:Sakura_K/module_admin/controller
        self.controller_dir_path = self.app_dir_path.parent / "controller"  # 已改好

        if en_name:
            self.en_name = en_name
        else:
            self.en_name = self.model.__name__
        # 生成 entity/vo/xx_vo.py 文件
        self.vo_file_path = self.vo_dir_path / f"{self.en_name}_vo.py"
        # 生成 dao/xx_dao.py 文件
        self.dao_file_path = self.dao_dir_path / f"{self.en_name}_dao.py"
        # 生成 service/xx_service.py 文件
        self.service_file_path = self.service_dir_path / f"{self.en_name}_service.py"
        # 生成 controller/xx_controller.py 文件
        self.controller_file_path = self.controller_dir_path / f"{self.en_name}_controller.py"

        # 生成 vo 中的 pydantic 类名
        self.vo_base_model_class_name = f"{self.snake_to_camel(self.en_name)}Model(BaseModel)"  # Dept2Model(BaseModel)
        self.vo_model_class_name = f"{self.snake_to_camel(self.en_name)}Model"  # Dept2Model
        self.vo_query_model_class_name = f"{self.snake_to_camel(self.en_name)}QueryModel"  # Dept2QueryModel
        self.vo_query_class_name = f"{self.snake_to_camel(self.en_name)}QueryModel({self.vo_model_class_name})"  # Dept2QueryModel(Dept2Model)
        self.vo_page_query_class_name = f"{self.snake_to_camel(self.en_name)}PageQueryModel"  # Dept2PageQueryModel
        self.vo_delete_class_name = f"Delete{self.snake_to_camel(self.en_name)}Model"  # DeleteDept2Model
        # 生成 dao 中的class 类名： xx_Dao类名
        self.dao_base_class_name = f"{self.snake_to_camel(self.en_name)}Dao"
        # 生成 service 中 xx_Service类名
        self.service_base_class_name = f"{self.snake_to_camel(self.en_name)}Service"

    # todo: 先注释
    # def generate_codes(self):
    #     """
    #     生成代码， 不做实际操作，只是将代码打印出来
    #     :return:
    #     """
    #     print(f"==========================={self.vo_file_path} 代码内容=================================")
    #     schema = VoGenerate(
    #         self.model,
    #         self.zh_name,
    #         self.en_name,
    #         self.vo_file_path,
    #         self.vo_dir_path,
    #         self.base_class_name,
    #         self.vo_query_class_name,
    #         self.vo_page_query_class_name,
    #         self.vo_delete_class_name
    #     )
    #     print(schema.generate_code())
    #
    #     print(f"==========================={self.dao_file_path} 代码内容=================================")
    #     dal = DalGenerate(
    #         self.model,
    #         self.zh_name,
    #         self.en_name,
    #         self.dao_file_path
    #     )
    #     print(dal.generate_code())

    # print(f"==========================={self.service_file_path} 代码内容=================================")
    # params = ParamsGenerate(
    #     self.model,
    #     self.zh_name,
    #     self.en_name,
    #     self.service_dir_path,
    #     self.service_file_path,
    #     self.param_class_name
    # )
    # print(params.generate_code())

    # print(f"==========================={self.view_file_path} 代码内容=================================")
    # view = ViewGenerate(
    #     self.model,
    #     self.zh_name,
    #     self.en_name,
    #     self.base_class_name,
    #     self.dao_delete_class_name,
    #     self.dal_class_name,
    #     self.param_class_name
    # )
    # print(view.generate_code())

    def main(self):
        """
        开始生成 crud 代码，并直接写入到项目中，目前还未实现
        1. 生成 schemas 代码
        2. 生成 dal 代码
        3. 生成 params 代码
        4. 生成 views 代码
        :return:
        """
        # 1. 生成 entity/vo/xxx_vo 代码 已改好
        vo = VoGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.vo_file_path,
            self.vo_dir_path,
            self.vo_base_model_class_name,
            self.vo_model_class_name,
            self.vo_query_class_name,
            self.vo_query_model_class_name,
            self.vo_page_query_class_name,
            self.vo_delete_class_name
        )
        vo.write_generate_code()

        # 2.生成 dao/xxx_dao 代码 已改好
        dao = DaoGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.dao_dir_path,
            self.dao_file_path,
            self.dao_base_class_name,
            self.vo_model_class_name
        )
        dao.write_generate_code()

        # 3. 生成 service/xxx_service 代码 已改好
        server = ServiceGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.service_dir_path,
            self.service_file_path,
            self.service_base_class_name,
            self.dao_base_class_name,
            self.vo_page_query_class_name
        )
        server.write_generate_code()

        # 4. 生成 controller/xxx_controller 代码 已改好
        controller = ControllerGenerate(
            self.model,
            self.zh_name,
            self.en_name,
            self.controller_dir_path,
            self.controller_file_path,
            self.vo_page_query_class_name,
            self.service_base_class_name
        )
        controller.write_generate_code()


if __name__ == '__main__':
    from module_admin.entity.do.dept2_do import Dept2

    crud = CrudGenerate(Dept2, zh_name="部门表2", en_name="dept2")
    # 只打印代码，不执行创建写入
    # crud.generate_codes()
    # 创建并写入代码
    crud.main()
