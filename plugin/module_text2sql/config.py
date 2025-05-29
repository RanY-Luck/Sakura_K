#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/29 09:20
# @Author  : 冉勇
# @Site    : 
# @File    : config.py
# @Software: PyCharm
# @desc    : Text2SQL模块配置管理

import os
from dotenv import load_dotenv
from utils.log_util import logger

# 获取当前环境，默认为 'dev'
ENV = os.getenv("ENV", "dev")
env_file = f".env.{ENV}"

# 加载环境变量
try:
    if os.path.exists(env_file):
        load_dotenv(dotenv_path=env_file)
        logger.info(f"成功从 {env_file} 加载环境变量")
    else:
        logger.warning(f"环境变量文件 {env_file} 不存在，使用默认值")
except Exception as e:
    logger.error(f"加载环境变量失败：{e}")


class Text2SqlConfig:
    """Text2SQL模块配置类，提供全局配置访问"""

    # 数据库配置
    DB_HOST = os.getenv("DB_HOST1")
    DB_NAME = os.getenv("DB_NAME1")
    DB_USER = os.getenv("DB_USER1")
    DB_PASSWORD = os.getenv("DB_PASSWORD1")
    DB_PORT = int(os.getenv("DB_PORT1"))

    # AI服务提供商配置
    DEFAULT_SUPPLIER = os.getenv("SUPPLIER", "GITEE")

    # 向量数据库配置
    VECTOR_DB_PATH = os.getenv("VECTOR_DB_PATH")

    # 嵌入模型配置
    EMBEDDING_SUPPLIER = os.getenv("EMBEDDING_SUPPLIER", "SiliconFlow")

    @classmethod
    def get_db_config(cls):
        """获取数据库配置"""
        # return {
        #     "host": cls.DB_HOST,
        #     "database": cls.DB_NAME,
        #     "db_name": cls.DB_NAME,
        #     "dbname": cls.DB_NAME,
        #     "user": cls.DB_USER,
        #     "password": cls.DB_PASSWORD,
        #     "port": cls.DB_PORT
        # }

        return {
            "host": "61.145.163.190",
            "database": "bms",
            "dbname": "bms",
            "user": "root",
            "password": "FK@mysql123",
            "port": "59296"
        }

    @classmethod
    def get_vanna_config(cls, supplier=None):
        """
        获取VannaServer配置
        
        Args:
            supplier: AI服务提供商，为空则使用默认值
            
        Returns:
            VannaServer配置字典
        """
        if not supplier:
            supplier = cls.DEFAULT_SUPPLIER

        return {
            # AI服务和嵌入相关配置
            "supplier": supplier,
            "embedding_supplier": cls.EMBEDDING_SUPPLIER,
            "vector_db_path": cls.VECTOR_DB_PATH,

            # 数据库配置
            **cls.get_db_config()
        }
