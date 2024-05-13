#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/11 22:26
# @Author  : 冉勇
# @Site    : 
# @File    : web_access.py
# @Software: PyCharm
# @desc    : 网页存活

import time
import requests


# 访问页面
def test_access(web_url):
    access_info = {}
    start_time = time.time()
    try:
        response = requests.get(web_url, timeout=5)
        access_info["status_code"] = response.status_code
        if response.status_code != 200:
            access_info["detail"] = response.text
        # 响应时间
        access_info["time"] = str(int((time.time() - start_time) * 1000)) + " ms"
    except Exception as e:
        access_info["status_code"] = 500
        access_info["detail"] = str(e)
        access_info["time"] = None
    return access_info


# 获取所有需要测试网址的状态
def test_all(web_urls):
    access_infos = {}
    for web_url in web_urls:
        access_infos[web_url] = test_access(web_url)
    return access_infos


if __name__ == "__main__":
    print(test_all(["https://www.baidu.com", "https://www.google.com"]))
