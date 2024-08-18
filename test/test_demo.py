#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/18 11:00
# @Author  : 冉勇
# @Site    : 
# @File    : test_demo.py
# @Software: PyCharm
# @desc    :
from fastapi.testclient import TestClient

from server import app


def test_get_post_list():
    with TestClient(app) as client:
        response = client.get(
            '/system/post/list',
            headers={
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjE0NmIyYmE5LWUzZDgtNGUyZi05ZTZjLWFjNTY5OThlNWZkNiIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjpudWxsLCJsb2dpbkxvY2F0aW9uIjoiXHU2NzJhXHU3N2U1IiwiYnJvd3NlciI6IkNocm9tZSAxMDkiLCJvcyI6Ik1hYyBPUyBYIDEwIiwibG9naW5UaW1lIjoiMjAyNC0wOC0xOCAxMjo0MTozNyJ9LCJleHAiOjE3MjQwNDI0OTd9.qaK2CFCP_oJ67yZ5Rd7rkkh1ZCUvpTE9_MHU5AVcIR8'
            },
        )
        assert response.status_code == 200
        assert response.json().get('code') == 200
