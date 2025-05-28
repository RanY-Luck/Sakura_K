#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/8 10:00
# @Author  : 冉勇
# @Site    : 
# @File    : text2sql_vo.py
# @Software: PyCharm
# @desc    : Text2SQL-pydantic模型

from pydantic import BaseModel, Field
from typing import Any, Optional, List, Dict, Union


class TrainRequest(BaseModel):
    """训练请求模型"""
    question: str = Field(default="", description="问题")
    sql: str = Field(default="", description="SQL语句")
    documentation: str = Field(default="", description="文档")
    ddl: str = Field(default="", description="DDL语句")
    use_schema: bool = Field(default=False, description="是否训练模式")
    supplier: str = Field(default="", description="AI供应商")


class AskRequest(BaseModel):
    """查询请求模型"""
    question: str = Field(..., description="问题")
    visualize: bool = Field(default=True, description="是否生成可视化")
    auto_train: bool = Field(default=True, description="是否自动训练成功的查询")
    supplier: str = Field(default="", description="AI供应商")


class SqlResult(BaseModel):
    """SQL执行结果模型"""
    sql: str = Field(..., description="生成的SQL语句")
    data: str = Field(..., description="数据结果的JSON字符串")


class TrainingData(BaseModel):
    """训练数据模型"""
    questions_and_sql: List[Dict[str, str]] = Field(default=[], description="问题和SQL配对")
    sql_only: List[str] = Field(default=[], description="仅SQL语句")
    documentation: List[str] = Field(default=[], description="训练文档") 