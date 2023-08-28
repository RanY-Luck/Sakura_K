#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 17:45
# @Author  : 冉勇
# @Site    :
# @File    : login.py
# @Software: PyCharm
# @desc    : 安全认证试图
"""
JWT 表示 「JSON Web Tokens」。https://jwt.io/
它是一个将 JSON 对象编码为密集且没有空格的长字符串的标准。
通过这种方式，你可以创建一个有效期为 1 周的令牌。然后当用户第二天使用令牌重新访问时，你知道该用户仍然处于登入状态。
一周后令牌将会过期，用户将不会通过认证，必须再次登录才能获得一个新令牌。
我们需要安装 python-jose 以在 Python 中生成和校验 JWT 令牌：pip3 install python-jose[cryptography]
PassLib 是一个用于处理哈希密码的很棒的 Python 包。它支持许多安全哈希算法以及配合算法使用的实用程序。
推荐的算法是 「Bcrypt」：pip3 install passlib[bcrypt]
"""
from datetime import timedelta

import jwt
from fastapi import APIRouter, Depends, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from application import settings
from apps.vadmin.auth.crud import MenuDal, UserDal
from apps.vadmin.auth.models import VadminUser
from apps.vadmin.record.models import VadminLoginRecord
from core.database import db_getter, redis_getter
from core.exception import CustomException
from utils import status
from utils.response import SuccessResponse, ErrorResponse
from utils.wx.oauth import WXOAuth
from .current import FullAdminAuth
from .login_manage import LoginManage
from .validation import LoginForm, WXLoginForm
from .validation.auth import Auth

app = APIRouter()


@app.post("/api/login", summary="API 手机号密码登录", description="Swagger API 文档登录认证")
async def api_login_for_access_token(
        request: Request,
        data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(db_getter)
):
    user = await UserDal(db).get_data(telephone=data.username, v_return_none=True)
    if not user:
        raise CustomException(status_code=401, code=401, msg="该手机号不存在")
    result = VadminUser.verify_password(data.password, user.password)
    if not result:
        raise CustomException(status_code=401, code=401, msg="手机号或密码错误")
    if not user.is_active:
        raise CustomException(status_code=401, code=401, msg="此手机号已被冻结")
    elif not user.is_staff:
        raise CustomException(status_code=401, code=401, msg="此手机号无权限")
    access_token = LoginManage.create_token({"sub": user.telephone})
    record = LoginForm(platform='2', method='0', telephone=data.username, password=data.password)
    resp = {"access_token": access_token, "token_type": "bearer"}
    await VadminLoginRecord.create_login_record(db, record, True, request, resp)
    return resp


@app.post("/login", summary="手机号密码登录", description="员工登录通道，限制最多输错次数，达到最大值后将is_active=False")
async def login_for_access_token(
        request: Request,
        data: LoginForm,
        manage: LoginManage = Depends(),
        db: AsyncSession = Depends(db_getter)
):
    """
    先使用try-except语句捕获可能出现的异常。
    接着根据传入的data参数中的method属性值，调用不同的登录方法，例如password_login或sms_login等。
    这些方法会检查用户提交的登录信息是否正确，并返回一个结果(result)对象。
    如果结果对象的status属性为False，则表示登录失败，此时会抛出ValueError异常。
    """
    try:
        if data.method == "0":
            result = await manage.password_login(data, db, request)
        elif data.method == "1":
            result = await manage.sms_login(data, db, request)
        else:
            raise ValueError("无效参数")
        # 如果登录成功，代码将创建一个JWT(access_token)和刷新令牌(refresh_token)，并将其打包在resp字典中。
        if not result.status:
            raise ValueError(result.msg)

        access_token = LoginManage.create_token({"sub": result.user.telephone, "is_refresh": False})
        expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        refresh_token = LoginManage.create_token({"sub": result.user.telephone, "is_refresh": True}, expires=expires)
        # 如果登录成功，代码将创建一个JWT(access_token)和刷新令牌(refresh_token)，并将其打包在resp字典中。
        # 此外，resp字典中还包含了其他一些用户信息，例如"is_reset_password"和"is_wx_server_openid"等。
        resp = {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "is_reset_password": result.user.is_reset_password,
            "is_wx_server_openid": result.user.is_wx_server_openid
        }
        # 然后，它将resp字典作为参数，调用VadminLoginRecord类中的create_login_record方法，将登录记录保存到数据库中。
        await VadminLoginRecord.create_login_record(db, data, True, request, resp)
        return SuccessResponse(resp)
    except ValueError as e:
        # 如果登录失败，将会创建一个包含错误信息的ErrorResponse对象返回。
        await VadminLoginRecord.create_login_record(db, data, False, request, {"message": str(e)})
        return ErrorResponse(msg=str(e))


