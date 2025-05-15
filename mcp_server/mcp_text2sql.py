#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/14 17:00
# @Author   : 冉勇
# @File     : mcp_text2sql.py
# @Software : PyCharm
# @Desc     : MCP服务 - 自然语言转SQL查询服务
import os
import time
import asyncio
import json
import aiomysql
from typing import Dict, Any, List, AsyncGenerator
from mcp.server.fastmcp import FastMCP
from utils.log_util import logger

# 初始化 MCP 服务器
mcp = FastMCP("SakuraText2SqlService")

# MySQL数据库表students的表格式
DB_SCHEMA = """
CREATE TABLE IF NOT EXISTS students (
    student_id SERIAL PRIMARY KEY,              
    first_name VARCHAR(50) NOT NULL,         
    gender CHAR(100) NOT NULL CHECK (gender IN ('男', '女')), 
    date_of_birth DATE NOT NULL,               
    phone_number VARCHAR(15),                
    address TEXT,                             
    grade_level SMALLINT CHECK (grade_level BETWEEN 1 AND 12), 
    gpa NUMERIC(3, 2) DEFAULT 0.0 CHECK (gpa >= 0 AND gpa <= 4.0), 
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP   
);
"""

# 数据库连接配置
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "123456"),
    "database": os.getenv("MYSQL_DATABASE", "test02"),
    "table_name": os.getenv("MYSQL_TABLE", "students")
}

# 数据库连接池
db_pool = None


async def init_db_pool():
    """初始化数据库连接池"""
    global db_pool
    try:
        # 创建连接池
        db_pool = await aiomysql.create_pool(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            db=DB_CONFIG["database"],
            autocommit=True
        )
        
        # 创建数据库和表
        await ensure_database_and_table()
        logger.info("数据库连接池初始化成功")
        return True
    except Exception as e:
        logger.error(f"数据库连接池初始化失败: {str(e)}")
        return False


async def ensure_database_and_table():
    """确保数据库和表存在"""
    # 创建单独的连接用于初始化
    conn = await aiomysql.connect(
        host=DB_CONFIG["host"], 
        user=DB_CONFIG["user"], 
        password=DB_CONFIG["password"]
    )
    
    try:
        async with conn.cursor() as cursor:
            # 检查数据库是否存在
            await cursor.execute(f"SHOW DATABASES LIKE '{DB_CONFIG['database']}'")
            result = await cursor.fetchone()
            if not result:
                # 创建数据库
                await cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
                logger.info(f"创建数据库: {DB_CONFIG['database']}")
            
            # 选择数据库
            await cursor.execute(f"USE {DB_CONFIG['database']}")
            
            # 检查表是否存在
            await cursor.execute(f"SHOW TABLES LIKE '{DB_CONFIG['table_name']}'")
            result = await cursor.fetchone()
            if not result:
                # 创建表
                await cursor.execute(DB_SCHEMA)
                logger.info(f"创建表: {DB_CONFIG['table_name']}")
    finally:
        conn.close()


@mcp.tool()
async def text_to_sql(query: str) -> Dict[str, Any]:
    """
    将自然语言查询转换为SQL查询并执行，支持批量返回结果
    :param query: 自然语言查询，例如"查询所有男性学生"
    :return: 包含SQL查询和执行结果的字典
    """
    try:
        if not db_pool:
            await init_db_pool()
            if not db_pool:
                return {"error": "数据库连接失败"}
        
        # 使用自定义推理函数生成SQL
        start_time = time.time()
        sql_query = await generate_sql_query(query)
        
        # 执行SQL查询
        all_results = []
        async for batch_result in execute_query_streaming(sql_query):
            if "error" in batch_result:
                return batch_result
            
            if "batch" in batch_result:
                all_results.extend(batch_result["batch"])
        
        # 记录执行时间
        execution_time = time.time() - start_time
        logger.info(f"查询执行成功: '{query}' => '{sql_query}', 耗时: {execution_time:.2f}秒")
        
        return {
            "sql_query": sql_query,
            "results": all_results,
            "execution_time": f"{execution_time:.2f}秒",
            "row_count": len(all_results)
        }
    except Exception as e:
        logger.error(f"查询执行失败: {str(e)}")
        return {"error": f"查询执行失败: {str(e)}"}


