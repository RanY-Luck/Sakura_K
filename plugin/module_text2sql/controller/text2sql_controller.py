'''
Descripttion: Text2SQL控制器实现
version: 1.0.0
Author: 冉勇
Date: 2025-06-20 10:00:00
LastEditTime: 2025-06-20 10:00:00
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc    : Text2SQL控制器实现

from fastapi import APIRouter, Body, Depends
from typing import Optional
from utils.response_util import ResponseUtil
from module_admin.service.login_service import LoginService
from plugin.module_text2sql.service.text2sql_service import Text2SQLService

# 创建路由器，要求登录验证
text2sqlController = APIRouter(prefix="/text2sql", dependencies=[Depends(LoginService.get_current_user)])

# 获取服务实例
text2sql_service = Text2SQLService.get_instance()


@text2sqlController.post("/generate")
async def generate_sql(
    question: str = Body(..., description="自然语言问题")
):
    """
    将自然语言问题转换为SQL查询
    
    Args:
        question: 自然语言问题
    
    Returns:
        生成的SQL查询结果
    """
    result = text2sql_service.generate_sql(question)
    
    if result["success"]:
        return ResponseUtil.success(data=result)
    else:
        return ResponseUtil.error(msg=result["message"])


@text2sqlController.post("/execute")
async def execute_query(
    question: Optional[str] = Body(None, description="自然语言问题"),
    sql: Optional[str] = Body(None, description="SQL查询语句")
):
    """
    执行查询并返回结果
    
    Args:
        question: 自然语言问题（可选）
        sql: SQL查询语句（可选，与question二选一）
    
    Returns:
        查询结果
    """
    if not question and not sql:
        return ResponseUtil.error(msg="必须提供问题或SQL查询语句")
    
    result = text2sql_service.execute_query(question, sql)
    
    if result["success"]:
        return ResponseUtil.success(data=result)
    else:
        return ResponseUtil.error(msg=result["message"])


@text2sqlController.post("/train/example")
async def train_with_example(
    question: str = Body(..., description="问题示例"),
    sql: str = Body(..., description="对应的SQL查询")
):
    """
    使用示例训练模型
    
    Args:
        question: 问题示例
        sql: 对应的SQL查询
    
    Returns:
        训练结果
    """
    result = text2sql_service.train_with_example(question, sql)
    
    if result["success"]:
        return ResponseUtil.success(msg=result["message"])
    else:
        return ResponseUtil.error(msg=result["message"])


@text2sqlController.post("/train/schema")
async def train_database_schema():
    """
    训练数据库架构
    
    Returns:
        训练结果
    """
    result = text2sql_service.train_database_schema()
    
    if result["success"]:
        return ResponseUtil.success(msg=result["message"])
    else:
        return ResponseUtil.error(msg=result["message"])


@text2sqlController.post("/train/full")
async def run_full_training():
    """
    运行完整的训练流程
    
    Returns:
        训练结果
    """
    result = text2sql_service.run_full_training()
    
    if result["success"]:
        return ResponseUtil.success(msg=result["message"])
    else:
        return ResponseUtil.error(msg=result["message"])


@text2sqlController.get("/tables")
async def get_all_tables():
    """
    获取所有表信息
    
    Returns:
        所有表的信息
    """
    result = text2sql_service.get_all_tables()
    
    if result["success"]:
        return ResponseUtil.success(data=result)
    else:
        return ResponseUtil.error(msg=result["message"])


@text2sqlController.get("/tables/{table_name}")
async def get_table_info(table_name: str):
    """
    获取指定表的详细信息
    
    Args:
        table_name: 表名
    
    Returns:
        表的详细信息
    """
    result = text2sql_service.get_table_info(table_name)
    
    if result["success"]:
        return ResponseUtil.success(data=result)
    else:
        return ResponseUtil.error(msg=result["message"]) 