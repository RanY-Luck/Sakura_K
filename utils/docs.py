#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/8/26 11:25
# @Author  : 冉勇
# @Site    : 
# @File    : docs.py
# @Software: PyCharm
# @desc    :
# 自定义接口文档静态文件：https://fastapi.tiangolo.com/how-to/custom-docs-ui-assets/
from fastapi import FastAPI
from fastapi.openapi.docs import (
    get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
)
from config.env import AppConfig


def custom_api_docs(app: FastAPI):
    """
    自定义配置接口本地静态文档
    :param app:
    :return:
    """

    @app.get("/docs", include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.get_swagger_ui_oauth2_redirect_html,
            swagger_js_url="/static/swagger_ui/swagger-ui-bundle.js",
            swagger_css_url="/static/swagger_ui/swagger-ui.css",
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get("/redoc", include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=app.openapi_url,
            title=AppConfig.app_name + " - ReDoc",
            redoc_js_url="/static/redoc_ui/redoc.standalone.js",
        )
