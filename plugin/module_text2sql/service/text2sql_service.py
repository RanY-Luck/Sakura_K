#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-05-28 18:25:00
# @Author   : 冉勇
# @File     : text2sql_service.py
# @Software : PyCharm
# @Desc     : Text2SQL服务类，处理业务逻辑
import os
from typing import Dict, Any, Tuple, Optional, Union
import pandas as pd
from functools import lru_cache
from plugin.module_text2sql.core.vanna_text2sql import VannaServer


# 存储不同的 VannaServer 实例
vn_instances = {}


class Text2SQLService:
    """Text2SQL服务类，处理业务逻辑"""

    def __init__(self):
        """初始化服务"""
        pass

    def get_vn_instance(self, supplier: str = "") -> VannaServer:
        """
        获取或创建VannaServer实例，实现单例模式

        Args:
            supplier: AI服务提供商标识，默认从环境变量中获取

        Returns:
            对应提供商的VannaServer实例
        """
        if supplier == "":
            supplier = os.getenv("SUPPLIER", "GITEE")
        if supplier not in vn_instances:
            # 配置类
            config = {
                "supplier": supplier,
                "embedding_supplier": os.getenv("TEXT2SQL_EMBEDDING_SUPPLIER", "SiliconFlow"),
                "vector_db_path": os.getenv("VECTOR_DB_PATH", "vector_db"),
                "host": os.getenv("DB_HOST1"),
                "dbname": os.getenv("DB_NAME1"),
                "user": os.getenv("DB_USER1"),
                "password": os.getenv("DB_PASSWORD1"),
                "port": int(os.getenv("DB_PORT1", "3306"))
            }
            vn_instances[supplier] = VannaServer(config)
        return vn_instances[supplier]

    def train(self, supplier: str = "", question: str = "", sql: str = "", 
              documentation: str = "", ddl: str = "", schema: bool = False) -> bool:
        """
        训练Text2SQL模型

        Args:
            supplier: AI服务提供商标识
            question: 问题文本
            sql: SQL查询
            documentation: 文档说明
            ddl: DDL语句
            schema: 是否训练数据库模式

        Returns:
            训练是否成功的布尔值
        """
        try:
            server = self.get_vn_instance(supplier)
            server.vn_train(question=question, sql=sql, documentation=documentation, ddl=ddl)
            if schema:
                server.schema_train()
            return True
        except Exception as e:
            print(f"训练失败: {e}")
            return False

    @lru_cache(maxsize=128)
    def get_training_data(self, supplier: str = "") -> Dict[str, Any]:
        """
        获取训练数据

        Args:
            supplier: AI服务提供商标识

        Returns:
            训练数据字典
        """
        server = self.get_vn_instance(supplier)
        return server.get_training_data()

    def ask(self, question: str, visualize: bool = True, 
            auto_train: bool = True, supplier: str = "") -> Tuple[str, pd.DataFrame, Any]:
        """
        处理自然语言问题，生成SQL并执行

        Args:
            question: 自然语言问题
            visualize: 是否生成可视化
            auto_train: 是否自动训练成功的查询
            supplier: AI服务提供商标识

        Returns:
            SQL查询、结果数据和可视化图表的元组
        """
        server = self.get_vn_instance(supplier)
        return server.ask(
            question=question,
            visualize=visualize,
            auto_train=auto_train
        ) 