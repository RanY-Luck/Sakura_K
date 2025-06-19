#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/4/16 9:42
# @Author   : 冉勇
# @File     : mcp_server.py
# @Software : PyCharm
# @Desc     : MCP服务
import os
import time
import json
import aiohttp
from typing import Dict, Any, Optional
from fastapi import WebSocket
from mcp.server.fastmcp import FastMCP
from tool_weather import WeatherTool
from utils.log_util import logger
from plugin.module_text2sql.service.text2sql_service import Text2SQLService
from plugin.module_text2sql.entity.vo.text2sql_vo import TrainRequest, AskRequest

# 初始化 MCP 服务器
mcp = FastMCP("SakuraMcpServer")

# 初始化Text2SQL服务
text2sql_service = Text2SQLService()

# 导入text2sql2模块
import sys
import pandas as pd

sys.path.append('./mcp_server')
try:
    from text2sql2.text2sql import vn, MyVanna

    logger.info("成功导入 text2sql2 模块")
except Exception as e:
    logger.error(f"导入 text2sql2 模块失败: {str(e)}")
    vn = None

# 从text2sql2.train导入训练器
try:
    from text2sql2.train import VannaTrainer

    trainer = VannaTrainer(vn) if vn else None
    logger.info("成功导入 VannaTrainer")
except Exception as e:
    logger.error(f"导入 VannaTrainer 失败: {str(e)}")
    trainer = None

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


@mcp.tool()
@validate_tool
async def text2sql_train(
        supplier: str = "",
        question: str = "",
        sql: str = "",
        documentation: str = "",
        ddl: str = "",
        db_schema: str = ""
) -> Dict[str, Any]:
    """
    训练Text2SQL模型
    
    :param supplier: AI服务提供商
    :param question: 问题示例
    :param sql: SQL示例
    :param documentation: 文档
    :param ddl: 数据定义语言
    :param db_schema: 数据库模式
    :return: 包含训练结果的字典
    """
    try:
        # 验证至少有一个参数不为空
        if not any([question, sql, documentation, ddl, db_schema]):
            return {"success": False, "message": "至少需要提供一个参数(question, sql, documentation, ddl, db_schema)"}

        success = text2sql_service.train(
            supplier=supplier,
            question=question,
            sql=sql,
            documentation=documentation,
            ddl=ddl,
            schema=db_schema
        )

        return {
            "success": success,
            "message": "训练成功" if success else "训练失败"
        }
    except Exception as e:
        logger.error(f"训练模型失败: {str(e)}")
        return {"success": False, "message": f"训练异常: {str(e)}"}


@mcp.tool()
@validate_tool
async def text2sql_ask(
        question: str,
        auto_train: bool = True,
        supplier: str = ""
) -> Dict[str, Any]:
    """
    提问接口，将自然语言问题转换为SQL查询并执行
    
    :param question: 自然语言问题
    :param auto_train: 是否自动训练成功的查询
    :param supplier: AI服务提供商
    :return: 包含SQL和结果数据的字典
    """
    try:
        if not question:
            return {"success": False, "message": "问题不能为空"}

        # 打印请求信息，便于调试
        logger.info(f"接收到问题请求: {question}")
        logger.info(f"供应商: {supplier or '默认'}")

        # 调用服务处理问题
        sql, df, fig = text2sql_service.ask(
            question=question,
            auto_train=auto_train,
            supplier=supplier
        )

        logger.info(f"生成SQL: {sql}")
        logger.info(f"结果数据行数: {len(df)}")

        # 将DataFrame转换为记录列表
        records = df.to_dict(orient='records')
        logger.info(f"转换后的数据: {records}")

        return {
            "success": True,
            "data": {
                "sql": sql,
                "data": records
            }
        }
    except Exception as e:
        logger.error(f"处理问题失败: {str(e)}")
        return {"success": False, "message": f"处理问题失败: {str(e)}"}


@mcp.tool()
@validate_tool
async def text2sql_schema_train(supplier: str = "") -> Dict[str, Any]:
    """
    训练数据库模式
    
    :param supplier: AI服务提供商
    :return: 包含训练结果的字典
    """
    try:
        vn_instance = text2sql_service.get_vn_instance(supplier)
        success = vn_instance.schema_train()
        return {
            "success": success,
            "message": "数据库模式训练成功" if success else "数据库模式训练失败"
        }
    except Exception as e:
        logger.error(f"训练数据库模式失败: {str(e)}")
        return {"success": False, "message": f"训练数据库模式失败: {str(e)}"}