@mcp.tool()
async def text_to_sql_sse(query: str) -> AsyncGenerator[Dict[str, Any], None]:
    """
    将自然语言查询转换为SQL查询并执行，支持SSE（Server-Sent Events）模式流式返回结果
    :param query: 自然语言查询，例如"查询所有男性学生"
    :return: 流式返回查询结果
    """
    try:
        if not db_pool:
            await init_db_pool()
            if not db_pool:
                yield {"error": "数据库连接失败"}
                return
        
        # 使用自定义推理函数生成SQL
        start_time = time.time()
        sql_query = await generate_sql_query(query)
        
        # 先返回SQL查询语句
        yield {
            "type": "sql_generated",
            "sql_query": sql_query,
            "timestamp": time.time()
        }
        
        # 统计结果总数
        total_rows = 0
        processed_rows = 0
        
        # 执行SQL查询并流式返回结果
        async for batch_result in execute_query_streaming(sql_query, batch_size=5):  # 减小批次大小以更频繁更新
            if "error" in batch_result:
                yield batch_result
                return
            
            if "metadata" in batch_result:
                total_rows = batch_result["metadata"]["total_rows"]
                # 返回元数据
                yield {
                    "type": "metadata",
                    "columns": batch_result["metadata"]["columns"],
                    "total_rows": total_rows,
                    "timestamp": time.time()
                }
                continue
                
            if "batch" in batch_result:
                # 更新计数
                batch_size = len(batch_result["batch"])
                processed_rows += batch_size
                
                # 返回批次数据
                yield {
                    "type": "data_batch",
                    "batch": batch_result["batch"],
                    "batch_size": batch_size,
                    "processed_rows": processed_rows,
                    "total_rows": total_rows,
                    "progress": f"{(processed_rows / total_rows * 100) if total_rows > 0 else 0:.1f}%",
                    "is_last_batch": batch_result.get("is_last_batch", False),
                    "timestamp": time.time()
                }
        
        # 查询结束，返回摘要信息
        execution_time = time.time() - start_time
        logger.info(f"SSE查询执行成功: '{query}' => '{sql_query}', 耗时: {execution_time:.2f}秒, 共{total_rows}条记录")
        
        yield {
            "type": "summary",
            "sql_query": sql_query,
            "total_rows": total_rows,
            "execution_time": f"{execution_time:.2f}秒",
            "completed": True,
            "timestamp": time.time()
        }
    except Exception as e:
        error_msg = f"SSE查询执行失败: {str(e)}"
        logger.error(error_msg)
        yield {"type": "error", "error": error_msg, "timestamp": time.time()}


async def generate_sql_query(query: str) -> str:
    """
    使用预定义的规则和模板生成SQL查询
    :param query: 自然语言查询
    :return: SQL查询语句
    """
    # 简单关键词映射
    keywords = {
        "男": "gender = '男'",
        "男性": "gender = '男'",
        "女": "gender = '女'",
        "女性": "gender = '女'",
        "学生": "students",
        "GPA": "gpa",
        "大于": ">",
        "小于": "<",
        "等于": "=",
        "高于": ">",
        "低于": "<",
        "年级": "grade_level",
        "电话": "phone_number",
        "姓名": "first_name",
        "地址": "address",
        "生日": "date_of_birth",
        "出生日期": "date_of_birth",
        "按": "ORDER BY",
        "排序": "ORDER BY",
        "降序": "DESC",
        "升序": "ASC",
        "从高到低": "DESC",
        "从低到高": "ASC",
        "最近": "created_at >= NOW() - INTERVAL",
        "限制": "LIMIT",
        "最多": "LIMIT"
    }
    
    # 默认查询
    sql = "SELECT * FROM students"
    
    # 条件标志
    has_where = False
    
    # 检查是否包含特定条件
    for keyword, sql_part in keywords.items():
        if keyword in query:
            # 第一个条件使用WHERE，后续条件使用AND
            if not has_where and any(kw in ["gender", "gpa", "grade_level", "address", "phone_number", "first_name", "date_of_birth"] for kw in sql_part.split()):
                sql += f" WHERE {sql_part}"
                has_where = True
            # 排序条件
            elif "ORDER BY" in sql_part and "ORDER BY" not in sql:
                # 确定排序字段，默认为gpa
                sort_field = "gpa"
                if "姓名" in query:
                    sort_field = "first_name"
                elif "出生" in query or "生日" in query:
                    sort_field = "date_of_birth"
                elif "创建" in query:
                    sort_field = "created_at"
                
                sql += f" ORDER BY {sort_field}"
                # 添加排序方向
                if "DESC" in sql_part or "从高到低" in query:
                    sql += " DESC"
                elif "ASC" in sql_part or "从低到高" in query:
                    sql += " ASC"
            # 限制条件
            elif "LIMIT" in sql_part and "LIMIT" not in sql:
                # 查找数字作为限制数量
                import re
                numbers = re.findall(r'\d+', query)
                limit = 10  # 默认限制
                if numbers:
                    limit = numbers[0]
                sql += f" LIMIT {limit}"
    
    # 如果没有检测到条件，返回所有学生
    if sql == "SELECT * FROM students" and "所有" not in query:
        sql += " LIMIT 100"  # 默认限制返回数量
        
    return sql


