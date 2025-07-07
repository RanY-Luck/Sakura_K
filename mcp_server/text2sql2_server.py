#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/6/18 9:42
# @Author   : 冉勇
# @File     : text2sql2_server.py
# @Software : PyCharm
# @Desc     : Text2SQL2 MCP服务

import os
import time
import json
import sys
import logging
import pandas as pd
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP

# 配置日志
logging.basicConfig(level=logging.INFO,
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 添加模块路径
sys.path.append('.')

# 初始化 MCP 服务器
mcp = FastMCP("Text2SQL2McpServer")

# 导入text2sql2模块
try:
    from text2sql2.text2sql import vn, MyVanna
    logger.info("成功导入 text2sql2 模块")
except Exception as e:
    logger.error(f"导入 text2sql2 模块失败: {str(e)}")
    vn = None

# 从text2sql2.train导入训练器
try:
    from text2sql2.train import VannaTrainer
    trainer = VannaTrainer(vn) if vn else None
    logger.info("成功导入 VannaTrainer")
except Exception as e:
    logger.error(f"导入 VannaTrainer 失败: {str(e)}")
    trainer = None


# 工具验证函数
def validate_tool(func):
    """验证工具函数的签名和参数"""
    # 这里可以添加更多验证逻辑
    return func


@mcp.tool()
@validate_tool
async def sql_query(question: str) -> Dict[str, Any]:
    """
    将自然语言问题转换为SQL并执行查询
    
    :param question: 用户的自然语言问题
    :return: 包含SQL和查询结果的字典
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }
    
    try:
        logger.info(f"处理问题: {question}")
        start_time = time.time()
        
        # 生成SQL
        sql = vn.generate_sql(question)
        if not sql:
            return {
                "success": False,
                "message": "无法生成SQL查询",
                "sql_query": ""
            }
            
        logger.info(f"生成的SQL: {sql}")
        
        # 执行SQL查询
        df = vn.run_sql(sql)
        execution_time = f"{time.time() - start_time:.2f}秒"
        
        # 如果为空，返回空结果
        if df is None or df.empty:
            return {
                "success": True,
                "sql_query": sql,
                "execution_time": execution_time,
                "row_count": 0,
                "results": []
            }
            
        # 转换为字典列表
        results = df.to_dict(orient='records')
        row_count = len(results)
        
        # 生成总结（如果结果不为空）
        summary = vn.generate_summary(question, df) if row_count > 0 else ""
        
        return {
            "success": True,
            "sql_query": sql,
            "execution_time": execution_time,
            "row_count": row_count,
            "results": results,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"SQL查询失败: {str(e)}")
        return {
            "success": False,
            "message": f"查询失败: {str(e)}",
            "sql_query": sql if 'sql' in locals() else ""
        }


@mcp.tool()
@validate_tool
async def execute_sql(sql: str) -> Dict[str, Any]:
    """
    直接执行SQL语句并返回结果
    
    :param sql: 要执行的SQL语句
    :return: 包含执行结果的字典
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }
    
    try:
        logger.info(f"执行SQL: {sql}")
        start_time = time.time()
        
        # 执行SQL查询
        df = vn.run_sql(sql)
        execution_time = f"{time.time() - start_time:.2f}秒"
        
        # 如果为空，返回空结果
        if df is None or df.empty:
            return {
                "success": True,
                "sql_query": sql,
                "execution_time": execution_time,
                "row_count": 0,
                "results": []
            }
            
        # 转换为字典列表
        results = df.to_dict(orient='records')
        row_count = len(results)
        
        return {
            "success": True,
            "sql_query": sql,
            "execution_time": execution_time,
            "row_count": row_count,
            "results": results
        }
    except Exception as e:
        logger.error(f"执行SQL失败: {str(e)}")
        return {
            "success": False,
            "message": f"执行失败: {str(e)}",
            "sql_query": sql
        }


