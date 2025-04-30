#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/19 14:38
# @Author   : 冉勇
# @File     : ctx.py
# @Software : PyCharm
# @Desc     :
import contextvars
from uuid import uuid4

CTX_REQUEST_ID: contextvars.ContextVar[str] = contextvars.ContextVar('request-id', default='')


class TraceCtx:
    @staticmethod
    def set_id():
        _id = uuid4().hex
        CTX_REQUEST_ID.set(_id)
        return _id
    
    @staticmethod
    def set_id_with_value(trace_id: str):
        """
        使用指定的值设置trace_id
        """
        CTX_REQUEST_ID.set(trace_id)
        return trace_id

    @staticmethod
    def get_id():
        return CTX_REQUEST_ID.get()
