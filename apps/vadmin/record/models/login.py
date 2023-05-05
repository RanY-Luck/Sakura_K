#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/24 14:51
# @Author  : 冉勇
# @Site    : 
# @File    : login.py
# @Software: PyCharm
# @desc    : 登录记录模型
import json
from application.settings import LOGIN_LOG_RECORD
from apps.vadmin.auth.utils.validation import LoginForm, WXLoginForm
from utils.ip_manage import IPManage
from sqlalchemy.ext.asyncio import AsyncSession
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, TEXT
from fastapi import Request
from user_agents import parse


class VadminLoginRecord(BaseModel):
    __tablename__ = "vadmin_record_login"
    __table_args__ = ({"comment": "登录记录表"})

    telephone = Column(String(255), index=True, nullable=False, comment="手机号")
    status = Column(Boolean, default=True, comment="是否登录成功")
    platform = Column(String(8), comment="登陆平台")
    login_method = Column(String(8), comment="认证方式")
    ip = Column(String(50), comment="登陆地址")
    address = Column(String(255), comment="登陆地点")
    country = Column(String(255), comment="国家")
    province = Column(String(255), comment="县")
    city = Column(String(255), comment="城市")
    county = Column(String(255), comment="区/县")
    operator = Column(String(255), comment="运营商")
    postal_code = Column(String(255), comment="邮政编码")
    area_code = Column(String(255), comment="地区区号")
    browser = Column(String(50), comment="浏览器")
    system = Column(String(50), comment="操作系统")
    response = Column(TEXT, comment="响应信息")
    request = Column(TEXT, comment="请求信息")

    @classmethod
    async def create_login_record(
            cls,
            db: AsyncSession,
            data: LoginForm | WXLoginForm,
            status: bool,
            req: Request,
            resp: dict
    ):
        """
        创建登录记录
        :param db:
        :param data:
        :param status:
        :param req:
        :param resp:
        :return:
        代码解释：
        用于在数据库中创建一个新的登录记录。
        该方法接受多个参数，例如db、data、status、req和resp等，这些参数分别代表着数据库会话、用户登录信息、登录状态、请求对象和响应信息等。
        在方法内部，它会根据传入的参数构建一个新的VadminLoginRecord对象，并将其添加到数据库中。
        """
        # 首先，它会检查LOGIN_LOG_RECORD这个全局变量是否为True，如果不是则直接返回None，不做任何操作。
        if not LOGIN_LOG_RECORD:
            return None
        header = {}
        # 从请求对象(req)中获取请求头部信息，并将其存储在header字典中。
        for k, v in req.headers.items():
            header[k] = v
        # 然后使用asyncio包中的await关键字异步获取请求体信息并解析成字典格式的数据，存储在body变量中。
        body = json.loads((await req.body()).decode())
        # 从请求头部中获取用户代理信息(user_agent)，并解析出操作系统(system)和浏览器(browser)等信息。
        user_agent = parse(req.headers.get("user-agent"))
        system = f"{user_agent.os.family} {user_agent.os.version_string}"
        browser = f"{user_agent.browser.family} {user_agent.browser.version_string}"
        # 然后，它使用IPManage类解析请求的客户端IP地址，并获取其所在位置(location)，这些信息都将用于创建登录记录。
        ip = IPManage(req.client.host)
        location = await ip.parse()
        # 最后，该段代码将请求头和请求体数据组成一个字典params，并将其序列化为JSON字符串。
        params = json.dumps({"body": body, "headers": header})
        # 然后使用上述获取到的信息，以及其他传入的参数(data、status、resp等)，构造一个新的VadminLoginRecord对象(obj)。
        obj = VadminLoginRecord(
            **location.dict(),
            telephone=data.telephone if data.telephone else data.code,
            status=status,
            browser=browser,
            system=system,
            response=json.dumps(resp),
            request=params,
            platform=data.platform,
            login_method=data.method
        )
        # 最后将该对象添加到会话中(db.add(obj))，并使用await db.flush()提交到数据库中。
        db.add(obj)
        await db.flush()
