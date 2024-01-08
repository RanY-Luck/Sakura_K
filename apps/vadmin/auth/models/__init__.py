#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : __init__.py
# @Software: PyCharm
# @desc    : 初始化文件

from .dept import VadminDept
from .m2m import vadmin_auth_user_roles, vadmin_auth_role_menus, vadmin_auth_user_depts, vadmin_auth_role_depts
from .menu import VadminMenu
from .role import VadminRole
from .user import VadminUser
