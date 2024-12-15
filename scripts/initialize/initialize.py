# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2024/12/2 11:46
# # @Author  : 冉勇
# # @Site    :
# # @File    : initialize.py
# # @Software: PyCharm
# # @desc    :
# import os
# import subprocess
# from enum import Enum
# from application.settings import BASE_DIR, VERSION
#
#
# class Environment(str, Enum):
#     dev = "dev"
#     pro = "pro"
#
#
# class InitializeData:
#     """
#     初始化数据
#
#     生成步骤：
#         1. 读取数据
#         2. 获取数据库
#         3. 创建数据
#     """
#
#     SCRIPT_DIR = os.path.join(BASE_DIR, 'scripts', 'initialize')
#
#     def __init__(self):
#         self.sheet_names = []
#         self.datas = {}
#         self.ex = None
#         self.db = None
#         self.__get_sheet_data()
#
#     @classmethod
#     def migrate_model(cls, env: Environment = Environment.pro):
#         """
#         模型迁移映射到数据库
#         """
#         subprocess.check_call(
#             ['alembic', '--name', f'{env.value}', 'revision', '--autogenerate', '-m', f'{VERSION}'], cwd=BASE_DIR
#         )
#         subprocess.check_call(['alembic', '--name', f'{env.value}', 'upgrade', 'head'], cwd=BASE_DIR)
#         print(f"环境：{env}  {VERSION} 数据库表迁移完成")
#
#     def __get_sheet_data(self):
#         """
#         获取工作区数据
#         """
#         for sheet in self.sheet_names:
#             sheet_data = []
#             self.ex.open_sheet(sheet)
#             headers = self.ex.get_header()
#             datas = self.ex.readlines(min_row=2, max_col=len(headers))
#             for row in datas:
#                 sheet_data.append(dict(zip(headers, row)))
#             self.datas[sheet] = sheet_data
#
#     async def run(self, env: Environment = Environment.pro):
#         """
#         执行初始化工作
#         """
#         self.migrate_model(env)
#         print(f"环境：{env} {VERSION} 数据已初始化完成")
