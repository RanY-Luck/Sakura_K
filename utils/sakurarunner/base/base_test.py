#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/7 13:58
# @Author   : 冉勇
# @File     : base_test.py
# @Software : PyCharm
# @Desc     :
import requests

from core.logger import logger


class BaseTest:
    response_json = None
    response = None

    @staticmethod
    def RunRequest(method, url, headers, payload=()):
        """
        发起请求
        :param method: 请求方法
        :param url: 请求URL
        :param headers: 请求头
        :param payload: 请求参数
        :return:
        """
        logger.info(f'🏄URL: {url}')
        logger.info(f'🌐Headers: {headers}')
        logger.info(f'🌐Payload: {payload}')
        logger.info(f'🌐Method: {method}')
        response = requests.request(method=method, url=url, headers=headers, data=payload, verify=False)
        logger.info(f'🌐response status_code: {response.status_code}')
        if response.status_code == 200:
            # 打印返回内容，用于调试
            # logger.info(f'🌐response: {response.text}')
            BaseTest.response_json = response.json()
            BaseTest.response = response
            return response
        else:
            BaseTest.response = response
            return response

    @staticmethod
    def assert_status_code(expected_code: int):
        """
        返回码断言
        :param expected_code:
        :return:
        """
        logger.info(f'------------------🔎返回码断言-------------------')
        status_code = BaseTest.response.status_code
        logger.info(f'status_code: {status_code}')
        logger.info(f'expected_code: {expected_code}')
        assert status_code == expected_code, f"Expected status code: {expected_code}, Actual status code: {BaseTest.response.status_code}"


if __name__ == '__main__':
    BaseTest.RunRequest(
        method="GET", url="http://127.0.0.1:9000/openapi.json", headers={
            'Authorization': '{{admin-token}}',
            'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Host': '127.0.0.1:9000',
            'Connection': 'keep-alive'
        }
    )
    BaseTest.assert_status_code(200)
