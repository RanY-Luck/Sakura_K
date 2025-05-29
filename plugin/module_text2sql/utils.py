#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/29 09:55
# @Author  : 冉勇
# @Site    : 
# @File    : utils.py
# @Software: PyCharm
# @desc    : Text2SQL模块工具类

import os
import shutil
from utils.log_util import logger


class Text2SqlUtils:
    """Text2SQL模块工具类，提供文件和资源管理功能"""

    @staticmethod
    def ensure_path_exists(path):
        """
        确保路径存在，如果不存在则创建
        
        Args:
            path: 要检查/创建的目录路径
            
        Returns:
            bool: 操作是否成功
        """
        try:
            os.makedirs(path, exist_ok=True)
            return True
        except Exception as e:
            logger.error(f"创建目录 {path} 失败: {e}")
            return False

    @staticmethod
    def get_file_path(base_dir, filename):
        """
        获取文件的完整路径
        
        Args:
            base_dir: 基础目录
            filename: 文件名
            
        Returns:
            str: 文件的完整路径
        """
        return os.path.join(base_dir, filename)
