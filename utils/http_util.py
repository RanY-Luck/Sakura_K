#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/29 17:46
# @Author  : 冉勇
# @Site    :
# @File    : http_util.py
# @Software: PyCharm
# @desc    : http发起请求工具
import asyncio
import json
import time
from typing import Dict, Any

import aiohttp
import uuid
from datetime import timedelta
from enum import IntEnum
from aiohttp import FormData
from config.enums import RedisInitKeyConfig
from fastapi import Request

from module_admin.entity.vo.login_vo import UserLogin


class BodyType(IntEnum):
    """body类型"""
    none = 0
    json = 1
    form = 2
    x_form = 3
    raw = 4


class AsyncRequest(object):
    def __init__(self, url: str, token: str = None, timeout=15, **kwargs):
        self.url = url
        self.token = token
        self.kwargs = kwargs
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    def get_cookie(self, session):
        cookies = session.cookie_jar.filter_cookies(self.url)
        return {k: v.value for k, v in cookies.items()}

    def get_data(self, kwargs):
        if kwargs.get("json") is not None:
            return kwargs.get("json")
        return kwargs.get("data")

    async def invoke(self, method: str):
        start = time.time()
        headers = self.kwargs.get('headers', {})
        headers['Authorization'] = f'Bearer {self.token}'
        self.kwargs['headers'] = headers

        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
            async with session.request(
                    method, self.url, timeout=self.timeout,
                    ssl=False, **self.kwargs
            ) as resp:
                cost = "%.0fms" % ((time.time() - start) * 1000)
                response, json_format = await AsyncRequest.get_resp(resp)
                cookie = self.get_cookie(session)
                return await self.collect(
                    resp.status == 200, self.get_data(self.kwargs), resp.status, response,
                    resp.headers, resp.request_info.headers, elapsed=cost,
                    cookies=cookie, json_format=json_format
                )

    @staticmethod
    async def get_resp(resp):
        try:
            data = await resp.json(encoding='utf-8')
            return json.dumps(data, ensure_ascii=False, indent=4), True
        except:
            data = await resp.text()
            return data, False

    @staticmethod
    async def client(url: str, token: str = None, body_type: BodyType = BodyType.json, timeout=15, **kwargs):
        if not url.startswith(("http://", "https://")):
            raise Exception("请输入正确的url,带上http")

        headers = kwargs.get("headers", {})
        body = kwargs.get("body", {})

        # Add token to headers
        headers['Authorization'] = f'Bearer {token}'

        if body_type == BodyType.json:
            if "Content-Type" not in headers:
                headers['Content-Type'] = "application/json; charset=UTF-8"
            try:
                if isinstance(body, str):
                    body = json.loads(body)
            except Exception as e:
                raise Exception(f"json格式不正确:{e}") from e
            r = AsyncRequest(url, token, headers=headers, timeout=timeout, json=body)
        elif body_type == BodyType.form:
            try:
                form_data = FormData()
                if isinstance(body, dict):
                    for key, value in body.items():
                        if isinstance(value, (str, int, float, bool)):
                            form_data.add_field(key, str(value))
                        elif isinstance(value, list):
                            form_data.add_field(key, json.dumps(value))
                        else:
                            form_data.add_field(key, str(value))
                elif isinstance(body, str):
                    items = json.loads(body)
                    for item in items:
                        if item.get("type") == "TEXT":
                            form_data.add_field(item.get("key"), item.get("value", ''))
                        else:
                            raise Exception("error creating form")
                else:
                    raise Exception("Body must be a dict or a JSON string for form data")
                r = AsyncRequest(url, token, headers=headers, data=form_data, timeout=timeout)
            except Exception as e:
                raise Exception(f"解析form-data失败: {str(e)}")
        elif body_type == BodyType.x_form:
            headers['Content-Type'] = "application/x-www-form-urlencoded"
            if isinstance(body, str):
                body = json.loads(body)
            r = AsyncRequest(url, token, headers=headers, data=body, timeout=timeout)
        else:
            r = AsyncRequest(url, token, headers=headers, timeout=timeout, data=body)
        return r

    def get_request_data(self):
        request_body = self
        if isinstance(self, bytes):
            request_body = request_body.decode()
        if isinstance(self, FormData):
            request_body = str(self)
        if isinstance(request_body, str) or request_body is None:
            return request_body
        return json.dumps(request_body, ensure_ascii=False, indent=4)

    @staticmethod
    async def collect(
            status, request_data, status_code=200, response=None, response_headers=None,
            request_headers=None, cookies=None, elapsed=None, msg="success", **kwargs
    ):
        def ensure_json_string(data):
            if isinstance(data, str):
                try:
                    json.loads(data)
                    return data
                except json.JSONDecodeError:
                    return json.dumps({"data": data}, ensure_ascii=False)
            elif isinstance(data, dict):
                return json.dumps(data, ensure_ascii=False)
            else:
                return json.dumps({}, ensure_ascii=False)

        request_headers = ensure_json_string(request_headers)
        response_headers = ensure_json_string(response_headers)

        if cookies is not None and not isinstance(cookies, str):
            cookies = json.dumps(cookies, ensure_ascii=False)
        elif cookies is None:
            cookies = json.dumps({}, ensure_ascii=False)
        return {
            "status": status, "response": response, "status_code": status_code,
            "request_data": AsyncRequest.get_request_data(request_data),
            "response_headers": response_headers,
            "request_headers": request_headers,
            "msg": "success" if status else f"http状态码为{status_code}",
            "cost": elapsed,
            "cookies": cookies,
            **kwargs,
        }


