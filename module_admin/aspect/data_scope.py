#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 17:10
# @Author  : 冉勇
# @Site    : 
# @File    : data_scope.py
# @Software: PyCharm
# @desc    : 获取当前用户数据权限对应的查询sql语句
from fastapi import Depends
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from typing import Optional


class GetDataScope:
    """
    获取当前用户数据权限对应的查询sql语句
    """
    # 数据权限
    DATA_SCOPE_ALL = '1'
    # 自定义数据权限
    DATA_SCOPE_CUSTOM = '2'
    # 部门数据权限
    DATA_SCOPE_DEPT = '3'
    # 部门及以下数据权限
    DATA_SCOPE_DEPT_AND_CHILD = '4'
    # 仅本人数据权限
    DATA_SCOPE_SELF = '5'

    def __init__(
            self,
            query_alias: Optional[str] = '',
            db_alias: Optional[str] = 'db',
            user_alias: Optional[str] = 'user_id',
            dept_alias: Optional[str] = 'dept_id'
    ):
        """
        获取当前用户数据权限对应的查询sql语句

        :param query_alias: 所要查询表对应的sqlalchemy模型名称，默认为''
        :param db_alias: orm对象别名，默认为'db'
        :param user_alias: 用户id字段别名，默认为'user_id'
        :param dept_alias: 部门id字段别名，默认为'dept_id'
        """
        # 所要查询表对应的sqlalchemy模型名称
        self.query_alias = query_alias
        # orm对象别名
        self.db_alias = db_alias
        # 用户id字段别名
        self.user_alias = user_alias
        # 部门id字段别名
        self.dept_alias = dept_alias

    # 获取当前用户数据权限对应的查询sql语句
    def __call__(self, current_user: CurrentUserModel = Depends(LoginService.get_current_user)):
        # 获取当前用户id
        user_id = current_user.user.user_id
        # 获取当前用户部门id
        dept_id = current_user.user.dept_id
        # 获取自定义数据权限角色id列表
        custom_data_scope_role_id_list = [
            item.role_id for item in current_user.user.role if item.data_scope == self.DATA_SCOPE_CUSTOM
        ]
        # 自定义数据权限角色id列表为空，则返回全部数据权限
        param_sql_list = []
        # 遍历角色，获取对应数据权限的查询sql语句
        for role in current_user.user.role:
            # 超级管理员或拥有全部数据权限，则返回全部数据权限
            if current_user.user.admin or role.data_scope == self.DATA_SCOPE_ALL:
                param_sql_list = ['1 == 1']
                break
            # 自定义数据权限，则获取对应部门id的查询sql语句
            elif role.data_scope == self.DATA_SCOPE_CUSTOM:
                if len(custom_data_scope_role_id_list) > 1:
                    param_sql_list.append(
                        f"{self.query_alias}.{self.dept_alias}.in_(select(SysRoleDept.dept_id).where(SysRoleDept.role_id.in_({custom_data_scope_role_id_list}))) if hasattr({self.query_alias}, '{self.dept_alias}') else 1 == 0"
                    )
                else:
                    param_sql_list.append(
                        f"{self.query_alias}.{self.dept_alias}.in_(select(SysRoleDept.dept_id).where(SysRoleDept.role_id == {role.role_id})) if hasattr({self.query_alias}, '{self.dept_alias}') else 1 == 0"
                    )
            # 处理部门数据权限
            elif role.data_scope == self.DATA_SCOPE_DEPT:
                param_sql_list.append(
                    f"{self.query_alias}.{self.dept_alias} == {dept_id} if hasattr({self.query_alias}, '{self.dept_alias}') else 1 == 0"
                )
            # 部门及以下数据权限
            elif role.data_scope == self.DATA_SCOPE_DEPT_AND_CHILD:
                param_sql_list.append(
                    f"{self.query_alias}.{self.dept_alias}.in_(select(SysDept.dept_id).where(or_(SysDept.dept_id == {dept_id}, func.find_in_set({dept_id}, SysDept.ancestors)))) if hasattr({self.query_alias}, '{self.dept_alias}') else 1 == 0"
                )
            # 处理仅本人数据权限
            elif role.data_scope == self.DATA_SCOPE_SELF:
                param_sql_list.append(
                    f"{self.query_alias}.{self.user_alias} == {user_id} if hasattr({self.query_alias}, '{self.user_alias}') else 1 == 0"
                )
            else:
                # 未知数据权限，则返回全部数据权限
                param_sql_list.append('1 == 0')
        # 去重
        param_sql_list = list(dict.fromkeys(param_sql_list))
        # 拼接sql语句
        param_sql = f"or_({', '.join(param_sql_list)})"

        return param_sql
