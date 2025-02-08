#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:56
# @Author   : 冉勇
# @File     : gen_table_do.py
# @Software : PyCharm
# @Desc     :
import datetime
from sqlalchemy import Column, ForeignKey, BigInteger, DateTime, String, text
from config.database import Base


class GenTable(Base):
    __tablename__ = "gen_table"

    table_id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True, comment='编号')

    table_name = Column(String(length=200), default='', comment='表名称')

    table_comment = Column(String(length=500), default='', comment='表描述')

    sub_table_name = Column(String(length=64), comment='关联子表的表名')

    sub_table_fk_name = Column(String(length=64), comment='子表关联的外键名')

    class_name = Column(String(length=100), default='', comment='实体类名称')

    tpl_category = Column(String(length=200), default='crud', comment='使用的模板（crud单表操作 tree树表操作）')

    tpl_web_type = Column(String(length=30), default='', comment='前端模板类型（element-ui模版 element-plus模版）')

    package_name = Column(String(length=100), comment='生成包路径')

    module_name = Column(String(length=30), comment='生成模块名')

    business_name = Column(String(length=30), comment='生成业务名')

    function_name = Column(String(length=50), comment='生成功能名')

    function_author = Column(String(length=50), comment='生成功能作者')

    gen_type = Column(String(length=1), default='0', comment='生成代码方式（0zip压缩包 1自定义路径）')

    gen_path = Column(String(length=200), default='/', comment='生成路径（不填默认项目路径）')

    options = Column(String(length=1000), comment='其它生成选项')

    create_by = Column(String(length=64), default='', comment='创建者')

    update_by = Column(String(length=64), default='', comment='更新者')

    remark = Column(String(length=500), comment='备注')

    del_flag = Column(
        String(1), nullable=False, default='0', server_default=text("'0'"), comment='删除标志（0代表存在 2代表删除）'
    )

    create_time = Column(DateTime, nullable=False, default=datetime.datetime.now, comment='创建时间')
    update_time = Column(
        DateTime, nullable=False, default=datetime.datetime.now,
        onupdate=datetime.datetime.now, index=True, comment='更新时间'
    )