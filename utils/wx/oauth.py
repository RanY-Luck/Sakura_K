#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 15:45
# @Author  : 冉勇
# @Site    : 
# @File    : oauth.py
# @Software: PyCharm
# @desc    :
import requests
from redis.asyncio import Redis

from core.logger import logger
from utils.cache import Cache
from utils.wx.wx_access_token import WxAccessToken


class WXOAuth:

    def __init__(self, rd: Redis, index: int = 0):
        """
        初始化微信认证
        :param rd:
        :param index:
        """
        # 重试次数
        self.retry_count = 5
        self.appid = None
        self.secret = None
        self.rd = rd
        self.tab_name = None
        if index == 0:
            self.tab_name = "wx_server"

    async def __get_settings(self, retry: int = 3):
        """
        获取小程序的配置信息
        :param retry:
        :return:
        代码解释：
        首先通过判断实例变量self.tab_name是否存在，检查是否针对某个认证的微信平台进行了配置。如果不存在，则记录错误日志"请选择认证的微信平台"。
        接着，该方法调用Cache类的get_tab_name方法，使用self.rd作为参数传入，并将实例变量self.tab_name和可选参数retry传入，获取指定微信平台的配置信息，并将结果保存在wx_config变量中。
        最后，将wx_config字典中的"wx_server_app_id"和"wx_server_app_secret"分别赋值给AccessToken对象的实例变量self.appid和self.secret，以便其他方法的调用使用。
        需要注意的是，在调用Cache类的get_tab_name方法时，该方法使用了异步函数await关键字，因此是一个异步方法。
        同时，在该方法中还定义了一个可选参数retry，默认值为3，表示获取配置信息时的重试次数。
        """
        if not self.tab_name:
            logger.error(f"请选择认证的微信平台")
        wx_config = await Cache(self.rd).get_tab_name(self.tab_name, retry)
        self.appid = wx_config.get("wx_server_app_id")
        self.secret = wx_config.get("wx_server_app_secret")

    async def get_code2session(self, code: str) -> dict:
        """
        通过微信用户临时登录凭证 code 进行校验，获取用户openid，与 session 信息
        官方文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/login/auth.code2Session.html
        :param code: 登录时获取的 code
        :return: 正确：{'session_key': 'F8/5LZrdtINYLPEdUJgXXQ==', 'openid': 'okLlC5Kcv7DH2J99dz-Z2FwJeEeU'}
        :return: 报错：{'errcode': 40029, 'errmsg': 'invalid code, rid: 62308e5d-0b0b697e-1db652eb'}
        代码解释：
        首先检查实例变量self.appid和self.secret是否存在，如果不存在，则调用AccessToken类中的私有方法__get_settings获取配置信息。
        获取到的self.appid和self.secret将用于接下来的请求。
        接着，该方法使用requests库的get方法向"https://api.weixin.qq.com/sns/jscode2session"地址发送get请求，并传入字典类型的参数params，
        其中包含获取session_key和openid所需的参数：self.appid、self.secret、code和grant_type。获取到的响应对象response可以获取到服务器返回的响应数据。
        然后，该方法通过响应对象response的json方法，将响应数据转换成字典形式的数据，并将其保存在变量result中。
        接着，通过判断result字典中是否包含"openid"键值对，来确定微信校验是否成功。如成功，则记录日志，并将result结果作为字典类型的结果返回给调用方；
        否则，则记录错误日志，并将包含"errcode"和"errmsg"键值对的字典类型的错误结果返回给调用方。
        需要注意的是，在请求https://api.weixin.qq.com/sns/jscode2session地址时，该方法使用了requests库的get方法，并将参数params通过params参数传入，
        表示以查询字符串的方式将params参数添加到请求地址的末尾。同时，在该方法中还定义了一个参数code，表示微信用户的临时登录凭证。
        """
        if not self.appid or not self.secret:
            await self.__get_settings()
        api = "https://api.weixin.qq.com/sns/jscode2session"
        params = {
            "appid": self.appid,
            "secret": self.secret,
            "js_code": code,
            "grant_type": "authorization_code"
        }
        response = requests.get(url=api, params=params)
        result = response.json()
        if "openid" not in result:
            logger.error(f"微信校验失败：{result}, code：{code}")
        else:
            logger.info(f"微信校验成功：{result}, code：{code}")
        return result

    async def get_phone_number(self, code: str):
        """
        获取微信用户手机号
        官方文档：https://developers.weixin.qq.com/miniprogram/dev/api-backend/open-api/phonenumber/phonenumber.getPhoneNumber.html
        :param code: 动态令牌。可通过动态令牌换取用户手机号。
        :return: 成功：{'errcode': 0, 'errmsg': 'ok', 'phone_info': {'phoneNumber': 'xxxxxx'
        , 'purePhoneNumber': 'xxxxxx', 'countryCode': '86', 'watermark': {'timestamp': 1647355468, 'appid': 'xxxx'}}}
        失败：{'errcode': 40001, 'errmsg': 'invalid credential, access_token is invalid or not latest rid: 62690257-2894b530-58c6fcf3'}
        代码解释：
        首先检查实例变量self.appid和self.secret是否存在，如果不存在，则调用AccessToken类中的私有方法__get_settings获取配置信息。
        接着，该方法构造请求地址api，并创建了一个WxAccessToken类的实例at，用于获取微信令牌access_token。
        然后，获取access_token的过程通过await异步调用WxAccessToken类的get方法实现。
        如果获取access_token失败，则返回包含错误信息的字典类型的数据result给调用方，
        否则，将获取到的access_token添加到请求参数params中，并将参数code以json格式添加到请求体data中。
        之后，该方法使用requests库的post方法向api地址发送post请求，并传入参数params和data。响应对象response可以获取到服务器返回的响应数据。
        接着，该方法通过响应对象response的json方法，将响应数据转换成字典形式的数据，并将其保存在变量result中。
        如果result字典中的"errcode"值为0，则记录日志，并将result结果作为字典类型的数据返回给调用方；否则，则记录错误日志，并根据不同错误码进行相应的处理。
        如果错误码为40001，则表示微信令牌失效，该方法通过调用WxAccessToken类的update方法更新微信令牌，然后通过递归调用该方法重新尝试获取微信用户的手机号。
        """
        if not self.appid or not self.secret:
            await self.__get_settings()
        api = "https://api.weixin.qq.com/wxa/business/getuserphonenumber"
        at = WxAccessToken(self.appid, self.secret, self.rd)
        access_token = await at.get()
        if not access_token.get("status", False):
            result = {'errcode': 40001, 'errmsg': '获取微信令牌失败'}
            # print(result)
            logger.error(f"获取微信用户手机号失败：{result}")
            return result
        params = {
            "access_token": access_token.get("token"),
        }
        data = {
            "code": code,
        }
        response = requests.post(url=api, params=params, json=data)
        result = response.json()
        if result.get("errcode", 0) == 0:
            logger.info(f"获取微信用户手机号成功：{result}, code：{code}")
        else:
            logger.error(f"获取微信用户手机号失败：{result}, code：{code}")
            if result.get("errcode", 0) == 40001:
                await at.update()
                if self.retry_count > 0:
                    logger.error(f"重试获取微信手机号，重试剩余次数, {self.retry_count}")
                    self.retry_count -= 1
                    return await self.get_phone_number(code)
        return result

    async def parsing_phone_number(self, code: str):
        """
        解析微信用户手机号
        :param code: 动态令牌。可通过动态令牌换取用户手机号。
        :return:
        代码解释：
        首先调用异步方法get_phone_number，并将参数code传入，以获取微信用户的手机号信息。
        接着，该方法对获取到的结果进行判断，如果result字典中的"errcode"值为0，则表明获取手机号成功，
        接下来从字典中提取phone_info字典，并使用assert语句确保phone_info变量是字典类型，最后返回字典中"phoneNumber"对应的值。
        如果result字典中的"errcode"值不为0，则返回None表示获取手机号失败。
        需要注意的是，该方法中使用了assert语句来确保获取到的phone_info变量是字典类型，如果phone_info不是字典类型，程序将抛出AssertionError异常。
        """
        result = await self.get_phone_number(code)
        if result.get("errcode") == 0:
            phone_info = result["phone_info"]
            assert isinstance(phone_info, dict)
            return phone_info["phoneNumber"]
        return None

    async def parsing_openid(self, code: str):
        """
        解析openid
        :param code: 动态令牌。可通过动态令牌换取用户手机号。
        :return:
        代码解释：
        首先调用异步方法get_code2session，并将参数code传入，以获取微信用户的会话密钥信息。
        接着，该方法对获取到的结果进行判断，如果result字典中包含键名为"openid"，则表明获取openid成功，直接返回result字典中"openid"对应的值即可。
        如果result字典中不包含"openid"这个键名，则返回None表示获取openid失败。
        需要注意的是，该方法并没有处理result字典中的错误码，因此如果get_code2session方法返回的结果中包含错误码，该方法仍然将其视为失败，返回None。
        """
        result = await self.get_code2session(code)
        if "openid" in result:
            return result["openid"]
        return None
