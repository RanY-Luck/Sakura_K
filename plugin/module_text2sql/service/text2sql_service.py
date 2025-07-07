'''
Descripttion: Text2SQL服务实现
version: 1.0.0
Author: 冉勇
Date: 2025-06-20 10:00:00
LastEditTime: 2025-06-20 16:40:44
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc    : Text2SQL服务实现

import logging
from typing import Dict, Any, Optional
from plugin.module_text2sql.core.text2sql_client import Text2SQLClient

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Text2SQLService:
    """Text2SQL服务类，提供自然语言到SQL的转换服务"""
    
    _instance = None
    
    @classmethod
    def get_instance(cls) -> 'Text2SQLService':
        """单例模式获取服务实例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def __init__(self):
        """初始化Text2SQL服务"""
        self.client = Text2SQLClient.get_instance()
    
    def generate_sql(self, question: str) -> Dict[str, Any]:
        """
        生成SQL查询
        
        Args:
            question: 自然语言问题
            
        Returns:
            Dict: 包含生成的SQL和相关信息
        """
        logger.info(f"生成SQL查询: {question}")
        return self.client.generate_sql(question)
    
    def execute_query(self, question: str = None, sql: str = None) -> Dict[str, Any]:
        """
        执行查询并返回结果
        
        Args:
            question: 自然语言问题（如果提供，将先转换为SQL）
            sql: 直接提供的SQL查询
            
        Returns:
            Dict: 包含查询结果和相关信息
        """
        if question:
            logger.info(f"根据问题执行查询: {question}")
        if sql:
            logger.info(f"直接执行SQL: {sql}")
        
        return self.client.execute_sql_query(question, sql)
    
    def train_with_example(self, question: str, sql: str) -> Dict[str, Any]:
        """
        使用示例训练模型
        
        Args:
            question: 问题示例
            sql: 对应的SQL查询
            
        Returns:
            Dict: 训练结果
        """
        logger.info(f"使用示例训练模型: 问题='{question}', SQL='{sql}'")
        return self.client.train_with_example(question, sql)
    
    def train_database_schema(self) -> Dict[str, Any]:
        """
        训练数据库架构
        
        Returns:
            Dict: 训练结果
        """
        logger.info("开始训练数据库架构")
        return self.client.train_database_schema()
    
    def run_full_training(self) -> Dict[str, Any]:
        """
        运行完整的训练流程
        
        Returns:
            Dict: 训练结果
        """
        logger.info("开始执行完整训练流程")
        return self.client.run_full_training()
    
    def get_all_tables(self) -> Dict[str, Any]:
        """
        获取所有表信息
        
        Returns:
            Dict: 包含所有表信息
        """
        logger.info("获取所有表信息")
        return self.client.get_all_tables()
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        获取指定表的详细信息
        
        Args:
            table_name: 表名
            
        Returns:
            Dict: 表的详细信息
        """
        logger.info(f"获取表 {table_name} 的详细信息")
        return self.client.get_table_info(table_name)
        
    def ask(self, question: str, auto_train: bool = False, visualize: bool = False) -> Dict[str, Any]:
        """
        回答问题（兼容性方法）
        
        Args:
            question: 自然语言问题
            auto_train: 是否自动训练成功的查询
            visualize: 是否生成可视化代码
        
        Returns:
            Dict: 包含回答和生成的SQL
        """
        logger.info(f"回答问题: {question}, auto_train={auto_train}, visualize={visualize}")
        # 先生成SQL
        sql_result = self.client.generate_sql(question)
        
        if not sql_result["success"]:
            return {
                "success": False,
                "message": sql_result["message"],
                "sql": None,
                "result": None
            }
        
        # 执行生成的SQL
        query_result = self.client.execute_sql_query(sql=sql_result["sql"])
        
        # 如果成功且需要自动训练，则保存这个示例
        if auto_train and query_result["success"]:
            try:
                self.client.train_with_example(question=question, sql=sql_result["sql"])
                logger.info(f"自动训练成功: 问题='{question}', SQL='{sql_result['sql']}'")
            except Exception as e:
                logger.warning(f"自动训练失败: {str(e)}")
        
        # 组合结果
        result = {
            "success": True,
            "sql": sql_result["sql"],
            "result": query_result.get("data", []),
            "columns": query_result.get("columns", []),
            "summary": query_result.get("summary", "")
        }
        
        # 如果需要可视化，尝试生成Plotly代码
        if visualize and query_result.get("success", False) and query_result.get("data"):
            try:
                # 这里我们只返回一个简单的提示，因为完整实现可视化代码生成超出范围
                result["plotly_code"] = "# 可视化代码生成功能需要单独实现"
            except Exception as e:
                logger.warning(f"生成可视化代码失败: {str(e)}")
        
        return result 