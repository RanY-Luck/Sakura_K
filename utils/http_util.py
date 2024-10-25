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
import urllib
from enum import IntEnum

import aiohttp
from aiohttp import FormData


class BodyType(IntEnum):
    """body类型"""
    none = 0
    json = 1
    form = 2
    x_form = 3
    raw = 4


class AsyncRequest(object):
    def __init__(self, url: str, token: str = None, timeout=15, **kwargs):
        """
        初始化请求客户端
        :param url: 请求URL
        :param token: 认证token
        :param timeout: 超时时间
        :param kwargs: 其他参数
        """
        self.url = url
        self.token = token
        self.kwargs = kwargs
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    def get_cookie(self, session):
        """获取会话cookie"""
        cookies = session.cookie_jar.filter_cookies(self.url)
        return {k: v.value for k, v in cookies.items()}

    def get_data(self, kwargs):
        """获取请求数据"""
        if kwargs.get("json") is not None:
            return kwargs.get("json")
        return kwargs.get("data")

    @staticmethod
    def get_request_data(data):
        """处理请求数据格式"""
        request_body = data
        if isinstance(data, bytes):
            request_body = request_body.decode()
        if isinstance(data, FormData):
            request_body = str(data)
        if isinstance(request_body, str) or request_body is None:
            return request_body
        return json.dumps(request_body, ensure_ascii=False, indent=4)

    async def invoke(self, method: str):
        """
        执行请求
        :param method: 请求方法
        :return: 响应结果
        """
        start = time.time()
        headers = self.kwargs.get('headers', {})
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        self.kwargs['headers'] = headers

        # 确保我们使用的是 json 参数
        if 'data' in self.kwargs and 'json' not in self.kwargs:
            self.kwargs['json'] = self.kwargs.pop('data')

        async with aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar(unsafe=True)) as session:
            try:
                async with session.request(
                        method, self.url, timeout=self.timeout,
                        ssl=False, **self.kwargs
                ) as resp:
                    cost = "%.0fms" % ((time.time() - start) * 1000)
                    response, json_format = await self.get_resp(resp)
                    cookie = self.get_cookie(session)

                    return await self.collect(
                        resp.status == 200,
                        self.get_data(self.kwargs),
                        resp.status,
                        response,
                        resp.headers,
                        resp.request_info.headers,
                        elapsed=cost,
                        cookies=cookie,
                        json_format=json_format
                    )
            except Exception as e:
                cost = "%.0fms" % ((time.time() - start) * 1000)
                return await self.collect(
                    False,
                    self.get_data(self.kwargs),
                    500,
                    str(e),
                    None,
                    headers,
                    elapsed=cost,
                    cookies=None,
                    json_format=False
                )

    @staticmethod
    async def get_resp(resp):
        """获取响应内容"""
        try:
            data = await resp.json(encoding='utf-8')
            return json.dumps(data, ensure_ascii=False, indent=4), True
        except:
            data = await resp.text()
            return data, False

    @staticmethod
    async def client(url: str, body: dict = None, body_type: BodyType = BodyType.json, timeout: int = 15, **kwargs):
        """
        异步请求客户端
        :param url: 请求URL
        :param body: 请求体
        :param body_type: 请求体类型
        :param timeout: 超时时间
        :param kwargs: 其他参数，包括 headers 等
        :return: AsyncRequest 实例
        """
        if not url.startswith(("http://", "https://")):
            raise Exception("请输入正确的url,带上http")
        headers = kwargs.get("headers", {})
        token = kwargs.get("token")  # 从kwargs中获取token
        body = body or kwargs.get("body", {})

        try:
            if body_type == "json":
                return await AsyncRequest._handle_json_request(url, headers, body, timeout, token)
            elif body_type == "form":
                return await AsyncRequest._handle_form_request(url, headers, body, timeout, token)
            elif body_type == "x_form":
                return await AsyncRequest._handle_x_form_request(url, headers, body, timeout, token)
            else:
                return AsyncRequest(url, token=token, headers=headers, timeout=timeout, data=body)
        except Exception as e:
            print(f"请求预处理错误: {str(e)}")
            raise

    @staticmethod
    async def _handle_json_request(url: str, headers: dict, body: dict, timeout: int, token: str = None):
        """处理 JSON 类型请求"""
        if "Content-Type" not in headers:
            headers['Content-Type'] = "application/json; charset=UTF-8"

        try:
            if isinstance(body, str):
                body = json.loads(body)
        except Exception as e:
            raise Exception(f"json格式不正确:{e}") from e

        return AsyncRequest(url, token=token, headers=headers, timeout=timeout, json=body)

    @staticmethod
    async def _handle_json_request(url, headers, body, timeout, token):
        """处理 JSON 格式的请求"""
        headers['Content-Type'] = 'application/json'

        # 确保 body 是正确的 JSON 格式
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                body = {"data": body}

        # 确保 body 是字典类型
        if not isinstance(body, dict):
            body = {"data": body}

        # 使用 json 参数而不是 data 参数
        return AsyncRequest(
            url,
            token=token,
            headers=headers,
            timeout=timeout,
            json=body  # 使用 json 参数让 aiohttp 自动处理 JSON 序列化
        )

    @staticmethod
    async def _handle_form_request(url, headers, body, timeout, token):
        """处理 form 格式的请求"""
        if not headers.get('Content-Type'):
            headers['Content-Type'] = 'application/x-www-form-urlencoded'

        # 确保 body 是字典类型
        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                # 如果不是有效的 JSON 字符串，尝试解析为表单数据
                try:
                    body = dict(urllib.parse.parse_qsl(body))
                except:
                    body = {"data": body}

        return AsyncRequest(
            url,
            token=token,
            headers=headers,
            timeout=timeout,
            data=body
        )

    @staticmethod
    async def _handle_x_form_request(url, headers, body, timeout, token):
        """处理 x-form 格式的请求"""
        if not headers.get('Content-Type'):
            headers['Content-Type'] = 'multipart/form-data'

        # 处理 multipart/form-data 格式
        form_data = aiohttp.FormData()

        if isinstance(body, str):
            try:
                body = json.loads(body)
            except json.JSONDecodeError:
                body = {"data": body}

        if isinstance(body, dict):
            for key, value in body.items():
                form_data.add_field(key, str(value))

        return AsyncRequest(
            url,
            token=token,
            headers=headers,
            timeout=timeout,
            data=form_data
        )

    @staticmethod
    async def collect(
            status, request_data, status_code=200, response=None, response_headers=None,
            request_headers=None, cookies=None, elapsed=None, msg="success", json_format=True, **kwargs
    ):
        """收集并格式化响应数据"""

        def format_headers(headers):
            """格式化 headers"""
            if headers is None:
                return "{}"

            # 如果是 aiohttp 的 CIMultiDictProxy，转换为普通字典
            if hasattr(headers, 'items'):
                headers_dict = dict(headers.items())
            elif isinstance(headers, dict):
                headers_dict = headers
            else:
                headers_dict = {}

            # 确保所有值都是字符串
            formatted_dict = {
                str(k): str(v) for k, v in headers_dict.items()
            }

            return json.dumps(formatted_dict, ensure_ascii=False)

        # 格式化请求和响应头
        formatted_request_headers = format_headers(request_headers)
        formatted_response_headers = format_headers(response_headers)

        # 处理 cookies
        if cookies is not None and not isinstance(cookies, str):
            cookies = json.dumps(cookies, ensure_ascii=False)
        elif cookies is None:
            cookies = json.dumps({}, ensure_ascii=False)

        # 处理请求数据
        if isinstance(request_data, (dict, list)):
            request_data = json.dumps(request_data, ensure_ascii=False)
        elif request_data is None:
            request_data = "{}"

        # 处理响应数据
        if response is None:
            response = "{}"
        elif not isinstance(response, str):
            response = json.dumps(response, ensure_ascii=False)

        return {
            "status": status,
            "response": response,
            "status_code": status_code,
            "request_data": request_data,
            "response_headers": formatted_response_headers,
            "request_headers": formatted_request_headers,
            "msg": "success" if status else f"http状态码为{status_code}",
            "cost": elapsed,
            "cookies": cookies,
            "json_format": json_format,
            **kwargs
        }


