#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 15:46
# @Author  : 冉勇
# @Site    : 
# @File    : wx_access_token.py
# @Software: PyCharm
# @desc    : 获取小程序全局唯一后台接口调用凭据
import requests
from aioredis import Redis
from core.logger import logger


class WxAccessToken:
    """
    获取到的access_token存储在redis数据库中
    获取小程序全局唯一后台接口调用凭据（access_token）。调用绝大多数后台接口时都需使用 access_token，开发者需要进行妥善保存。
    官方文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/access-token/auth.getAccessToken.html
    """

    def __init__(self, appid: str, secret: str, rd: Redis, grant_type: str = "client_credential"):
        """
        代码解释：
        用于获取微信access_token的类AccessToken的初始化方法__init__，该类需要传入四个参数，分别为appid、secret、rd和grant_type，
        其中，appid表示应用ID，secret表示应用秘钥，rd表示redis对象，grant_type表示授权类型，可选参数，默认值为"client_credential"。
        具体来说，该方法首先定义了请求微信服务器获取access_token的url地址和请求方法为GET。
        然后，将appid和secret封装在字典类型的self.params中，作为向微信服务器发送请求的查询字符串参数之一，grant_type默认为"client_credential"。
        接着，该方法通过字符串拼接方式，将appid和"_access_token"拼接成字符串，作为在Redis数据库中存储access_token的键名，赋值给了实例变量self.appidKey。
        :param appid:
        :param secret:
        :param rd:
        :param grant_type:
        """
        self.__url = "https://api.weixin.qq.com/cgi-bin/token"
        self.__method = "get"
        self.appidKey = f"{appid}_access_token"
        self.redis = rd
        self.params = {
            "appid": appid,
            "secret": secret,
            "grant_type": grant_type
        }

    async def get(self) -> dict:
        """
        获取小程序access_token
        :return:
        代码解释：
        首先使用redis对象的get方法，根据实例变量self.appidKey获取存储在Redis数据库中的access_token，并将结果保存至变量token中。
        接着，该方法判断变量token是否存在，如果不存在，则调用AccessToken类的update方法进行更新，并返回更新后的access_token；
        否则，返回字典类型的结果，其中，"status": True表示获取access_token成功，"token": token表示获取到的access_token值。
        """
        token = await self.redis.get(self.appidKey)
        if not token:
            return await self.update()
        return {"status": True, "token": token}

    async def update(self) -> dict:
        """
        更新小程序access_token
        :return:
        代码解释：
        首先输出"开始更新 access_token"的信息，然后根据实例变量self.__method和self.__url，使用getattr函数获取requests库中对应的请求方法，
        并发送get请求向微信服务器获取access_token。获取到的响应对象保存在变量response中。
        接着，该方法使用响应对象的json方法将响应数据转换为字典类型的数据，并保存在变量result中。
        然后，根据result字典中的"errcode"字段是否为"0"，判断是否获取access_token成功。如果失败，则记录错误日志并返回包含状态为False的字典类型的结果；否
        则，将获取到的access_token保存至Redis数据库中，并记录成功日志，最后返回包含状态为True的字典类型的结果。
        需要注意的是，在保存access_token时，该方法使用了redis对象的set方法，将access_token存储到Redis数据库中，并设置过期时间(ex参数)为2000秒。
        """
        print("开始更新 access_token")
        method = getattr(requests, self.__method)
        response = method(url=self.__url, params=self.params)
        result = response.json()
        if result.get("errcode", "0") != "0":
            print("获取access_token失败", result)
            logger.error(f"获取access_token失败:{result}")
            return {"status": False, "token": None}
        print("成功获取到", result)
        await self.redis.set(self.appidKey, result.get("access_token"), ex=2000)
        logger.info(f"获取access_token成功：{result}")
        return {"status": True, "token": result.get("access_token")}
