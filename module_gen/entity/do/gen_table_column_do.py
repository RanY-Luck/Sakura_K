#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:52
# @Author   : 冉勇
# @File     : gen_table_column_do.py
# @Software : PyCharm
# @Desc     :
import datetime
from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, Integer, String, text
from config.database import BaseMixin, Base


class GenTableColumn(Base):
    __tablename__ = "gen_table_column"

    column_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='编号')

    table_id = Column(BigInteger, comment='归属表编号')

    column_name = Column(String(length=200), comment='列名称')

    column_comment = Column(String(length=500), comment='列描述')

    column_type = Column(String(length=100), comment='列类型')

    python_type = Column(String(length=500), comment='python类型')

    python_field = Column(String(length=200), comment='python字段名')

    is_pk = Column(String(length=1), comment='是否主键（1是）')

    is_increment = Column(String(length=1), comment='是否自增（1是）')

    is_required = Column(String(length=1), comment='是否必填（1是）')

    is_insert = Column(String(length=1), comment='是否为插入字段（1是）')

    is_edit = Column(String(length=1), comment='是否编辑字段（1是）')

    is_list = Column(String(length=1), comment='是否列表字段（1是）')

    is_query = Column(String(length=1), comment='是否查询字段（1是）')

    query_type = Column(String(length=200), default='EQ', comment='查询方式（等于、不等于、大于、小于、范围）')

    html_type = Column(String(length=200), comment='显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）')

    dict_type = Column(String(length=200), default='', comment='字典类型')

    sort = Column(Integer, comment='排序')

    create_by = Column(String(length=64), default='', comment='创建者')

    update_by = Column(String(length=64), default='', comment='更新者')

    del_flag = Column(
        String(1), nullable=False, default='0', server_default=text("'0'"),
        comment='删除标志（0代表存在 2代表删除）'
    )

    create_time = Column(DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    update_time = Column(
        DateTime, nullable=False, default=datetime.datetime.now,
        onupdate=datetime.datetime.now, index=True, comment='更新时间'
    )
