#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/28 12:00
# @Author   : 冉勇
# @File     : streamable_http_websocket.py
# @Software : PyCharm
# @Desc     : MCP服务的streamablehttp_client WebSocket服务器示例

import os
import json
import asyncio
import time
import argparse
from typing import Dict, Any, List, Optional, Union

# 导入FastAPI和WebSocket相关组件
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# 导入MCP的streamablehttp_client
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

# 如果有日志工具，可以导入
try:
    from utils.log_util import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("streamable_http_websocket")


class MCPWebSocketManager:
    """
    MCP WebSocket连接管理器
    用于管理WebSocket连接和MCP客户端会话
    """
    
    def __init__(self):
        """初始化WebSocket连接管理器"""
        self.active_connections: Dict[str, WebSocket] = {}
        self.mcp_clients: Dict[str, ClientSession] = {}
        self.connection_timeout = float(os.getenv("MCP_CONNECTION_TIMEOUT", "30.0"))
    
    async def connect(self, websocket: WebSocket, client_id: str) -> None:
        """
        建立WebSocket连接
        
        Args:
            websocket: WebSocket连接
            client_id: 客户端ID
        """
        await websocket.accept()
        self.active_connections[client_id] = websocket
        logger.info(f"WebSocket客户端连接: {client_id}")
    
    def disconnect(self, client_id: str) -> None:
        """
        断开WebSocket连接
        
        Args:
            client_id: 客户端ID
        """
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        # 清理MCP客户端会话
        asyncio.create_task(self._cleanup_mcp_client(client_id))
        logger.info(f"WebSocket客户端断开连接: {client_id}")
    
    async def _cleanup_mcp_client(self, client_id: str) -> None:
        """
        清理MCP客户端会话
        
        Args:
            client_id: 客户端ID
        """
        if client_id in self.mcp_clients:
            try:
                await self.mcp_clients[client_id].close()
            except Exception as e:
                logger.error(f"清理MCP客户端会话失败: {str(e)}")
            finally:
                del self.mcp_clients[client_id]
    
    async def connect_mcp(self, client_id: str, server_url: str) -> Dict[str, Any]:
        """
        连接到MCP服务器
        
        Args:
            client_id: 客户端ID
            server_url: MCP服务器URL
            
        Returns:
            连接结果
        """
        # 如果已经连接，先断开
        if client_id in self.mcp_clients:
            await self._cleanup_mcp_client(client_id)
        
        try:
            # 使用aiohttp连接
            import aiohttp
            
            # 创建HTTP会话
            http_session = aiohttp.ClientSession()
            
            # 尝试直接获取工具列表，跳过健康检查
            try:
                async with http_session.get(f"{server_url}/tools") as response:
                    if response.status != 200:
                        # 尝试另一个常见端点
                        async with http_session.get(f"{server_url}/api/tools") as alt_response:
                            if alt_response.status != 200:
                                raise Exception(f"无法获取工具列表，状态码: {response.status}")
                            tools_data = await alt_response.json()
                    else:
                        tools_data = await response.json()
                    
                    available_tools = tools_data.get("tools", [])
                    tools = [{"name": tool.get("name"), "description": tool.get("description", "")} 
                            for tool in available_tools]
                    logger.info(f"服务器工具: {[tool.get('name') for tool in available_tools]}")
            except Exception as e:
                # 如果无法获取工具列表，尝试直接创建会话
                logger.warning(f"无法获取工具列表: {str(e)}，将创建空工具列表")
                tools = []
            
            # 创建简单的会话
            class SimpleSession:
                def __init__(self, http_session, server_url):
                    self.http_session = http_session
                    self.server_url = server_url
                
                async def initialize(self):
                    pass
                
                async def list_tools(self):
                    async with self.http_session.get(f"{self.server_url}/tools") as response:
                        if response.status != 200:
                            raise Exception(f"无法获取工具列表，状态码: {response.status}")
                        
                        return await response.json()
                
                async def call_tool(self, tool_name, args):
                    async with self.http_session.post(
                        f"{self.server_url}/tools/{tool_name}",
                        json=args
                    ) as response:
                        if response.status not in (200, 201):
                            raise Exception(f"工具调用失败，状态码: {response.status}")
                        
                        return await response.json()
                
                async def stream_tool(self, tool_name, args):
                    async with self.http_session.post(
                        f"{self.server_url}/tools/{tool_name}/stream",
                        json=args
                    ) as response:
                        if response.status != 200:
                            raise Exception(f"流式工具调用失败，状态码: {response.status}")
                        
                        async for line in response.content:
                            if line.strip():
                                try:
                                    data = json.loads(line)
                                    yield data
                                except json.JSONDecodeError:
                                    yield line.decode('utf-8')
                
                async def call_resource(self, resource_path, params):
                    path = resource_path.replace("sakura://", "")
                    async with self.http_session.get(
                        f"{self.server_url}/resources/{path}",
                        params=params
                    ) as response:
                        if response.status != 200:
                            raise Exception(f"资源调用失败，状态码: {response.status}")
                        
                        return await response.json()
                
                async def close(self):
                    await self.http_session.close()
            
            # 创建会话
            session = SimpleSession(http_session, server_url)
            await session.initialize()
            
            # 存储会话
            self.mcp_clients[client_id] = session
            
            logger.info(f"客户端 {client_id} 已连接到MCP服务器: {server_url}")
            return {
                "status": "success",
                "message": f"已连接到MCP服务器: {server_url}",
                "tools": tools
            }
        except Exception as e:
            # 详细记录外部异常
            import traceback
            logger.error(f"连接MCP服务器失败: {str(e)}\n{traceback.format_exc()}")
            return {
                "status": "error",
                "message": f"连接MCP服务器失败: {str(e)}"
            }
    
    async def call_tool(self, client_id: str, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用MCP工具
        
        Args:
            client_id: 客户端ID
            tool_name: 工具名称
            args: 工具参数
            
        Returns:
            工具调用结果
        """
        if client_id not in self.mcp_clients:
            return {
                "status": "error",
                "message": "未连接到MCP服务器"
            }
        
        try:
            session = self.mcp_clients[client_id]
            result = await session.call_tool(tool_name, args)
            return {
                "status": "success",
                "result": result
            }
        except Exception as e:
            logger.error(f"调用工具失败: {str(e)}")
            return {
                "status": "error",
                "message": f"调用工具失败: {str(e)}"
            }
    
    async def stream_tool(self, client_id: str, tool_name: str, args: Dict[str, Any]) -> None:
        """
        流式调用MCP工具并通过WebSocket发送结果
        
        Args:
            client_id: 客户端ID
            tool_name: 工具名称
            args: 工具参数
        """
        if client_id not in self.mcp_clients or client_id not in self.active_connections:
            return
        
        websocket = self.active_connections[client_id]
        session = self.mcp_clients[client_id]
        
        try:
            # 发送开始流式调用的消息
            await websocket.send_json({
                "type": "stream_start",
                "tool": tool_name
            })
            
            # 流式调用工具并发送结果
            async for chunk in session.stream_tool(tool_name, args):
                # 根据数据类型处理
                if isinstance(chunk, dict):
                    await websocket.send_json({
                        "type": "stream_chunk",
                        "format": "json",
                        "data": chunk
                    })
                elif isinstance(chunk, str):
                    await websocket.send_json({
                        "type": "stream_chunk",
                        "format": "text",
                        "data": chunk
                    })
                else:
                    await websocket.send_json({
                        "type": "stream_chunk",
                        "format": "other",
                        "data": str(chunk)
                    })
            
            # 发送流式调用结束的消息
            await websocket.send_json({
                "type": "stream_end",
                "tool": tool_name
            })
        except Exception as e:
            logger.error(f"流式调用工具失败: {str(e)}")
            # 发送错误消息
            await websocket.send_json({
                "type": "stream_error",
                "message": f"流式调用工具失败: {str(e)}"
            })


# 创建FastAPI应用
app = FastAPI(title="MCP WebSocket服务", description="使用WebSocket连接MCP服务")

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境应该限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建WebSocket连接管理器
manager = MCPWebSocketManager()

# HTML页面，用于测试WebSocket连接
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>MCP WebSocket测试</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
            }
            #log {
                width: 100%;
                height: 300px;
                border: 1px solid #ccc;
                overflow-y: auto;
                padding: 10px;
                margin-bottom: 20px;
                font-family: monospace;
            }
            .input-group {
                margin-bottom: 10px;
            }
            label {
                display: block;
                margin-bottom: 5px;
            }
            input[type="text"] {
                width: 100%;
                padding: 5px;
                box-sizing: border-box;
            }
            button {
                padding: 8px 15px;
                background-color: #4CAF50;
                color: white;
                border: none;
                cursor: pointer;
                margin-right: 10px;
            }
            button:hover {
                background-color: #45a049;
            }
            .stream {
                color: #2196F3;
            }
            .error {
                color: #f44336;
            }
            .success {
                color: #4CAF50;
            }
        </style>
    </head>
    <body>
        <h1>MCP WebSocket测试</h1>
        
        <div id="log"></div>
        
        <div class="input-group">
            <label for="serverUrl">MCP服务器URL:</label>
            <input type="text" id="serverUrl" value="http://localhost:8000">
        </div>
        
        <div class="input-group">
            <label for="toolName">工具名称:</label>
            <input type="text" id="toolName" value="query_weather">
        </div>
        
        <div class="input-group">
            <label for="args">工具参数 (JSON格式):</label>
            <input type="text" id="args" value='{"city": "Shanghai"}'>
        </div>
        
        <button onclick="connectWebSocket()">连接WebSocket</button>
        <button onclick="connectMCP()">连接MCP服务器</button>
        <button onclick="callTool()">调用工具</button>
        <button onclick="streamTool()">流式调用工具</button>
        <button onclick="disconnect()">断开连接</button>
        
        <script>
            let ws = null;
            const clientId = "client_" + Math.random().toString(36).substr(2, 9);
            const logElement = document.getElementById('log');
            
            function log(message, className) {
                const entry = document.createElement('div');
                if (className) {
                    entry.className = className;
                }
                entry.textContent = message;
                logElement.appendChild(entry);
                logElement.scrollTop = logElement.scrollHeight;
            }
            
            function connectWebSocket() {
                if (ws) {
                    log("已经连接到WebSocket", "error");
                    return;
                }
                
                const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
                const wsUrl = `${protocol}//${window.location.host}/ws/${clientId}`;
                
                log(`正在连接到WebSocket: ${wsUrl}`);
                ws = new WebSocket(wsUrl);
                
                ws.onopen = function(event) {
                    log("WebSocket连接已建立", "success");
                };
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === "stream_chunk") {
                        let content = data.data;
                        if (data.format === "json") {
                            content = JSON.stringify(data.data);
                        }
                        log(`[流] ${content}`, "stream");
                    } else if (data.type === "stream_start") {
                        log(`开始流式调用工具: ${data.tool}`, "stream");
                    } else if (data.type === "stream_end") {
                        log(`结束流式调用工具: ${data.tool}`, "stream");
                    } else if (data.type === "stream_error") {
                        log(`流式调用错误: ${data.message}`, "error");
                    } else {
                        log(`收到消息: ${JSON.stringify(data)}`);
                    }
                };
                
                ws.onclose = function(event) {
                    log("WebSocket连接已关闭", "error");
                    ws = null;
                };
                
                ws.onerror = function(event) {
                    log("WebSocket错误", "error");
                };
            }
            
            function connectMCP() {
                if (!ws) {
                    log("请先连接WebSocket", "error");
                    return;
                }
                
                const serverUrl = document.getElementById('serverUrl').value;
                log(`正在连接到MCP服务器: ${serverUrl}`);
                
                ws.send(JSON.stringify({
                    action: "connect_mcp",
                    server_url: serverUrl
                }));
            }
            
            function callTool() {
                if (!ws) {
                    log("请先连接WebSocket", "error");
                    return;
                }
                
                const toolName = document.getElementById('toolName').value;
                const argsStr = document.getElementById('args').value;
                
                try {
                    const args = JSON.parse(argsStr);
                    log(`调用工具: ${toolName}, 参数: ${argsStr}`);
                    
                    ws.send(JSON.stringify({
                        action: "call_tool",
                        tool_name: toolName,
                        args: args
                    }));
                } catch (e) {
                    log(`参数格式错误: ${e.message}`, "error");
                }
            }
            
            function streamTool() {
                if (!ws) {
                    log("请先连接WebSocket", "error");
                    return;
                }
                
                const toolName = document.getElementById('toolName').value;
                const argsStr = document.getElementById('args').value;
                
                try {
                    const args = JSON.parse(argsStr);
                    log(`流式调用工具: ${toolName}, 参数: ${argsStr}`);
                    
                    ws.send(JSON.stringify({
                        action: "stream_tool",
                        tool_name: toolName,
                        args: args
                    }));
                } catch (e) {
                    log(`参数格式错误: ${e.message}`, "error");
                }
            }
            
            function disconnect() {
                if (ws) {
                    ws.close();
                    log("已断开WebSocket连接");
                }
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get_html():
    """返回HTML测试页面"""
    return HTMLResponse(html)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    """
    WebSocket端点
    
    Args:
        websocket: WebSocket连接
        client_id: 客户端ID
    """
    await manager.connect(websocket, client_id)
    
    try:
        while True:
            # 接收WebSocket消息
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action", "")
            
            # 处理不同类型的消息
            if action == "connect_mcp":
                server_url = message.get("server_url", "http://localhost:8000")
                result = await manager.connect_mcp(client_id, server_url)
                await websocket.send_json(result)
            
            elif action == "call_tool":
                tool_name = message.get("tool_name", "")
                args = message.get("args", {})
                result = await manager.call_tool(client_id, tool_name, args)
                await websocket.send_json(result)
            
            elif action == "stream_tool":
                tool_name = message.get("tool_name", "")
                args = message.get("args", {})
                await manager.stream_tool(client_id, tool_name, args)
            
            else:
                await websocket.send_json({
                    "status": "error",
                    "message": f"未知操作: {action}"
                })
    
    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket处理错误: {str(e)}")
        try:
            await websocket.send_json({
                "status": "error",
                "message": f"处理错误: {str(e)}"
            })
        except:
            pass
        manager.disconnect(client_id)


async def shutdown_event():
    """应用关闭时的清理操作"""
    for client_id in list(manager.mcp_clients.keys()):
        await manager.mcp_clients[client_id].close()
    manager.mcp_clients.clear()
    manager.active_connections.clear()


app.add_event_handler("shutdown", shutdown_event)


if __name__ == "__main__":
    # 解析命令行参数
    parser = argparse.ArgumentParser(description='MCP WebSocket服务器')
    parser.add_argument('--host', type=str, default='127.0.0.1', help='监听主机')
    parser.add_argument('--port', type=int, default=8080, help='监听端口')
    args = parser.parse_args()
    
    # 导入uvicorn并启动服务器
    import uvicorn
    uvicorn.run(app, host=args.host, port=args.port) 