async def main():
    """示例：获取认证token并使用token请求数据"""
    baseurl = "https://www.convercomm.com"

    # 1. 获取认证token
    auth_request = await AsyncRequest.client(
        url=f'{baseurl}/api/auth/jwt/miniLogin',
        body={
            "username": "ran_dev",
            "password": "3H/5JXwqnCGKh+s="
        },
        body_type=BodyType.json
    )
    auth_response = await auth_request.invoke(method='post')

    # 解析token
    response_json = json.loads(auth_response['response'])
    token = response_json['data']['accessToken']  # 不需要手动添加"Bearer"前缀

    # 2. 使用token请求倾角图表数据
    chart_request = await AsyncRequest.client(
        url=f'{baseurl}/api/admin/packetInfo/getDevicePacketChart',
        body={
            "imei": "BD012307272000FB",
            "startTime": "2024-04-01 00:00:00",
            "endTime": "2024-04-08 23:59:59"
        },
        body_type=BodyType.json,
        token=token,  # 直接传入token，不需要添加"Bearer"前缀
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyYW5fMDAxIiwidXNlcklkIjoiNDk2IiwibmFtZSI6InJhbl8wMDEiLCJpZCI6IjFhQ1dacjdEIiwiZXhwIjoxNzMwNjQzODQzfQ.G5PkcS1NTuC2rNdNV78jUFro5y-sqFifHEW2G-5AliUds1Ye0e0vCLlsvPDC_XupwT0dmKbnE4YyKtVLF35FOzj42X0xbeZcPNkr3IEUHICBKEMyjqLUsRq_HOPZcY2EKmO4xV-yJFFR2IWyixHUC465oU9F9f2OlThV_sU6QhU"
        }
    )
    chart_response = await chart_request.invoke(method='post')

    # 打印响应数据（response中已经包含了完整的响应信息，不需要再次使用collect方法）
    print(json.dumps(chart_response, ensure_ascii=False, indent=2))


