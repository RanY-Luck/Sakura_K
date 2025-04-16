#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/15 15:10
# @Author   : 冉勇
# @File     : ai_websocket.py
# @Software : PyCharm
# @Desc     : 封装websocket请求
import os
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from mcp_server.mcp_client import MCPClient
from utils.log_util import logger


async def init_ai_websocket(app: FastAPI):
    logger.info('开始启动MCP服务...')

    @app.websocket("/ws/chat")
    async def websocket_endpoint(websocket: WebSocket):
        await websocket.accept()
        user_id = id(websocket)
        user_contexts = {user_id: [{"role": "system", "content": "You are a helpful assistant."}]}
        client = MCPClient()
        await client.connect_to_server("mcp_server/mcp_server.py")
        try:
            while True:
                user_msg = await websocket.receive_text()
                user_contexts[user_id].append({"role": "user", "content": user_msg})
                await websocket.send_json({"role": "user", "content": user_msg})
                assistant_reply = ""
                response = client.put_query(user_msg)
                await websocket.send_json({"start": True})
                async for content_piece in response:
                    assistant_reply += content_piece
                    await websocket.send_json({"role": "assistant", "content": content_piece})
                await websocket.send_json({"done": True})
        except WebSocketDisconnect:
            print("WebSocket 断开连接")
            # 清理上下文
            user_contexts.pop(user_id, None)
            await client.cleanup()
