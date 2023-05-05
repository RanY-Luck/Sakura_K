#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 15:04
# @Author  : 冉勇
# @Site    : 
# @File    : login_manage.py
# @Software: PyCharm
# @desc    :
import jwt
from datetime import datetime, timedelta
from fastapi import Request
from application import settings
from apps.vadmin.auth import models
from .validation import LoginValidation, LoginForm, LoginResult
from utils.aliyun_sms import AliyunSMS


class LoginManage:
    """
    登录认证工具
    """

    @LoginValidation
    async def password_login(self, data: LoginForm, user: models.VadminUser, **kwargs) -> LoginResult:
        """
        验证用户密码
        :param data:
        :param user:
        :param kwargs:
        :return:
        代码解释：
        需要传入登录表单数据data和用户记录user；
        如果密码验证成功，则返回一个status为True、msg为“验证成功”的LoginResult对象，
        否则返回status为False、msg为“手机号或密码错误”的LoginResult对象。
        """
        result = models.VadminUser.verify_password(data.password, user.password)
        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="手机号或密码错误")

    @LoginValidation
    async def sms_login(self, data: LoginForm, request: Request, **kwargs) -> LoginResult:
        """
        验证用户短信验证码
        :param data:
        :param request:
        :param kwargs:
        :return:
        代码解释：
        需要传入登录表单数据data和请求对象request；
        在验证之前，该函数会根据用户提交的手机号码从Redis数据库中获取相应的验证码，并进行比对。
        如果比对成功，则返回一个status为True、msg为“验证成功”的LoginResult对象，否则返回status为False、msg为“验证码错误”的LoginResult对象。
        """
        rd = request.app.state.redis
        sms = AliyunSMS(rd, data.telephone)
        result = await sms.check_sms_code(data.password)
        if result:
            return LoginResult(status=True, msg="验证成功")
        return LoginResult(status=False, msg="验证码错误")

    @staticmethod
    def create_token(payload: dict, expires: timedelta = None):
        """
        创建一个生成新的访问令牌的工具函数。
        pyjwt：https://github.com/jpadilla/pyjwt/blob/master/docs/usage.rst
        jwt 博客：https://geek-docs.com/python/python-tutorial/j_python-jwt.html
        #TODO 传入的时间为UTC时间datetime.datetime类型，但是在解码时获取到的是本机时间的时间戳
        :param payload:
        :param expires:
        :return:
        代码解释：
        需要传入一个字典对象payload作为负载，在负载字典中需要包含过期时间exp，也可以选择传入过期时间的时间间隔（expires）。
        该函数使用了Python第三方库jwt来生成access token，并将其作为字符串返回给调用者。
        """
        if expires:
            expire = datetime.utcnow() + expires
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        payload.update({"exp": expire})
        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