# 如果需要调试单个请求的完整信息，可以这样写：
async def debug_request():
    baseurl = "https://www.convercomm.com"
    auth_request = await AsyncRequest.client(
        url=f'{baseurl}/api/auth/jwt/miniLogin',
        body={
            "username": "ran_dev",
            "password": "3H/5JXwqnCGKh+s="
        },
        body_type=BodyType.json
    )
    raw_response = await auth_request.invoke(method='post')

    # 这部分是可选的，因为invoke已经使用了collect方法
    formatted_response = await AsyncRequest.collect(
        status=True,
        request_data=auth_request.get_data(auth_request.kwargs),
        status_code=raw_response.get('status_code', 200),
        response=raw_response.get('response'),
        response_headers=raw_response.get('response_headers'),
        request_headers=raw_response.get('request_headers'),
        cookies=raw_response.get('cookies'),
        elapsed=raw_response.get('cost'),
        msg="认证请求成功"
    )
    print(json.dumps(formatted_response, ensure_ascii=False, indent=2))


async def debug_token_request():
    baseurl = "https://www.convercomm.com"
    chart_request = await AsyncRequest.client(
        url=f'{baseurl}/api/admin/packetInfo/getDevicePacketChart',
        body={
            "imei": "BD012307272000FB",
            "startTime": "2024-04-01 00:00:00",
            "endTime": "2024-04-08 23:59:59"
        },
        body_type=BodyType.json,
        # token=token,  # 直接传入token，不需要添加"Bearer"前缀
        headers={
            "Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJyYW5fMDAxIiwidXNlcklkIjoiNDk2IiwibmFtZSI6InJhbl8wMDEiLCJpZCI6IjFhQ1dacjdEIiwiZXhwIjoxNzMwNjQzODQzfQ.G5PkcS1NTuC2rNdNV78jUFro5y-sqFifHEW2G-5AliUds1Ye0e0vCLlsvPDC_XupwT0dmKbnE4YyKtVLF35FOzj42X0xbeZcPNkr3IEUHICBKEMyjqLUsRq_HOPZcY2EKmO4xV-yJFFR2IWyixHUC465oU9F9f2OlThV_sU6QhU"
        }
    )
    chart_response = await chart_request.invoke(method='post')

    # 打印响应数据（response中已经包含了完整的响应信息，不需要再次使用collect方法）
    print(json.dumps(chart_response, ensure_ascii=False, indent=2))

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
    # asyncio.run(debug_request())
    asyncio.run(debug_token_request())
