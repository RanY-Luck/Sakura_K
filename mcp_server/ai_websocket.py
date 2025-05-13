#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/15 15:10
# @Author   : 冉勇
# @File     : ai_websocket.py
# @Software : PyCharm
# @Desc     : 封装websocket请求
import os
import time
import asyncio
from utils.log_util import logger
from typing import Dict, List, Any
from fastapi import FastAPI
from starlette.websockets import WebSocket, WebSocketDisconnect
from mcp_server.mcp_client import MCPClient


class ConnectionManager:
    """WebSocket连接管理器"""

    def __init__(self):
        # 活跃的WebSocket连接
        self.active_connections: Dict[int, WebSocket] = {}
        # 用户上下文存储
        self.user_contexts: Dict[int, List[Dict[str, str]]] = {}
        # MCP客户端缓存
        self.mcp_clients: Dict[int, MCPClient] = {}
        # 最后活动时间
        self.last_activity: Dict[int, float] = {}
        # 清理任务
        self.cleanup_task = None

    async def connect(self, websocket: WebSocket) -> int:
        """接受WebSocket连接并返回用户ID"""
        await websocket.accept()
        user_id = id(websocket)
        self.active_connections[user_id] = websocket
        self.user_contexts[user_id] = [{"role": "system", "content": "You are a helpful assistant."}]
        self.last_activity[user_id] = time.time()
        logger.info(f"WebSocket连接建立: {user_id}")
        return user_id

    async def disconnect(self, user_id: int) -> None:
        """断开连接并清理资源"""
        # 从活跃连接中删除
        self.active_connections.pop(user_id, None)
        # 清理上下文
        self.user_contexts.pop(user_id, None)
        # 清理最后活动时间
        self.last_activity.pop(user_id, None)

        # 清理并关闭MCP客户端
        if user_id in self.mcp_clients:
            client = self.mcp_clients.pop(user_id)
            try:
                await client.cleanup()
            except Exception as e:
                logger.error(f"清理MCP客户端时出错: {e}")

        logger.info(f"WebSocket连接关闭: {user_id}")

    async def send_message(self, user_id: int, message: Dict[str, Any]) -> None:
        """发送消息到指定WebSocket连接"""
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_json(message)
                self.last_activity[user_id] = time.time()
            except Exception as e:
                logger.error(f"发送消息失败: {e}")
                await self.disconnect(user_id)

    async def get_mcp_client(self, user_id: int) -> MCPClient:
        """获取或创建用户的MCP客户端"""
        if user_id not in self.mcp_clients:
            client = MCPClient()
            try:
                await client.connect_to_server("mcp_server/mcp_server.py")
                self.mcp_clients[user_id] = client
            except Exception as e:
                logger.error(f"创建MCP客户端失败: {e}")
                raise
        return self.mcp_clients[user_id]

    async def start_cleanup_task(self):
        """启动定期清理任务"""
        if self.cleanup_task is None:
            self.cleanup_task = asyncio.create_task(self._cleanup_inactive_connections())

    async def _cleanup_inactive_connections(self):
        """定期清理不活跃的连接（1小时无活动）"""
        while True:
            try:
                current_time = time.time()
                inactive_users = []

                for user_id, last_time in self.last_activity.items():
                    # 如果连接超过1小时没有活动
                    if current_time - last_time > 3600:
                        inactive_users.append(user_id)

                for user_id in inactive_users:
                    logger.info(f"清理不活跃连接: {user_id}")
                    await self.disconnect(user_id)

                # 每5分钟检查一次
                await asyncio.sleep(300)
            except Exception as e:
                logger.error(f"清理不活跃连接时出错: {e}")
                await asyncio.sleep(60)  # 出错时等待1分钟再重试


# 创建全局连接管理器
connection_manager = ConnectionManager()


async def init_ai_websocket(app: FastAPI):
    logger.info('开始启动MCP WebSocket服务...')

    # 启动清理任务
    await connection_manager.start_cleanup_task()

    @app.websocket("/ws/chat")
    async def websocket_endpoint(websocket: WebSocket):
        user_id = await connection_manager.connect(websocket)

        try:
            # 获取MCP客户端
            client = await connection_manager.get_mcp_client(user_id)

            while True:
                # 接收用户消息
                user_msg = await websocket.receive_text()
                # 更新用户上下文
                connection_manager.user_contexts[user_id].append({"role": "user", "content": user_msg})
                # 回显用户消息
                await connection_manager.send_message(user_id, {"role": "user", "content": user_msg})

                try:
                    # 发送开始标记
                    await connection_manager.send_message(user_id, {"start": True})

                    # 调用MCP客户端处理查询
                    assistant_reply = ""
                    response = client.put_query(user_msg)

                    # 流式返回响应
                    async for content_piece in response:
                        assistant_reply += content_piece
                        await connection_manager.send_message(
                            user_id,
                            {"role": "assistant", "content": content_piece}
                        )

                    # 发送完成标记
                    await connection_manager.send_message(user_id, {"done": True})

                    # 更新用户上下文
                    connection_manager.user_contexts[user_id].append(
                        {"role": "assistant", "content": assistant_reply}
                    )
                except Exception as e:
                    logger.error(f"处理用户消息时出错: {e}")
                    error_msg = f"处理您的请求时发生错误: {str(e)}"
                    await connection_manager.send_message(
                        user_id,
                        {"role": "assistant", "content": error_msg, "error": True}
                    )
                    await connection_manager.send_message(user_id, {"done": True})

        except WebSocketDisconnect:
            logger.info(f"WebSocket断开连接: {user_id}")
        except Exception as e:
            logger.error(f"WebSocket处理时出错: {e}")
        finally:
            # 清理用户资源
            await connection_manager.disconnect(user_id)
