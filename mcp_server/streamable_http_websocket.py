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
    
    async def connect_mcp(self, client_id: str, server_url: str, tools_path: str = None) -> Dict[str, Any]:
        """
        连接到MCP服务器
        
        Args:
            client_id: 客户端ID
            server_url: MCP服务器URL
            tools_path: 自定义工具API路径（可选）
            
        Returns:
            连接结果
        """
        # 如果已经连接，先断开
        if client_id in self.mcp_clients:
            await self._cleanup_mcp_client(client_id)
        
        try:
            # 使用aiohttp连接
            import aiohttp
            
            # 创建HTTP会话，设置超时
            timeout = aiohttp.ClientTimeout(total=10)  # 10秒总超时
            http_session = aiohttp.ClientSession(timeout=timeout)
            
            # 尝试获取工具列表
            tools = []
            tools_found = False
            connection_error = None
            
            # 定义可能的API路径
            if tools_path is None:
                paths_to_try = [
                    "/ws/chat",       # 添加WebSocket聊天API路径
                    "/tools", 
                    "/api/tools", 
                    "/v1/tools", 
                    "/api/v1/tools", 
                    "/mcp/tools", 
                    "/mcp/api/tools"
                ]
            else:
                paths_to_try = [tools_path]
                
            # 尝试所有可能的路径
            for path in paths_to_try:
                try:
                    full_url = f"{server_url}{path}"
                    logger.info(f"尝试从 {full_url} 获取工具列表")
                    
                    # 对于/ws/chat路径使用WebSocket连接
                    if path == "/ws/chat":
                        try:
                            # 尝试使用WebSocket连接
                            import websockets
                            
                            # 将http://替换为ws://，https://替换为wss://
                            ws_url = full_url.replace("http://", "ws://").replace("https://", "wss://")
                            logger.info(f"尝试WebSocket连接: {ws_url}")
                            
                            async with websockets.connect(ws_url) as websocket:
                                # 发送工具列表请求
                                await websocket.send(json.dumps({"type": "list_tools"}))
                                
                                # 接收响应
                                response = await websocket.recv()
                                tools_data = json.loads(response)
                                
                                if "tools" in tools_data:
                                    available_tools = tools_data.get("tools", [])
                                    tools = [{"name": tool.get("name"), "description": tool.get("description", "")} 
                                            for tool in available_tools]
                                    logger.info(f"成功从WebSocket {ws_url} 获取到 {len(tools)} 个工具")
                                    tools_found = True
                                    connection_error = None
                                    break
                        except ImportError:
                            logger.warning("未安装websockets库，无法使用WebSocket连接")
                            connection_error = "未安装websockets库，无法使用WebSocket连接"
                        except Exception as e:
                            logger.warning(f"WebSocket连接失败: {str(e)}")
                            connection_error = f"WebSocket连接失败: {str(e)}"
                    else:
                        # 使用HTTP连接
                        async with http_session.get(full_url) as response:
                            if response.status == 200:
                                tools_data = await response.json()
                                available_tools = tools_data.get("tools", [])
                                tools = [{"name": tool.get("name"), "description": tool.get("description", "")} 
                                        for tool in available_tools]
                                logger.info(f"成功从 {full_url} 获取到 {len(tools)} 个工具")
                                tools_found = True
                                connection_error = None
                                break
                            else:
                                logger.warning(f"请求 {full_url} 返回状态码: {response.status}")
                                if not connection_error:
                                    connection_error = f"服务器返回状态码: {response.status}"
                except aiohttp.ClientConnectorError as e:
                    logger.warning(f"连接到 {full_url} 失败: {str(e)}")
                    if not connection_error:
                        connection_error = f"连接错误: {str(e)}"
                except aiohttp.ClientError as e:
                    logger.warning(f"HTTP客户端错误: {str(e)}")
                    if not connection_error:
                        connection_error = f"HTTP客户端错误: {str(e)}"
                except asyncio.TimeoutError:
                    logger.warning(f"连接 {full_url} 超时")
                    if not connection_error:
                        connection_error = "连接超时，请检查服务器地址和端口是否正确"
                except Exception as e:
                    logger.warning(f"尝试路径 {path} 失败: {str(e)}")
                    if not connection_error:
                        connection_error = str(e)
            
            if not tools_found:
                if connection_error:
                    logger.warning(f"无法连接到MCP服务器: {connection_error}")
                    await http_session.close()
                    return {
                        "status": "error",
                        "message": f"无法连接到MCP服务器: {connection_error}",
                        "error_type": "connection_error"
                    }
                else:
                    logger.warning(f"无法在任何路径获取工具列表，将创建空工具列表")
            
            # 创建简单的会话类
            class SimpleSession:
                def __init__(self, http_session, server_url):
                    self.http_session = http_session
                    self.server_url = server_url
                    self.api_paths = {
                        "tools": next((p for p in paths_to_try if tools_found), "/tools")
                    }
                    # 记录是否使用WebSocket
                    self.use_websocket = self.api_paths["tools"] == "/ws/chat"
                    self.ws_connection = None
                
                async def initialize(self):
                    if self.use_websocket:
                        import websockets
                        ws_url = self.server_url.replace("http://", "ws://").replace("https://", "wss://") + "/ws/chat"
                        self.ws_connection = await websockets.connect(ws_url)
                
                async def list_tools(self):
                    if self.use_websocket:
                        if not self.ws_connection:
                            await self.initialize()
                        
                        await self.ws_connection.send(json.dumps({"type": "list_tools"}))
                        response = await self.ws_connection.recv()
                        return json.loads(response)
                    else:
                        api_path = self.api_paths.get("tools", "/tools")
                        try:
                            async with self.http_session.get(f"{self.server_url}{api_path}") as response:
                                if response.status != 200:
                                    raise Exception(f"无法获取工具列表，状态码: {response.status}")
                                
                                return await response.json()
                        except Exception as e:
                            logger.error(f"获取工具列表失败: {str(e)}")
                            raise
                
                async def call_tool(self, tool_name, args):
                    if self.use_websocket:
                        if not self.ws_connection:
                            await self.initialize()
                        
                        # 使用WebSocket调用工具
                        request = {
                            "type": "call_tool",
                            "tool": tool_name,
                            "args": args
                        }
                        await self.ws_connection.send(json.dumps(request))
                        response = await self.ws_connection.recv()
                        return json.loads(response)
                    else:
                        # 尝试不同的工具调用路径
                        potential_paths = [
                            f"/tools/{tool_name}",
                            f"/api/tools/{tool_name}",
                            f"{self.api_paths.get('tools', '/tools')}/{tool_name}"
                        ]
                        
                        last_error = None
                        for path in potential_paths:
                            try:
                                async with self.http_session.post(
                                    f"{self.server_url}{path}",
                                    json=args
                                ) as response:
                                    if response.status in (200, 201):
                                        return await response.json()
                                    last_error = f"工具调用失败，状态码: {response.status}"
                            except Exception as e:
                                last_error = str(e)
                        
                        raise Exception(f"所有尝试都失败: {last_error}")
                
                async def stream_tool(self, tool_name, args):
                    if self.use_websocket:
                        if not self.ws_connection:
                            await self.initialize()
                        
                        # 使用WebSocket流式调用工具
                        request = {
                            "type": "stream_tool",
                            "tool": tool_name,
                            "args": args
                        }
                        await self.ws_connection.send(json.dumps(request))
                        
                        # 持续接收流式响应
                        while True:
                            response = await self.ws_connection.recv()
                            data = json.loads(response)
                            
                            # 如果是结束标记，退出循环
                            if data.get("type") == "stream_end":
                                break
                                
                            yield data
                    else:
                        # 尝试不同的流式工具调用路径
                        potential_paths = [
                            f"/tools/{tool_name}/stream",
                            f"/api/tools/{tool_name}/stream",
                            f"{self.api_paths.get('tools', '/tools')}/{tool_name}/stream"
                        ]
                        
                        last_error = None
                        for path in potential_paths:
                            try:
                                async with self.http_session.post(
                                    f"{self.server_url}{path}",
                                    json=args
                                ) as response:
                                    if response.status == 200:
                                        async for line in response.content:
                                            if line.strip():
                                                try:
                                                    data = json.loads(line)
                                                    yield data
                                                except json.JSONDecodeError:
                                                    yield line.decode('utf-8')
                                        return
                                    last_error = f"流式工具调用失败，状态码: {response.status}"
                            except Exception as e:
                                last_error = str(e)
                        
                        raise Exception(f"所有尝试都失败: {last_error}")
                
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
                    if self.ws_connection:
                        await self.ws_connection.close()
                    await self.http_session.close()
            
            # 创建会话
            session = SimpleSession(http_session, server_url)
            await session.initialize()
            
            # 存储会话
            self.mcp_clients[client_id] = session
            
            logger.info(f"客户端 {client_id} 已连接到MCP服务器: {server_url}")
            return {
                "status": "success",
                "message": f"已连接到MCP服务器: {server_url}" + (f", 发现 {len(tools)} 个工具" if tools else ", 未找到可用工具"),
                "tools": tools
            }
        except Exception as e:
            # 详细记录外部异常
            import traceback
            logger.error(f"连接MCP服务器失败: {str(e)}\n{traceback.format_exc()}")
            return {
                "status": "error",
                "message": f"连接MCP服务器失败: {str(e)}",
                "error_type": "general_error"
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
                margin-bottom: 10px;
            }
            button:hover {
                background-color: #45a049;
            }
            button:disabled {
                background-color: #cccccc;
                cursor: not-allowed;
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
            .info {
                color: #9c27b0;
            }
            .debug-panel {
                background-color: #f5f5f5;
                padding: 10px;
                margin-top: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            .tabs {
                display: flex;
                margin-bottom: 10px;
            }
            .tab {
                padding: 8px 15px;
                cursor: pointer;
                background-color: #eee;
                margin-right: 5px;
            }
            .tab.active {
                background-color: #4CAF50;
                color: white;
            }
            .tab-content {
                display: none;
            }
            .tab-content.active {
                display: block;
            }
            .server-status {
                padding: 8px;
                margin-top: 10px;
                border-radius: 4px;
            }
            .status-unknown {
                background-color: #f5f5f5;
                color: #666;
            }
            .status-online {
                background-color: #e8f5e9;
                color: #2e7d32;
            }
            .status-offline {
                background-color: #ffebee;
                color: #c62828;
            }
            .presets {
                display: flex;
                flex-wrap: wrap;
                margin-bottom: 10px;
            }
            .preset {
                padding: 5px 10px;
                margin-right: 5px;
                margin-bottom: 5px;
                background-color: #e0e0e0;
                border-radius: 3px;
                cursor: pointer;
            }
            .preset:hover {
                background-color: #bdbdbd;
            }
        </style>
    </head>
    <body>
        <h1>MCP WebSocket测试</h1>
        
        <div id="log"></div>
        
        <div class="tabs">
            <div class="tab active" data-tab="basic">基本设置</div>
            <div class="tab" data-tab="advanced">高级设置</div>
            <div class="tab" data-tab="connection">连接测试</div>
        </div>
        
        <div id="basic-tab" class="tab-content active">
            <div class="input-group">
                <label for="serverUrl">MCP服务器URL:</label>
                <input type="text" id="serverUrl" value="http://localhost:8000">
                <div class="presets">
                    <div class="preset" data-url="http://localhost:8000">本地:8000</div>
                    <div class="preset" data-url="http://localhost:8080">本地:8080</div>
                    <div class="preset" data-url="http://localhost:3000">本地:3000</div>
                    <div class="preset" data-url="http://127.0.0.1:8000">127.0.0.1:8000</div>
                </div>
            </div>
            
            <div class="input-group">
                <label for="toolsPath">API路径:</label>
                <input type="text" id="toolsPath" placeholder="/api/tools">
                <div class="presets">
                    <div class="preset" data-path="/ws/chat">WebSocket API (/ws/chat)</div>
                    <div class="preset" data-path="/tools">REST API (/tools)</div>
                    <div class="preset" data-path="/api/tools">REST API (/api/tools)</div>
                </div>
            </div>
            
            <div class="input-group">
                <label for="toolName">工具名称:</label>
                <input type="text" id="toolName" value="query_weather">
            </div>
            
            <div class="input-group">
                <label for="args">工具参数 (JSON格式):</label>
                <input type="text" id="args" value='{"city": "Shanghai"}'>
            </div>
        </div>
        
        <div id="advanced-tab" class="tab-content">
            <div class="input-group">
                <label for="verboseLogging">
                    <input type="checkbox" id="verboseLogging"> 启用详细日志
                </label>
            </div>
            
            <div class="input-group">
                <label for="connectionTimeout">
                    连接超时 (秒):
                    <input type="number" id="connectionTimeout" value="10" min="1" max="60">
                </label>
            </div>
        </div>
        
        <div id="connection-tab" class="tab-content">
            <h3>服务器连接测试</h3>
            <div class="server-status status-unknown" id="server-status">
                未测试连接状态
            </div>
            <button onclick="testServerConnection()">测试服务器连接</button>
            <div id="connection-details"></div>
        </div>
        
        <div>
            <button onclick="connectWebSocket()">连接WebSocket</button>
            <button onclick="connectMCP()" id="connect-mcp-btn">连接MCP服务器</button>
            <button onclick="callTool()" id="call-tool-btn" disabled>调用工具</button>
            <button onclick="streamTool()" id="stream-tool-btn" disabled>流式调用工具</button>
            <button onclick="disconnect()">断开连接</button>
            <button onclick="clearLog()">清空日志</button>
        </div>
        
        <div class="debug-panel">
            <h3>调试面板</h3>
            <div id="debug-info"></div>
        </div>
        
        <script>
            let ws = null;
            let mcpConnected = false;
            const clientId = "client_" + Math.random().toString(36).substr(2, 9);
            const logElement = document.getElementById('log');
            const debugInfoElement = document.getElementById('debug-info');
            const callToolBtn = document.getElementById('call-tool-btn');
            const streamToolBtn = document.getElementById('stream-tool-btn');
            
            // 标签页切换
            document.querySelectorAll('.tab').forEach(tab => {
                tab.addEventListener('click', function() {
                    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
                    
                    this.classList.add('active');
                    document.getElementById(this.dataset.tab + '-tab').classList.add('active');
                });
            });
            
            // 预设URL点击处理
            document.querySelectorAll('.preset[data-url]').forEach(preset => {
                preset.addEventListener('click', function() {
                    document.getElementById('serverUrl').value = this.dataset.url;
                });
            });
            
            // API路径预设点击处理
            document.querySelectorAll('.preset[data-path]').forEach(preset => {
                preset.addEventListener('click', function() {
                    document.getElementById('toolsPath').value = this.dataset.path;
                });
            });
            
            function log(message, className) {
                const entry = document.createElement('div');
                if (className) {
                    entry.className = className;
                }
                entry.textContent = new Date().toLocaleTimeString() + " - " + message;
                logElement.appendChild(entry);
                logElement.scrollTop = logElement.scrollHeight;
            }
            
            function updateDebugInfo() {
                if (!ws) {
                    debugInfoElement.textContent = "未连接到WebSocket";
                    return;
                }
                
                const serverUrl = document.getElementById('serverUrl').value;
                const toolsPath = document.getElementById('toolsPath').value;
                
                debugInfoElement.innerHTML = `
                    <div>客户端ID: ${clientId}</div>
                    <div>WebSocket状态: ${ws.readyState === 1 ? '已连接' : '未连接'}</div>
                    <div>MCP连接状态: ${mcpConnected ? '已连接' : '未连接'}</div>
                    <div>服务器URL: ${serverUrl}</div>
                    <div>工具API路径: ${toolsPath || '(自动尝试)'}</div>
                `;
            }
            
            function clearLog() {
                logElement.innerHTML = '';
                log("日志已清空", "info");
            }
            
            async function testServerConnection() {
                const serverUrl = document.getElementById('serverUrl').value;
                const statusElement = document.getElementById('server-status');
                const detailsElement = document.getElementById('connection-details');
                
                statusElement.className = 'server-status status-unknown';
                statusElement.textContent = '正在测试连接...';
                detailsElement.innerHTML = '';
                
                try {
                    const timeout = parseInt(document.getElementById('connectionTimeout').value) * 1000 || 10000;
                    const controller = new AbortController();
                    const timeoutId = setTimeout(() => controller.abort(), timeout);
                    
                    // 先测试基本的HTTP连接
                    const response = await fetch(serverUrl, {
                        method: 'HEAD',
                        signal: controller.signal
                    }).catch(error => {
                        throw new Error(`无法连接到服务器: ${error.message}`);
                    });
                    
                    clearTimeout(timeoutId);
                    
                    statusElement.className = 'server-status status-online';
                    statusElement.textContent = '服务器在线！';
                    
                    // 尝试检测API路径
                    const restPaths = ['/tools', '/api/tools', '/v1/tools', '/api/v1/tools'];
                    let apiFound = false;
                    
                    detailsElement.innerHTML = '<p>正在检测API路径...</p>';
                    
                    // 先尝试WebSocket API
                    try {
                        const wsUrl = serverUrl.replace("http://", "ws://").replace("https://", "wss://") + "/ws/chat";
                        detailsElement.innerHTML += `<p>尝试WebSocket连接: ${wsUrl}</p>`;
                        
                        const ws = new WebSocket(wsUrl);
                        
                        // 创建一个Promise来处理WebSocket连接
                        const wsPromise = new Promise((resolve, reject) => {
                            const wsTimeout = setTimeout(() => {
                                ws.close();
                                reject(new Error("WebSocket连接超时"));
                            }, 5000);
                            
                            ws.onopen = () => {
                                clearTimeout(wsTimeout);
                                
                                // 发送工具列表请求
                                ws.send(JSON.stringify({type: "list_tools"}));
                                
                                // 等待响应
                                ws.onmessage = (event) => {
                                    const data = JSON.parse(event.data);
                                    if (data.tools) {
                                        resolve({
                                            path: "/ws/chat",
                                            toolCount: data.tools.length,
                                            isWebSocket: true
                                        });
                                    } else {
                                        reject(new Error("未收到有效的工具列表"));
                                    }
                                    ws.close();
                                };
                            };
                            
                            ws.onerror = (error) => {
                                clearTimeout(wsTimeout);
                                reject(error);
                            };
                        });
                        
                        try {
                            const result = await wsPromise;
                            detailsElement.innerHTML += `<p class="success">✅ 发现WebSocket API路径: ${result.path}</p>`;
                            detailsElement.innerHTML += `<p>发现 ${result.toolCount} 个工具</p>`;
                            
                            // 自动设置路径
                            document.getElementById('toolsPath').value = result.path;
                            apiFound = true;
                        } catch (e) {
                            detailsElement.innerHTML += `<p>WebSocket API不可用: ${e.message}</p>`;
                        }
                    } catch (e) {
                        detailsElement.innerHTML += `<p>WebSocket API测试失败: ${e.message}</p>`;
                    }
                    
                    // 如果WebSocket API不可用，尝试REST API
                    if (!apiFound) {
                        for (const path of restPaths) {
                            try {
                                const apiResponse = await fetch(`${serverUrl}${path}`, {
                                    method: 'GET',
                                    headers: { 'Accept': 'application/json' }
                                });
                                
                                if (apiResponse.ok) {
                                    detailsElement.innerHTML += `<p class="success">✅ 发现REST API路径: ${path}</p>`;
                                    apiFound = true;
                                    
                                    // 自动设置路径
                                    document.getElementById('toolsPath').value = path;
                                    
                                    try {
                                        const data = await apiResponse.json();
                                        const toolCount = data.tools ? data.tools.length : 0;
                                        detailsElement.innerHTML += `<p>发现 ${toolCount} 个工具</p>`;
                                    } catch (e) {
                                        detailsElement.innerHTML += `<p class="error">无法解析API响应: ${e.message}</p>`;
                                    }
                                    
                                    break;
                                }
                            } catch (e) {
                                // 忽略错误，继续尝试其他路径
                            }
                        }
                    }
                    
                    if (!apiFound) {
                        detailsElement.innerHTML += '<p class="error">未找到有效的API路径</p>';
                        detailsElement.innerHTML += '<p>请手动设置API路径或尝试其他服务器URL</p>';
                    }
                    
                } catch (error) {
                    statusElement.className = 'server-status status-offline';
                    statusElement.textContent = '服务器离线或无法访问';
                    detailsElement.innerHTML = `<p class="error">${error.message}</p>`;
                }
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
                    document.getElementById('connect-mcp-btn').disabled = false;
                    updateDebugInfo();
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
                        if (document.getElementById('verboseLogging').checked) {
                            log(`收到消息: ${JSON.stringify(data)}`, "info");
                        } else {
                            // 只显示关键信息
                            if (data.status === "success") {
                                log(`成功: ${data.message || "操作成功"}`, "success");
                                
                                // 处理MCP连接成功
                                if (data.message && data.message.includes("已连接到MCP服务器")) {
                                    mcpConnected = true;
                                    callToolBtn.disabled = false;
                                    streamToolBtn.disabled = false;
                                    
                                    if (data.tools) {
                                        log(`获取到 ${data.tools.length} 个工具`, "info");
                                    }
                                }
                            } else if (data.status === "error") {
                                log(`错误: ${data.message}`, "error");
                                
                                // 特殊处理连接错误
                                if (data.error_type === "connection_error") {
                                    log("提示: 请检查服务器URL和端口是否正确，或使用连接测试功能", "info");
                                }
                            }
                        }
                    }
                    
                    updateDebugInfo();
                };
                
                ws.onclose = function(event) {
                    log("WebSocket连接已关闭", "error");
                    ws = null;
                    mcpConnected = false;
                    callToolBtn.disabled = true;
                    streamToolBtn.disabled = true;
                    document.getElementById('connect-mcp-btn').disabled = true;
                    updateDebugInfo();
                };
                
                ws.onerror = function(event) {
                    log("WebSocket错误", "error");
                    updateDebugInfo();
                };
            }
            
            function connectMCP() {
                if (!ws) {
                    log("请先连接WebSocket", "error");
                    return;
                }
                
                const serverUrl = document.getElementById('serverUrl').value;
                const toolsPath = document.getElementById('toolsPath').value;
                
                log(`正在连接到MCP服务器: ${serverUrl}${toolsPath ? ` (工具路径: ${toolsPath})` : ''}`);
                
                const request = {
                    action: "connect_mcp",
                    server_url: serverUrl
                };
                
                if (toolsPath) {
                    request.tools_path = toolsPath;
                }
                
                ws.send(JSON.stringify(request));
                updateDebugInfo();
            }
            
            function callTool() {
                if (!ws) {
                    log("请先连接WebSocket", "error");
                    return;
                }
                
                if (!mcpConnected) {
                    log("请先连接MCP服务器", "error");
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
                
                if (!mcpConnected) {
                    log("请先连接MCP服务器", "error");
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
                    mcpConnected = false;
                    callToolBtn.disabled = true;
                    streamToolBtn.disabled = true;
                    updateDebugInfo();
                }
            }
            
            // 页面加载时初始化UI
            document.addEventListener('DOMContentLoaded', function() {
                // 默认为详细日志关闭
                document.getElementById('verboseLogging').checked = false;
                
                // 禁用工具调用按钮，直到连接成功
                callToolBtn.disabled = true;
                streamToolBtn.disabled = true;
                document.getElementById('connect-mcp-btn').disabled = true;
                
                updateDebugInfo();
            });
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
                tools_path = message.get("tools_path", None)
                logger.info(f"客户端 {client_id} 请求连接到 {server_url}，工具路径: {tools_path}")
                result = await manager.connect_mcp(client_id, server_url, tools_path)
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