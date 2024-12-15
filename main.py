# # #!/usr/bin/env python
# # # -*- coding: utf-8 -*-
# # # @Time    : 2024/12/2 11:44
# # # @Author  : 冉勇
# # # @Site    :
# # # @File    : main.py
# # # @Software: PyCharm
# # # @desc    :
# # """
# # FastApi 更新文档：https://github.com/tiangolo/fastapi/releases
# # FastApi Github：https://github.com/tiangolo/fastapi
# # Typer 官方文档：https://typer.tiangolo.com/
# # """
# import typer
# from scripts.initialize.initialize import InitializeData, Environment
#
# shell_app = typer.Typer()
#
#
# @shell_app.command()
# def migrate(env: Environment = Environment.pro):
#     """
#     将模型迁移到数据库，更新数据库表结构
#     :param env: 指定数据库环境。如果没有提供该参数，则默认为 Environment.pro。
#     :return:
#     """
#     print("开始更新数据库表")
#     InitializeData.migrate_model(env)
#
#
# if __name__ == '__main__':
#     try:
#         shell_app()
#     except Exception as e:
#         raise e
