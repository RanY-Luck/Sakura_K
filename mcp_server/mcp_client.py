#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/15 15:16
# @Author   : 冉勇
# @File     : mcp_client.py
# @Software : PyCharm
# @Desc     : MCP 客户端
import os
import json
import asyncio
import sys
import time
import argparse
from utils.log_util import logger
from typing import Optional, Dict, Any, List, AsyncGenerator
from contextlib import AsyncExitStack
from openai import AsyncOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


# 自定义JSON编码器，用于处理特殊类型
class CustomJSONEncoder(json.JSONEncoder):
    """处理特殊类型的JSON编码器"""
    def default(self, obj):
        # 处理TextContent类型
        if hasattr(obj, '__dict__') and 'text' in obj.__dict__:
            return obj.text
        # 处理其他自定义类型
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        # 处理日期时间类型
        elif hasattr(obj, 'isoformat'):
            return obj.isoformat()
        # 默认处理
        return super().default(obj)


# 安全的JSON转换函数
def safe_json_dumps(obj: Any) -> str:
    """
    安全地将对象转换为JSON字符串
    :param obj: 要转换的对象
    :return: JSON字符串
    """
    try:
        return json.dumps(obj, ensure_ascii=False, indent=2, cls=CustomJSONEncoder)
    except Exception as e:
        logger.error(f"JSON序列化失败: {str(e)}")
        # 尝试转换为字符串
        try:
            if hasattr(obj, 'text'):
                return obj.text
            elif hasattr(obj, '__str__'):
                return str(obj)
            else:
                return f"无法序列化的对象: {type(obj)}"
        except:
            return "无法序列化的对象"


class MCPClientError(Exception):
    """MCP客户端自定义异常"""
    pass