@app.post("/wx/login", summary="微信服务端一键登录", description="员工登录通道")
async def wx_login_for_access_token(
        request: Request,
        data: WXLoginForm,  # 自定义的数据模型，用于接收请求中的参数。
        db: AsyncSession = Depends(db_getter),  # 异步数据库会话（AsyncSession），用于与数据库进行交互。
        rd: Redis = Depends(redis_getter)
):
    try:
        # 首先检查请求参数中的platform和method是否为1和2，若不是则抛出ValueError异常。
        if data.platform != "1" or data.method != "2":
            raise ValueError("无效参数")
        # 使用WXOAuth对象解析请求参数中的code字段，获取用户手机号，若手机号无效则抛出ValueError异常。
        wx = WXOAuth(rd, 0)
        telephone = await wx.parsing_phone_number(data.code)
        if not telephone:
            raise ValueError("无效Code")
        # 将手机号码存储在请求参数中的telephone字段中，并从数据库中查询该手机号对应的用户信息。
        # 如果用户不存在，则抛出ValueError异常，如果用户已被冻结，则抛出ValueError异常。
        data.telephone = telephone
        user = await UserDal(db).get_data(telephone=telephone, v_return_none=True)
        if not user:
            raise ValueError("手机号不存在")
        elif not user.is_active:
            raise ValueError("手机号已被冻结")
    except ValueError as e:
        """
        在try块中的异常处理部分，使用VadminLoginRecord对象记录用户登录信息，并返回一个包含错误信息的ErrorResponse对象。
        VadminLoginRecord是一个自定义的类，用于记录用户登录信息。
        ErrorResponse是一个自定义的数据模型，用于返回错误信息。
        """
        await VadminLoginRecord.create_login_record(db, data, False, request, {"message": str(e)})
        return ErrorResponse(msg=str(e))
    # 更新登录时间
    await UserDal(db).update_login_info(user, request.client.host)
    # 创建一个包含访问令牌和刷新令牌的响应信息。
    # 使用LoginManage对象创建一个访问令牌（access_token）和一个刷新令牌（refresh_token），并将它们存储在一个响应字典（resp）中。
    access_token = LoginManage.create_token({"sub": user.telephone, "is_refresh": False})
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = LoginManage.create_token({"sub": user.telephone, "is_refresh": True}, expires=expires)
    """
    在响应字典中，除了访问令牌和刷新令牌之外，还包含了一些其他的信息，比如令牌类型（token_type）、是否需要重置密码（is_reset_password）
    和是否使用微信服务端的openid进行登录（is_wx_server_openid）等。这些信息可以用于后续的业务逻辑处理。
    """
    resp = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "is_reset_password": user.is_reset_password,
        "is_wx_server_openid": user.is_wx_server_openid
    }
    """
    调用VadminLoginRecord对象的create_login_record()方法记录用户的登录信息，并返回一个包含响应信息的SuccessResponse对象。
    VadminLoginRecord是一个自定义的类，用于记录用户登录信息。SuccessResponse是一个自定义的数据模型，用于返回成功响应信息。
    """
    await VadminLoginRecord.create_login_record(db, data, True, request, resp)
    return SuccessResponse(resp)


@app.get("/getMenuList", summary="获取当前用户菜单树")
async def get_menu_list(
        # 该参数使用了依赖注入（Depends）来获取一个名为FullAdminAuth的认证依赖对象。
        # FullAdminAuth对象用于验证用户的身份和权限，并返回一个包含用户身份信息的Auth对象。
        auth: Auth = Depends(FullAdminAuth())
):
    """
    首先使用MenuDal对象从数据库中获取当前用户的菜单列表，并将其存储在一个SuccessResponse对象中返回。
    MenuDal是一个自定义的类，用于从数据库中获取菜单数据。
    SuccessResponse是一个自定义的数据模型，用于返回成功响应信息。
    """
    return SuccessResponse(await MenuDal(auth.db).get_routers(auth.user))


@app.post("/token/refresh", summary="刷新Token")
async def token_refresh(
        # 需要接受一个名为refresh的参数，该参数使用了FastAPI中的Body类来获取POST请求中的数据，即刷新令牌（refresh_token）。
        refresh: str = Body(..., title="刷新Token")
):
    error_code = status.HTTP_401_UNAUTHORIZED
    try:
        # 首先使用JWT（JSON Web Token）库的decode()方法来解码刷新令牌中的数据，并验证令牌的签名和过期时间。
        payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        telephone: str = payload.get("sub")
        # 如果解码失败或令牌无效，则返回一个ErrorResponse对象，表示认证失败。
        is_refresh: bool = payload.get("is_refresh")
        if telephone is None or not is_refresh:
            return ErrorResponse("未认证，请您重新登录", code=error_code, status=error_code)
    except jwt.exceptions.InvalidSignatureError:
        return ErrorResponse("无效认证，请您重新登录", code=error_code, status=error_code)
    except jwt.exceptions.ExpiredSignatureError:
        return ErrorResponse("登录已超时，请您重新登录", code=error_code, status=error_code)
    # 如果刷新令牌验证通过，则调用LoginManage对象的create_token()方法创建一个新的访问令牌和刷新令牌，并将它们存储在一个响应字典（resp）中。
    # 访问令牌和刷新令牌的创建依赖于JWT标准，可以提供安全的认证和授权功能。
    access_token = LoginManage.create_token({"sub": telephone, "is_refresh": False})
    expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = LoginManage.create_token({"sub": telephone, "is_refresh": True}, expires=expires)
    # 在响应字典中，除了访问令牌和刷新令牌之外，还包含了令牌类型（token_type）等信息。这些信息可以用于后续的业务逻辑处理。
    resp = {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
    # 最后，将响应字典包装在一个SuccessResponse对象中返回。SuccessResponse是一个自定义的数据模型，用于返回成功响应信息。
    return SuccessResponse(resp)
