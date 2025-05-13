#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/16 9:42
# @Author   : 冉勇
# @File     : mcp_server.py
# @Software : PyCharm
# @Desc     :
import os
import time
from mcp.server.fastmcp import FastMCP
from tool_weather import WeatherTool
from utils.log_util import logger

# 初始化 MCP 服务器
mcp = FastMCP("SakuraMcpServer")


# 工具验证函数
def validate_tool(func):
    """验证工具函数的签名和参数"""
    # 这里可以添加更多验证逻辑
    return func


# 使用普通装饰器进行验证，然后再应用mcp.tool()装饰器
@mcp.tool()
@validate_tool
async def query_weather(city: str) -> str:
    """
    输入指定城市的英文名称，返回今日天气查询结果。
    :param city: 城市名称（需使用英文）
    :return: 格式化后的天气信息
    """
    try:
        start_time = time.time()
        data = await WeatherTool.fetch_weather(city)
        result = WeatherTool.format_weather(data)
        logger.info(f"天气查询成功: {city}, 耗时: {time.time() - start_time:.2f}秒")
        return result
    except Exception as e:
        logger.error(f"天气查询失败: {str(e)}")
        return f"查询天气时出错: {str(e)}"


async def health_check():
    """服务健康检查"""
    try:
        # 测试天气API是否可用
        api_status = await WeatherTool.check_api_status()
        return {
            "status": "ok" if api_status else "degraded",
            "timestamp": time.time(),
            "service": "SakuraMcpServer",
            "version": "1.0.0"
        }
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }


if __name__ == '__main__':
    # 支持多种传输方法
    transport = os.getenv("MCP_TRANSPORT", "stdio")
    port = int(os.getenv("MCP_PORT", 8000))
    if transport == "http":
        mcp.run(transport='http', port=port)
    elif transport == "websocket":
        mcp.run(transport='websocket', port=port)
    else:
        # 默认使用stdio
        mcp.run(transport='stdio')