class LoginManager:
    def __init__(self):
        pass

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
            baseurl: str,
            username: str,
            password: str,
    ) -> Dict[str, Any]:
        """
        执行登录操作并将token存储到Redis
        :param baseurl: 基础URL
        :param username: 用户名
        :param password: 密码
        :param uuid: uuid(可修改)
        :param code: code(可修改)
        :return: 登录响应信息
        """
        try:
            # 首先尝试从Redis获取现有token
            redis_key = f'{RedisInitKeyConfig.TOKEN.key}:{username}'
            existing_token = await self.app.state.redis.get(redis_key)
            # if self.redis_client:
            #     existing_token = await self.redis_client.get(
            #         f'{RedisInitKeyConfig.TOKEN.key}:{username}'
            #     )
            if existing_token:
                if await self.verify_token(baseurl, existing_token):
                    return {"status": True, "token": existing_token, "msg": "Using cached token"}

            # 执行新的登录请求
            r = await AsyncRequest.client(
                url=f'{baseurl}/api/auth/jwt/miniLogin',
                body_type=BodyType.json,
                body={
                    "username": username,
                    "password": password
                }
            )
            raw_response = await r.invoke(method='post')
            response_str = raw_response['response']
            response_json = json.loads(response_str)

            if raw_response['status']:
                token = response_json['data']['accessToken']
                full_token = f"Bearer {token}"
                # 存储token到Redis
                if self.redis_client:
                    await self.redis_client.set(
                        f'{RedisInitKeyConfig.TOKEN.key}:{username}',
                        full_token,
                        ex=timedelta(minutes=10)
                    )
                return {
                    "status": True,
                    "token": full_token,
                    "msg": "Login successful",
                    "data": response_json['data']
                }
            return {
                "status": False,
                "msg": "Login failed",
                "data": response_json
            }
        except Exception as e:
            return {
                "status": False,
                "msg": f"Token refresh error: {str(e)}",
                "data": None
            }


async def example_usage():
    login_manager = LoginManager()  # 首先创建实例
    try:
        baseurl = "https://www.convercomm.com"
        username = "ran_001"
        password = "3H/5JXwqnCGKh+s="

        # 登录并获取token
        login_result = await login_manager.login(
            baseurl=baseurl,
            username=username,
            password=password
        )

        if login_result["status"]:
            # 使用token进行其他操作
            token = login_result["token"]
            print(f"Login successful, token: {token}")

            # 验证token
            is_valid = await login_manager.verify_token(baseurl, token)
            print(f"Token is valid: {is_valid}")

            # # 如果需要，刷新token
            # refresh_result = await AsyncRequest.refresh_token(baseurl, username, token)
            # if refresh_result["status"]:
            #     print(f"Token refreshed: {refresh_result['token']}")
    except Exception as e:
        print(f"Error during login: {str(e)}")


