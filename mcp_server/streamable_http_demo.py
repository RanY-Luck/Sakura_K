#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/28 10:00
# @Author   : 冉勇
# @File     : streamable_http_demo.py
# @Software : PyCharm
# @Desc     : MCP服务的streamablehttp_client示例

import os
import json
import asyncio
import time
from typing import Dict, Any, List, AsyncGenerator, Optional

# 导入MCP的streamablehttp_client
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession

# 如果有日志工具，可以导入
try:
    from utils.log_util import logger
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger("streamable_http_demo")


class StreamableHttpDemo:
    """
    使用streamablehttp_client的MCP客户端示例
    这个类演示了如何使用streamablehttp_client连接MCP服务
    """

    def __init__(self, 
                 server_url: str = "http://localhost:8000", 
                 retry_attempts: int = 3, 
                 retry_delay: float = 2.0):
        """
        初始化StreamableHttpDemo客户端
        
        Args:
            server_url: MCP服务器URL
            retry_attempts: 重试次数
            retry_delay: 重试延迟（秒）
        """
        self.server_url = server_url
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.connection_timeout = float(os.getenv("MCP_CONNECTION_TIMEOUT", "30.0"))
        
        # MCP会话
        self.session: Optional[ClientSession] = None
        self.available_tools = []
        self.is_connected = False
        self.connect_time = None

    async def connect_to_server(self) -> None:
        """
        连接到MCP服务器并列出可用工具
        
        使用streamablehttp_client连接到HTTP服务器
        """
        try:
            # 设置连接超时
            connect_task = self._connect_with_timeout()
            await asyncio.wait_for(connect_task, timeout=self.connection_timeout)
            
            # 列出服务器工具
            await self._list_available_tools()
            
            self.is_connected = True
            self.connect_time = time.time()
            logger.info(f"成功连接到MCP服务器: {self.server_url}")
            
        except asyncio.TimeoutError:
            await self.cleanup()
            raise Exception(f"连接MCP服务器超时，请检查服务器是否正常运行: {self.server_url}")
        except Exception as e:
            await self.cleanup()
            raise Exception(f"连接MCP服务器失败: {str(e)}")

    async def _connect_with_timeout(self) -> None:
        """
        在超时范围内尝试连接服务器
        
        使用aiohttp连接到HTTP服务器，替代streamablehttp_client
        """
        try:
            # 使用aiohttp连接
            import aiohttp
            
            # 创建HTTP会话
            self.http_session = aiohttp.ClientSession()
            
            # 尝试直接获取工具列表，跳过健康检查
            try:
                async with self.http_session.get(f"{self.server_url}/tools") as response:
                    if response.status != 200:
                        # 尝试另一个常见端点
                        async with self.http_session.get(f"{self.server_url}/api/tools") as alt_response:
                            if alt_response.status != 200:
                                raise Exception(f"无法获取工具列表，状态码: {response.status}")
                            tools_data = await alt_response.json()
                    else:
                        tools_data = await response.json()
                    
                    self.available_tools = tools_data.get("tools", [])
                    logger.info(f"服务器工具: {[tool.get('name') for tool in self.available_tools]}")
            except Exception as e:
                # 如果无法获取工具列表，尝试直接创建会话
                logger.warning(f"无法获取工具列表: {str(e)}，将创建空工具列表")
                self.available_tools = []
            
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
                        
                        tools_data = await response.json()
                        return tools_data
                
                async def call_tool(self, tool_name, args):
                    async with self.http_session.post(
                        f"{self.server_url}/tools/{tool_name}",
                        json=args
                    ) as response:
                        if response.status not in (200, 201):
                            raise Exception(f"工具调用失败，状态码: {response.status}")
                        
                        return await response.json()
                
                async def call_resource(self, resource_path, params):
                    path = resource_path.replace("sakura://", "")
                    async with self.http_session.get(
                        f"{self.server_url}/resources/{path}",
                        params=params
                    ) as response:
                        if response.status != 200:
                            raise Exception(f"资源调用失败，状态码: {response.status}")
                        
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
                
                async def stream_resource(self, resource_path, params=None):
                    path = resource_path.replace("sakura://", "")
                    async with self.http_session.get(
                        f"{self.server_url}/resources/{path}/stream",
                        params=params
                    ) as response:
                        if response.status != 200:
                            raise Exception(f"流式资源调用失败，状态码: {response.status}")
                        
                        async for line in response.content:
                            if line.strip():
                                try:
                                    data = json.loads(line)
                                    yield data
                                except json.JSONDecodeError:
                                    yield line.decode('utf-8')
                
                async def close(self):
                    await self.http_session.close()
            
            # 创建会话
            self.session = SimpleSession(self.http_session, self.server_url)
            await self.session.initialize()
        except asyncio.exceptions.CancelledError as e:
            logger.error(f"连接服务器被取消: {str(e)}")
            raise
        except Exception as inner_e:
            # 详细记录内部异常
            import traceback
            logger.error(f"连接服务器内部错误: {str(inner_e)}\n{traceback.format_exc()}")
            raise inner_e
        except Exception as e:
            # 详细记录外部异常
            import traceback
            logger.error(f"连接服务器失败: {str(e)}\n{traceback.format_exc()}")
            raise

    async def _list_available_tools(self) -> None:
        """
        获取并存储服务器可用工具
        """
        if not self.session:
            raise Exception("未连接到MCP服务器")
        
        response = await self.session.list_tools()
        self.available_tools = response.tools
        logger.info(f"服务器工具: {[tool.name for tool in self.available_tools]}")

    async def call_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        调用MCP服务器上的工具
        
        Args:
            tool_name: 工具名称
            args: 工具参数
            
        Returns:
            工具调用结果
        """
        if not self.is_connected or not self.session:
            raise Exception("未连接到MCP服务器，请先调用connect_to_server()")
        
        # 检查工具是否可用
        available_tool_names = [tool.name for tool in self.available_tools]
        if tool_name not in available_tool_names:
            raise Exception(f"工具 '{tool_name}' 不可用。可用工具: {available_tool_names}")
        
        # 调用工具
        for attempt in range(self.retry_attempts):
            try:
                logger.info(f"调用工具: {tool_name}, 参数: {args}")
                result = await self.session.call_tool(tool_name, args)
                logger.info(f"工具调用成功: {tool_name}")
                return result
            except Exception as e:
                logger.error(f"工具调用失败 (尝试 {attempt+1}/{self.retry_attempts}): {str(e)}")
                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise Exception(f"工具调用失败: {str(e)}")

    async def call_resource(self, resource_path: str, params: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        调用MCP服务器上的资源
        
        Args:
            resource_path: 资源路径
            params: 资源参数
            
        Returns:
            资源调用结果
        """
        if not self.is_connected or not self.session:
            raise Exception("未连接到MCP服务器，请先调用connect_to_server()")
        
        # 调用资源
        for attempt in range(self.retry_attempts):
            try:
                logger.info(f"调用资源: {resource_path}, 参数: {params or {}}")
                result = await self.session.call_resource(resource_path, params or {})
                logger.info(f"资源调用成功: {resource_path}")
                return result
            except Exception as e:
                logger.error(f"资源调用失败 (尝试 {attempt+1}/{self.retry_attempts}): {str(e)}")
                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    raise Exception(f"资源调用失败: {str(e)}")

    async def cleanup(self) -> None:
        """
        清理资源
        """
        if self.session:
            await self.session.close()
            self.session = None
        self.is_connected = False
        logger.info("已断开与MCP服务器的连接")