@mcp.tool()
@validate_tool
async def get_table_info(table_name: str) -> Dict[str, Any]:
    """
    获取指定表的详细信息
    
    :param table_name: 表名
    :return: 包含表结构和样本数据的字典
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }
    
    try:
        # 检查表是否存在
        all_tables = vn.run_sql("SHOW TABLES")
        table_list = all_tables.iloc[:, 0].tolist()
        
        if table_name not in table_list:
            return {
                "success": False,
                "message": f"表 '{table_name}' 不存在",
                "table_name": table_name
            }
        
        # 获取表注释
        table_status = vn.run_sql(f"SHOW TABLE STATUS WHERE Name = '{table_name}'")
        comment = table_status['Comment'].iloc[0] if not table_status.empty else ""
        
        # 获取表结构
        columns_info = vn.run_sql(f"DESCRIBE `{table_name}`")
        
        # 获取主键信息
        primary_keys = []
        try:
            primary_key_info = vn.run_sql(f"SHOW KEYS FROM `{table_name}` WHERE Key_name = 'PRIMARY'")
            if not primary_key_info.empty:
                primary_keys = primary_key_info['Column_name'].tolist()
        except:
            pass
        
        # 转换列信息为更详细的格式
        columns = []
        for _, row in columns_info.iterrows():
            is_primary = row['Field'] in primary_keys
            column_info = {
                "name": row['Field'],
                "type": row['Type'],
                "nullable": row['Null'] == 'YES',
                "default": row['Default'],
                "is_primary": is_primary,
                "comment": ""  # MySQL DESCRIBE不返回注释
            }
            columns.append(column_info)
        
        # 获取表行数
        count_result = vn.run_sql(f"SELECT COUNT(*) as count FROM `{table_name}`")
        row_count = count_result['count'].iloc[0] if not count_result.empty else 0
        
        # 获取样本数据
        sample_data = []
        if row_count > 0:
            sample_result = vn.run_sql(f"SELECT * FROM `{table_name}` LIMIT 10")
            sample_data = sample_result.to_dict(orient='records')
        
        return {
            "success": True,
            "table_name": table_name,
            "comment": comment,
            "row_count": row_count,
            "columns": columns,
            "sample_data": sample_data
        }
    except Exception as e:
        logger.error(f"获取表信息失败: {str(e)}")
        return {
            "success": False,
            "message": f"获取表信息失败: {str(e)}",
            "table_name": table_name
        }


@mcp.tool()
@validate_tool
async def get_all_tables() -> Dict[str, Any]:
    """
    获取数据库中所有表的列表和基本信息
    
    :return: 包含所有表信息的字典
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }
    
    try:
        # 获取当前数据库名
        db_info = vn.run_sql("SELECT DATABASE() as db")
        database = db_info['db'].iloc[0] if not db_info.empty else "未知数据库"
        
        # 获取所有表
        tables_result = vn.run_sql("SHOW TABLES")
        if tables_result.empty:
            return {
                "success": True,
                "database": database,
                "table_count": 0,
                "tables": []
            }
        
        table_names = tables_result.iloc[:, 0].tolist()
        
        # 获取表状态信息
        tables_status = vn.run_sql("SHOW TABLE STATUS")
        
        # 构建表信息列表
        tables_info = []
        for table in table_names:
            try:
                # 从表状态中获取信息
                table_row = tables_status[tables_status['Name'] == table]
                comment = table_row['Comment'].iloc[0] if not table_row.empty else ""
                rows = table_row['Rows'].iloc[0] if not table_row.empty else 0
                
                # 获取列信息
                columns_info = vn.run_sql(f"DESCRIBE `{table}`")
                
                table_info = {
                    "table_name": table,
                    "comment": comment,
                    "row_count": rows,
                    "columns": columns_info['Field'].tolist()
                }
                tables_info.append(table_info)
            except Exception as e:
                logger.error(f"获取表 {table} 信息时出错: {str(e)}")
                tables_info.append({
                    "table_name": table,
                    "comment": "获取信息出错",
                    "row_count": 0,
                    "columns": []
                })
        
        return {
            "success": True,
            "database": database,
            "table_count": len(tables_info),
            "tables": tables_info
        }
    except Exception as e:
        logger.error(f"获取所有表信息失败: {str(e)}")
        return {
            "success": False,
            "message": f"获取所有表信息失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def train_sql_example(question: str, sql: str) -> Dict[str, Any]:
    """
    训练一个自然语言问题和对应的SQL对
    
    :param question: 自然语言问题
    :param sql: 对应的SQL语句
    :return: 训练结果
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }
    
    try:
        logger.info(f"训练SQL示例 - 问题: {question}, SQL: {sql}")
        
        # 使用Vanna的train方法
        vn.train(question=question, sql=sql)
        
        return {
            "success": True,
            "message": "训练成功",
            "data": {
                "question": question,
                "sql": sql
            }
        }
    except Exception as e:
        logger.error(f"训练SQL示例失败: {str(e)}")
        return {
            "success": False,
            "message": f"训练失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def train_database_schema() -> Dict[str, Any]:
    """
    训练数据库模式，包括表结构和关系
    
    :return: 训练结果
    """
    if trainer is None:
        return {
            "success": False,
            "message": "VannaTrainer未正确初始化"
        }
    
    try:
        logger.info("开始训练数据库模式...")
        
        # 使用VannaTrainer的训练方法
        success = trainer.train_database_structure()
        
        if success:
            return {
                "success": True,
                "message": "数据库模式训练成功"
            }
        else:
            return {
                "success": False,
                "message": "数据库模式训练失败，请检查日志"
            }
    except Exception as e:
        logger.error(f"训练数据库模式失败: {str(e)}")
        return {
            "success": False,
            "message": f"训练失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def train_with_examples() -> Dict[str, Any]:
    """
    使用动态生成的示例问题训练模型
    
    :return: 训练结果
    """
    if trainer is None:
        return {
            "success": False,
            "message": "VannaTrainer未正确初始化"
        }
    
    try:
        logger.info("开始训练示例问题...")
        
        # 使用VannaTrainer的示例训练方法
        trainer.add_example_questions()
        
        return {
            "success": True,
            "message": "示例问题训练成功"
        }
    except Exception as e:
        logger.error(f"训练示例问题失败: {str(e)}")
        return {
            "success": False,
            "message": f"训练失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def run_full_training() -> Dict[str, Any]:
    """
    运行完整的训练流程，包括数据库模式和示例问题
    
    :return: 训练结果
    """
    if trainer is None:
        return {
            "success": False,
            "message": "VannaTrainer未正确初始化"
        }
    
    try:
        logger.info("开始执行完整训练流程...")
        
        # 使用VannaTrainer的完整训练流程
        success = trainer.full_training_pipeline()
        
        if success:
            return {
                "success": True,
                "message": "完整训练流程执行成功"
            }
        else:
            return {
                "success": False,
                "message": "训练流程执行失败，请检查日志"
            }
    except Exception as e:
        logger.error(f"执行训练流程失败: {str(e)}")
        return {
            "success": False,
            "message": f"训练失败: {str(e)}"
        }


@mcp.resource("text2sql2://health")
async def health_check():
    """服务健康检查"""
    try:
        # 检查模块是否可用
        module_status = vn is not None
        
        # 尝试获取所有表
        db_status = False
        if module_status:
            try:
                vn.run_sql("SHOW TABLES")
                db_status = True
            except:
                db_status = False
        
        return {
            "status": "ok" if (module_status and db_status) else "degraded",
            "services": {
                "text2sql2_module": "ok" if module_status else "error",
                "database": "ok" if db_status else "error",
            },
            "timestamp": time.time(),
            "service": "Text2SQL2McpServer",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }


# 服务器启动入口点
if __name__ == "__main__":
    # 注册事件已经在上面使用装饰器完成
    logger.info("Text2SQL2 MCP服务器启动...")
    # 启动服务器
    mcp.run() 