async def main():
    # 获取 token
    baseurl = "https://www.convercomm.com"
    r = await AsyncRequest.client(
        url=f'{baseurl}/api/auth/jwt/miniLogin',
        body_type=BodyType.json,
        body={
            "username": "ran_001",
            "password": "3H/5JXwqnCGKh+s="
        }
    )
    raw_response = await r.invoke(method='post')
    response_str = raw_response['response']
    response_json = json.loads(response_str)
    token = f"Bearer {response_json['data']['accessToken']}"

    # 查询倾角图表
    url = f'{baseurl}/api/admin/packetInfo/getDevicePacketChart'
    body = {
        "imei": "BD012307272000FB",
        "startTime": "2024-04-01 00:00:00",
        "endTime": "2024-04-08 23:59:59"
    }
    r = await AsyncRequest.client(
        url,
        token,
        body_type=BodyType.json,
        body=body
    )
    raw_response = await r.invoke(method='post')

    # 使用 collect 方法整理响应数据
    formatted_response = await AsyncRequest.collect(
        status=True,
        request_data=None,  # 或者你的请求数据
        status_code=raw_response.get('status_code', 200),
        response=raw_response.get('response'),
        response_headers=raw_response.get('response_headers'),
        request_headers=raw_response.get('request_headers'),
        cookies=raw_response.get('cookies'),
        elapsed=raw_response.get('cost'),
        msg="请求成功"  # 或者根据实际情况设置消息
    )
    print(json.dumps(formatted_response, ensure_ascii=False, indent=2))

    # 发送 get 请求
    # url = 'http://127.0.0.1:9099/dev-api/apitest/apiInfo/list'
    # token = f"Bearer {token}"
    # data = {"pageNum": "1", "pageSize": "10"}
    # r = await AsyncRequest.client(url, token, data=data, body_type=BodyType.form)
    # raw_response = await r.invoke(method='get')
    # # 使用 collect 方法整理响应数据
    # formatted_response = await AsyncRequest.collect(
    #     status=True,
    #     request_data=None,  # 或者你的请求数据
    #     status_code=raw_response.get('status_code', 200),
    #     response=raw_response.get('response'),
    #     response_headers=raw_response.get('response_headers'),
    #     request_headers=raw_response.get('request_headers'),
    #     cookies=raw_response.get('cookies'),
    #     elapsed=raw_response.get('cost'),
    #     msg="请求成功"  # 或者根据实际情况设置消息
    # )
    # print(json.dumps(formatted_response, ensure_ascii=False, indent=2))

    # 发送 post 请求
    # url = 'http://127.0.0.1:9099/dev-api/apitest/apiInfo'
    # body = {
    #     "apiId": 90,
    #     "apiName": "90",
    #     "projectId": 1,
    #     "apiMethod": "GET",
    #     "apiUrl": "/login",
    #     "apiStatus": "0",
    #     "apiLevel": "P1",
    #     "apiTags": [
    #         "登录",
    #         "注册"
    #     ],
    #     "requestDataType": 1,
    #     "requestData": [
    #         {
    #             "name": "ranyong"
    #         }
    #     ],
    #     "requestHeaders": [
    #         {
    #             "key": "Authorization",
    #             "value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImE1YzQ5MDhhLTNjMTgtNDE1Ni1hNTkwLWFkMGIyZDY1NDNhYSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTEyLjk2LjIyNC4xMzgiLCJsb2dpbkxvY2F0aW9uIjoiXHU0ZTlhXHU2ZDMyLVx1NWU3Zlx1NGUxY1x1NzcwMSIsImJyb3dzZXIiOiJDaHJvbWUgMTA5Iiwib3MiOiJNYWMgT1MgWCAxMCIsImxvZ2luVGltZSI6IjIwMjQtMDktMjYgMjA6NTc6MzMifSwiZXhwIjoxNzI3NDQxODUzfQ.UMV9sONUcsMOje0eMmrfwJRlzST29DsQR5XaPinsSiU",
    #             "remarks": "这是一个请求头"
    #         }
    #     ],
    #     "createBy": "admin",
    #     "createTime": "2024-10-08T21:30:43",
    #     "updateBy": "admin",
    #     "updateTime": "2024-10-08T21:30:43",
    #     "remark": "string"
    # }
    # r = await AsyncRequest.client(
    #     url,
    #     token,
    #     body_type=BodyType.json,
    #     body=body
    # )
    # raw_response = await r.invoke(method='post')
    #
    # # 使用 collect 方法整理响应数据
    # formatted_response = await AsyncRequest.collect(
    #     status=True,
    #     request_data=None,  # 或者你的请求数据
    #     status_code=raw_response.get('status_code', 200),
    #     response=raw_response.get('response'),
    #     response_headers=raw_response.get('response_headers'),
    #     request_headers=raw_response.get('request_headers'),
    #     cookies=raw_response.get('cookies'),
    #     elapsed=raw_response.get('cost'),
    #     msg="请求成功"  # 或者根据实际情况设置消息
    # )
    # print(json.dumps(formatted_response, ensure_ascii=False, indent=2))

    # PUT请求with form data
    # url = 'http://127.0.0.1:9099/dev-api/apitest/apiInfo'
    # body = {
    #     "apiId": 4,
    #     "apiName": "游戏",
    #     "projectId": 1,
    #     "apiMethod": "POST",
    #     "apiUrl": "/login",
    #     "apiStatus": "0",
    #     "apiLevel": "P1",
    #     "apiTags": [
    #         "123",
    #         "注册"
    #     ],
    #     "requestDataType": "x_www_form_urlencoded",
    #     "requestData": [
    #         {
    #             "key": "ranyong",
    #             "value": "yong",
    #             "remarks": "这是 x_www_form_urlencoded"
    #         }
    #     ],
    #     "requestHeaders": [
    #         {
    #             "key": "Authorization",
    #             "value": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6ImE1YzQ5MDhhLTNjMTgtNDE1Ni1hNTkwLWFkMGIyZDY1NDNhYSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjoiMTEyLjk2LjIyNC4xMzgiLCJsb2dpbkxvY2F0aW9uIjoiXHU0ZTlhXHU2ZDMyLVx1NWU3Zlx1NGUxY1x1NzcwMSIsImJyb3dzZXIiOiJDaHJvbWUgMTA5Iiwib3MiOiJNYWMgT1MgWCAxMCIsImxvZ2luVGltZSI6IjIwMjQtMDktMjYgMjA6NTc6MzMifSwiZXhwIjoxNzI3NDQxODUzfQ.UMV9sONUcsMOje0eMmrfwJRlzST29DsQR5XaPinsSiU",
    #             "remarks": "这是一个请求头"
    #         }
    #     ],
    #     "createBy": "admin",
    #     "createTime": "2024-09-27T17:43:19",
    #     "updateBy": "admin",
    #     "updateTime": "2024-09-27T17:43:19",
    #     "remark": "这是一个编辑功能"
    # }
    # r = await AsyncRequest.client(
    #     url,
    #     token,
    #     body_type=BodyType.json,
    #     body=body
    # )
    # raw_response = await r.invoke(method='PUT')
    # formatted_response = await AsyncRequest.collect(
    #     status=True,
    #     request_data=None,  # 或者你的请求数据
    #     status_code=raw_response.get('status_code', 200),
    #     response=raw_response.get('response'),
    #     response_headers=raw_response.get('response_headers'),
    #     request_headers=raw_response.get('request_headers'),
    #     cookies=raw_response.get('cookies'),
    #     elapsed=raw_response.get('cost'),
    #     msg="请求成功"  # 或者根据实际情况设置消息
    # )
    # print(json.dumps(formatted_response, ensure_ascii=False, indent=2))

    # 发送 delete 请求
    # url = 'http://127.0.0.1:9099/dev-api/apitest/apiInfo/90'
    # r = await AsyncRequest.client(
    #     url,
    #     token,
    #     body_type=BodyType.none,
    # )
    # raw_response = await r.invoke(method='DELETE')
    # # 使用 collect 方法整理响应数据
    # formatted_response = await AsyncRequest.collect(
    #     status=raw_response['status_code'] == 200,
    #     request_data=r.get_data(r.kwargs),
    #     status_code=raw_response.get('status_code', 200),
    #     response=raw_response.get('response'),
    #     response_headers=raw_response.get('response_headers'),
    #     request_headers=raw_response.get('request_headers'),
    #     cookies=raw_response.get('cookies'),
    #     elapsed=raw_response.get('cost'),
    #     msg="请求成功" if raw_response['status_code'] == 200 else f"请求失败，状态码：{raw_response['status_code']}"
    # )
    # print(json.dumps(formatted_response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.run(example_usage())
