#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/18 11:00
# @Author  : 冉勇
# @Site    : 
# @File    : test_demo.py
# @Software: PyCharm
# @desc    :
import pytest
from fastapi.testclient import TestClient

from server import app


@pytest.fixture
def client():
    return TestClient(app)


def auth_headers():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjIwMzdlZWViLTIzMjYtNGVhMy1hNGI1LTlmM2Q2MTMyZmI1ZSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjpudWxsLCJsb2dpbkxvY2F0aW9uIjoiXHU2NzJhXHU3N2U1IiwiYnJvd3NlciI6Ik90aGVyIiwib3MiOiJPdGhlciIsImxvZ2luVGltZSI6IjIwMjQtMDgtMTggMTc6Mjk6MTYifSwiZXhwIjoxNzI0MDU5NzU2fQ.86a-ItXgED6U70ysHraIhcGE-UwHVwtVIVrlq5njm4E"}


def test_get_post_list(client):
    with TestClient(app) as client:
        response = client.get(
            '/system/post/list',
            headers=auth_headers()
        )
        assert response.status_code == 200
        assert response.json().get('code') == 200
