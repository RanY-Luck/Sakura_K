#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/16 9:42
# @Author   : 冉勇
# @File     : mcp_server.py
# @Software : PyCharm
# @Desc     : MCP服务
import os
import time
import aiohttp
from typing import Dict, Any, Optional
from mcp.server.fastmcp import FastMCP
from tool_weather import WeatherTool
from utils.log_util import logger

# 初始化 MCP 服务器
mcp = FastMCP("SakuraMcpServer")

# 服务器初始化标志
db_initialized = False


# 工具验证函数
def validate_tool(func):
    """验证工具函数的签名和参数"""
    # 这里可以添加更多验证逻辑
    return func


class OllamaModel:
    """Ollama模型接口封装"""

    def __init__(self, base_url: str = "http://localhost:11434"):
        """
        初始化Ollama客户端
        :param base_url: Ollama服务地址，默认为本地11434端口
        """
        self.base_url = base_url.rstrip('/')
        self.session = None

    async def _ensure_session(self):
        """确保aiohttp会话已创建"""
        if self.session is None:
            self.session = aiohttp.ClientSession()

    async def close(self):
        """关闭aiohttp会话"""
        if self.session:
            await self.session.close()
            self.session = None

    async def generate(
            self,
            model: str,
            prompt: str,
            system: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        使用Ollama模型生成文本
        :param model: 模型名称，如 "llama3"
        :param prompt: 提示文本
        :param system: 系统提示，可选
        :param temperature: 温度参数，控制随机性
        :param max_tokens: 最大生成token数，可选
        :return: 生成结果
        """
        await self._ensure_session()

        payload = {
            "model": model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": False
        }

        if system:
            payload["system"] = system

        if max_tokens:
            payload["max_tokens"] = max_tokens

        try:
            async with self.session.post(f"{self.base_url}/api/generate", json=payload) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"Ollama API调用失败: {response.status}, {error_text}")
                    return {"error": f"API错误: {response.status}", "message": error_text}

                result = await response.json()
                return result
        except Exception as e:
            logger.error(f"Ollama调用出错: {str(e)}")
            return {"error": "连接错误", "message": str(e)}

    async def list_models(self) -> Dict[str, Any]:
        """获取可用的Ollama模型列表"""
        await self._ensure_session()

        try:
            async with self.session.get(f"{self.base_url}/api/tags") as response:
                if response.status != 200:
                    error_text = await response.text()
                    logger.error(f"获取Ollama模型列表失败: {response.status}, {error_text}")
                    return {"error": f"API错误: {response.status}", "message": error_text}

                result = await response.json()
                return result
        except Exception as e:
            logger.error(f"获取Ollama模型列表出错: {str(e)}")
            return {"error": "连接错误", "message": str(e)}


# 创建全局Ollama客户端
ollama_client = OllamaModel(os.getenv("OLLAMA_URL", "http://localhost:11434"))


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


@mcp.tool()
@validate_tool
async def ollama_generate(
        model: str, prompt: str, system: Optional[str] = None,
        temperature: float = 0.7, max_tokens: Optional[int] = None
) -> str:
    """
    使用本地Ollama模型生成文本
    :param model: 模型名称，如 "llama3", "gemma", "mistral" 等
    :param prompt: 用户提示文本
    :param system: 系统提示，可选
    :param temperature: 温度参数，控制随机性，默认0.7
    :param max_tokens: 最大生成token数，可选
    :return: 生成的文本内容
    """
    try:
        start_time = time.time()
        result = await ollama_client.generate(
            model=model,
            prompt=prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens
        )

        # 检查是否有错误
        if "error" in result:
            logger.error(f"Ollama生成失败: {result.get('message', '未知错误')}")
            return f"模型生成失败: {result.get('message', '未知错误')}"

        # 提取生成文本
        generated_text = result.get("response", "")

        # 输出性能指标
        logger.info(f"Ollama生成成功: 模型={model}, 耗时={time.time() - start_time:.2f}秒")
        return generated_text

    except Exception as e:
        logger.error(f"Ollama生成出错: {str(e)}")
        return f"模型生成出错: {str(e)}"


@mcp.tool()
@validate_tool
async def list_ollama_models() -> str:
    """
    获取本地可用的Ollama模型列表
    :return: 格式化的模型列表信息
    """
    try:
        result = await ollama_client.list_models()

        # 检查是否有错误
        if "error" in result:
            logger.error(f"获取Ollama模型列表失败: {result.get('message', '未知错误')}")
            return f"获取模型列表失败: {result.get('message', '未知错误')}"

        # 提取和格式化模型列表
        models = result.get("models", [])
        if not models:
            return "未找到可用的Ollama模型。请先使用'ollama pull'命令下载模型。"

        # 格式化为易读文本
        formatted_models = "可用的Ollama模型:\n\n"
        for model in models:
            name = model.get("name", "未知")
            modified = model.get("modified_at", "未知时间")
            size = model.get("size", 0) / (1024 * 1024 * 1024)  # 转换为GB
            formatted_models += f"- {name}\n  大小: {size:.2f} GB\n  更新时间: {modified}\n\n"

        return formatted_models

    except Exception as e:
        logger.error(f"获取Ollama模型列表出错: {str(e)}")
        return f"获取模型列表出错: {str(e)}"


@mcp.resource("sakura://health")
async def health_check():
    """服务健康检查"""
    try:
        # 测试天气API是否可用
        api_status = await WeatherTool.check_api_status()

        # 测试Ollama API是否可用
        ollama_status = False
        try:
            result = await ollama_client.list_models()
            ollama_status = "error" not in result
        except:
            ollama_status = False

        return {
            "status": "ok" if (api_status and ollama_status) else "degraded",
            "services": {
                "weather": "ok" if api_status else "error",
                "ollama": "ok" if ollama_status else "error",
            },
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


# 初始化服务器
async def init_server():
    """初始化服务器"""
    global db_initialized

    logger.info("MCP服务初始化完成")


@mcp.tool()
@validate_tool
async def generate_text(
        prompt: str,
        system: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
) -> str:
    """
    使用本地Ollama模型生成文本（默认使用Ollama）
    :param prompt: 用户提示文本
    :param system: 系统提示，可选
    :param temperature: 温度参数，控制随机性，默认0.7
    :param max_tokens: 最大生成token数，可选
    :return: 生成的文本内容
    """
    # 从环境变量获取模型配置
    model = os.getenv("OLLAMA_MODEL")

    try:
        # 调用ollama_generate函数
        logger.info(f"使用Ollama模型 '{model}' 生成文本")
        result = await ollama_generate(
            model=model,
            prompt=prompt,
            system=system,
            temperature=temperature,
            max_tokens=max_tokens
        )
        return result
    except Exception as e:
        logger.error(f"Ollama模型生成失败: {str(e)}")
        return f"生成文本时出错: {str(e)}"


# 服务器启动入口点
if __name__ == "__main__":
    # 注册事件已经在上面使用装饰器完成
    # 启动服务器
    mcp.run()