async def execute_query_streaming(sql_query: str, batch_size: int = 10) -> AsyncGenerator[Dict[str, Any], None]:
    """
    执行SQL查询并以流式方式返回结果
    :param sql_query: SQL查询语句
    :param batch_size: 每批次返回的记录数
    :return: 流式查询结果
    """
    if not db_pool:
        raise Exception("数据库连接池未初始化")
    
    try:
        async with db_pool.acquire() as conn:
            async with conn.cursor(aiomysql.DictCursor) as cursor:
                # 执行查询
                await cursor.execute(sql_query)
                
                # 获取列名
                columns = [column[0] for column in cursor.description]
                
                # 一次性获取所有结果
                results = await cursor.fetchall()
                total_rows = len(results)
                
                # 先返回元数据
                yield {
                    "metadata": {
                        "columns": columns,
                        "total_rows": total_rows,
                        "sql_query": sql_query
                    }
                }
                
                # 批量处理结果
                for i in range(0, total_rows, batch_size):
                    batch = results[i:i+batch_size]
                    if not batch:
                        break
                    
                    # 添加少量延迟以模拟实际网络环境中的流式传输（仅用于演示）
                    if i > 0:  # 第一批立即返回，之后的批次添加少量延迟
                        await asyncio.sleep(0.1)
                    
                    # 转换批次为可序列化格式
                    serializable_batch = []
                    for row in batch:
                        serializable_row = {}
                        for key, value in row.items():
                            # 处理日期和时间类型
                            if hasattr(value, 'isoformat'):
                                serializable_row[key] = value.isoformat()
                            else:
                                serializable_row[key] = value
                        serializable_batch.append(serializable_row)
                    
                    # 判断是否为最后一批
                    is_last_batch = (i + batch_size >= total_rows)
                    
                    yield {
                        "batch": serializable_batch,
                        "batch_size": len(batch),
                        "total_rows": total_rows,
                        "is_last_batch": is_last_batch
                    }
    except Exception as e:
        logger.error(f"执行流式查询失败: {str(e)}")
        yield {"error": f"执行查询失败: {str(e)}"}


async def execute_query(sql_query: str) -> List[Dict[str, Any]]:
    """
    执行SQL查询并返回结果
    :param sql_query: SQL查询语句
    :return: 查询结果列表
    """
    if not db_pool:
        raise Exception("数据库连接池未初始化")
    
    async with db_pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cursor:
            await cursor.execute(sql_query)
            results = await cursor.fetchall()
            # 转换结果为可序列化的字典
            serializable_results = []
            for row in results:
                serializable_row = {}
                for key, value in row.items():
                    # 处理日期和时间类型
                    if hasattr(value, 'isoformat'):
                        serializable_row[key] = value.isoformat()
                    else:
                        serializable_row[key] = value
                serializable_results.append(serializable_row)
            return serializable_results


@mcp.tool()
async def query(query: str) -> Dict[str, Any]:
    """
    直接执行SQL查询语句
    :param query: SQL查询语句
    :return: 查询结果
    """
    try:
        if not db_pool:
            await init_db_pool()
            if not db_pool:
                return {"error": "数据库连接失败"}
        
        # 记录查询开始时间
        start_time = time.time()
        
        # 执行SQL查询
        results = await execute_query(query)
        
        # 记录执行时间
        execution_time = time.time() - start_time
        logger.info(f"直接SQL查询执行成功: '{query}', 耗时: {execution_time:.2f}秒")
        
        return {
            "sql_query": query,
            "results": results,
            "execution_time": f"{execution_time:.2f}秒",
            "row_count": len(results)
        }
    except Exception as e:
        logger.error(f"直接SQL查询执行失败: {str(e)}")
        return {"error": f"查询执行失败: {str(e)}"}


