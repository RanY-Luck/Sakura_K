#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:51
# @Author   : 冉勇
# @File     : gen_table_column_dao.py
# @Software : PyCharm
# @Desc     :
from datetime import datetime, time
from typing import List
from sqlalchemy import and_, delete, desc, func, or_, select, update, text, case, asc
from sqlalchemy.ext.asyncio import AsyncSession
from module_gen.entity.do.gen_table_column_do import GenTableColumn
from module_gen.entity.vo.gen_table_column_vo import GenTableColumnPageModel, GenTableColumnModel
from utils.page_util import PageUtil, PageResponseModel


class GenTableColumnDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, gen_table_column_id: int) -> GenTableColumn:
        """根据主键获取单条记录"""
        gen_table_column = (((await db.execute(
            select(GenTableColumn)
            .where(GenTableColumn.column_id == gen_table_column_id)
        ))
                             .scalars())
                            .first())
        return gen_table_column

    """
    查询
    """

    @classmethod
    async def get_gen_table_column_list(
            cls, db: AsyncSession,
            query_object: GenTableColumnPageModel,
            data_scope_sql: str = None,
            is_page: bool = False
    ) -> PageResponseModel | list:

        query = (
            select(GenTableColumn)
            .where(

                GenTableColumn.column_id == query_object.column_id if query_object.column_id else True,

                GenTableColumn.table_id == query_object.table_id if query_object.table_id else True,

                GenTableColumn.column_name.like(f"%{query_object.column_name}%") if query_object.column_name else True,

                GenTableColumn.column_comment.like(
                    f"%{query_object.column_comment}%"
                ) if query_object.column_comment else True,

                GenTableColumn.column_type.like(f"%{query_object.column_type}%") if query_object.column_type else True,

                GenTableColumn.python_type.like(f"%{query_object.python_type}%") if query_object.python_type else True,

                GenTableColumn.python_field.like(
                    f"%{query_object.python_field}%"
                ) if query_object.python_field else True,

                GenTableColumn.is_pk.like(f"%{query_object.is_pk}%") if query_object.is_pk else True,

                GenTableColumn.is_increment.like(
                    f"%{query_object.is_increment}%"
                ) if query_object.is_increment else True,

                GenTableColumn.is_required.like(f"%{query_object.is_required}%") if query_object.is_required else True,

                GenTableColumn.is_insert.like(f"%{query_object.is_insert}%") if query_object.is_insert else True,

                GenTableColumn.is_edit.like(f"%{query_object.is_edit}%") if query_object.is_edit else True,

                GenTableColumn.is_list.like(f"%{query_object.is_list}%") if query_object.is_list else True,

                GenTableColumn.is_query.like(f"%{query_object.is_query}%") if query_object.is_query else True,

                GenTableColumn.query_type.like(f"%{query_object.query_type}%") if query_object.query_type else True,

                GenTableColumn.html_type.like(f"%{query_object.html_type}%") if query_object.html_type else True,

                GenTableColumn.dict_type.like(f"%{query_object.dict_type}%") if query_object.dict_type else True,

                GenTableColumn.sort == query_object.sort if query_object.sort else True,

                GenTableColumn.create_by.like(f"%{query_object.create_by}%") if query_object.create_by else True,

                GenTableColumn.create_time == query_object.create_time if query_object.create_time else True,

                GenTableColumn.update_by.like(f"%{query_object.update_by}%") if query_object.update_by else True,

                GenTableColumn.update_time == query_object.update_time if query_object.update_time else True,

                eval(data_scope_sql) if data_scope_sql else True,
            )
            .order_by(asc(GenTableColumn.column_name))
            .distinct()
        )
        gen_table_column_list = await PageUtil.paginate(
            db, query, query_object.page_num, query_object.page_size, is_page
        )
        return gen_table_column_list

    @classmethod
    async def add_gen_table_column(cls, db: AsyncSession, add_model: GenTableColumnModel) -> GenTableColumn:
        """
        增加
        """
        gen_table_column = GenTableColumn(**add_model.model_dump(exclude_unset=True))
        db.add(gen_table_column)
        await db.flush()
        return gen_table_column

    @classmethod
    async def edit_gen_table_column(cls, db: AsyncSession, edit_model: GenTableColumnModel, auto_commit: bool = True):
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=False)
        await db.execute(update(GenTableColumn), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return edit_model

    @classmethod
    async def del_gen_table_column(
            cls, db: AsyncSession, del_model: GenTableColumnModel, soft_del: bool = True, auto_commit: bool = True
    ):
        """
        删除
        """
        if soft_del:
            await db.execute(
                update(GenTableColumn).where(GenTableColumn.column_id == del_model.column_id).values(del_flag='2')
            )
        else:
            await db.execute(delete(GenTableColumn).where(GenTableColumn.column_id == del_model.column_id))
        await db.flush()
        if auto_commit:
            await db.commit()

    @classmethod
    async def del_gen_table_column_by_table_ids(
            cls, db: AsyncSession, table_ids: List[int], soft_del: bool = True, auto_commit: bool = True
    ):
        """
        删除
        """
        if soft_del:
            await db.execute(update(GenTableColumn).where(GenTableColumn.table_id.in_(table_ids)).values(del_flag='2'))
        else:
            await db.execute(delete(GenTableColumn).where(GenTableColumn.table_id.in_(table_ids)))
        await db.flush()
        if auto_commit:
            await db.commit()

    @classmethod
    async def select_db_table_columns_by_name(cls, session: AsyncSession, table_name: str) -> List[GenTableColumnModel]:
        """
        查询指定表的列信息。
        :param session: AsyncSession 数据库会话
        :param table_name: 表名
        :return: 查询结果映射到 GenTableColumnResult 对象的列表
        """
        # 检查表名是否为空
        if not table_name:
            raise ValueError("Table name cannot be empty.")

        # 基础查询
        query = text(
            """
                    SELECT column_name,
                           (CASE WHEN (is_nullable = 'no' AND column_key != 'PRI') THEN '1' ELSE '0' END) AS is_required,
                           (CASE WHEN column_key = 'PRI' THEN '1' ELSE '0' END) AS is_pk,
                           ordinal_position AS sort,
                           column_comment,
                           (CASE WHEN extra = 'auto_increment' THEN '1' ELSE '0' END) AS is_increment,
                           column_type
                    FROM information_schema.columns
                    WHERE table_schema = (SELECT DATABASE())
                    AND table_name = :table_name
                    ORDER BY ordinal_position
                """
        )

        # 执行查询并传递参数
        result = await session.execute(query, {"table_name": table_name})
        rows = result.fetchall()
        # 将结果映射到 GenTableColumnResult 对象
        return [
            GenTableColumnModel(
                columnName=row[0],
                isRequired=row[1],
                isPk=row[2],
                sort=row[3],
                columnComment=row[4],
                isIncrement=row[5],
                columnType=row[6]
            )
            for row in rows
        ]
