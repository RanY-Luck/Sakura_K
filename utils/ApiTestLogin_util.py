#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/10/24 16:35
# @Author   : 冉勇
# @File     : ApiTestLogin_util.py
# @Software : PyCharm
# @Desc     : 自动化登录保存token到redis，取redis的token
import json
from datetime import timedelta
from typing import Dict, Any

from fastapi import Request

from config.enums import RedisInitKeyConfig
from utils.http_util import AsyncRequest, BodyType


class LoginManager:

    async def verify_token(self, baseurl: str, token: str) -> bool:
        """
        验证token是否有效
        :param baseurl: 基础URL
        :param token: token字符串
        :return: token是否有效
        """
        try:
            r = await AsyncRequest.client(
                url=f'{baseurl}/api/admin/user/v2/front/info',
                token=token,
                body_type=BodyType.none
            )
            response = await r.invoke(method='get')
            return response['status'] == 200
        except Exception:
            return False

    async def login(
            self,
            request: Request,
            baseurl: str,
            username: str,
            password: str
    ) -> Dict[str, Any]:
        """
        执行登录操作并将token存储到Redis
        :param baseurl: 基础URL
        :param username: 用户名
        :param password: 密码
        :return: 登录响应信息
        """
        redis_key = f'{RedisInitKeyConfig.TOKEN.key}:{username}'
        try:
            # 获取并验证现有token
            if existing_token := await request.app.state.redis.get(redis_key):
                try:
                    if await self.verify_token(baseurl, existing_token):
                        return {
                            "status": True,
                            "token": existing_token,
                            "msg": "Using cached token"
                        }
                except Exception:
                    # Token验证失败，继续执行新登录流程
                    pass
            # 执行新的登录请求
            try:
                r = await AsyncRequest.client(
                    url=f'{baseurl}/api/auth/jwt/miniLogin',
                    body_type=BodyType.json,
                    body={
                        "username": username,
                        "password": password
                    }
                )
                raw_response = await r.invoke(method='post')
                response_json = json.loads(raw_response['response'])

                if not raw_response['status']:
                    return {
                        "status": False,
                        "msg": "Login failed",
                        "data": response_json
                    }
                # 登录成功，处理token
                token = response_json['data']['accessToken']
                full_token = f"Bearer {token}"
                # 存储token到Redis
                await request.app.state.redis.set(
                    redis_key,
                    full_token,
                    ex=timedelta(minutes=10)
                )
                return {
                    "status": True,
                    "token": full_token,
                    "msg": "Login successful",
                    "data": response_json['data']
                }
            except Exception as e:
                return {
                    "status": False,
                    "msg": f"Login request failed: {str(e)}",
                    "data": None
                }
        except Exception as e:
            return {
                "status": False,
                "msg": f"Redis operation failed: {str(e)}",
                "data": None
            }