@mcp.tool()
async def query_sse(query: str) -> AsyncGenerator[Dict[str, Any], None]:
    """
    直接执行SQL查询语句，支持SSE（Server-Sent Events）模式流式返回结果
    :param query: SQL查询语句
    :return: 流式返回查询结果
    """
    try:
        if not db_pool:
            await init_db_pool()
            if not db_pool:
                yield {"error": "数据库连接失败"}
                return
        
        # 记录查询开始时间
        start_time = time.time()
        
        # 先返回SQL查询语句
        yield {
            "type": "sql_generated",
            "sql_query": query,
            "timestamp": time.time()
        }
        
        # 统计结果总数
        total_rows = 0
        processed_rows = 0
        
        # 执行SQL查询并流式返回结果
        async for batch_result in execute_query_streaming(query, batch_size=5):
            if "error" in batch_result:
                yield batch_result
                return
            
            if "metadata" in batch_result:
                total_rows = batch_result["metadata"]["total_rows"]
                # 返回元数据
                yield {
                    "type": "metadata",
                    "columns": batch_result["metadata"]["columns"],
                    "total_rows": total_rows,
                    "timestamp": time.time()
                }
                continue
                
            if "batch" in batch_result:
                # 更新计数
                batch_size = len(batch_result["batch"])
                processed_rows += batch_size
                
                # 返回批次数据
                yield {
                    "type": "data_batch",
                    "batch": batch_result["batch"],
                    "batch_size": batch_size,
                    "processed_rows": processed_rows,
                    "total_rows": total_rows,
                    "progress": f"{(processed_rows / total_rows * 100) if total_rows > 0 else 0:.1f}%",
                    "is_last_batch": batch_result.get("is_last_batch", False),
                    "timestamp": time.time()
                }
        
        # 查询结束，返回摘要信息
        execution_time = time.time() - start_time
        logger.info(f"SSE直接SQL查询执行成功: '{query}', 耗时: {execution_time:.2f}秒, 共{total_rows}条记录")
        
        yield {
            "type": "summary",
            "sql_query": query,
            "total_rows": total_rows,
            "execution_time": f"{execution_time:.2f}秒",
            "completed": True,
            "timestamp": time.time()
        }
    except Exception as e:
        error_msg = f"SSE直接SQL查询执行失败: {str(e)}"
        logger.error(error_msg)
        yield {"type": "error", "error": error_msg, "timestamp": time.time()}


@mcp.tool()
async def describe_table() -> Dict[str, Any]:
    """
    获取students表的结构信息
    :return: 表结构信息
    """
    try:
        if not db_pool:
            await init_db_pool()
            if not db_pool:
                return {"error": "数据库连接失败"}
        
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(f"DESCRIBE {DB_CONFIG['table_name']}")
                columns = await cursor.fetchall()
                
                # 获取表的其他信息
                await cursor.execute(f"SELECT COUNT(*) FROM {DB_CONFIG['table_name']}")
                count = await cursor.fetchone()
                
                return {
                    "table_name": DB_CONFIG['table_name'],
                    "columns": [
                        {
                            "field": col[0],
                            "type": col[1],
                            "null": col[2],
                            "key": col[3],
                            "default": col[4],
                            "extra": col[5]
                        } for col in columns
                    ],
                    "row_count": count[0],
                    "schema": DB_SCHEMA
                }
    except Exception as e:
        logger.error(f"获取表结构失败: {str(e)}")
        return {"error": f"获取表结构失败: {str(e)}"}


