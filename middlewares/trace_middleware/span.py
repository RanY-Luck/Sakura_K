#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/19 14:38
# @Author   : 冉勇
# @File     : span.py
# @Software : PyCharm
# @Desc     :
from contextlib import asynccontextmanager
from starlette.types import Scope, Message
from .ctx import TraceCtx


class Span:
    """
    整个http生命周期：
        request(before) --> request(after) --> response(before) --> response(after)
    """

    def __init__(self, scope: Scope):
        self.scope = scope
        self.trace_id = None

    async def request_before(self):
        """
        request_before: 处理header信息等, 如记录请求体信息
        """
        # 生成或从请求头中获取trace_id
        self.trace_id = self._get_trace_id_from_headers() or TraceCtx.set_id()

    def _get_trace_id_from_headers(self):
        """
        从请求头中获取trace_id
        """
        if 'headers' in self.scope:
            for name, value in self.scope['headers']:
                if name.lower() == b'x-trace-id':
                    trace_id = value.decode()
                    TraceCtx.set_id_with_value(trace_id)
                    return trace_id
        return None

    async def request_after(self, message: Message):
        """
        request_after: 处理请求bytes， 如记录请求参数
        example:
            message: {'type': 'http.request', 'body': b'{\r\n    "name": "\xe8\x8b\x8f\xe8\x8b\x8f\xe8\x8b\x8f"\r\n}', 'more_body': False}
        """
        return message

    async def response(self, message: Message):
        """
        if message['type'] == "http.response.start":   -----> request-before
            pass
        if message['type'] == "http.response.body":    -----> request-after
            message.get('body', b'')
            pass
        """
        if message['type'] == 'http.response.start':
            # 添加trace_id到响应头
            trace_id = TraceCtx.get_id()
            message['headers'].append((b'x-trace-id', trace_id.encode()))
            
            # 确保内容类型是JSON的响应也包含trace_id
            for name, value in message['headers']:
                if name.lower() == b'content-type' and b'application/json' in value.lower():
                    # 在response.body中处理JSON响应
                    self.should_add_trace_to_json = True
                    break
        
        elif message['type'] == 'http.response.body' and hasattr(self, 'should_add_trace_to_json'):
            # 确保是JSON响应，并且有body
            body = message.get('body', b'')
            if body:
                import json
                try:
                    # 尝试解析JSON
                    data = json.loads(body)
                    if isinstance(data, dict):
                        # 添加trace_id到响应JSON
                        data['trace_id'] = TraceCtx.get_id()
                        # 更新响应body
                        message['body'] = json.dumps(data).encode()
                except (json.JSONDecodeError, UnicodeDecodeError):
                    # 如果不是有效的JSON，则不做任何处理
                    pass
        
        return message


@asynccontextmanager
async def get_current_span(scope: Scope):
    yield Span(scope)
