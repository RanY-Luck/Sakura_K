#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/27 19:09
# @Author  : 冉勇
# @Site    : 
# @File    : initialize.py
# @Software: PyCharm
# @desc    :
import os
import subprocess
from enum import Enum

from sqlalchemy.sql.schema import Table

from application.settings import BASE_DIR, VERSION
from apps.vadmin.auth import models as auth_models
from apps.vadmin.system import models as system_models
from core.database import db_getter
from utils.excel.excel_manage import ExcelManage


class Environment(str, Enum):
    dev = "dev"
    pro = "pro"


class InitializeData():
    """
    初始化数据
    生成步骤：
        1、读取数据
        2、获取数据库
        3、创建数据
    """
    SCRIPT_DIR = os.path.join(BASE_DIR, "scripts", "initialize")

    def __init__(self):
        """
        代码解释：
        用于初始化类的属性和调用类的私有方法"__serializer_data"和"__get_sheet_data"，用于序列化数据和获取Excel表格数据。
        在方法中，首先初始化了四个类属性：sheet_names、datas、ex和db。sheet_names用于存储Excel表格中的工作表名，
        datas用于存储Excel表格中各个工作表的数据，ex用于存储读取Excel表格的对象，db用于存储连接到数据库的对象。
        接下来，调用了类的私有方法"__serializer_data"，用于将配置文件中的数据进行序列化，方便后续操作。
        然后调用了类的私有方法"__get_sheet_data"，用于获取Excel表格中各个工作表的数据，并将数据存储到类属性datas中。
        """
        self.sheet_names = []
        self.datas = {}
        self.ex = None
        self.db = None
        self.__serializer_data()
        self.__get_sheet_data()

    @classmethod
    def migrate_model(
            cls,
            env: Environment = Environment.pro  # 表示要映射到的数据库环境，该参数的默认值为Environment.pro。
    ):
        """
        模型迁移映射到数据库
        :param env:
        :return:
        """
        # 首先调用了一个名为"subprocess.check_call"的函数，该函数用于在命令行中执行指定的命令。这里执行的命令是使用Alembic库进行模型迁移的命令，具体命令如下：
        # alembic --name {env.value} revision --autogenerate -m "{VERSION}"
        # 其中，"{env.value}"表示要映射到的数据库环境的名称，"{VERSION}"表示模型版本号。这个命令会自动生成一个迁移脚本，用于将模型变更应用到数据库中。
        subprocess.check_call(
            ['alembic', '--name', f'{env.value}', 'revision', '--autogenerate', '-m', f'{VERSION}'], cwd=BASE_DIR
        )
        # 接着，方法又调用了一次"subprocess.check_call"函数，执行另一个Alembic命令：
        # alembic --name {env.value} upgrade head
        subprocess.check_call(['alembic', '--name', f'{env.value}', 'upgrade', 'head'], cwd=BASE_DIR)
        print(f"环境：{env} {VERSION} 数据库表迁移完成")

    def __serializer_data(self):
        """
        序列化数据，将excel数据转为python对象
        :return:
        """
        # 首先创建了一个ExcelManage对象"self.ex"，用于管理Excel文件。
        self.ex = ExcelManage()
        # 接着，调用该对象的"open_workbook"方法，打开指定的Excel文件，文件路径为"SCRIPT_DIR/data/init.xlsx"，并设置只读模式。
        self.ex.open_workbook(os.path.join(self.SCRIPT_DIR, 'data', 'init.xlsx'), read_only=True)
        # 调用ExcelManage对象的"get_sheets"方法，获取Excel文件中的所有工作表的名称，并将这些名称保存到对象的"sheet_names"属性中，以便后续使用。
        self.sheet_names = self.ex.get_sheets()

    def __get_sheet_data(self):
        """
        获取工作区数据
        :return:
        """
        # 首先使用一个for循环遍历所有工作表的名称，对于每个工作表，创建一个空列表"sheet_data"用于保存工作表的数据。
        for sheet in self.sheet_names:
            sheet_data = []
            # 然后，调用ExcelManage对象的"open_sheet"方法，打开当前工作表
            self.ex.open_sheet(sheet)
            # 使用"get_header"方法获取工作表的表头信息。
            headers = self.ex.get_header()
            # 接着，调用ExcelManage对象的"readlines"方法，读取工作表中的数据，
            # 其中"min_row=2"表示从第二行开始读取（忽略表头），"max_col=len(headers)"表示读取的最大列数与表头的列数相同。
            # 读取的数据是一个二维数组，每个子数组代表一行数据。
            datas = self.ex.readlines(min_row=2, max_col=len(headers))
            # 使用一个for循环遍历每行数据，将每行数据转换成一个字典对象，字典的key是表头的列名，value是当前行对应列的值。
            for row in datas:
                sheet_data.append(dict(zip(headers, row)))
            # 将转换后的字典对象添加到"sheet_data"列表中。
            # 将当前工作表的数据保存到对象的"datas"属性中，"datas"是一个字典对象，key是工作表的名称，value是对应工作表的数据列表。
            # 每个数据列表中包含多个字典对象，每个字典对象代表一行数据。
            self.datas[sheet] = sheet_data

    async def __generate_data(self, table_name: str, model):
        """
        生成数据
        :param table_name: 表名
        :param model: 数据表模型
        :return:
        """
        # 首先获取一个异步数据库会话"async_session"，这里使用了一个"db_getter"函数来获取异步数据库的会话。
        async_session = db_getter()
        # 接着，使用"await async_session.anext()"方法获取一个异步数据库连接"db"。
        db = await async_session.__anext__()
        # 然后，判断数据表模型"model"是否为Table类型，如果是，则说明使用SQLAlchemy的Core API来执行插入操作。
        if isinstance(model, Table):
            # 接着，使用一个for循环遍历表名为"table_name"的数据列表，将每个字典对象作为参数传递给"model.insert()"方法
            for data in self.datas.get(table_name):
                # 使用"await db.execute()"方法执行插入操作。
                await db.execute(model.insert().values(**data))
        # 如果数据表模型"model"不是Table类型，则说明使用SQLAlchemy的ORM API来执行插入操作。
        else:
            for data in self.datas.get(table_name):
                # 在这种情况下，需要使用"db.add()"方法向会话中添加数据，然后使用"await db.flush()"方法将数据写入数据库。
                db.add(model(**data))
        print(f"{table_name} 表数据已生成")
        # 注意，ORM API中的数据表模型应该是一个类对象，可以使用"model(**data)"的方式创建一个实例对象，并将字典对象"data"作为参数传递给构造函数。
        await db.flush()
        await db.commit()

    async def generate_menu(self):
        """
        生成菜单数据并保存到数据库中
        :return:
        """
        # 首先调用"__generate_data"方法，传递两个参数，分别是表名"vadmin_auth_menu"和数据表模型"auth_models.VadminMenu"。
        # "vadmin_auth_menu"是菜单表的表名，"auth_models.VadminMenu"是使用SQLAlchemy ORM API定义的菜单数据表模型。
        await self.__generate_data("vadmin_auth_menu", auth_models.VadminMenu)

    async def generate_role(self):
        """
        生成角色数据并保存到数据库中
        :return:
        """
        # 首先调用"__generate_data"方法，传递两个参数，分别是表名"vadmin_auth_role"和数据表模型"auth_models.VadminRole"。
        # "vadmin_auth_role"是角色表的表名，"auth_models.VadminRole"是使用SQLAlchemy ORM API定义的角色数据表模型。
        await self.__generate_data("vadmin_auth_role", auth_models.VadminRole)

    async def generate_user(self):
        """
        生成用户
        :return:
        """
        await self.__generate_data("vadmin_auth_user", auth_models.VadminUser)

    async def generate_user_role(self):
        """
        生成用户角色数据并保存到数据库中
        :return:
        """
        # 首先调用"__generate_data"方法，传递两个参数，分别是表名"vadmin_auth_user_roles"和数据表模型"auth_models.vadmin_user_roles"。
        # "vadmin_auth_user_roles"是用户角色关联表的表名，"auth_models.vadmin_user_roles"是使用SQLAlchemy ORM API定义的用户角色关联数据表模型。
        await self.__generate_data("vadmin_auth_user_roles", auth_models.vadmin_user_roles)

    async def generate_system_tab(self):
        """
        生成系统配置分类数据并保存到数据库中
        :return:
        """
        # 首先调用"__generate_data"方法，传递两个参数，分别是表名"vadmin_system_settings_tab"和数据表模型"system_models.VadminSystemSettingsTab"。
        # "vadmin_system_settings_tab"是系统配置分类表的表名，"system_models.VadminSystemSettingsTab"是使用SQLAlchemy ORM API定义的系统配置分类数据表模型。
        await self.__generate_data("vadmin_system_settings_tab", system_models.VadminSystemSettingsTab)

    async def generate_system_config(self):
        """
        生成系统配置数据并保存到数据库中
        :return:
        """
        # 首先调用"__generate_data"方法，传递两个参数，分别是表名"vadmin_system_settings"和数据表模型"system_models.VadminSystemSettings"。
        # "vadmin_system_settings"是系统配置表的表名，"system_models.VadminSystemSettings"是使用SQLAlchemy ORM API定义的系统配置数据表模型。
        await self.__generate_data("vadmin_system_settings", system_models.VadminSystemSettings)

    async def generate_dict_type(self):
        """
        生成字典类型数据并保存到数据库中
        :return:
        """
        # 首先调用"__generate_data"方法，传递两个参数，分别是表名"vadmin_system_dict_type"和数据表模型"system_models.VadminDictType"。
        # "vadmin_system_dict_type"是字典类型表的表名，"system_models.VadminDictType"是使用SQLAlchemy ORM API定义的字典类型数据表模型。
        await self.__generate_data("vadmin_system_dict_type", system_models.VadminDictType)

    async def generate_dict_details(self):
        """
        生成字典详情数据并保存到数据库中
        :return:
        """
        # 首先调用"__generate_data"方法，传递两个参数，分别是表名"vadmin_system_dict_details"和数据表模型"system_models.VadminDictDetails"。
        # "vadmin_system_dict_details"是字典详情表的表名，"system_models.VadminDictDetails"是使用SQLAlchemy ORM API定义的字典详情数据表模型。
        await self.__generate_data("vadmin_system_dict_details", system_models.VadminDictDetails)

    async def run(self, env: Environment = Environment.pro):
        """
        执行初始化工作
        :param env:
        :return:
        """
        self.migrate_model(env)
        await self.generate_menu()
        await self.generate_role()
        await self.generate_user()
        await self.generate_user_role()
        await self.generate_system_tab()
        await self.generate_dict_type()
        await self.generate_system_config()
        await self.generate_dict_details()
        print(f"环境：{env} {VERSION} 数据已初始化完成")
