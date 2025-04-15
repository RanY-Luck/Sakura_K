#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/15 15:16
# @Author   : 冉勇
# @File     : mcp_client.py
# @Software : PyCharm
# @Desc     :
import os
import json
import argparse
import asyncio
from typing import Optional
from contextlib import AsyncExitStack
from click import argument
from openai import AsyncOpenAI
from dotenv import load_dotenv
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client




class MCPClient:
    def __init__(self):
        """初始化 MCP 客户端"""
        self.exit_stack = AsyncExitStack()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")  # 读取 OpenAI API Key
        self.base_url = os.getenv("OPENAI_API_URL")  # 读取 BASE YRL
        self.model = os.getenv("OPENAI_API_MODEL")  # 读取 model
        if not self.openai_api_key:
            raise ValueError("❌ 未找到 OpenAI API Key，请在 .env 文件中设置 OPENAI_API_KEY")
        self.client = AsyncOpenAI(api_key=self.openai_api_key, base_url=self.base_url)  # 创建OpenAI client
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.messages = []

    async def connect_to_server(self, server_script_path: str):
        """连接到 MCP 服务器并列出可用工具"""
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("服务器脚本必须是 .py 或 .js 文件")

        # 必须设置项目根目录，否则无法获取到其他引用代码文件
        project_root = os.path.abspath(os.getcwd())
        python_cmd_path = os.getenv("PYTHON_PATH")
        command = python_cmd_path if is_python else "node"

        parser = argparse.ArgumentParser(description='命令行参数')
        parser.add_argument('--env', type=str, default='', help='运行环境')
        args, unknown = parser.parse_known_args()

        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path, f'--env={args.env}'],
            env={"PYTHONPATH": project_root}
        )

        # 启动 MCP 服务器并建立通信
        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # 列出 MCP 服务器上的工具
        response = await self.session.list_tools()
        tools = response.tools
        print("\n已连接到服务器，支持以下工具:", [tool.name for tool in tools])



    async def process_query(self, query: str):
        """
        使用大模型处理查询并调用可用的 MCP 工具 (Function Calling)
        """
        self.messages.append({"role": "user", "content": query})

        response = await self.session.list_tools()

        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
        } for tool in response.tools]
        # print(available_tools)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            stream=True,
            tools=available_tools
        )
        is_tool_call = False
        tool_name = None
        tool_args = ''
        tool_call_id = None
        content = ''
        yield f'🤖AI：'
        async for chunk in response:
            # print(chunk)
            if chunk.choices and chunk.choices[0].delta.tool_calls:
                #调用工具
                tool_call = chunk.choices[0].delta.tool_calls[0]
                if tool_call.id:
                    is_tool_call = True
                    tool_name = tool_call.function.name
                    tool_call_id = tool_call.id
                    yield f'开始调用工具【{tool_call.function.name}】,参数为'
                else:
                    tool_args += tool_call.function.arguments
                    yield tool_call.function.arguments
            elif chunk.choices and chunk.choices[0].delta.content:
                # 大模型解答
                content += chunk.choices[0].delta.content
                yield chunk.choices[0].delta.content
            elif chunk.choices and chunk.choices[0].finish_reason == 'tool_calls':
                # 参数处理完毕
                pass
            elif chunk.choices and chunk.choices[0].finish_reason == 'stop':
                self.messages.append({
                    "role": "assistant",
                    "content": content
                })
                pass
        # 处理返回的内容
        if is_tool_call:
            # 如何是需要使用工具，就解析工具
            # 执行工具
            print(f"\n\n[Calling tool {tool_name} with args {tool_args}]\n\n")
            result = await self.session.call_tool(tool_name, json.loads(tool_args))
            print(result)
            # 将模型返回的调用哪个工具数据和工具执行完成后的数据都存入messages中
            self.messages.append({
                "role": "assistant",
                "content": "",
                "index": 0,
                "tool_calls": [{
                    "id": tool_call_id,
                    "type": "function",
                    "function": {
                        "name": tool_name,
                        "arguments": tool_args
                    }
                }]
            })
            self.messages.append({
                "role": "tool",
                "content": result.content[0].text,
                "tool_call_id": tool_call_id,
            })

            # 将上面的结果再返回给大模型用于生产最终的结果
            result_response = await self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                stream=True,
            )
            result_content = ''
            async for chunk in result_response:
                if chunk.choices and chunk.choices[0].delta.content:
                    result_content += chunk.choices[0].delta.content
                    yield chunk.choices[0].delta.content
            self.messages.append({
                "role": "assistant",
                'content': result_content,
            })
        return

    async def put_query(self, query: str):
        print(f"\n🤖 OpenAI: ", end="", flush=True)
        response = self.process_query(query)  # 发送用户输入到 OpenAI API
        async for value in response:
            print(value, end="", flush=True)
            yield value

    async def chat_loop(self):
        """运行交互式聊天循环"""
        print("\n🤖 MCP 客户端已启动！输入 'quit' 退出")

        while True:
            try:
                query = input("\n你: ").strip()
                if query.lower() == 'quit':
                    break


                print(f"\n🤖 OpenAI: ", end="", flush=True)
                response = self.process_query(query)  # 发送用户输入到 OpenAI API
                async for value in response:
                    print(value, end="", flush=True)

            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self):
        """清理资源"""
        await self.exit_stack.aclose()


async def main(server_script_path: str):

    client = MCPClient()
    try:
        await client.connect_to_server(server_script_path)
        await client.chat_loop()
    finally:
        await client.cleanup()


if __name__ == "__main__":

    asyncio.run(main('mcp_server.py'))