@mcp.tool()
async def insert_sample_data(count: int = 10):
    """
    流式插入示例数据到students表
    :param count: 要插入的示例数据数量
    :return: 插入过程状态流
    """
    try:
        if not db_pool:
            await init_db_pool()
            if not db_pool:
                yield {"error": "数据库连接失败"}
                return
        
        # 样本数据生成
        import random
        from datetime import datetime, timedelta
        
        # 名字样本
        first_names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", 
                       "郑一", "王二", "陈一", "林二", "黄三", "刘四", "杨五"]
        
        # 地址样本
        addresses = ["北京", "上海", "广州", "深圳", "成都", "杭州", "武汉", "南京", 
                    "西安", "重庆", "长沙", "郑州", "天津", "苏州", "青岛"]
        
        # 生成插入的SQL语句
        inserted_count = 0
        async with db_pool.acquire() as conn:
            async with conn.cursor() as cursor:
                # 每10条或总数的10%报告一次进度，以较小者为准
                report_frequency = min(10, max(1, count // 10))
                
                # 发送开始事件
                yield {
                    "type": "start", 
                    "message": f"开始插入{count}条示例数据",
                    "timestamp": time.time()
                }
                
                for i in range(count):
                    # 生成随机数据
                    first_name = random.choice(first_names)
                    gender = random.choice(["男", "女"])
                    # 生成10-18岁的学生出生日期
                    years_ago = random.randint(10, 18)
                    dob = datetime.now() - timedelta(days=years_ago*365 + random.randint(0, 364))
                    dob_str = dob.strftime("%Y-%m-%d")
                    phone = f"1{random.choice(['3', '5', '7', '8', '9'])}{random.randint(10000000, 99999999)}"
                    address = random.choice(addresses)
                    grade_level = random.randint(1, 12)
                    gpa = round(random.uniform(2.0, 4.0), 2)
                    
                    # 执行插入
                    try:
                        sql = f"""INSERT INTO {DB_CONFIG['table_name']} 
                                (first_name, gender, date_of_birth, phone_number, address, grade_level, gpa) 
                                VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                        await cursor.execute(sql, (first_name, gender, dob_str, phone, address, grade_level, gpa))
                        inserted_count += 1
                        
                        # 报告进度
                        if (i + 1) % report_frequency == 0 or i == count - 1:
                            progress = (i + 1) / count * 100
                            yield {
                                "type": "progress",
                                "progress": f"{progress:.1f}%",
                                "inserted_count": inserted_count,
                                "total": count,
                                "current": i + 1,
                                "completed": i == count - 1,
                                "timestamp": time.time()
                            }
                    except Exception as e:
                        logger.error(f"插入样本数据失败: {str(e)}")
                        yield {
                            "type": "error",
                            "error": f"插入第{i+1}条数据时失败: {str(e)}",
                            "inserted_count": inserted_count,
                            "total": count,
                            "current": i + 1,
                            "completed": True,
                            "timestamp": time.time()
                        }
                
                await conn.commit()
                
                yield {
                    "type": "complete",
                    "success": True,
                    "inserted_count": inserted_count,
                    "message": f"成功插入{inserted_count}条示例数据",
                    "completed": True,
                    "timestamp": time.time()
                }
    except Exception as e:
        logger.error(f"插入示例数据失败: {str(e)}")
        yield {
            "type": "error", 
            "error": f"插入示例数据失败: {str(e)}", 
            "completed": True,
            "timestamp": time.time()
        }


@mcp.resource("sql://health")
async def health_check():
    """服务健康检查"""
    try:
        # 测试数据库连接
        db_status = False
        if db_pool:
            try:
                async with db_pool.acquire() as conn:
                    async with conn.cursor() as cursor:
                        await cursor.execute("SELECT 1")
                        db_status = True
            except:
                db_status = False
        else:
            # 尝试初始化连接池
            db_status = await init_db_pool()
        
        return {
            "status": "ok" if db_status else "error",
            "services": {
                "database": "ok" if db_status else "error"
            },
            "timestamp": time.time(),
            "service": "SakuraText2SqlService",
            "version": "1.9.0",  # 更新版本号
            "database": DB_CONFIG["database"],
            "table": DB_CONFIG["table_name"],
            "features": ["Streaming", "SSE"]  # 添加SSE特性
        }
    except Exception as e:
        logger.error(f"健康检查失败: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "timestamp": time.time()
        }


# 清理资源函数
async def cleanup():
    """清理资源"""
    global db_pool
    if db_pool:
        db_pool.close()
        await db_pool.wait_closed()
        logger.info("数据库连接池已关闭")


# 初始化服务器
async def init_server():
    """初始化服务器"""
    # 初始化数据库连接池
    await init_db_pool()
    logger.info("Text2SQL MCP服务初始化完成 (支持SSE模式)")


# 服务器启动入口点
if __name__ == "__main__":
    # 注册事件
    mcp.on_start(init_server)
    mcp.on_shutdown(cleanup)
    
    # 启动服务器
    mcp.run()
