#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/28 18:10
# @Author  : 冉勇
# @Site    : 
# @File    : text2sql_service.py
# @Software: PyCharm
# @desc    : 文本转SQL服务层
import os
from typing import Dict, List, Any
from utils.log_util import logger
from mcp_server.text2sql.vanna_text2sql import VannaServer


class Text2SqlService:
    """文本转SQL服务类，封装VannaServer的调用逻辑"""

    # 存储不同提供商的VannaServer实例
    _vn_instances = {}

    @classmethod
    async def _get_vn_instance(cls, supplier: str = "") -> VannaServer:
        """
        获取或创建VannaServer实例（单例模式）
        
        Args:
            supplier: AI服务提供商，默认使用环境变量中配置的提供商
            
        Returns:
            VannaServer实例
        """
        if not supplier:
            supplier = os.getenv("SUPPLIER", "GITEE")

        if supplier not in cls._vn_instances:
            logger.info(f"创建新的VannaServer实例，提供商: {supplier}")
            try:
                # 获取数据库配置
                db_host = os.getenv("DB_HOST1")
                db_name = os.getenv("DB_NAME1")
                db_user = os.getenv("DB_USER1")
                db_password = os.getenv("DB_PASSWORD1")
                db_port = os.getenv("DB_PORT1")

                # 记录数据库连接信息
                logger.info(f"数据库连接参数: host={db_host}, database={db_name}, user={db_user}, port={db_port}")

                # 构建配置，包含多种参数命名方式以确保兼容性
                config = {
                    "supplier": supplier,
                    "embedding_supplier": "SiliconFlow",
                    "vector_db_path": os.getenv("VECTOR_DB_PATH"),
                    "host": db_host,
                    "database": db_name,  # 新版参数名
                    "db_name": db_name,  # 旧版参数名
                    "dbname": db_name,  # 另一种可能的参数名
                    "user": db_user,
                    "password": db_password,
                    "port": int(db_port)  # 确保端口是整数
                }

                # 创建VannaServer实例
                cls._vn_instances[supplier] = VannaServer(config)
                logger.info(f"VannaServer实例创建成功: {supplier}")
            except Exception as e:
                logger.error(f"创建VannaServer实例失败: {str(e)}")
                raise Exception(f"初始化Text2SQL服务失败: {str(e)}")

        return cls._vn_instances[supplier]

    @classmethod
    async def train_service(
            cls,
            question: str = "",
            sql: str = "",
            documentation: str = "",
            ddl: str = "",
            schema: bool = False,
            supplier: str = ""
    ) -> Dict[str, Any]:
        """
        训练文本到SQL模型
        
        Args:
            question: 训练问题
            sql: SQL语句
            documentation: 文档
            ddl: DDL语句
            schema: 是否训练数据库模式
            supplier: AI服务提供商
            
        Returns:
            训练结果
        """
        # 验证至少有一个参数不为空
        if not any([question, sql, documentation, ddl, schema]):
            raise ValueError("至少需要提供一个训练参数(question, sql, documentation, ddl, schema)")

        try:
            # 获取VannaServer实例
            server = await cls._get_vn_instance(supplier)

            # 训练模型
            if question or sql or documentation or ddl:
                logger.info(
                    f"开始训练: question={bool(question)}, sql={bool(sql)}, documentation={bool(documentation)}, ddl={bool(ddl)}"
                )
                server.vn_train(
                    question=question,
                    sql=sql,
                    documentation=documentation,
                    ddl=ddl
                )

            # 如果需要训练数据库模式
            if schema:
                logger.info("开始训练数据库模式")
                server.schema_train()

            return {"status": "success", "message": "训练成功"}
        except Exception as e:
            logger.error(f"训练失败: {str(e)}")
            raise Exception(f"训练失败: {str(e)}")

    @classmethod
    async def get_training_data_service(cls, supplier: str = "") -> List[Dict[str, Any]]:
        """
        获取训练数据
        
        Args:
            supplier: AI服务提供商
            
        Returns:
            训练数据列表
        """
        try:
            # 获取VannaServer实例
            server = await cls._get_vn_instance(supplier)

            # 获取训练数据
            training_data = server.get_training_data()
            logger.info(f"成功获取训练数据，包含{len(training_data)}条记录")

            return training_data
        except Exception as e:
            logger.error(f"获取训练数据失败: {str(e)}")
            raise Exception(f"获取训练数据失败: {str(e)}")

    @classmethod
    async def ask_service(
            cls,
            question: str,
            visualize: bool = True,
            auto_train: bool = True,
            supplier: str = ""
    ) -> Dict[str, Any]:
        """
        处理自然语言问题并转换为SQL查询
        
        Args:
            question: 自然语言问题
            visualize: 是否生成可视化
            auto_train: 是否自动训练成功的查询
            supplier: AI服务提供商
            
        Returns:
            包含SQL、数据结果和可能的可视化信息的字典
        """
        if not question:
            raise ValueError("问题不能为空")

        try:
            # 获取VannaServer实例
            server = await cls._get_vn_instance(supplier)

            # 处理问题
            logger.info(f"处理问题: {question}")
            sql, df, fig = server.ask(
                question=question,
                visualize=visualize,
                auto_train=auto_train
            )

            # 转换DataFrame为JSON
            df_json = df.to_json(orient='records', force_ascii=False)

            # 构建结果
            result = {
                'sql': sql,
                'data': df_json
            }

            # 如果生成了可视化，添加到结果中
            if fig:
                # 可以在这里处理图表，例如保存为HTML或转换为base64
                pass

            logger.info(f"问题处理成功: {question}")
            return result
        except Exception as e:
            logger.error(f"处理问题失败: {str(e)}")
            raise Exception(f"处理问题失败: {str(e)}")
