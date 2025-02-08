#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 9:59
# @Author   : 冉勇
# @File     : velocity_initializer.py
# @Software : PyCharm
# @Desc     :
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from module_gen.utils.jinja2_tools import snake_to_pascal_case, snake_to_camel, snake_2_colon, is_base_column, \
    get_sqlalchemy_type, get_column_options


class VelocityInitializer:
    """模板引擎初始化器"""

    @staticmethod
    def init_velocity() -> Environment:
        """初始化模板引擎"""
        try:
            # 设置模板加载器
            template_dir = os.path.abspath(os.path.join(os.getcwd(), 'module_gen/templates'))
            loader = FileSystemLoader(template_dir)

            # 创建Jinja2环境
            env = Environment(
                loader=loader,
                autoescape=select_autoescape(['html', 'xml']),
                trim_blocks=True,
                lstrip_blocks=True
            )

            # 添加自定义过滤器
            env.filters.update(
                {
                    'capitalize': lambda x: x.capitalize(),
                    'lower': lambda x: x.lower(),
                    'upper': lambda x: x.upper(),
                    'camelcase': lambda x: ''.join(word.title() for word in x.split('_')),
                    'snakecase': lambda x: '_'.join(x.lower().split()),
                    'snake_to_pascal_case': snake_to_pascal_case,
                    'snake_to_camel': snake_to_camel,
                    'snake_2_colon': snake_2_colon,
                    'is_base_column': is_base_column,
                    'get_sqlalchemy_type': get_sqlalchemy_type,
                    'get_column_options': get_column_options,
                }
            )

            return env

        except Exception as e:
            raise RuntimeError(f"初始化模板引擎失败: {str(e)}")
