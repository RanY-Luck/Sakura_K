#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 10:31
# @Author   : 冉勇
# @File     : gen_table_column_service.py
# @Software : PyCharm
# @Desc     :
from typing import List
from module_gen.dao.gen_table_column_dao import GenTableColumnDao
from module_gen.entity.do.gen_table_column_do import GenTableColumn
from module_gen.entity.vo.gen_table_column_vo import GenTableColumnPageModel


class GenTableColumnService:
    """代码生成业务字段 服务层实现"""

    # @classmethod
    # async def select_gen_table_column_by_table_id(cls, table_id: int, query_db) -> List[GenTableColumn]:
    #     """查询业务字段列表"""
    #     return await GenTableColumnDao.get_gen_table_column_list(query_db, GenTableColumnPageModel(tableId=table_id))
    #
    #
    # async def insert_gen_table_column(cls, gen_table_column: GenTableColumn) -> int:
    #     """新增业务字段"""
    #     return await GenTableColumnDao.insert_gen_table_column(gen_table_column)
    #
    # async def update_gen_table_column(cls, gen_table_column: GenTableColumn) -> int:
    #     """修改业务字段"""
    #     return await GenTableColumnDao.update_gen_table_column(gen_table_column)
    #
    # async def delete_gen_table_column_by_ids(cls, ids: List[int]) -> int:
    #     """删除业务字段信息"""
    #     return await GenTableColumnDao.delete_gen_table_column_by_ids(ids)