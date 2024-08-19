# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# # @Time    : 2024/8/18 11:00
# # @Author  : 冉勇
# # @Site    :
# # @File    : test_demo.py
# # @Software: PyCharm
# # @desc    :
# import pytest
# from fastapi.testclient import TestClient
# from server import app
#
#
# @pytest.fixture
# def client():
#     return TestClient(app)
#
#
def auth_headers():
    return {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiMSIsInVzZXJfbmFtZSI6ImFkbWluIiwiZGVwdF9uYW1lIjoiXHU3ODE0XHU1M2QxXHU5MGU4XHU5NWU4Iiwic2Vzc2lvbl9pZCI6IjA3MzBmM2VmLTA4ZmMtNGJkMC1hYWYzLWZiODdlMmU0NDE1YSIsImxvZ2luX2luZm8iOnsiaXBhZGRyIjpudWxsLCJsb2dpbkxvY2F0aW9uIjoiXHU2NzJhXHU3N2U1IiwiYnJvd3NlciI6Ik90aGVyIiwib3MiOiJPdGhlciIsImxvZ2luVGltZSI6IjIwMjQtMDgtMTggMTg6NDU6NDIifSwiZXhwIjoxNzI0MDY0MzQyfQ.Om2j7K2pU6OAryJ9YYKUvK9Kffi8nzngiSJTQKDtkcY"}


#
# def test_get_system_post_list(client):
#     with TestClient(app) as client:
#         response = client.get(
#             '/system/post/list',
#             headers=auth_headers()
#         )
#         assert response.status_code == 200
#         assert response.json().get('code') == 200
#         assert response.json().get('msg') == "操作成功"
#
#
# def test_post_post(client):
#     with TestClient(app) as client:
#         response = client.post(
#             url='/system/post',
#             json={
#                 "postId": 99,
#                 "postCode": "test",
#                 "postName": "test",
#                 "postSort": 1,
#                 "status": "0",
#                 "createBy": "admin",
#                 "createTime": "2024-08-13T18:18:19",
#                 "updateBy": "",
#                 "updateTime": "2024-08-13T18:18:19",
#                 "remark": "这是一个测试"
#             },
#             headers=auth_headers()
#         )
#         # assert response.status_code == 200
#         assert response.json().get('code') == 200
#         # assert response.json().get('msg') == "新增成功"


import pytest
from httpx import AsyncClient
from server import app


@pytest.mark.anyio
async def test_root():
    async with AsyncClient(
            app=app,
            base_url="http://127.0.0.1:9099"
    ) as ac:
        response = await ac.get("/system/post/list", headers=auth_headers())
    assert response.status_code == 200
