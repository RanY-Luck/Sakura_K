#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/12 17:19
# @Author   : 冉勇
# @File     : import_parse.py
# @Software : PyCharm
# @Desc     :
import importlib

from functools import lru_cache
from typing import Any, Type, TypeVar

from exceptions.exception import PermissionException
from utils.log_util import logger

T = TypeVar('T')


@lru_cache(maxsize=512)
def import_module_cached(module_path: str) -> Any:
    """
    缓存导入模块

    :param module_path: 模块路径
    :return:
    """
    return importlib.import_module(module_path)


def dynamic_import_data_model(module_path: str) -> Type[T]:
    """
    动态导入数据模型

    :param module_path: 模块路径，格式为 'module_path.class_name'
    :return:
    """
    try:
        module_path, class_name = module_path.rsplit('.', 1)
        module = import_module_cached(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        logger.error(f'动态导入数据模型失败：{e}')
        raise PermissionException(message='数据模型列动态解析失败，请联系系统超级管理员')
