#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/24 14:53
# @Author  : 冉勇
# @Site    : 
# @File    : ip_manage.py
# @Software: PyCharm
# @desc    : 获取IP地址归属地
"""
文档：https://user.ip138.com/ip/doc
IP查询第三方服务，有1000次的免费次数

JSONP请求示例（IPv4）
https://api.ip138.com/ip/?ip=58.16.180.3&datatype=jsonp&token=cc87f3c77747bccbaaee35006da1ebb65e0bad57

aiohttp 异步请求文档：https://docs.aiohttp.org/en/stable/client_quickstart.html
"""
import aiohttp
from aiohttp import TCPConnector
from application.settings import IP_PARSE_TOKEN, IP_PARSE_ENABLE
from core.logger import logger
from pydantic import BaseModel
from typing import Optional


class IPLocationOut(BaseModel):
    ip: Optional[str] = None
    address: Optional[str] = None
    country: Optional[str] = None
    province: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    operator: Optional[str] = None
    postal_code: Optional[str] = None
    area_code: Optional[str] = None


class IPManage:
    def __init__(self, ip: str):
        self.ip = ip
        self.url = f"https://api.ip138.com/ip/?ip={ip}&datatype=jsonp&token={IP_PARSE_TOKEN}"

    async def parse(self):
        """
        IP数据分析
        {'ret': 'ok', 'ip': '114.222.121.253','data': ['中国', '江苏', '南京', '江宁区', '电信', '211100', '025']}
        该函数用于解析IP地址，并返回一个IPLocationOut对象，用于获取IP的相关信息。
        :return: IPLocationOut对象，包含如下属性：
            - ip：输入的IP地址
            - address：IP地址所在的城市
            - country：IP地址所在的国家
            - province：IP地址所在的省份
            - city：IP地址所在的城市
            - county：IP地址所在的县/区
            - operator：IP地址所属运营商
            - postal_code：IP地址所属地邮编
            - area_code：IP地址所属地区号
        """
        # 创建一个IPLocationOut对象，并将用户输入的IP地址保存到对象的ip属性中。
        out = IPLocationOut()
        out.ip = self.ip
        # 判断是否开启了IP地址数据解析功能，若未开启，则返回创建的IPLocationOut对象。
        if not IP_PARSE_ENABLE:
            logger.warning(
                "未开启IP地址数据解析，无法获取到IP所属地，请在application/config/production.py:IP_PARSE_ENABLE中开启！"
            )
            return out
        # 使用aiohttp通过TCP连接器连接IP查询API，并获取API返回的JSON格式数据。
        async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
            async with session.get(session.url) as resp:
                body = await resp.json()
                # 若返回数据的ret字段不等于"ok"，则打印错误日志并返回之前创建的IPLocationOut对象。
                if body.get("ret") != "ok":
                    logger.error(f"获取IP所属地失败：{body}")
                    return out
                data = body.get("data")
                # 解析API返回的JSON数据，将解析结果保存到IPLocationOut对象的相应属性中，并最终返回该对象。
                out.address = f"{''.join(data[i] for i in range(0, 4))} {data[4]}"
                out.country = data[0]
                out.province = data[1]
                out.city = data[2]
                out.county = data[3]
                out.operator = data[4]
                out.postal_code = data[5]
                out.area_code = data[6]
                return out