async def demo_weather_query(client: StreamableHttpDemo, city: str) -> None:
    """
    演示查询天气工具
    
    Args:
        client: StreamableHttpDemo客户端
        city: 城市名称
    """
    try:
        # 调用天气查询工具
        result = await client.call_tool("query_weather", {"city": city})
        print(f"\n===== 天气查询结果 =====\n{result}\n")
    except Exception as e:
        print(f"天气查询失败: {str(e)}")


async def demo_ollama_generate(client: StreamableHttpDemo, prompt: str) -> None:
    """
    演示使用Ollama生成文本
    
    Args:
        client: StreamableHttpDemo客户端
        prompt: 提示文本
    """
    try:
        # 调用Ollama生成工具
        result = await client.call_tool("ollama_generate", {
            "model": "llama3", 
            "prompt": prompt,
            "temperature": 0.7
        })
        print(f"\n===== Ollama生成结果 =====\n{result}\n")
    except Exception as e:
        print(f"Ollama生成失败: {str(e)}")


async def demo_health_check(client: StreamableHttpDemo) -> None:
    """
    演示健康检查资源
    
    Args:
        client: StreamableHttpDemo客户端
    """
    try:
        # 调用健康检查资源
        result = await client.call_resource("sakura://health")
        print(f"\n===== 健康检查结果 =====\n{json.dumps(result, indent=2, ensure_ascii=False)}\n")
    except Exception as e:
        print(f"健康检查失败: {str(e)}")


async def main() -> None:
    """
    主函数
    """
    # 创建客户端
    client = StreamableHttpDemo(server_url="http://localhost:8000")
    
    try:
        # 连接到服务器
        print("正在连接到MCP服务器...")
        await client.connect_to_server()
        print(f"已连接到MCP服务器，可用工具: {[tool.name for tool in client.available_tools]}")
        
        # 演示调用工具和资源
        await demo_weather_query(client, "Shanghai")
        await demo_ollama_generate(client, "介绍一下Python语言的特点")
        await demo_health_check(client)
        
    except Exception as e:
        print(f"错误: {str(e)}")
    finally:
        # 清理资源
        await client.cleanup()


if __name__ == "__main__":
    # 运行主函数
    asyncio.run(main()) 