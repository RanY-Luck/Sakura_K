#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 17:36
# @Author  : 冉勇
# @Site    : 
# @File    : import_manage.py
# @Software: PyCharm
# @desc    : 数据导入管理
from enum import Enum
from typing import List

from fastapi import UploadFile

from core.exception import CustomException
from utils import status
from utils.file.file_manage import FileManage
from .excel_manage import ExcelManage
from .write_xlsx import WriteXlsx
from ..tools import list_dict_find


class FieldType(Enum):
    list = "list"
    str = "str"


class ImportManage:
    """
    数据导入管理
    只支持导入 .xlsx 后缀类型的文件
    """
    file_type = ["application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]

    def __init__(self, file: UploadFile, headers: List[dict]):
        self.__table_data = None
        self.__table_header = None
        self.__filename = None
        self.errors = []
        self.success = []
        self.success_number = 0
        self.error_number = 0
        self.check_file_type(file)
        self.file = file
        self.headers = headers

    @classmethod
    def check_file_type(cls, file: UploadFile) -> None:
        """
        验证文件类型
        """
        if file.content_type not in cls.file_type:
            raise CustomException(msg="文件类型必须为xlsx类型", code=status.HTTP_ERROR)

    async def get_table_data(self, header_row: int = 1, data_row: int = 2) -> None:
        """
        获取表格数据与表头
        :param header_row: 表头在第几行
        :param data_row: 数据开始行
        """
        self.__filename = await FileManage.save_tmp_file(self.file)
        es = ExcelManage()
        es.open_sheet(file=self.__filename, read_only=True)
        self.__table_header = es.get_header(header_row, len(self.headers), asterisk=True)
        self.__table_data = es.readlines(min_row=data_row, max_col=len(self.headers))
        es.close()

    def check_table_data(self) -> None:
        """
        检查表格数据
        :return:
        """
        for row in self.__table_data:
            result = self.__check_row(row)
            if not result[0]:
                row.append(result[1])
                self.errors.append(row)
                self.error_number += 1
            else:
                self.success_number += 1
                self.success.append(result[1])

    def __check_row(self, row: list) -> tuple:
        """
        检查行数据
        检查条件：
        1、检查是否为必填项
        2、检查是否为选项列表
        3、检查是否符合规则
        :param row: 列表形式的一行数据（每个元素为单元格的值）。
        :return:
        代码解释：
        首先定义一个空字典 data，用于存储转换后的数据。
        然后循环遍历每个单元格 cell，根据单元格所在列的配置信息 field 进行不同的处理：
        1、如果单元格的值为空，但是该列必填，则返回 False 和错误提示信息。
        2、如果单元格有值，且该列是选项列表，则检查该值是否为选项列表中的合法值，如果是，则将其转换为选项列表中对应的值 value；否则返回 False 和错误提示信息。
        3、如果单元格有值，且该列有规则验证，则逐个调用规则函数，验证该值是否符合规则，如果不符合则返回 False 和错误提示信息。
        4、如果单元格有值，且该列没有规则验证，则将单元格的值赋给对应的字段 key 并加入 data 中。如果该列是列表类型，则需要将值转换成列表形式。
        最后将该行原始数据列表 old_data_list 也加入 data 中，并返回 True 和转换后的字典数据。
        """
        data = {}
        for index, cell in enumerate(row):
            value = cell
            field = self.headers[index]
            label = self.__table_header[index]
            if not cell and field.get("required", False):
                return False, f"{label}不能为空！"
            elif field.get("options", []) and cell:
                item = list_dict_find(field.get("options", []), "label", cell)
                if item:
                    value = item.get("value")
                else:
                    return False, f"请选择正确的{label}"
            elif field.get("rules", []) and cell:
                rules = field.get("rules")
                for validator in rules:
                    try:
                        validator(str(cell))
                    except ValueError as e:
                        return False, f"{label}：{e.__str__()}"
            if value:
                field_type = field.get("type", FieldType.str)
                if field_type == FieldType.list:
                    data[field.get("field")] = [value]
                elif field_type == FieldType.str:
                    data[field.get("field")] = str(value)
            else:
                data[field.get("field")] = value
        data["old_data_list"] = row
        return True, data

    def generate_error_url(self) -> str:
        """
        生成用户导入失败数据的 Excel 文件，并返回该文件的链接
        :return:
        代码解释：
        首先判断错误数量 self.error_number 是否小于等于 0，如果是则直接返回空字符串。
        如果错误数量大于 0，创建一个 WriteXlsx 的对象 em，并调用该对象的 generate_template 方法生成 Excel 文件的头部和表格格式。
        generate_template 方法会根据传入的 headers，自动生成表头信息，并根据字段类型、选项以及保留小数位等参数设置对应单元格的格式。max_row 参数表示表格最大行数。
        接着将错误信息 self.errors 写入 Excel 文件中，使用 em 的 write_list 方法将错误列表写入到表格中。
        最后调用 em 对象的 close 方法关闭 Excel 文件，并返回文件链接 em.file_url。
        """
        if self.error_number <= 0:
            return ""
        em = WriteXlsx(sheet_name="用户导入失败数据")
        em.generate_template(self.headers, max_row=self.error_number)
        em.write_list(self.errors)
        em.close()
        return em.file_url

    def add_error_data(self, row: dict) -> None:
        """
        将导入数据中有错误的行添加到错误列表并更新错误数量和成功数量
        :param row: 字典形式的一行数据
        :return:
        代码解释：
        首先将错误数据 row 加入到错误列表 self.errors 中。
        然后将错误数量 self.error_number 加 1，表示当前导入数据中有一个错误。
        最后将成功数量 self.success_number 减 1，表示当前导入数据的总成功数量减 1。
        """
        self.errors.append(row)
        self.error_number += 1
        self.success_number -= 1