@mcp.resource("sakura://text2sql/training_data/{supplier}")
async def get_training_data(supplier: str = ""):
    """
    获取训练数据
    
    :param supplier: AI服务提供商
    :return: 包含训练数据的字典
    """
    try:
        training_data = text2sql_service.get_training_data(supplier)
        return {
            "status": "ok",
            "data": training_data
        }
    except Exception as e:
        logger.error(f"获取训练数据失败: {str(e)}")
        return {
            "status": "error",
            "message": f"获取训练数据失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def sql_query(question: str) -> Dict[str, Any]:
    """
    将自然语言问题转换为SQL并执行查询
    
    :param question: 用户的自然语言问题
    :return: 包含SQL和查询结果的字典
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }

    try:
        logger.info(f"处理问题: {question}")
        start_time = time.time()

        # 生成SQL
        sql = vn.generate_sql(question)
        if not sql:
            return {
                "success": False,
                "message": "无法生成SQL查询",
                "sql_query": ""
            }

        logger.info(f"生成的SQL: {sql}")

        # 执行SQL查询
        df = vn.run_sql(sql)
        execution_time = f"{time.time() - start_time:.2f}秒"

        # 如果为空，返回空结果
        if df is None or df.empty:
            return {
                "success": True,
                "sql_query": sql,
                "execution_time": execution_time,
                "row_count": 0,
                "results": []
            }

        # 转换为字典列表
        results = df.to_dict(orient='records')
        row_count = len(results)

        # 生成总结（如果结果不为空）
        summary = vn.generate_summary(question, df) if row_count > 0 else ""

        return {
            "success": True,
            "sql_query": sql,
            "execution_time": execution_time,
            "row_count": row_count,
            "results": results,
            "summary": summary
        }
    except Exception as e:
        logger.error(f"SQL查询失败: {str(e)}")
        return {
            "success": False,
            "message": f"查询失败: {str(e)}",
            "sql_query": sql if 'sql' in locals() else ""
        }


@mcp.tool()
@validate_tool
async def execute_sql(sql: str) -> Dict[str, Any]:
    """
    直接执行SQL语句并返回结果
    
    :param sql: 要执行的SQL语句
    :return: 包含执行结果的字典
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }

    try:
        logger.info(f"执行SQL: {sql}")
        start_time = time.time()

        # 执行SQL查询
        df = vn.run_sql(sql)
        execution_time = f"{time.time() - start_time:.2f}秒"

        # 如果为空，返回空结果
        if df is None or df.empty:
            return {
                "success": True,
                "sql_query": sql,
                "execution_time": execution_time,
                "row_count": 0,
                "results": []
            }

        # 转换为字典列表
        results = df.to_dict(orient='records')
        row_count = len(results)

        return {
            "success": True,
            "sql_query": sql,
            "execution_time": execution_time,
            "row_count": row_count,
            "results": results
        }
    except Exception as e:
        logger.error(f"执行SQL失败: {str(e)}")
        return {
            "success": False,
            "message": f"执行失败: {str(e)}",
            "sql_query": sql
        }


