#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/30 22:23
# @Author  : 冉勇
# @Site    : 
# @File    : auto_import_routes.py
# @Software: PyCharm
# @desc    :
import os
import importlib
from fastapi import FastAPI
from typing import List, Dict

app = FastAPI()

ROUTE_DIR = 'module_admin/controller'


def auto_import_routes(directory: str) -> List[Dict[str, any]]:
    controller_list = []
    for filename in os.listdir(directory):
        if filename.endswith('_controller.py'):
            module_name = f'{directory.replace("/", ".")}.{filename.replace(".py", "")}'
            module = importlib.import_module(module_name)
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if hasattr(attr, 'router'):
                    controller_list.append({'router': attr, 'tags': [attr_name]})
    return controller_list


controller_list = auto_import_routes(ROUTE_DIR)
for controller in controller_list:
    print("controller-->",controller)
    app.include_router(
        controller['router'],
        prefix=f"/{controller['router'].__name__.replace('Controller', '').lower()}",
        tags=controller['tags']
    )
