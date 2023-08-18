#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/11 19:50
# @Author  : 冉勇
# @Site    : 
# @File    : response.py
# @Software: PyCharm
# @desc    : 响应
# 赖安装：pip install orjson
from fastapi.responses import ORJSONResponse as Response
from fastapi import status as http_status
from utils import status as http


class SuccessResponse(Response):
    """
    成功响应
    代码解释：
    首先将传入的参数封装为一个字典对象，其中包括了响应状态码、消息和数据。
    self.data.update(kwargs)用于将额外提供的其他参数添加到响应数据中。
    最后，调用父类FastAPI中Response类的构造函数，传入响应数据和HTTP状态码，以创建一个自定义的HTTP响应类。
    """

    def __init__(
            self, data=None, msg="success", code=http.HTTP_SUCCESS, status=http_status.HTTP_200_OK
            , **kwargs
    ):
        self.data = {
            "code": code,
            "message": msg,
            "data": data
        }
        self.data = {
            "code": code,
            "message": msg,
            "data": data
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)


class ErrorResponse(Response):
    """
    失败响应
    代码解释：
    首先创建了一个包含 code、message 和一个空数组作为 data的字典对象 self.data，其中用于存储错误相关的数据信息。
    self.data.update(kwargs) 用于将额外提供的其他参数添加到响应数据中，以便客户端进行解析和处理。
    最后，通过调用父类 FastAPI 中 Response 类的构造函数，传入响应数据和 HTTP 状态码，创建了一个自定义的 HTTP 错误响应类。
    """

    def __init__(self, msg=None, code=http.HTTP_ERROR, status=http_status.HTTP_200_OK, **kwargs):
        self.data = {
            "code": code,
            "message": msg,
            "data": []
        }
        self.data.update(kwargs)
        super().__init__(content=self.data, status_code=status)
