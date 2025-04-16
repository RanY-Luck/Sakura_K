#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/16 9:42
# @Author   : 冉勇
# @File     : mcp_server.py
# @Software : PyCharm
# @Desc     :
from mcp.server.fastmcp import FastMCP
from tool_weather import WeatherTool

# 初始化 MVP 服务器
mcp = FastMCP("SakuraMcpServer")


@mcp.tool()
async def query_weather(city: str) -> str:
    """
    输入指定城市的英文名称，返回今日天气查询结果。
    :param city: 城市名称（需使用英文）
    :return: 格式化后的天气信息
    """
    data = await WeatherTool.fetch_weather(city)
    return WeatherTool.format_weather(data)


if __name__ == '__main__':
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')
