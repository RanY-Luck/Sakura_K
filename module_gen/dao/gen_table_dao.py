#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:56
# @Author   : 冉勇
# @File     : gen_table_dao.py
# @Software : PyCharm
# @Desc     :
from datetime import datetime, time
from datetime import datetime, time
from typing import List
from sqlalchemy import and_, delete, desc, func, or_, select, update, MetaData, text, not_, Table, Column, String, \
    DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from module_gen.entity.do.gen_table_do import GenTable
from module_gen.entity.vo.gen_table_vo import GenTablePageModel, GenTableModel
from utils.common_util import CamelCaseUtil
from utils.page_util import PageUtil, PageResponseModel



class GenTableDao:

    @classmethod
    async def get_by_id(cls, db: AsyncSession, gen_table_id: int) -> GenTable:
        """根据主键获取单条记录"""
        gen_table = (((await db.execute(
            select(GenTable)
            .where(GenTable.table_id == gen_table_id)
        ))
                      .scalars())
                     .first())
        return gen_table

    @classmethod
    async def get_by_table_name(cls, db: AsyncSession, table_name: str) -> GenTable:
        """根据名称获取单条记录"""
        gen_table = (((await db.execute(
            select(GenTable)
            .where(GenTable.table_name == table_name)
        ))
                      .scalars())
                     .first())
        return gen_table

    """
    查询
    """

    @classmethod
    async def get_gen_table_list(
            cls, db: AsyncSession,
            query_object: GenTablePageModel,
            data_scope_sql: str,
            is_page: bool = False
    ) -> PageResponseModel:

        query = (
            select(GenTable)
            .where(

                GenTable.table_id == query_object.table_id if query_object.table_id else True,

                GenTable.table_name.like(f"%{query_object.table_name}%") if query_object.table_name else True,

                GenTable.table_comment.like(f"%{query_object.table_comment}%") if query_object.table_comment else True,

                GenTable.sub_table_name.like(
                    f"%{query_object.sub_table_name}%"
                ) if query_object.sub_table_name else True,

                GenTable.sub_table_fk_name.like(
                    f"%{query_object.sub_table_fk_name}%"
                ) if query_object.sub_table_fk_name else True,

                GenTable.class_name.like(f"%{query_object.class_name}%") if query_object.class_name else True,

                GenTable.tpl_category.like(f"%{query_object.tpl_category}%") if query_object.tpl_category else True,

                GenTable.tpl_web_type.like(f"%{query_object.tpl_web_type}%") if query_object.tpl_web_type else True,

                GenTable.package_name.like(f"%{query_object.package_name}%") if query_object.package_name else True,

                GenTable.module_name.like(f"%{query_object.module_name}%") if query_object.module_name else True,

                GenTable.business_name.like(f"%{query_object.business_name}%") if query_object.business_name else True,

                GenTable.function_name.like(f"%{query_object.function_name}%") if query_object.function_name else True,

                GenTable.function_author.like(
                    f"%{query_object.function_author}%"
                ) if query_object.function_author else True,

                GenTable.gen_type.like(f"%{query_object.gen_type}%") if query_object.gen_type else True,

                GenTable.gen_path.like(f"%{query_object.gen_path}%") if query_object.gen_path else True,

                GenTable.options.like(f"%{query_object.options}%") if query_object.options else True,

                GenTable.create_by.like(f"%{query_object.create_by}%") if query_object.create_by else True,

                GenTable.create_time == query_object.create_time if query_object.create_time else True,

                GenTable.update_by.like(f"%{query_object.update_by}%") if query_object.update_by else True,

                GenTable.update_time == query_object.update_time if query_object.update_time else True,

                GenTable.remark.like(f"%{query_object.remark}%") if query_object.remark else True,

                eval(data_scope_sql),
            )
            .order_by(desc(GenTable.create_time))
            .distinct()
        )
        gen_table_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)
        return gen_table_list

    @classmethod
    async def add_gen_table(cls, db: AsyncSession, add_model: GenTableModel) -> GenTable:
        """
        增加
        """
        gen_table = GenTable(**add_model.model_dump(exclude_unset=True))
        db.add(gen_table)
        await db.flush()
        return gen_table

    @classmethod
    async def edit_gen_table(cls, db: AsyncSession, edit_model: GenTableModel, auto_commit: bool = True):
        """
        修改
        """
        edit_dict_data = edit_model.model_dump(exclude_unset=True)
        await db.execute(update(GenTable), [edit_dict_data])
        await db.flush()
        if auto_commit:
            await db.commit()
        return edit_model

    @classmethod
    async def del_gen_table(
            cls, db: AsyncSession, del_model: GenTableModel, soft_del: bool = True, auto_commit: bool = True
    ):
        """
        删除
        """
        if soft_del:
            await db.execute(update(GenTable).where(GenTable.table_id == del_model.id).values(del_flag='2'))
        else:
            await db.execute(delete(GenTable).where(GenTable.table_id == del_model.id))
        await db.flush()
        if auto_commit:
            await db.commit()

    @classmethod
    async def del_gen_table_by_ids(
            cls, db: AsyncSession, ids: List[int], soft_del: bool = True, auto_commit: bool = True
    ):
        """
        批量删除
        """
        if soft_del:
            await db.execute(update(GenTable).where(GenTable.table_id.in_(ids)).values(del_flag='2'))
        else:
            await db.execute(delete(GenTable).where(GenTable.table_id.in_(ids)))
        await db.flush()
        if auto_commit:
            await db.commit()

    # 定义查询方法
    @classmethod
    async def select_db_table_list(
            cls, session: AsyncSession, gen_table: GenTablePageModel, is_page=False
    ) -> PageResponseModel:
        """
        查询数据库中的表信息，根据 GenTable 入参动态添加过滤条件。
        """
        """查询数据库表列表"""
        query = (
            select(
                text("table_name"),
                text("table_comment"),
                text("create_time"),
                text("update_time"),
            )
            .select_from(text("information_schema.tables"))
            .where(
                and_(
                    text("table_schema = (select database())"),
                    text("table_name NOT LIKE 'qrtz\\_%'"),
                    text("table_name NOT LIKE 'gen\\_%'"),
                    text("table_name NOT IN (select table_name from gen_table)"),
                )
            )
        )
        # 动态条件构造
        if gen_table.table_name:
            query = query.where(
                text("lower(table_name) like lower(:table_name)")
            )
        if gen_table.table_comment:
            query = query.where(
                text("lower(table_comment) like lower(:table_comment)")
            )
        # 排序
        query = query.order_by(text("create_time DESC"))
        # 参数绑定
        params = {}
        if gen_table.table_name:
            params["table_name"] = f"%{gen_table.table_name}%"
        if gen_table.table_comment:
            params["table_comment"] = f"%{gen_table.table_comment}%"

        rows = await PageUtil.paginate(
            session, query.params(**params), gen_table.page_num, gen_table.page_size, is_page
        )
        return rows
        # 执行查询
        # result = await session.execute(query.params(**params))
        # rows = result.fetchall()
        # # 将结果映射到 GenTableResult 对象
        # return [
        #     GenTableModel(tableName=row[0], tableComment=row[1], createTime=row[2], updateTime=row[3]) for row in rows
        # ]

    @classmethod
    async def select_db_table_list_by_names(cls, session: AsyncSession, table_names: List[str]):
        """根据表名称查询数据库表信息"""
        table_str = ",".join([f"'{item}'" for item in table_names])
        if not table_names:
            return []
        query = select(
            text("table_name"),
            text("table_comment"),
            text("create_time"),
            text("update_time"),
        ).select_from(text('information_schema.tables')).where(
            and_(
                text("table_name NOT LIKE 'qrtz\\_%'"),
                text("table_name NOT LIKE 'gen\\_%'"),
                text("table_name NOT IN (select table_name from gen_table)"),
                text(f"table_name IN ({table_str})"),
                text("table_schema = (select database())")
            )
        )

        result = await session.execute(query)
        rows = result.fetchall()
        # return CamelCaseUtil.transform_result(rows)
        return [
            GenTableModel(tableName=row[0], tableComment=row[1], createTime=row[2], updateTime=row[3]) for row in rows
        ]

    @classmethod
    async def create_table(cls, session: AsyncSession, sql: str) -> bool:
        """ 创建表 """
        try:
            await session.execute(text(sql))
            # 提交事务
            await session.commit()
            await session.flush()
            return True
        except Exception as e:
            # 如果发生异常，回滚事务
            await session.rollback()
            print(f"创建表时发生错误: {e}")
            return False
