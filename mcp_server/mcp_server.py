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
import base64
import io
from typing import Dict, Any, Optional, List, Union
from mcp.server.fastmcp import FastMCP
from tool_weather import WeatherTool
from utils.log_util import logger
from mcp_text2sql import (
    text_to_sql,
    text_to_sql_sse,
    query,
    describe_table,
    describe_tables,
    init_db_pool, cleanup as sql_cleanup
)

# 尝试导入可视化相关库
try:
    import matplotlib
    matplotlib.use('Agg')  # 使用非交互式后端
    import matplotlib.pyplot as plt
    import pandas as pd
    import numpy as np
    VISUALIZATION_AVAILABLE = True
    logger.info("可视化库加载成功，图表功能可用")
except ImportError:
    VISUALIZATION_AVAILABLE = False
    logger.warning("无法加载可视化库，图表功能不可用。请安装依赖：pip install matplotlib pandas numpy")

# 初始化 MCP 服务器
mcp = FastMCP("SakuraMcpServer")

# 服务器初始化标志
db_initialized = False

# 注册事件 - 在服务器启动前初始化数据库连接

async def on_server_start():
    """服务器启动事件处理"""
    await init_server()

# 注册事件 - 在服务器关闭时清理资源

async def on_server_shutdown():
    """服务器关闭事件处理"""
    await cleanup()

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
            
        # 测试SQL数据库连接是否可用
        db_status = False
        try:
            # 重用text2sql模块中的数据库连接池
            from mcp_text2sql import db_pool
            if db_pool:
                async with db_pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute("SELECT 1")
                        db_status = True
            else:
                # 尝试初始化连接池
                db_status = await init_db_pool()
        except:
            db_status = False

        return {
            "status": "ok" if (api_status and ollama_status and db_status) else "degraded",
            "services": {
                "weather": "ok" if api_status else "error",
                "ollama": "ok" if ollama_status else "error",
                "sql_database": "ok" if db_status else "error"
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


# 注册Text2SQL服务工具
@mcp.tool()
@validate_tool
async def sql_query(query: str) -> Dict[str, Any]:
    """
    将自然语言转换为SQL查询并执行
    :param query: 自然语言查询，例如"查询所有男性学生"
    :return: 包含SQL查询和执行结果的字典
    """
    # 确保数据库已初始化
    global db_initialized
    if not db_initialized:
        await init_server()
    
    return await text_to_sql(query)


@mcp.tool()
@validate_tool
async def sql_query_stream(query: str):
    """
    将自然语言转换为SQL查询并执行，以流式方式返回结果
    :param query: 自然语言查询，例如"查询所有男性学生"
    :return: 流式返回查询结果
    """
    # 确保数据库已初始化
    global db_initialized
    if not db_initialized:
        await init_server()
        
    async for result in text_to_sql_sse(query):
        yield result


@mcp.tool()
@validate_tool
async def execute_sql(sql: str) -> Dict[str, Any]:
    """
    直接执行SQL查询语句
    :param sql: SQL查询语句
    :return: 查询结果
    """
    # 确保数据库已初始化
    global db_initialized
    if not db_initialized:
        await init_server()
        
    return await query(sql)


@mcp.tool()
@validate_tool
async def get_table_info(table_name: str = "") -> Dict[str, Any]:
    """
    获取指定数据库表的结构信息
    :param table_name: 可选的表名，如果不提供则返回第一个表
    :return: 表结构信息
    """
    # 确保数据库已初始化
    global db_initialized
    if not db_initialized:
        await init_server()
    
    # 记录请求参数
    logger.info(f"请求表信息: 表名='{table_name}'")
    
    # 尝试获取表信息
    try:
        result = await describe_table(table_name)
        
        # 记录结果状态
        if "error" in result:
            logger.error(f"获取表信息失败: {result['error']}")
        else:
            logger.info(f"获取表信息成功: 表名={result.get('table_name', '未知')}, 列数={len(result.get('columns', []))}")
            
        return result
    except Exception as e:
        logger.error(f"获取表信息异常: {str(e)}")
        return {"error": f"获取表信息异常: {str(e)}"}


@mcp.tool()
@validate_tool
async def get_all_tables() -> Dict[str, Any]:
    """
    获取数据库中所有表的结构信息
    :return: 所有表的结构信息
    """
    # 确保数据库已初始化
    global db_initialized
    if not db_initialized:
        await init_server()
        
    return await describe_tables()


# 清理资源函数
async def cleanup():
    """清理资源"""
    # 关闭Ollama客户端
    await ollama_client.close()
    
    # 关闭SQL服务资源
    await sql_cleanup()


# 初始化服务器
async def init_server():
    """初始化服务器"""
    global db_initialized
    
    # 初始化SQL数据库连接
    try:
        db_init_success = await init_db_pool()
        if db_init_success:
            db_initialized = True
            logger.info("MCP服务数据库连接初始化成功")
        else:
            logger.error("MCP服务数据库连接初始化失败")
    except Exception as e:
        logger.error(f"数据库初始化错误: {str(e)}")
    
    logger.info("MCP服务初始化完成")


# 图表工具函数
class ChartTools:
    """图表生成工具类"""
    
    @staticmethod
    def create_chart(
        data: List[Dict[str, Any]], 
        chart_type: str, 
        x_field: str, 
        y_field: str, 
        title: str = "",
        color: str = "blue",
        limit: int = 20,
        sort_by: Optional[str] = None,
        sort_order: str = "desc",
        group_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        创建图表
        :param data: 数据列表
        :param chart_type: 图表类型 (bar, line, pie, scatter)
        :param x_field: X轴字段
        :param y_field: Y轴字段
        :param title: 图表标题
        :param color: 图表颜色
        :param limit: 数据点数量限制
        :param sort_by: 排序字段
        :param sort_order: 排序顺序 (asc, desc)
        :param group_by: 分组字段
        :return: 包含图表数据的字典
        """
        if not VISUALIZATION_AVAILABLE:
            return {
                "error": "缺少可视化库，请安装 matplotlib, pandas, numpy",
                "install_command": "pip install matplotlib pandas numpy"
            }
        
        try:
            # 转换为DataFrame
            df = pd.DataFrame(data)
            
            # 检查字段是否存在
            if x_field not in df.columns:
                return {"error": f"X轴字段 '{x_field}' 不存在"}
            if y_field not in df.columns:
                return {"error": f"Y轴字段 '{y_field}' 不存在"}
            if group_by and group_by not in df.columns:
                return {"error": f"分组字段 '{group_by}' 不存在"}
            
            # 数据预处理
            # 限制数据量
            if len(df) > limit:
                # 如果需要排序
                if sort_by:
                    if sort_by in df.columns:
                        ascending = sort_order.lower() != "desc"
                        df = df.sort_values(by=sort_by, ascending=ascending)
                    else:
                        return {"error": f"排序字段 '{sort_by}' 不存在"}
                
                df = df.head(limit)
            
            # 处理数据类型
            if pd.api.types.is_numeric_dtype(df[y_field]):
                df[y_field] = pd.to_numeric(df[y_field], errors='coerce')
            
            # 设置图表样式
            plt.style.use('seaborn-v0_8-darkgrid')
            fig, ax = plt.subplots(figsize=(10, 6))
            
            # 根据图表类型绘制
            if chart_type.lower() == 'bar':
                if group_by:
                    # 分组柱状图
                    groups = df.groupby([x_field, group_by])[y_field].sum().unstack()
                    groups.plot(kind='bar', ax=ax)
                else:
                    # 普通柱状图
                    df.plot(kind='bar', x=x_field, y=y_field, color=color, ax=ax)
            
            elif chart_type.lower() == 'line':
                if group_by:
                    # 分组线图
                    for name, group in df.groupby(group_by):
                        group.plot(kind='line', x=x_field, y=y_field, label=name, ax=ax)
                else:
                    # 普通线图
                    df.plot(kind='line', x=x_field, y=y_field, color=color, ax=ax)
            
            elif chart_type.lower() == 'pie':
                # 饼图需要聚合数据
                pie_data = df.groupby(x_field)[y_field].sum()
                pie_data.plot(kind='pie', autopct='%1.1f%%', ax=ax)
                ax.set_ylabel('')  # 移除Y轴标签
            
            elif chart_type.lower() == 'scatter':
                if group_by:
                    # 分组散点图
                    for name, group in df.groupby(group_by):
                        group.plot(kind='scatter', x=x_field, y=y_field, label=name, ax=ax)
                else:
                    # 普通散点图
                    df.plot(kind='scatter', x=x_field, y=y_field, color=color, ax=ax)
            
            else:
                return {"error": f"不支持的图表类型: {chart_type}"}
            
            # 设置标题和标签
            if title:
                ax.set_title(title)
            ax.set_xlabel(x_field)
            ax.set_ylabel(y_field)
            
            # 添加图例（如果有分组）
            if group_by:
                ax.legend(title=group_by)
            
            # 调整布局
            plt.tight_layout()
            
            # 将图表转换为base64编码的图像
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            plt.close(fig)
            
            # 返回图表数据
            return {
                "chart_type": chart_type,
                "title": title,
                "x_field": x_field,
                "y_field": y_field,
                "data_points": len(df),
                "image": f"data:image/png;base64,{image_base64}"
            }
        
        except Exception as e:
            logger.error(f"生成图表失败: {str(e)}", exc_info=True)
            return {"error": f"生成图表失败: {str(e)}"}

# 图表生成工具
@mcp.tool()
@validate_tool
async def generate_chart(
    data: Optional[List[Dict[str, Any]]] = None,
    sql: Optional[str] = None,
    natural_query: Optional[str] = None,
    chart_type: str = "bar",
    x_field: str = "",
    y_field: str = "",
    title: str = "",
    color: str = "blue",
    limit: int = 20,
    sort_by: Optional[str] = None,
    sort_order: str = "desc",
    group_by: Optional[str] = None
) -> Dict[str, Any]:
    """
    根据数据生成图表
    :param data: 可选的数据列表，如果提供则直接使用
    :param sql: 可选的SQL查询，如果提供则执行此查询获取数据
    :param natural_query: 可选的自然语言查询，如果提供则转换为SQL并执行
    :param chart_type: 图表类型 (bar, line, pie, scatter)
    :param x_field: X轴字段
    :param y_field: Y轴字段
    :param title: 图表标题
    :param color: 图表颜色
    :param limit: 数据点数量限制
    :param sort_by: 排序字段
    :param sort_order: 排序顺序 (asc, desc)
    :param group_by: 分组字段
    :return: 包含图表的字典
    """
    # 确保数据库已初始化
    global db_initialized
    if not db_initialized:
        await init_server()
    
    # 获取数据
    chart_data = None
    query_info = {}
    
    try:
        if data:
            # 直接使用提供的数据
            chart_data = data
            query_info["data_source"] = "direct"
            query_info["data_count"] = len(data)
        
        elif sql:
            # 执行SQL查询
            query_result = await query(sql)
            if "error" in query_result:
                return query_result
            
            chart_data = query_result.get("results", [])
            query_info["data_source"] = "sql"
            query_info["sql"] = sql
            query_info["execution_time"] = query_result.get("execution_time")
            query_info["row_count"] = query_result.get("row_count", 0)
        
        elif natural_query:
            # 执行自然语言查询
            query_result = await text_to_sql(natural_query)
            if "error" in query_result:
                return query_result
            
            chart_data = query_result.get("results", [])
            query_info["data_source"] = "natural_language"
            query_info["query"] = natural_query
            query_info["sql"] = query_result.get("sql_query")
            query_info["execution_time"] = query_result.get("execution_time")
            query_info["row_count"] = query_result.get("row_count", 0)
        
        else:
            return {"error": "必须提供以下参数之一: data, sql, 或 natural_query"}
        
        # 检查数据
        if not chart_data:
            return {"error": "查询结果为空，无法生成图表"}
        
        # 检查是否提供了必要的字段
        if not x_field or not y_field:
            # 尝试自动推断字段
            available_fields = list(chart_data[0].keys())
            
            if not x_field:
                # 寻找可能的分类型字段作为X轴
                for field in available_fields:
                    field_lower = field.lower()
                    if any(term in field_lower for term in ['name', 'id', 'category', 'type', 'date']):
                        x_field = field
                        break
                
                # 如果没找到，使用第一个字段
                if not x_field and available_fields:
                    x_field = available_fields[0]
            
            if not y_field:
                # 寻找可能的数值型字段作为Y轴
                numeric_fields = []
                for field in available_fields:
                    try:
                        # 检查第一条数据的这个字段是否是数字
                        value = chart_data[0].get(field)
                        if isinstance(value, (int, float)) or (isinstance(value, str) and value.replace('.', '', 1).isdigit()):
                            numeric_fields.append(field)
                    except:
                        pass
                
                # 选择第一个数值型字段
                if numeric_fields:
                    y_field = numeric_fields[0]
                    # 如果有count, sum等聚合字段优先使用
                    for field in numeric_fields:
                        field_lower = field.lower()
                        if any(term in field_lower for term in ['count', 'sum', 'total', 'amount']):
                            y_field = field
                            break
                elif available_fields and available_fields != [x_field]:
                    # 如果没有数值型字段，使用第一个不是X轴的字段
                    for field in available_fields:
                        if field != x_field:
                            y_field = field
                            break
                else:
                    # 如果实在找不到合适的Y轴，返回错误
                    return {"error": "无法自动推断Y轴字段，请手动指定y_field参数"}
            
            # 如果没有标题，使用字段名作为标题
            if not title:
                title = f"{y_field} by {x_field}"
        
        # 生成图表
        chart_result = ChartTools.create_chart(
            data=chart_data,
            chart_type=chart_type,
            x_field=x_field,
            y_field=y_field,
            title=title,
            color=color,
            limit=limit,
            sort_by=sort_by,
            sort_order=sort_order,
            group_by=group_by
        )
        
        # 添加查询信息
        chart_result["query_info"] = query_info
        
        return chart_result
    
    except Exception as e:
        logger.error(f"图表生成失败: {str(e)}", exc_info=True)
        return {"error": f"图表生成失败: {str(e)}"}


@mcp.tool()
@validate_tool
async def analyze_data(
    sql: Optional[str] = None,
    natural_query: Optional[str] = None
) -> Dict[str, Any]:
    """
    分析数据并生成统计信息
    :param sql: 可选的SQL查询
    :param natural_query: 可选的自然语言查询
    :return: 数据分析结果
    """
    if not VISUALIZATION_AVAILABLE:
        return {
            "error": "缺少分析库，请安装 pandas, numpy",
            "install_command": "pip install pandas numpy"
        }
    
    # 确保数据库已初始化
    global db_initialized
    if not db_initialized:
        await init_server()
    
    try:
        # 获取数据
        data = None
        query_info = {}
        
        if sql:
            # 执行SQL查询
            query_result = await query(sql)
            if "error" in query_result:
                return query_result
            
            data = query_result.get("results", [])
            query_info["sql"] = sql
        
        elif natural_query:
            # 执行自然语言查询
            query_result = await text_to_sql(natural_query)
            if "error" in query_result:
                return query_result
            
            data = query_result.get("results", [])
            query_info["natural_query"] = natural_query
            query_info["sql"] = query_result.get("sql_query")
        
        else:
            return {"error": "必须提供以下参数之一: sql 或 natural_query"}
        
        # 检查数据
        if not data:
            return {"error": "查询结果为空，无法执行分析"}
        
        # 转换为DataFrame
        df = pd.DataFrame(data)
        
        # 执行分析
        analysis = {
            "record_count": len(df),
            "column_count": len(df.columns),
            "columns": {}
        }
        
        # 分析每列
        for column in df.columns:
            col_data = df[column]
            col_analysis = {}
            
            # 通用统计
            col_analysis["missing_values"] = col_data.isna().sum()
            col_analysis["missing_percent"] = f"{(col_data.isna().sum() / len(df) * 100):.2f}%"
            col_analysis["unique_values"] = col_data.nunique()
            
            # 获取数据类型
            dtype_name = str(col_data.dtype)
            col_analysis["data_type"] = dtype_name
            
            # 数值型列的统计
            if pd.api.types.is_numeric_dtype(col_data):
                # 尝试转换为数值类型
                numeric_data = pd.to_numeric(col_data, errors='coerce')
                col_analysis["min"] = numeric_data.min()
                col_analysis["max"] = numeric_data.max()
                col_analysis["mean"] = numeric_data.mean()
                col_analysis["median"] = numeric_data.median()
                col_analysis["std"] = numeric_data.std()
                
                # 计算分位数
                quantiles = numeric_data.quantile([0.25, 0.5, 0.75]).to_dict()
                col_analysis["quartiles"] = {
                    "q1": quantiles.get(0.25),
                    "q2": quantiles.get(0.5),
                    "q3": quantiles.get(0.75)
                }
            
            # 分类或文本列的统计
            else:
                # 最常见的值
                try:
                    value_counts = col_data.value_counts().head(5).to_dict()
                    col_analysis["common_values"] = value_counts
                except:
                    col_analysis["common_values"] = "无法计算"
                
                # 尝试计算字符串长度统计
                try:
                    str_lengths = col_data.astype(str).str.len()
                    col_analysis["mean_length"] = str_lengths.mean()
                    col_analysis["max_length"] = str_lengths.max()
                    col_analysis["min_length"] = str_lengths.min()
                except:
                    pass
            
            analysis["columns"][column] = col_analysis
        
        # 添加查询信息
        analysis["query_info"] = query_info
        
        return analysis
    
    except Exception as e:
        logger.error(f"数据分析失败: {str(e)}", exc_info=True)
        return {"error": f"数据分析失败: {str(e)}"}

# 服务器启动入口点
if __name__ == "__main__":
    # 注册事件已经在上面使用装饰器完成
    # 启动服务器
    mcp.run()