class MCPClient:
    """MCP 客户端实现，支持重试和错误处理"""

    def __init__(self, retry_attempts: int = 3, retry_delay: float = 2.0):
        """
        初始化 MCP 客户端
        :param retry_attempts: 重试次数
        :param retry_delay: 重试延迟（秒）
        """
        self.exit_stack = AsyncExitStack()

        # 从环境变量获取配置
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("OPENAI_API_URL")
        self.model = os.getenv("OPENAI_API_MODEL")
        self.retry_attempts = retry_attempts
        self.retry_delay = retry_delay
        self.connection_timeout = float(os.getenv("MCP_CONNECTION_TIMEOUT", "30.0"))

        # 验证API密钥
        if not self.openai_api_key:
            raise ValueError("❌ 未找到 OpenAI API Key，请在 .env 文件中设置 OPENAI_API_KEY")

        # 初始化OpenAI客户端，添加超时设置
        self.client = AsyncOpenAI(
            api_key=self.openai_api_key,
            base_url=self.base_url,
            timeout=45.0  # 设置较长的超时时间
        )

        # MCP会话
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.messages: List[Dict[str, Any]] = []

        # 连接状态
        self.is_connected = False
        self.connect_time = None
        self.available_tools = []
        self.stdio = None
        self.write = None

    async def connect_to_server(self, server_script_path: str) -> None:
        """
        连接到 MCP 服务器并列出可用工具
        :param server_script_path: 服务器脚本路径
        """
        # 检查脚本类型
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("服务器脚本必须是 .py 或 .js 文件")

        # 必须设置项目根目录，否则无法获取到其他引用代码文件
        project_root = os.path.abspath(os.getcwd())
        python_cmd_path = os.getenv("PYTHON_PATH", "python")
        command = python_cmd_path if is_python else "node"

        # 解析命令行参数
        parser = argparse.ArgumentParser(description='命令行参数')
        parser.add_argument('--env', type=str, default='', help='运行环境')
        args, unknown = parser.parse_known_args()

        # 配置服务器参数
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path, f'--env={args.env}'],
            env={"PYTHONPATH": project_root}
        )

        # 为Windows设置正确的事件循环策略
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        try:
            # 设置连接超时
            connect_task = self._connect_with_timeout(server_params)
            await asyncio.wait_for(connect_task, timeout=self.connection_timeout)

            # 列出服务器工具
            await self._list_available_tools()

            self.is_connected = True
            self.connect_time = time.time()
            logger.info(f"成功连接到MCP服务器: {server_script_path}")

        except asyncio.TimeoutError:
            await self.cleanup()
            raise MCPClientError(f"连接MCP服务器超时，请检查服务器是否正常运行: {server_script_path}")
        except Exception as e:
            await self.cleanup()
            raise MCPClientError(f"连接MCP服务器失败: {str(e)}")

    async def _connect_with_timeout(self, server_params: StdioServerParameters) -> None:
        """
        在超时范围内尝试连接服务器
        :param server_params: 服务器参数
        """
        try:
            # 使用原始的stdio_client，但确保在正确的事件循环策略下运行
            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            self.stdio, self.write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
            await self.session.initialize()
        except Exception as e:
            logger.error(f"连接服务器失败: {str(e)}")
            raise

    async def _list_available_tools(self) -> None:
        """获取并存储服务器可用工具"""
        if not self.session:
            raise MCPClientError("未连接到MCP服务器")

        response = await self.session.list_tools()
        self.available_tools = response.tools
        logger.info(f"服务器工具: {[tool.name for tool in self.available_tools]}")

    async def process_query(self, query: str) -> AsyncGenerator[str, None]:
        """
        使用大模型处理查询并调用可用的 MCP 工具 (Function Calling)
        :param query: 用户查询
        :yield: 流式响应内容
        """
        if not self.is_connected or not self.session:
            try:
                # 尝试重新初始化会话
                logger.warning("会话未初始化，尝试重新连接...")
                yield "⚠️ 正在重新连接服务器..."
                # 这里需要再次调用连接方法，但此处无法获知服务器脚本路径
                raise MCPClientError("会话已断开，请重新连接")
            except Exception as e:
                yield f"❌ 无法处理请求: {str(e)}"
                return

        # 添加用户消息到历史
        self.messages.append({"role": "user", "content": query})

        # 获取可用工具列表
        if not self.available_tools:
            try:
                await self._list_available_tools()
            except Exception as e:
                yield f"❌ 获取可用工具失败: {str(e)}"
                return

        # 转换为OpenAI工具格式
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.inputSchema
            }
        } for tool in self.available_tools]

        # 尝试多次调用模型，处理可能的临时错误
        for attempt in range(self.retry_attempts):
            try:
                response = await self.client.chat.completions.create(
                    model=self.model,
                    messages=self.messages,
                    stream=True,
                    tools=available_tools,
                    timeout=30.0
                )

                # 处理流式响应
                is_tool_call = False
                tool_name = None
                tool_args = ''
                tool_call_id = None
                content = ''

                # 提示AI正在思考
                yield f'🤖 '

                async for chunk in response:
                    # 处理工具调用
                    if chunk.choices and chunk.choices[0].delta.tool_calls:
                        tool_call = chunk.choices[0].delta.tool_calls[0]
                        if tool_call.id:
                            is_tool_call = True
                            tool_name = tool_call.function.name
                            tool_call_id = tool_call.id
                            yield f'正在调用工具【{tool_call.function.name}】'
                        else:
                            tool_args += tool_call.function.arguments
                    # 处理文本内容
                    elif chunk.choices and chunk.choices[0].delta.content:
                        content_piece = chunk.choices[0].delta.content
                        content += content_piece
                        yield content_piece
                    # 处理完成原因
                    elif chunk.choices and chunk.choices[0].finish_reason == 'tool_calls':
                        # 参数处理完毕
                        pass
                    elif chunk.choices and chunk.choices[0].finish_reason == 'stop':
                        self.messages.append(
                            {
                                "role": "assistant",
                                "content": content
                            }
                        )
                        pass

                # 如果需要调用工具
                if is_tool_call:
                    try:
                        # 解析工具参数（处理可能的JSON错误）
                        try:
                            tool_args_dict = json.loads(tool_args)
                        except json.JSONDecodeError:
                            yield f"\n⚠️ 工具参数格式错误: {tool_args}"
                            return

                        # 执行工具
                        yield f"\n⏳ 正在执行工具..."
                        result = await self._call_tool_with_retry(tool_name, tool_args_dict)

                        # 检查结果
                        if "error" in result:
                            yield f"\n❌ 工具执行失败: {result['error']}"
                            return

                        # 格式化工具结果用于显示
                        tool_content = self._format_tool_result(tool_name, result)

                        # 将工具调用和结果添加到消息历史
                        self.messages.append(
                            {
                                "role": "assistant",
                                "content": "",
                                "tool_calls": [{
                                    "id": tool_call_id,
                                    "type": "function",
                                    "function": {
                                        "name": tool_name,
                                        "arguments": tool_args
                                    }
                                }]
                            }
                        )

                        # 将结果转换为字符串以添加到消息历史
                        # 使用安全的JSON序列化
                        result_str = safe_json_dumps(result)

                        # 添加工具响应
                        self.messages.append(
                            {
                                "role": "tool",
                                "content": result_str,
                                "tool_call_id": tool_call_id,
                            }
                        )

                        # 使用工具结果让模型生成最终回答
                        # yield f"\n📊 工具执行结果：\n{tool_content}\n\n🤖 AI解析结果：\n"
                        yield f"\n🤖 AI解析结果：\n"

                        # 创建新的聊天补全
                        result_response = await self.client.chat.completions.create(
                            model=self.model,
                            messages=self.messages,
                            stream=True,
                        )

                        # 流式处理最终结果
                        result_content = ''
                        async for chunk in result_response:
                            if chunk.choices and chunk.choices[0].delta.content:
                                content_piece = chunk.choices[0].delta.content
                                result_content += content_piece
                                yield content_piece

                        # 添加最终回答到消息历史
                        self.messages.append(
                            {
                                "role": "assistant",
                                'content': result_content,
                            }
                        )
                    except Exception as e:
                        yield f"\n❌ 工具处理出错: {str(e)}"
                        logger.error(f"工具处理错误: {str(e)}")

                # 处理成功，跳出重试循环
                break

            except Exception as e:
                logger.error(f"处理查询出错 (尝试 {attempt + 1}/{self.retry_attempts}): {str(e)}")
                if attempt < self.retry_attempts - 1:
                    yield f"\n⚠️ 处理请求时出错，正在重试... ({attempt + 1}/{self.retry_attempts})"
                    await asyncio.sleep(self.retry_delay)
                else:
                    yield f"\n❌ 处理请求失败: {str(e)}"
                    return

    async def _call_tool_with_retry(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """
        带重试的工具调用
        :param tool_name: 工具名称
        :param args: 工具参数
        :return: 工具执行结果
        """
        for attempt in range(self.retry_attempts):
            try:
                result = await self.session.call_tool(tool_name, args)
                # 解析结果对象为字典并安全处理
                try:
                    # 如果result已经是字典类型，直接返回
                    if isinstance(result, dict):
                        return result
                    # 如果是特殊对象，尝试获取__dict__属性
                    elif hasattr(result, '__dict__'):
                        return result.__dict__
                    # 其他情况返回对象的字符串表示
                    else:
                        return {"content": str(result)}
                except Exception as e:
                    logger.error(f"结果解析失败: {str(e)}")
                    return {"error": f"结果处理失败: {str(e)}"}
            except Exception as e:
                logger.error(f"工具调用失败 (尝试 {attempt + 1}/{self.retry_attempts}): {str(e)}")
                if attempt < self.retry_attempts - 1:
                    await asyncio.sleep(self.retry_delay)
                else:
                    return {"error": f"工具调用失败: {str(e)}"}

    async def put_query(self, query: str) -> AsyncGenerator[str, None]:
        """
        处理用户查询，返回流式响应
        :param query: 用户查询
        :yield: 流式响应内容
        """
        response = self.process_query(query)
        async for value in response:
            yield value

    async def chat_loop(self) -> None:
        """运行交互式聊天循环"""
        print("\n🤖 MCP 客户端已启动！输入 'quit' 退出")

        while True:
            try:
                query = input("\n你: ").strip()
                if query.lower() == 'quit':
                    break

                print(f"\n🤖 AI: ", end="", flush=True)
                response = self.process_query(query)
                async for value in response:
                    print(value, end="", flush=True)
                print()

            except Exception as e:
                print(f"\n⚠️ 发生错误: {str(e)}")

    async def cleanup(self) -> None:
        """清理资源"""
        try:
            await self.exit_stack.aclose()
            self.is_connected = False
            logger.info("MCP客户端资源已清理")
        except Exception as e:
            logger.error(f"清理资源时出错: {str(e)}")

    def _format_tool_result(self, tool_name: str, result: Dict[str, Any]) -> str:
        """
        根据工具类型格式化结果
        :param tool_name: 工具名称
        :param result: 工具结果
        :return: 格式化的结果字符串
        """
        # Text2SQL工具的特殊处理
        if tool_name in ["sql_query", "execute_sql"]:
            # 处理SQL查询结果
            sql = result.get("sql_query", "未提供SQL")
            execution_time = result.get("execution_time", "未知")
            row_count = result.get("row_count", 0)
            
            formatted = f"📝 SQL查询: {sql}\n"
            formatted += f"⏱️ 执行时间: {execution_time}\n"
            formatted += f"📊 查询结果 ({row_count} 行):\n"
            
            # 格式化结果数据
            results = result.get("results", [])
            if results:
                # 提取列名
                columns = list(results[0].keys())
                # 创建表头
                formatted += "| " + " | ".join(columns) + " |\n"
                formatted += "| " + " | ".join(["---" for _ in columns]) + " |\n"
                
                # 添加每一行数据
                for row in results[:20]:  # 限制显示前20行
                    formatted += "| " + " | ".join([str(row.get(col, "")) for col in columns]) + " |\n"
                
                if len(results) > 20:
                    formatted += f"... 还有 {len(results) - 20} 行未显示\n"
            else:
                formatted += "没有返回数据\n"
                
            # 添加AI生成的数据总结（如果有）
            summary = result.get("summary", "")
            if summary:
                formatted += f"\n📈 数据总结:\n{summary}\n"
                
            return formatted
            
        elif tool_name in ["get_table_info", "describe_table"]:
            # 处理表结构信息
            table_name = result.get("table_name", "未知表")
            comment = result.get("comment", "")
            row_count = result.get("row_count", 0)
            
            formatted = f"📋 表名: {table_name}"
            if comment:
                formatted += f" ({comment})"
            formatted += f"\n📊 行数: {row_count}\n"
            formatted += "📑 列结构:\n"
            
            # 格式化列信息
            columns = result.get("columns", [])
            if columns:
                formatted += "| 名称 | 类型 | 可空 | 默认值 | 主键 | 备注 |\n"
                formatted += "| --- | --- | --- | --- | --- | --- |\n"
                
                for col in columns:
                    name = col.get("name", "")
                    col_type = col.get("type", "")
                    nullable = "是" if col.get("nullable", True) else "否"
                    default = col.get("default", "") or ""
                    is_primary = "✓" if col.get("is_primary", False) else ""
                    comment = col.get("comment", "")
                    
                    formatted += f"| {name} | {col_type} | {nullable} | {default} | {is_primary} | {comment} |\n"
            else:
                formatted += "没有列信息\n"
                
            # 添加样本数据
            sample_data = result.get("sample_data", [])
            if sample_data:
                formatted += "\n📝 样本数据:\n"
                # 提取列名
                columns = list(sample_data[0].keys())
                # 创建表头
                formatted += "| " + " | ".join(columns) + " |\n"
                formatted += "| " + " | ".join(["---" for _ in columns]) + " |\n"
                
                # 添加每一行数据
                for row in sample_data:
                    formatted += "| " + " | ".join([str(row.get(col, "")) for col in columns]) + " |\n"
                    
            return formatted
            
        elif tool_name == "get_all_tables":
            # 处理所有表信息
            database = result.get("database", "未知数据库")
            table_count = result.get("table_count", 0)
            
            formatted = f"🗃️ 数据库: {database}\n"
            formatted += f"📊 表数量: {table_count}\n\n"
            
            # 格式化表信息
            tables = result.get("tables", [])
            if tables:
                formatted += "| 表名 | 描述 | 行数 | 列数 |\n"
                formatted += "| --- | --- | --- | --- |\n"
                
                for table in tables:
                    name = table.get("table_name", "")
                    comment = table.get("comment", "")
                    row_count = table.get("row_count", 0)
                    col_count = len(table.get("columns", []))
                    
                    formatted += f"| {name} | {comment} | {row_count} | {col_count} |\n"
            else:
                formatted += "没有表信息\n"
                
            return formatted
            
        elif tool_name in ["train_sql_example", "train_database_schema", "train_with_examples", "run_full_training"]:
            # 处理训练结果
            success = result.get("success", False)
            message = result.get("message", "未知结果")
            
            if success:
                formatted = f"✅ 训练成功: {message}\n"
            else:
                formatted = f"❌ 训练失败: {message}\n"
                
            # 添加训练数据详情（如果有）
            data = result.get("data", {})
            if data and isinstance(data, dict):
                formatted += "\n训练数据详情:\n"
                for key, value in data.items():
                    formatted += f"- {key}: {value}\n"
                    
            return formatted
            
        # 默认处理（尝试JSON格式化）
        else:
            try:
                return json.dumps(result, ensure_ascii=False, indent=2)
            except:
                # 如果无法JSON格式化，返回原始内容
                return str(result)


async def main(server_script_path: str) -> None:
    """
    主入口函数
    :param server_script_path: 服务器脚本路径
    """
    client = MCPClient()
    try:
        await client.connect_to_server(server_script_path)
        await client.chat_loop()
    except Exception as e:
        print(f"❌ 启动失败: {str(e)}")
    finally:
        await client.cleanup()
