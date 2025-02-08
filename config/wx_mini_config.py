#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/7 17:28
# @Author   : 冉勇
# @File     : wx_mini_config.py
# @Software : PyCharm
# @Desc     : 微信登录基本配置
from typing import Any
from pydantic_settings import BaseSettings


class WxMiniConfig(BaseSettings):
    WX_MINI_APPID: str = "xxxx"
    WX_MINI_APPID_SECRET: str = "xxxx"

    WX_MINI_TOKEN_URL: str = ("https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}"
                              .format(WX_MINI_APPID, WX_MINI_APPID_SECRET))
    WX_MINI_GET_PHONE_URL: str = "https://api.weixin.qq.com/wxa/business/getuserphonenumber?access_token={}"
    WX_MINI_LOGIN: str = ("https://api.weixin.qq.com/sns/jscode2session?grant_type=authorization_code&appid={}"
                          "&secret={}&js_code={}")
    # 获取微信小程序码
    WX_MINI_GEN_PATH_CODE: str = 'https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token={}'
    # 微信小程序发送订阅消息
    WX_MINI_SEND_SUBSCRIBE_MSG: str = 'https://api.weixin.qq.com/cgi-bin/message/subscribe/send?access_token={}'
    # 微信商户ID，后续支付使用
    WXPAY_MCHID: str = "xxxx"
    # 微信支付 API v3秘钥
    WXPAY_APIV3_KEY: str = "xxxx"
    # 微信支付结果回调接口
    WXPAY_NOTIFYURL: str = "微信支付结果回调接口"
    # 商户证书序列号
    WXPAY_SERIALNO: str = "xxxx"
    # 商户私钥
    WXPAY_CLIENT_PRIKEY: str = "wxmini/wepay_cert/apiclient_key.pem"
    # 商品描述(统一下单接口用到)
    WXPAY_PAY_DESC: str = "商品描述(统一下单接口用到)"
    # 回调地址，也可以在调用接口的时候覆盖
    NOTIFY_URL: str = 'https://xxxx.xxxxx.cn/api/v1/wepay/notify'
    # 微信支付平台证书缓存目录，减少证书下载调用次数，首次使用确保此目录为空目录.
    # 初始调试时可不设置，调试通过后再设置，示例值:'./cert'
    CERT_DIR: str = './cert'

    SubscribeTemplate: Any = {
        # 微信小程序通知模板ID
        "rest_minute": "xxxxx"
    }
    pass


wxMiniSettings = WxMiniConfig()
