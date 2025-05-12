#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 17:09
# @Author  : 冉勇
# @Site    : 
# @File    : interface_auth.py
# @Software: PyCharm
# @desc    : 校验当前用户是否具有相应的接口权限
from fastapi import Depends
from typing import Union, List
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from exceptions.exception import PermissionException


class CheckUserInterfaceAuth:
    """
    校验当前用户是否具有相应的接口权限
    :param perm: 权限标识
    :param is_strict: 当传入的权限标识是list类型时，是否开启严格模式，开启表示会校验列表中的每一个权限标识，所有的校验结果都需要为True才会通过
    """

    def __init__(self, perm: Union[str, List], is_strict: bool = False):
        # 权限标识
        self.perm = perm
        # 是否开启严格模式
        self.is_strict = is_strict

    # 校验当前用户是否具有相应的接口权限
    def __call__(self, current_user: CurrentUserModel = Depends(LoginService.get_current_user)):
        # 超级管理员拥有所有权限
        user_auth_list = current_user.permissions
        if '*:*:*' in user_auth_list:
            return True
        # 校验权限
        if isinstance(self.perm, str):
            # 权限标识为字符串
            if self.perm in user_auth_list:
                return True
        # 权限标识为列表
        if isinstance(self.perm, list):
            # 开启严格模式
            if self.is_strict:
                # 校验列表中的每一个权限标识
                if all([perm_str in user_auth_list for perm_str in self.perm]):
                    return True
            else:
                # 校验列表中的任意一个权限标识
                if any([perm_str in user_auth_list for perm_str in self.perm]):
                    return True
        raise PermissionException(data="", message="该用户无此接口权限")


class CheckRoleInterfaceAuth:
    """
    根据角色校验当前用户是否具有相应的接口权限
    :param role_key: 角色标识
    :param is_strict: 当传入的角色标识是list类型时，是否开启严格模式，开启表示会校验列表中的每一个角色标识，所有的校验结果都需要为True才会通过
    """

    def __init__(self, role_key: Union[str, List], is_strict: bool = False):
        # 角色标识
        self.role_key = role_key
        # 是否开启严格模式
        self.is_strict = is_strict

    # 校验当前用户是否具有相应的接口权限
    def __call__(self, current_user: CurrentUserModel = Depends(LoginService.get_current_user)):
        # 超级管理员拥有所有权限
        user_role_list = current_user.user.role
        # 校验角色
        user_role_key_list = [role.role_key for role in user_role_list]
        # 校验角色标识
        if isinstance(self.role_key, str):
            # 角色标识为字符串
            if self.role_key in user_role_key_list:
                return True
        # 角色标识为列表
        if isinstance(self.role_key, list):
            # 开启严格模式
            if self.is_strict:
                # 校验列表中的每一个角色标识
                if all([role_key_str in user_role_key_list for role_key_str in self.role_key]):
                    return True
            else:
                # 校验列表中的任意一个角色标识
                if any([role_key_str in user_role_key_list for role_key_str in self.role_key]):
                    return True
        raise PermissionException(data="", message="该用户无此接口权限")