@mcp.tool()
@validate_tool
async def get_table_info(table_name: str) -> Dict[str, Any]:
    """
    获取指定表的详细信息
    
    :param table_name: 表名
    :return: 包含表结构和样本数据的字典
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }

    try:
        # 检查表是否存在
        all_tables = vn.run_sql("SHOW TABLES")
        table_list = all_tables.iloc[:, 0].tolist()

        if table_name not in table_list:
            return {
                "success": False,
                "message": f"表 '{table_name}' 不存在",
                "table_name": table_name
            }

        # 获取表注释
        table_status = vn.run_sql(f"SHOW TABLE STATUS WHERE Name = '{table_name}'")
        comment = table_status['Comment'].iloc[0] if not table_status.empty else ""

        # 获取表结构
        columns_info = vn.run_sql(f"DESCRIBE `{table_name}`")

        # 获取主键信息
        primary_keys = []
        try:
            primary_key_info = vn.run_sql(f"SHOW KEYS FROM `{table_name}` WHERE Key_name = 'PRIMARY'")
            if not primary_key_info.empty:
                primary_keys = primary_key_info['Column_name'].tolist()
        except:
            pass

        # 转换列信息为更详细的格式
        columns = []
        for _, row in columns_info.iterrows():
            is_primary = row['Field'] in primary_keys
            column_info = {
                "name": row['Field'],
                "type": row['Type'],
                "nullable": row['Null'] == 'YES',
                "default": row['Default'],
                "is_primary": is_primary,
                "comment": ""  # MySQL DESCRIBE不返回注释
            }
            columns.append(column_info)

        # 获取表行数
        count_result = vn.run_sql(f"SELECT COUNT(*) as count FROM `{table_name}`")
        row_count = count_result['count'].iloc[0] if not count_result.empty else 0

        # 获取样本数据
        sample_data = []
        if row_count > 0:
            sample_result = vn.run_sql(f"SELECT * FROM `{table_name}` LIMIT 10")
            sample_data = sample_result.to_dict(orient='records')

        return {
            "success": True,
            "table_name": table_name,
            "comment": comment,
            "row_count": row_count,
            "columns": columns,
            "sample_data": sample_data
        }
    except Exception as e:
        logger.error(f"获取表信息失败: {str(e)}")
        return {
            "success": False,
            "message": f"获取表信息失败: {str(e)}",
            "table_name": table_name
        }


@mcp.tool()
@validate_tool
async def get_all_tables() -> Dict[str, Any]:
    """
    获取数据库中所有表的列表和基本信息
    
    :return: 包含所有表信息的字典
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }

    try:
        # 获取当前数据库名
        db_info = vn.run_sql("SELECT DATABASE() as db")
        database = db_info['db'].iloc[0] if not db_info.empty else "未知数据库"

        # 获取所有表
        tables_result = vn.run_sql("SHOW TABLES")
        if tables_result.empty:
            return {
                "success": True,
                "database": database,
                "table_count": 0,
                "tables": []
            }

        table_names = tables_result.iloc[:, 0].tolist()

        # 获取表状态信息
        tables_status = vn.run_sql("SHOW TABLE STATUS")

        # 构建表信息列表
        tables_info = []
        for table in table_names:
            try:
                # 从表状态中获取信息
                table_row = tables_status[tables_status['Name'] == table]
                comment = table_row['Comment'].iloc[0] if not table_row.empty else ""
                rows = table_row['Rows'].iloc[0] if not table_row.empty else 0

                # 获取列信息
                columns_info = vn.run_sql(f"DESCRIBE `{table}`")

                table_info = {
                    "table_name": table,
                    "comment": comment,
                    "row_count": rows,
                    "columns": columns_info['Field'].tolist()
                }
                tables_info.append(table_info)
            except Exception as e:
                logger.error(f"获取表 {table} 信息时出错: {str(e)}")
                tables_info.append(
                    {
                        "table_name": table,
                        "comment": "获取信息出错",
                        "row_count": 0,
                        "columns": []
                    }
                )

        return {
            "success": True,
            "database": database,
            "table_count": len(tables_info),
            "tables": tables_info
        }
    except Exception as e:
        logger.error(f"获取所有表信息失败: {str(e)}")
        return {
            "success": False,
            "message": f"获取所有表信息失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def train_sql_example(question: str, sql: str) -> Dict[str, Any]:
    """
    训练一个自然语言问题和对应的SQL对
    
    :param question: 自然语言问题
    :param sql: 对应的SQL语句
    :return: 训练结果
    """
    if vn is None:
        return {
            "success": False,
            "message": "Text2SQL模块未正确初始化"
        }

    try:
        logger.info(f"训练SQL示例 - 问题: {question}, SQL: {sql}")

        # 使用Vanna的train方法
        vn.train(question=question, sql=sql)

        return {
            "success": True,
            "message": "训练成功",
            "data": {
                "question": question,
                "sql": sql
            }
        }
    except Exception as e:
        logger.error(f"训练SQL示例失败: {str(e)}")
        return {
            "success": False,
            "message": f"训练失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def train_database_schema() -> Dict[str, Any]:
    """
    训练数据库模式，包括表结构和关系
    
    :return: 训练结果
    """
    if trainer is None:
        return {
            "success": False,
            "message": "VannaTrainer未正确初始化"
        }

    try:
        logger.info("开始训练数据库模式...")

        # 使用VannaTrainer的训练方法
        success = trainer.train_database_structure()

        if success:
            return {
                "success": True,
                "message": "数据库模式训练成功"
            }
        else:
            return {
                "success": False,
                "message": "数据库模式训练失败，请检查日志"
            }
    except Exception as e:
        logger.error(f"训练数据库模式失败: {str(e)}")
        return {
            "success": False,
            "message": f"训练失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def train_with_examples() -> Dict[str, Any]:
    """
    使用动态生成的示例问题训练模型
    
    :return: 训练结果
    """
    if trainer is None:
        return {
            "success": False,
            "message": "VannaTrainer未正确初始化"
        }

    try:
        logger.info("开始训练示例问题...")

        # 使用VannaTrainer的示例训练方法
        trainer.add_example_questions()

        return {
            "success": True,
            "message": "示例问题训练成功"
        }
    except Exception as e:
        logger.error(f"训练示例问题失败: {str(e)}")
        return {
            "success": False,
            "message": f"训练失败: {str(e)}"
        }


@mcp.tool()
@validate_tool
async def run_full_training() -> Dict[str, Any]:
    """
    运行完整的训练流程，包括数据库模式和示例问题
    
    :return: 训练结果
    """
    if trainer is None:
        return {
            "success": False,
            "message": "VannaTrainer未正确初始化"
        }

    try:
        logger.info("开始执行完整训练流程...")

        # 使用VannaTrainer的完整训练流程
        success = trainer.full_training_pipeline()

        if success:
            return {
                "success": True,
                "message": "完整训练流程执行成功"
            }
        else:
            return {
                "success": False,
                "message": "训练流程执行失败，请检查日志"
            }
    except Exception as e:
        logger.error(f"执行训练流程失败: {str(e)}")
        return {
            "success": False,
            "message": f"训练失败: {str(e)}"
        }


# 服务器启动入口点
if __name__ == "__main__":
    # 注册事件已经在上面使用装饰器完成
    # 启动服务器
    mcp.run()
