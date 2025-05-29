#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/28 14:54
# @Author   : 冉勇
# @File     : __init__.py
# @Software : PyCharm
# @Desc     : Text2SQL模块初始化

import os
import sys
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

# 添加当前模块路径到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 导出常用类和函数，方便外部直接使用
from plugin.module_text2sql.controller.text2sql_controller import text2sqlController
from plugin.module_text2sql.service.text2sql_service import Text2SqlService
from plugin.module_text2sql.config import Text2SqlConfig
from plugin.module_text2sql.utils import Text2SqlUtils

__all__ = [
    'text2sqlController',
    'Text2SqlService',
    'Text2SqlConfig',
    'Text2SqlUtils'
] 