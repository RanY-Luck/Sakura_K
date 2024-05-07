#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/5/7 13:58
# @Author   : 冉勇
# @File     : base_test.py
# @Software : PyCharm
# @Desc     :
import time

import jmespath
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

    @staticmethod
    def assert_response_time(max_time: int):
        """
        返回时间断言,用于测试接口在max_time时间内的响应
        :param max_time: 最大响应时间
        :return:
        """
        logger.info(f'------------------🔎返回时间断言-------------------')
        response_time = BaseTest.response.elapsed.total_seconds()
        logger.info(f'response_time: {response_time}(s)')
        logger.info(f'max_time: {max_time}(s)')
        assert response_time < max_time, f"Response time exceeds maximum allowed time of {max_time} seconds"

    @staticmethod
    def assert_equal(jmes_path, expected_value, msg=None):
        """
        jmes_path断言
        官方文档：https://www.osgeo.cn/jmespath/tutorial.html
        :param jmes_path: jmes_path路径
        :param expected_value: 期望值
        :param msg: 断言失败提示
        :return:
        """
        logger.info(f'------------------🔎返回Json断言-------------------')
        actual_value = jmespath.search(jmes_path, BaseTest.response_json)
        logger.info(f'actual_value: {actual_value}')
        logger.info(f'jmes_path: {jmes_path}')
        logger.info(f'expected_value: {expected_value}({type(expected_value).__name__})')
        logger.info(f'actual_value: {actual_value}({type(actual_value).__name__})')
        if msg is not None:
            assert actual_value == expected_value, f"{msg}"
        assert actual_value == expected_value, f"断言失败"

    @staticmethod
    def extract_value(jmes_path):
        """
        根据jmes_path提取参数
        :param jmes_path: jmes_path路径
        :return:
        """
        logger.info(f'------------------🎨提取变量-------------------')
        value = jmespath.search(jmes_path, BaseTest.response_json)
        logger.info(f'jmes_path: {jmes_path}')
        logger.info(f'value: {value}')
        return value

    @staticmethod
    def wait(seconds: int):
        """
        强制等待时间
        :param seconds: 等待时间
        :return:
        """
        logger.info(f'------------------⏰️等待{seconds}秒-------------------')
        time.sleep(seconds)


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
    BaseTest.assert_response_time(3)
    BaseTest.assert_equal('openapi', '3.1.0')
    BaseTest.extract_value('openapi')
    BaseTest.wait(3)
