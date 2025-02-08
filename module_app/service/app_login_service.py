#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/7 17:27
# @Author   : 冉勇
# @File     : app_login_service.py
# @Software : PyCharm
# @Desc     : 小程序登录服务
import uuid
import requests
from datetime import timedelta, datetime
from redis import Redis
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request
from config.enums import RedisInitKeyConfig
from module_admin.entity.do.user_do import SysUser, UserWechat
from module_admin.service.user_service import UserService
from utils.common_util import SqlalchemyUtil
from utils.log_util import logger
from config.env import JwtConfig, AppConfig
from config.wx_mini_config import wxMiniSettings
from module_admin.dao.user_dao import UserDao
from module_admin.dao.wx_user_dao import WxUserDao
from module_admin.entity.vo.log_vo import WxMiniPhoneNumberCode, WxMiniLoginCode
from module_admin.entity.vo.login_vo import UserLogin
from module_admin.entity.vo.user_vo import UserModel, UserWechatModel, CurrentUserModel, EditUserModel
from module_admin.service.login_service import LoginService
from module_app.entity.vo.WxLogin import AppLoginModelResp
from utils.pwd_util import PwdUtil


class WxLoginService:

    @classmethod
    async def login_with_code(cls,  req: Request, post: WxMiniLoginCode,
                                 db: AsyncSession) -> AppLoginModelResp | None:

        wx_mini_access_token = await cls.__get_access_token(req)
        # 获取登录信息
        login_json = requests.request('GET',
                                      wxMiniSettings.WX_MINI_LOGIN.format(
                                          wxMiniSettings.WX_MINI_APPID,
                                          wxMiniSettings.WX_MINI_APPID_SECRET,
                                          post.login_code
                                      )).json()
        logger.info("获取微信openid" + str(login_json))
        wx_user = await WxUserDao.get_wx_user_by_openid(db, openid=login_json['openid'])
        sys_user = await UserDao.get_user_by_info(db, UserModel(phonenumber=wx_user.user_phone))
        data = await cls.__login_with_user(req, db , sys_user, wx_user)
        return data


    @classmethod
    async def register_with_code(cls, req: Request, post: WxMiniPhoneNumberCode,
                                 db: AsyncSession) -> AppLoginModelResp | None:
        """
        小程序注册并且登录
        """
        wx_mini_access_token = await cls.__get_access_token(req)
        # 获取登录信息
        login_json = requests.request('GET',
                                      wxMiniSettings.WX_MINI_LOGIN.format(
                                          wxMiniSettings.WX_MINI_APPID,
                                          wxMiniSettings.WX_MINI_APPID_SECRET,
                                          post.login_code
                                      )).json()
        logger.info("获取微信openid" + str(login_json))

        get_phone_param = {'code': post.phone_num_code}
        get_phone_response = requests.request('POST', wxMiniSettings.WX_MINI_GET_PHONE_URL.format(wx_mini_access_token),
                                              json=get_phone_param)
        phone_json = get_phone_response.json()
        logger.info("获取微信手机号" + str(phone_json))
        if phone_json['errcode'] == 0:
            phone_number = phone_json['phone_info']['purePhoneNumber']
            sys_user = await UserDao.get_user_by_info(db, UserModel(phonenumber=phone_number))
            wx_user = await WxUserDao.get_wx_user_by_phone(db, phone=phone_number)

            if not sys_user:
                # 创建用户
                sys_user = await UserDao.add_user_dao(db, UserModel(phonenumber=phone_number,
                                                                    userName=phone_number,
                                                                    nickName=phone_number,
                                                                    password=PwdUtil.get_password_hash(phone_number),
                                                                    # 手机号作为密码
                                                                    sex='2'))
                await db.commit()
            if not wx_user:
                wx_user = await WxUserDao.add_wx_user_dao(db, UserWechatModel(userPhone=phone_number,
                                                                        openid=login_json['openid'],
                                                                        unionId=login_json['unionid'],
                                                                        userId=sys_user.user_id))
                await db.commit()

            data = await cls.__login_with_user(req, db, sys_user, wx_user)
            return data
        else:
            return None

    @classmethod
    async def __get_access_token(cls, req: Request) -> str:
        """
        获取小程序的access_token
        """
        redis: Redis = await req.app.state.redis
        wx_mini_access_token = await redis.get(name="wx_mini_access_token")
        if not wx_mini_access_token:
            token_response = requests.request('GET', wxMiniSettings.WX_MINI_TOKEN_URL)
            result = token_response.json()
            print("获取accessToken" + str(result))
            wx_mini_access_token = result['access_token']
            await redis.set("wx_mini_access_token", wx_mini_access_token, 7200)
        return wx_mini_access_token

    @classmethod
    async def __login_with_user(cls, req: Request, db: AsyncSession, sys_user:SysUser, wx_user: UserWechat) -> AppLoginModelResp:
        """
        统一登录用户
        """
        user = UserLogin(
            userName=sys_user.user_name,
            password=sys_user.phonenumber,
            code='',
            uuid=str(uuid.uuid4()),
            loginInfo=None,
            captchaEnabled=False,
        )
        result = await LoginService.authenticate_user(req, db, user)
        access_token_expires = timedelta(minutes=JwtConfig.jwt_expire_minutes)
        session_id = str(uuid.uuid4())
        access_token = await LoginService.create_access_token(
            data={
                'user_id': str(result[0].user_id),
                'user_name': result[0].user_name,
                'dept_name': result[1].dept_name if result[1] else None,
                'session_id': session_id,
                'login_info': user.login_info,
            },
            expires_delta=access_token_expires
        )
        # 保存redis Token
        if AppConfig.app_same_time_login:
            await req.app.state.redis.set(
                f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{session_id}',
                access_token,
                ex=timedelta(minutes=JwtConfig.jwt_redis_expire_minutes),
            )
        else:
            # 此方法可实现同一账号同一时间只能登录一次
            await req.app.state.redis.set(
                f'{RedisInitKeyConfig.ACCESS_TOKEN.key}:{result[0].user_id}',
                access_token,
                ex=timedelta(minutes=JwtConfig.jwt_redis_expire_minutes),
            )

        login_model_resp = AppLoginModelResp(
            token=access_token,
            expiresIn='',
            user=UserModel(**SqlalchemyUtil.base_to_dict(sys_user, 'snake_to_camel')),
            wxUser=UserWechatModel(**SqlalchemyUtil.base_to_dict(wx_user, 'snake_to_camel'))
        )
        await UserService.edit_user_services(
            db, EditUserModel(userId=result[0].user_id, loginDate=datetime.now(), type='status')
        )
        logger.info('登录成功')
        return login_model_resp

    @classmethod
    async def get_wx_user_info(cls,
                                req: Request,
                                db: AsyncSession,
                                user: CurrentUserModel) -> UserWechatModel | None:
        """
        获取微信用户信息
        """
        wx_user = await WxUserDao.get_wx_user_by_phone(db, user.user.phonenumber)
        return UserWechatModel(**SqlalchemyUtil.base_to_dict(wx_user, 'snake_to_camel'))
