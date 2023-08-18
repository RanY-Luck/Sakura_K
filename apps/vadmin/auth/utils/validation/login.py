#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/24 14:02
# @Author  : 冉勇
# @Site    :
# @File    : login.py
# @Software: PyCharm
# @desc    : 登录验证装饰器
from fastapi import Request
from pydantic import BaseModel, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

from application.settings import DEFAULT_AUTH_ERROR_MAX_NUMBER, DEMO
from apps.vadmin.auth import crud, schemas
from core.database import redis_getter
from core.validator import vali_telephone
from utils.count import Count


class LoginForm(BaseModel):
    telephone: str
    password: str
    method: str = '0'  # 认证方式，0：密码登录，1：短信登录，2：微信一键登录
    platform: str = '0'  # 登录平台，0：PC端管理系统，1：移动端管理系统
    # 重用验证器：https://docs.pydantic.dev/dev-v2/usage/validators/#reuse-validators
    normalize_telephone = field_validator('telephone')(vali_telephone)


class WXLoginForm(BaseModel):
    telephone: str | None = None
    code: str
    method: str = '2'  # 认证方式，0：密码登录，1：短信登录，2：微信一键登录
    platform: str = '1'  # 登录平台，0：PC端管理系统，1：移动端管理系统


class LoginResult(BaseModel):
    status: bool | None = False
    user: schemas.UserOut | None = None
    msg: str | None = None

    class Config:
        arbitrary_types_allowed = True


class LoginValidation:
    """
    实现了对用户登录表单数据的验证，以及对用户进行验证认证的功能。
    如果认证失败次数达到设定上限，则会冻结用户。
    如果验证成功，则会将用户的详细信息存入LoginResult对象中返回给调用者。
    """

    def __init__(self, func):
        self.func = func

    """
    代码解释：
    __call__方法实现了类似于函数调用的功能，接收四个参数：
    data表示提交的登录表单数据；db表示异步会话；request表示请求对象，返回一个LoginResult对象。
    首先，该方法会对提交的数据进行验证，如果发现数据不合法（例如platform或者method的值非法），则直接返回错误信息。
    接着，通过调用crud.UserDal中的get_data方法，从数据库中获取与提交的手机号相应的用户记录。
    如果用户不存在，则返回“该手机号不存在！”的错误信息。
    """

    async def __call__(self, data: LoginForm, db: AsyncSession, request: Request) -> LoginResult:
        self.result = LoginResult()
        if data.platform not in ["0", "1"] or data.method not in ["0", "1"]:
            self.result.msg = "无效参数"
            return self.result
        user = await crud.UserDal(db).get_data(telephone=data.telephone, v_return_none=True)
        if not user:
            self.result.msg = "该手机号不存在！"
            return self.result

        result = await self.func(self, data=data, user=user, request=request)

        count_key = f"{data.telephone}_password_auth" if data.method == '0' else f"{data.telephone}_sms_auth"
        count = Count(redis_getter(request), count_key)

        if not result.status:
            self.result.msg = result.msg
            if not DEMO:
                number = await count.add(ex=86400)
                if number >= DEFAULT_AUTH_ERROR_MAX_NUMBER:
                    await count.reset()
                    # 如果等于最大次数，那么就将用户 is_active=False
                    user.is_active = False
                    await db.flush()
        elif not user.is_active:
            self.result.msg = "此手机号已被冻结！"
        elif data.platform in ["0", "1"] and not user.is_staff:
            self.result.msg = "此手机号无权限！"
        else:
            if not DEMO:
                await count.delete()
            self.result.msg = "OK"
            self.result.status = True
            self.result.user = schemas.UserSimpleOut.model_validate(user)
            await user.update_login_info(db, request.client.host)
        return self.result
