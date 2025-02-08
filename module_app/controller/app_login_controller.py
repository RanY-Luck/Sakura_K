#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/7 17:26
# @Author   : 冉勇
# @File     : app_login_controller.py
# @Software : PyCharm
# @Desc     :
from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from config.get_db import get_db
from module_admin.entity.vo.log_vo import WxMiniPhoneNumberCode, WxMiniLoginCode
from module_admin.entity.vo.user_vo import UserWechatModel, CurrentUserModel
from module_admin.service.login_service import LoginService
from module_app.entity.vo.WxLogin import AppLoginModelResp
from module_app.service.app_login_service import WxLoginService
from utils.response_util import ResponseUtil

appLoginController = APIRouter()


@appLoginController.post("/auth/register", summary="用户登录注册", response_model=AppLoginModelResp)
async def register_with_code(req: Request, post: WxMiniPhoneNumberCode, query_db: AsyncSession = Depends(get_db)):
    app_login_model = await WxLoginService.register_with_code(req, post, query_db)
    if app_login_model:
        return ResponseUtil.success(data=app_login_model)
    else:
        return ResponseUtil.failure(msg='登录失败')


@appLoginController.post("/auth/login", summary="用户使用openid登录", response_model=AppLoginModelResp)
async def register_with_code(req: Request, post: WxMiniLoginCode, query_db: AsyncSession = Depends(get_db)):
    app_login_model = await WxLoginService.login_with_code(req, post, query_db)
    if app_login_model:
        return ResponseUtil.success(data=app_login_model)
    else:
        return ResponseUtil.failure(msg='登录失败')


@appLoginController.get("/user/info", summary="获取微信信息", response_model=UserWechatModel)
async def get_wx_user_info(
        req: Request,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    wx_user = await WxLoginService.get_wx_user_info(req, query_db, current_user)
    if wx_user:
        return ResponseUtil.success(data=wx_user)
    else:
        return ResponseUtil.failure(msg='获取用户信息失败')
