#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 17:45
# @Author  : 冉勇
# @Site    :
# @File    : current.py
# @Software: PyCharm
# @desc    : 获取认证后的信息工具
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from application import settings
from apps.vadmin.auth.crud import UserDal
from apps.vadmin.auth.models import VadminUser
from core.database import db_getter
from core.exception import CustomException
from utils import status
from .validation import AuthValidation
from .validation.auth import Auth


class OpenAuth(AuthValidation):
    """
    开放认证，无认证也可以访问
    认证了以后可以获取到用户信息，无认证则获取不到
    """

    async def __call__(
            self,
            request: Request,
            token: str = Depends(settings.oauth2_scheme),
            db: AsyncSession = Depends(db_getter)
    ):
        """
        每次调用依赖此类的接口会执行该方法
        :param request: 表示 HTTP 请求
        :param token: 表示 OAuth 2.0 认证的 access token
        :param db: 表示异步数据库会话
        :return:
        代码解释：
        首先，代码检查了是否启用了开放认证模式，如果没有启用，则直接返回 Auth(db=db)。
        否则，代码尝试通过验证 token 来获得用户信息，并使用 UserDal 类从数据库中获取用户数据。
        如果获取到了用户数据，则将其作为参数传递给 validate_user 方法，以进行进一步的验证。如果出现自定义异常，则返回 Auth(db=db)。
        """
        if not settings.OAUTH_ENABLE:
            return Auth(db=db)
        try:
            telephone = self.validate_token(request, token)
            user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
            return await self.validate_user(request, user, db)
        except CustomException:
            return Auth(db=db)


class AllUserAuth(AuthValidation):
    """
    支持所有用户认证
    获取用户基本信息
    """

    async def __call__(
            self,
            request: Request,
            token: str = Depends(settings.oauth2_scheme),
            db: AsyncSession = Depends(db_getter)
    ):
        """
        每次调用依赖此类的接口会执行该方法
        :param request: 表示 HTTP 请求。
        :param token: 表示 OAuth 2.0 认证的 access token
        :param db: 表示异步数据库会话
        :return:
        代码解释：
        首先，代码检查了是否启用了 OAuth2.0 认证模式，如果没有启用，则直接返回 Auth(db=db)。
        否则，代码通过验证 token 来获得用户电话号码，并使用 UserDal 类从数据库中获取用户数据。
        如果获取到了用户数据，则将其作为参数传递给 validate_user 方法，以进行进一步的验证。最后，将验证后的用户信息返回。
        """
        if not settings.OAUTH_ENABLE:
            return Auth(db=db)
        telephone = self.validate_token(request, token)
        user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
        return await self.validate_user(request, user, db)


class FullAdminAuth(AuthValidation):
    """
    只支持员工用户认证
    获取员工用户完整信息
    如果有权限 那么会验证该用户是否包括权限列表中的其中一个权限
    """

    def __init__(self, permissions: list[str] | None = None):
        if permissions:
            self.permissions = set(permissions)
        else:
            self.permissions = None

    async def __call__(
            self,
            request: Request,
            token: str = Depends(settings.oauth2_scheme),
            db: AsyncSession = Depends(db_getter)
    ) -> Auth:
        """
        每次调用依赖此类的接口会执行该方法
        :param request:
        :param token:
        :param db:
        :return:
        代码解释：
        首先判断settings.OAUTH_ENABLE是否为True，如果为False，则返回一个Auth对象，否则通过调用validate_token方法校验token的有效性并返回对应电话号码。
        然后使用该电话号码从数据库中查询对应的用户信息，并使用joinedload选项一并加载该用户的角色和菜单信息。
        接着调用validate_user方法校验用户信息并返回结果。
        最后，调用get_user_permissions方法获取该用户的权限，并判断其是否在permissions列表中出现，如果未出现，则抛出CustomException异常。
        最终返回validate_user方法的结果。
        """
        if not settings.OAUTH_ENABLE:
            return Auth(db=db)
        telephone = self.validate_token(request, token)
        options = [joinedload(VadminUser.roles), joinedload("roles.menus")]
        user = await UserDal(db).get_data(telephone=telephone, v_return_none=True, v_options=options, is_staff=True)
        result = await self.validate_user(request, user, db)
        permissions = self.get_user_permissions(user)
        if permissions != {'*.*.*'} and self.permissions:
            if not (self.permissions & permissions):
                raise CustomException(msg="无权限操作", code=status.HTTP_403_FORBIDDEN)
        return result
