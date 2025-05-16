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
import re
from typing import Dict, Any, List, AsyncGenerator, Tuple, Optional
from mcp.server.fastmcp import FastMCP
from utils.log_util import logger
from dotenv import load_dotenv

# 获取当前环境，默认为 'dev'
ENV = os.getenv("ENV", "dev")

# 根据环境加载对应的环境变量文件
env_file = f".env.{ENV}"
print(f"Loading environment from {env_file}")
load_dotenv(env_file)

# 初始化 MCP 服务器
mcp = FastMCP("SakuraText2SqlService")



# 数据库连接配置
DB_CONFIG = {
    "host": os.getenv("MYSQL_HOST"),
    "user": os.getenv("MYSQL_USER"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "database": os.getenv("MYSQL_DATABASE")
}

# 数据库连接池
db_pool = None
# 数据库元数据缓存
db_metadata = {
    "tables": {},
    "last_updated": 0
}


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
        
        # 创建数据库
        await ensure_database()
        # 初始化加载元数据
        await load_database_metadata()
        logger.info("数据库连接池初始化成功")
        return True
    except Exception as e:
        logger.error(f"数据库连接池初始化失败: {str(e)}")
        return False


async def ensure_database():
    """确保数据库存在"""
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
    finally:
        conn.close()


# ======================== 查询分析器与SQL生成的新流水线组件 ========================

class MetadataManager:
    """数据库元数据管理器"""
    @staticmethod
    async def load_metadata() -> Dict[str, Any]:
        """加载数据库元数据"""
        global db_metadata
        
        # 如果元数据已经加载且不超过10分钟，直接返回缓存
        if db_metadata["last_updated"] > 0 and time.time() - db_metadata["last_updated"] < 600:
            return db_metadata
            
        try:
            if not db_pool:
                await init_db_pool()
                
            tables = {}
            async with db_pool.acquire() as conn:
                async with conn.cursor() as cursor:
                    # 获取所有表
                    await cursor.execute("SHOW TABLES")
                    all_tables = await cursor.fetchall()
                    
                    for table_row in all_tables:
                        table_name = table_row[0]
                        table_info = {
                            "name": table_name,
                            "columns": [],
                            "column_types": {},
                            "primary_key": None,
                            "row_count": 0,
                            "fields_zh": {}  # 存储字段的中文名称映射，用于后续查询分析
                        }
                        
                        # 获取表结构
                        await cursor.execute(f"DESCRIBE {table_name}")
                        columns = await cursor.fetchall()
                        
                        for col in columns:
                            column_name = col[0]
                            column_type = col[1]
                            is_pk = col[3] == "PRI"
                            
                            table_info["columns"].append(column_name)
                            table_info["column_types"][column_name] = {
                                "type": column_type,
                                "nullable": col[2] == "YES",
                                "default": col[4],
                                "extra": col[5]
                            }
                            
                            if is_pk:
                                table_info["primary_key"] = column_name
                        
                        # 获取行数
                        await cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                        count_result = await cursor.fetchone()
                        table_info["row_count"] = count_result[0] if count_result else 0
                        
                        # 获取表注释（可能包含表的中文名称）
                        await cursor.execute(f"""
                            SELECT table_comment 
                            FROM information_schema.tables 
                            WHERE table_schema = '{DB_CONFIG['database']}' 
                            AND table_name = '{table_name}'
                        """)
                        table_comment = await cursor.fetchone()
                        if table_comment and table_comment[0]:
                            table_info["comment"] = table_comment[0]
                        
                        # 获取列注释（可能包含列的中文名称）
                        await cursor.execute(f"""
                            SELECT column_name, column_comment
                            FROM information_schema.columns
                            WHERE table_schema = '{DB_CONFIG['database']}'
                            AND table_name = '{table_name}'
                        """)
                        column_comments = await cursor.fetchall()
                        if column_comments:
                            table_info["column_comments"] = {}
                            for col_name, col_comment in column_comments:
                                if col_comment:
                                    table_info["column_comments"][col_name] = col_comment
                                    # 尝试从注释中提取中文名称
                                    if col_comment and any('\u4e00' <= c <= '\u9fff' for c in col_comment):
                                        # 假设注释的第一个词是字段的中文名
                                        zh_name = col_comment.split()[0] if ' ' in col_comment else col_comment
                                        table_info["fields_zh"][zh_name] = col_name
                        
                        tables[table_name] = table_info
            
            db_metadata = {
                "tables": tables,
                "last_updated": time.time()
            }
            
            # 基于获取的元数据，动态更新字段别名映射
            QueryAnalyzer.update_field_mappings(db_metadata)
            
            logger.info(f"数据库元数据加载成功: {len(tables)}个表")
            return db_metadata
            
        except Exception as e:
            logger.error(f"加载数据库元数据失败: {str(e)}")
            return {"tables": {}, "last_updated": 0, "error": str(e)}
    
    @staticmethod
    def get_table_info(table_name: str) -> Optional[Dict[str, Any]]:
        """获取表的元数据信息"""
        return db_metadata["tables"].get(table_name)
    
    @staticmethod
    def get_column_info(table_name: str, column_name: str) -> Optional[Dict[str, Any]]:
        """获取列的元数据信息"""
        table_info = MetadataManager.get_table_info(table_name)
        if not table_info:
            return None
        return table_info["column_types"].get(column_name)
    
    @staticmethod
    def get_all_tables() -> List[str]:
        """获取所有表名"""
        return list(db_metadata["tables"].keys())
    
    @staticmethod
    def get_table_zh_mappings() -> Dict[str, str]:
        """获取表的中文名称映射"""
        mappings = {}
        for table_name, table_info in db_metadata["tables"].items():
            if "comment" in table_info and table_info["comment"]:
                # 假设注释的第一个词是表的中文名
                zh_name = table_info["comment"].split()[0] if ' ' in table_info["comment"] else table_info["comment"]
                mappings[zh_name] = table_name
        return mappings


class QueryAnalyzer:
    """查询分析器 - 将自然语言查询分解为结构化组件"""
    
    # 关键词映射表 - 将中文关键词映射到SQL组件
    KEYWORDS = {
        # 条件运算符
        "等于": "=",
        "不等于": "!=",
        "大于": ">",
        "小于": "<",
        "大于等于": ">=",
        "小于等于": "<=",
        "包含": "LIKE",
        "不包含": "NOT LIKE",
        "开始于": "LIKE",
        "结束于": "LIKE",
        
        # 逻辑运算符
        "和": "AND",
        "或者": "OR",
        "但是": "AND",
        "不是": "NOT",
        
        # 排序
        "升序": "ASC",
        "降序": "DESC",
        "从小到大": "ASC",
        "从大到小": "DESC",
        "从高到低": "DESC",
        "从低到高": "ASC",
        
        # 函数
        "平均": "AVG",
        "总和": "SUM",
        "数量": "COUNT",
        "最大值": "MAX",
        "最小值": "MIN",
        
        # 其他
        "分组": "GROUP BY",
        "限制": "LIMIT",
        "按": "ORDER BY",
        "排序": "ORDER BY"
    }
    
    # 字段映射表 - 常见字段的中文别名（基础预设，将根据数据库元数据动态扩展）
    FIELD_ALIASES = {
        "学号": "student_id",
        "姓名": "first_name",
        "性别": "gender",
        "生日": "date_of_birth",
        "出生日期": "date_of_birth",
        "电话": "phone_number",
        "联系方式": "phone_number",
        "地址": "address",
        "住址": "address",
        "年级": "grade_level",
        "班级": "grade_level",
        "成绩": "gpa",
        "绩点": "gpa",
        "GPA": "gpa",
        "创建时间": "created_at",
        "更新时间": "updated_at"
    }
    
    # 表名映射表（基础预设，将根据数据库元数据动态扩展）
    TABLE_ALIASES = {
        "学生": "students",
        "学生表": "students",
        "学员": "students"
    }
    
    # 值映射表 - 特定词语到SQL值的映射
    VALUE_ALIASES = {
        "男": "'男'",
        "女": "'女'",
        "男性": "'男'",
        "女性": "'女'"
    }
    
    @classmethod
    def update_field_mappings(cls, metadata: Dict[str, Any]):
        """
        根据数据库元数据更新字段和表名映射
        :param metadata: 数据库元数据
        """
        # 更新表映射
        table_zh_mappings = {}
        for table_name, table_info in metadata["tables"].items():
            if "comment" in table_info and table_info["comment"]:
                # 从表注释中提取可能的中文名称
                comment = table_info["comment"]
                if any('\u4e00' <= c <= '\u9fff' for c in comment):  # 检查是否包含中文
                    # 假设注释的第一个词是表的中文名
                    zh_name = comment.split()[0] if ' ' in comment else comment
                    table_zh_mappings[zh_name] = table_name
                    # 添加带"表"后缀的映射
                    if not zh_name.endswith('表'):
                        table_zh_mappings[f"{zh_name}表"] = table_name
        
        # 更新字段映射
        field_zh_mappings = {}
        for table_name, table_info in metadata["tables"].items():
            if "column_comments" in table_info:
                for col_name, comment in table_info["column_comments"].items():
                    if comment and any('\u4e00' <= c <= '\u9fff' for c in comment):
                        # 从列注释中提取可能的中文名称
                        zh_name = comment.split()[0] if ' ' in comment else comment
                        # 记录格式：tablename.colname，用于处理多表查询
                        field_zh_mappings[zh_name] = f"{table_name}.{col_name}"
                        # 同时记录不带表名的映射，用于简单查询
                        if zh_name not in cls.FIELD_ALIASES:
                            cls.FIELD_ALIASES[zh_name] = col_name
        
        # 合并映射
        cls.TABLE_ALIASES.update(table_zh_mappings)
        logger.info(f"表名映射更新完成：{len(cls.TABLE_ALIASES)}个映射")
        logger.info(f"字段映射更新完成：{len(cls.FIELD_ALIASES)}个映射")
    
    @staticmethod
    def identify_table(query: str) -> Tuple[str, float]:
        """
        识别查询中提到的表名
        :param query: 自然语言查询
        :return: (表名, 置信度)
        """
        # 首先检查是否明确提到了某个表名
        for alias, table_name in QueryAnalyzer.TABLE_ALIASES.items():
            if alias in query:
                return table_name, 0.9  # 高置信度
        
        # 如果没有明确的表名，检查字段是否暗示了某个表
        table_mentions = {}
        for field_alias, field_name in QueryAnalyzer.FIELD_ALIASES.items():
            if field_alias in query:
                # 如果字段名包含表名（如table.column格式）
                if "." in field_name:
                    table = field_name.split(".")[0]
                    table_mentions[table] = table_mentions.get(table, 0) + 1
        
        # 选择提及最多的表
        if table_mentions:
            most_mentioned = max(table_mentions.items(), key=lambda x: x[1])
            return most_mentioned[0], 0.7  # 中等置信度
        
        # 如果没有找到表名，获取所有表并检查哪个表具有查询中提到的字段
        all_tables = list(db_metadata["tables"].keys())
        if all_tables:
            # 默认使用第一个表
            default_table = all_tables[0]
            # 如果只有一个表，直接返回
            if len(all_tables) == 1:
                return default_table, 0.6  # 低等置信度
            # 如果有多个表，尝试找出最匹配的
            field_matches = {}
            for table in all_tables:
                table_info = db_metadata["tables"][table]
                column_count = 0
                for column in table_info["columns"]:
                    if column in query:
                        column_count += 1
                if column_count > 0:
                    field_matches[table] = column_count
            
            if field_matches:
                best_match = max(field_matches.items(), key=lambda x: x[1])
                return best_match[0], 0.65  # 略高的低等置信度
            return default_table, 0.5  # 很低的置信度
        
        # 如果没有任何表，返回一个空字符串
        return "", 0.0
    
    @staticmethod
    def analyze(query: str) -> Dict[str, Any]:
        """
        分析自然语言查询，提取结构化组件
        :param query: 自然语言查询
        :return: 包含查询结构的字典
        """
        # 识别查询中的表
        table_name, table_confidence = QueryAnalyzer.identify_table(query)
        
        # 初始化查询结构
        analysis = {
            "select": ["*"],  # 默认选择所有字段
            "from": table_name,  # 识别出的表名
            "table_confidence": table_confidence,  # 表名识别的置信度
            "where": [],
            "order_by": [],
            "group_by": [],
            "limit": None,
            "aggregations": [],
            "original_query": query,
            "confidence": table_confidence  # 初始置信度设置为表名识别的置信度
        }
        
        # 如果没有找到表名，返回空分析结果
        if not table_name:
            analysis["error"] = "无法识别查询中的表名"
            return analysis
        
        # 检测字段选择
        # 如果查询中包含"统计"、"计数"、"数一数"等词语，默认使用COUNT
        if any(term in query for term in ["统计", "计数", "数一数", "多少个", "多少条"]):
            analysis["select"] = ["COUNT(*)"]
            analysis["aggregations"].append({"type": "COUNT", "field": "*"})
        
        # 检测是否包含特定的聚合函数
        for agg_term, agg_func in [("平均", "AVG"), ("总和", "SUM"), ("数量", "COUNT"), 
                                   ("最大", "MAX"), ("最小", "MIN"), ("最高", "MAX"), ("最低", "MIN")]:
            if agg_term in query:
                # 查找可能的字段
                for field_alias, field_name in QueryAnalyzer.FIELD_ALIASES.items():
                    if field_alias in query and f"{agg_term}{field_alias}" in query:
                        # 处理可能的表前缀
                        if "." in field_name:
                            # 如果field_name是table.column格式，检查table是否是识别出的表
                            field_table, field_col = field_name.split(".")
                            if field_table == table_name:
                                field_name = field_col
                            else:
                                # 如果字段不属于识别的表，跳过
                                continue
                        
                        analysis["select"] = [f"{agg_func}({field_name})"]
                        analysis["aggregations"].append({"type": agg_func, "field": field_name})
                        break
        
        # 如果查询明确提到某些字段，则选择这些字段
        selected_fields = []
        for field_alias, field_name in QueryAnalyzer.FIELD_ALIASES.items():
            # 使用正则表达式确保是完整单词匹配
            if re.search(rf'\b{field_alias}\b', query):
                # 处理可能的表前缀
                if "." in field_name:
                    field_table, field_col = field_name.split(".")
                    if field_table == table_name:
                        field_name = field_col
                    else:
                        # 如果字段不属于识别的表，跳过
                        continue
                
                # 避免将条件中的字段添加到选择列表
                # 简单启发式: 如果字段后面跟着条件操作词，则可能是条件而非选择
                if not any(f"{field_alias}{cond}" in query for cond in ["大于", "小于", "等于"]):
                    # 检查字段是否在表中
                    table_info = db_metadata["tables"].get(table_name, {})
                    if field_name in table_info.get("columns", []):
                        selected_fields.append(field_name)
        
        if selected_fields:
            analysis["select"] = selected_fields
        
        # 检测WHERE条件
        # 处理简单的等值条件
        for field_alias, field_name in QueryAnalyzer.FIELD_ALIASES.items():
            # 处理可能的表前缀
            if "." in field_name:
                field_table, field_col = field_name.split(".")
                if field_table == table_name:
                    field_name = field_col
                else:
                    # 如果字段不属于识别的表，跳过
                    continue
            
            # 检查字段是否在表中
            table_info = db_metadata["tables"].get(table_name, {})
            if field_name not in table_info.get("columns", []):
                continue
            
            # 检查是否包含特定值比较
            for value_alias, sql_value in QueryAnalyzer.VALUE_ALIASES.items():
                if f"{field_alias}{value_alias}" in query or f"{field_alias}是{value_alias}" in query:
                    analysis["where"].append({
                        "field": field_name,
                        "operator": "=",
                        "value": sql_value.strip("'")
                    })
            
            # 处理数值比较
            for cond_alias, operator in [("大于", ">"), ("小于", "<"), ("等于", "="), 
                                        ("大于等于", ">="), ("小于等于", "<=")]:
                if f"{field_alias}{cond_alias}" in query:
                    # 尝试提取数值
                    number_match = re.search(rf'{field_alias}{cond_alias}\s*(\d+(\.\d+)?)', query)
                    if number_match:
                        analysis["where"].append({
                            "field": field_name,
                            "operator": operator,
                            "value": number_match.group(1)
                        })
        
        # 检测ORDER BY
        order_terms = ["排序", "按", "顺序"]
        if any(term in query for term in order_terms):
            direction = "DESC" if any(desc in query for desc in ["降序", "从大到小", "从高到低"]) else "ASC"
            
            # 查找可能的排序字段
            for field_alias, field_name in QueryAnalyzer.FIELD_ALIASES.items():
                if f"按{field_alias}" in query or f"{field_alias}排序" in query:
                    # 处理可能的表前缀
                    if "." in field_name:
                        field_table, field_col = field_name.split(".")
                        if field_table == table_name:
                            field_name = field_col
                        else:
                            # 如果字段不属于识别的表，跳过
                            continue
                    
                    # 检查字段是否在表中
                    table_info = db_metadata["tables"].get(table_name, {})
                    if field_name in table_info.get("columns", []):
                        analysis["order_by"].append({"field": field_name, "direction": direction})
                        break
            
            # 如果没有找到特定字段但有排序关键词，选择第一个主键或ID列
            if not analysis["order_by"] and any(term in query for term in order_terms):
                table_info = db_metadata["tables"].get(table_name, {})
                default_sort_field = table_info.get("primary_key")
                if default_sort_field:
                    analysis["order_by"].append({"field": default_sort_field, "direction": direction})
                else:
                    # 尝试找到名为id的列
                    if "id" in table_info.get("columns", []):
                        analysis["order_by"].append({"field": "id", "direction": direction})
        
        # 检测LIMIT
        limit_match = re.search(r'(?:限制|最多|前)\s*(\d+)\s*(?:条|个|项)', query)
        if limit_match:
            analysis["limit"] = int(limit_match.group(1))
        else:
            # 默认限制为100条记录
            analysis["limit"] = 100
        
        # 如果是简单的统计查询，调整limit为不限制
        if analysis["select"] == ["COUNT(*)"]:
            analysis["limit"] = None
        
        # 调整置信度
        # 越多的结构化元素被识别，置信度越高
        confidence_factors = 0
        if analysis["where"]:
            confidence_factors += len(analysis["where"]) * 0.1
        if analysis["order_by"]:
            confidence_factors += 0.1
        if analysis["select"] != ["*"]:
            confidence_factors += 0.1
        
        # 最终置信度不应超过表名识别置信度+0.25
        analysis["confidence"] = min(analysis["table_confidence"] + confidence_factors, 0.95)
        
        return analysis


class SqlGenerator:
    """SQL生成器 - 基于查询分析生成SQL语句"""
    
    @staticmethod
    def generate(query_analysis: Dict[str, Any]) -> str:
        """
        基于查询分析生成SQL语句
        :param query_analysis: 查询分析结果
        :return: SQL语句
        """
        # 检查是否存在错误
        if "error" in query_analysis:
            return f"-- 分析错误: {query_analysis['error']}\nSELECT 1"
        
        # 检查表名是否存在
        if not query_analysis["from"]:
            return "-- 无法识别表名\nSELECT 1"
        
        # 构建SELECT子句
        select_clause = "SELECT " + ", ".join(query_analysis["select"])
        
        # 构建FROM子句
        from_clause = f"FROM {query_analysis['from']}"
        
        # 构建WHERE子句
        where_clause = ""
        if query_analysis["where"]:
            conditions = []
            for condition in query_analysis["where"]:
                # 处理不同的操作符类型
                if condition["operator"] == "LIKE":
                    # 对LIKE条件进行特殊处理
                    value = f"'%{condition['value']}%'"
                    conditions.append(f"{condition['field']} LIKE {value}")
                else:
                    # 对字符串值添加引号
                    value = condition["value"]
                    if isinstance(value, str) and not value.isdigit() and not value.startswith("'"):
                        value = f"'{value}'"
                    conditions.append(f"{condition['field']} {condition['operator']} {value}")
            
            where_clause = "WHERE " + " AND ".join(conditions)
        
        # 构建GROUP BY子句
        group_by_clause = ""
        if query_analysis["group_by"]:
            group_by_clause = "GROUP BY " + ", ".join(query_analysis["group_by"])
        
        # 构建ORDER BY子句
        order_by_clause = ""
        if query_analysis["order_by"]:
            order_terms = []
            for order in query_analysis["order_by"]:
                order_terms.append(f"{order['field']} {order['direction']}")
            order_by_clause = "ORDER BY " + ", ".join(order_terms)
        
        # 构建LIMIT子句
        limit_clause = ""
        if query_analysis["limit"] is not None:
            limit_clause = f"LIMIT {query_analysis['limit']}"
        
        # 组合所有子句
        sql_parts = [select_clause, from_clause]
        
        if where_clause:
            sql_parts.append(where_clause)
        
        if group_by_clause:
            sql_parts.append(group_by_clause)
        
        if order_by_clause:
            sql_parts.append(order_by_clause)
        
        if limit_clause:
            sql_parts.append(limit_clause)
        
        return " ".join(sql_parts)


class SqlValidator:
    """SQL验证器 - 验证生成的SQL语句的有效性和安全性"""
    
    @staticmethod
    def validate(sql: str, metadata: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        验证SQL语句的有效性和安全性
        :param sql: SQL语句
        :param metadata: 数据库元数据
        :return: (是否有效, 错误消息)
        """
        # 检查SQL是否为错误占位符
        if sql == "SELECT 1":
            return False, "SQL生成失败，无法识别查询内容"
        
        # 检查是否包含危险操作
        dangerous_keywords = ["DROP", "DELETE", "TRUNCATE", "UPDATE", "INSERT", "ALTER", "CREATE"]
        for keyword in dangerous_keywords:
            if re.search(rf'\b{keyword}\b', sql.upper()):
                return False, f"SQL语句包含不允许的操作: {keyword}"
        
        # 解析SQL以验证字段和表名
        try:
            # 简单解析表名
            table_match = re.search(r'FROM\s+(\w+)', sql, re.IGNORECASE)
            if table_match:
                table_name = table_match.group(1)
                if table_name not in metadata["tables"]:
                    return False, f"表名不存在: {table_name}"
                
                # 验证字段名
                table_info = metadata["tables"][table_name]
                
                # 提取SELECT子句中的字段
                select_clause = re.search(r'SELECT\s+(.*?)\s+FROM', sql, re.IGNORECASE)
                if select_clause:
                    fields = select_clause.group(1).strip()
                    
                    # 处理星号
                    if fields == "*":
                        pass  # 星号是有效的
                    elif "COUNT(*)" in fields.upper() or "COUNT(1)" in fields.upper():
                        pass  # COUNT(*) 和 COUNT(1) 是有效的
                    else:
                        # 验证每个字段
                        for field in re.split(r',\s*', fields):
                            # 移除函数包装，例如 MAX(field)
                            field_clean = re.sub(r'\w+\((.*?)\)', r'\1', field).strip()
                            
                            # 跳过特殊情况，例如 COUNT(*)
                            if field_clean == "*" or ".*" in field_clean:
                                continue
                                
                            # 检查字段是否存在
                            if field_clean not in table_info["columns"] and field_clean.lower() != "count(*)":
                                # 检查是否是函数表达式
                                if not re.match(r'^(AVG|SUM|COUNT|MAX|MIN)\([\w\*]+\)$', field, re.IGNORECASE):
                                    return False, f"字段不存在: {field_clean}"
            
            # 如果以上检查没有问题，SQL语句暂时认为是有效的
            return True, None
            
        except Exception as e:
            return False, f"SQL语句解析失败: {str(e)}"


async def load_database_metadata():
    """加载数据库元数据"""
    try:
        logger.info("开始加载数据库元数据")
        metadata = await MetadataManager.load_metadata()
        logger.info(f"元数据加载成功，发现 {len(metadata['tables'])} 个表")
        return metadata
    except Exception as e:
        logger.error(f"元数据加载失败: {str(e)}", exc_info=True)
        return {"tables": {}, "last_updated": 0, "error": str(e)}


async def generate_sql_query(query: str) -> str:
    """
    使用新的Text2SQL流水线生成SQL查询
    :param query: 自然语言查询
    :return: SQL查询语句
    """
    # 1. 加载/更新数据库元数据
    metadata = await MetadataManager.load_metadata()
    
    # 2. 使用查询分析器分析查询
    query_analysis = QueryAnalyzer.analyze(query)
    logger.info(f"查询分析结果: {json.dumps(query_analysis, ensure_ascii=False)}")
    
    # 3. 使用SQL生成器生成SQL语句
    sql = SqlGenerator.generate(query_analysis)
    logger.info(f"生成的SQL: {sql}")
    
    # 4. 验证SQL语句
    is_valid, error_message = SqlValidator.validate(sql, metadata)
    
    if not is_valid:
        logger.error(f"SQL验证失败: {error_message}, 原始查询: {query}")
        # 如果验证失败，回退到简单的SQL生成方式
        sql = fallback_generate_sql_query(query)
        logger.info(f"回退生成的SQL: {sql}")
    
    return sql


def fallback_generate_sql_query(query: str) -> str:
    """
    简单关键词映射的回退SQL生成方法
    :param query: 自然语言查询
    :return: SQL查询语句
    """
    # 获取数据库中的所有表
    all_tables = list(db_metadata["tables"].keys())
    
    # 如果没有表，返回错误SQL
    if not all_tables:
        return "SELECT 1 -- 无法找到任何表"
    
    # 尝试确定使用哪个表
    target_table = ""
    for table in all_tables:
        if table in query.lower():
            target_table = table
            break
    
    # 如果没有找到明确的表名，使用第一个表
    if not target_table and all_tables:
        target_table = all_tables[0]
    
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
    sql = f"SELECT * FROM {target_table}"
    
    # 条件标志
    has_where = False
    
    # 检查表是否存在目标字段
    table_info = db_metadata["tables"].get(target_table, {})
    columns = table_info.get("columns", [])
    
    # 检查是否包含特定条件
    for keyword, sql_part in keywords.items():
        if keyword in query:
            # 提取字段名
            field_match = re.search(r'^(\w+)', sql_part)
            if field_match:
                field_name = field_match.group(1)
                # 检查字段是否存在于表中
                if field_name in columns:
                    # 第一个条件使用WHERE，后续条件使用AND
                    if not has_where:
                        sql += f" WHERE {sql_part}"
                        has_where = True
            # 排序条件
            elif "ORDER BY" in sql_part and "ORDER BY" not in sql:
                # 确定排序字段
                sort_field = None
                
                # 尝试找到表中存在的可排序字段
                candidates = ["id", "created_at", "updated_at"]
                if "姓名" in query and "first_name" in columns:
                    sort_field = "first_name"
                elif ("出生" in query or "生日" in query) and "date_of_birth" in columns:
                    sort_field = "date_of_birth"
                elif "创建" in query and "created_at" in columns:
                    sort_field = "created_at"
                elif "gpa" in columns:
                    sort_field = "gpa"
                else:
                    # 使用第一个可用的候选字段
                    for candidate in candidates:
                        if candidate in columns:
                            sort_field = candidate
                            break
                    # 如果没有找到候选字段，使用主键或第一列
                    if not sort_field:
                        sort_field = table_info.get("primary_key") or columns[0] if columns else "id"
                
                sql += f" ORDER BY {sort_field}"
                # 添加排序方向
                if "DESC" in sql_part or "从高到低" in query:
                    sql += " DESC"
                elif "ASC" in sql_part or "从低到高" in query:
                    sql += " ASC"
            # 限制条件
            elif "LIMIT" in sql_part and "LIMIT" not in sql:
                # 查找数字作为限制数量
                numbers = re.findall(r'\d+', query)
                limit = 10  # 默认限制
                if numbers:
                    limit = numbers[0]
                sql += f" LIMIT {limit}"
    
    # 如果没有检测到条件，返回有限数量的记录
    if sql == f"SELECT * FROM {target_table}" and "所有" not in query:
        sql += " LIMIT 100"  # 默认限制返回数量
        
    return sql


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
        
        # 获取查询分析结果，但排除大型对象以保持响应简洁
        query_analysis = QueryAnalyzer.analyze(query)
        # 移除过大或敏感字段
        if "metadata" in query_analysis:
            del query_analysis["metadata"]
        
        return {
            "sql_query": sql_query,
            "results": all_results,
            "execution_time": f"{execution_time:.2f}秒",
            "row_count": len(all_results),
            "query_analysis": query_analysis,
            "used_table": query_analysis.get("from", "")
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
        
        # 获取查询分析结果
        query_analysis = QueryAnalyzer.analyze(query)
        used_table = query_analysis.get("from", "")
        
        # 先返回SQL查询语句和分析结果
        yield {
            "type": "sql_generated",
            "sql_query": sql_query,
            "used_table": used_table,
            "confidence": query_analysis.get("confidence", 0),
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
            "used_table": used_table,
            "timestamp": time.time()
        }
    except Exception as e:
        error_msg = f"SSE查询执行失败: {str(e)}"
        logger.error(error_msg)
        yield {"type": "error", "error": error_msg, "timestamp": time.time()}


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
async def describe_tables() -> Dict[str, Any]:
    """
    获取数据库中所有表的结构信息
    :return: 所有表的结构信息
    """
    try:
        # 检查数据库连接
        if not db_pool:
            logger.info(f"describe_tables: 数据库连接未初始化，尝试初始化")
            initialized = await init_db_pool()
            if not initialized or not db_pool:
                logger.error(f"describe_tables: 数据库连接初始化失败")
                return {"error": "数据库连接失败，请检查数据库配置和连接"}
        
        # 加载元数据（强制刷新）
        try:
            global db_metadata
            db_metadata["last_updated"] = 0  # 强制刷新
            metadata = await load_database_metadata()
            
            # 检查是否有表
            if not metadata["tables"]:
                logger.warning(f"describe_tables: 数据库中没有找到任何表")
                return {
                    "error": "数据库中没有表，请先创建表",
                    "database": DB_CONFIG["database"],
                    "table_count": 0
                }
                
            # 日志：发现的表
            table_list = list(metadata["tables"].keys())
            logger.info(f"describe_tables: 在数据库中发现表: {table_list}")
        except Exception as e:
            logger.error(f"describe_tables: 加载元数据失败: {str(e)}")
            return {"error": f"加载数据库元数据失败: {str(e)}"}
        
        tables_info = []
        for table_name, table_info in metadata["tables"].items():
            # 获取表的行数
            row_count = table_info.get("row_count", 0)
            
            # 构建表的结构信息
            table_structure = {
                "table_name": table_name,
                "comment": table_info.get("comment", ""),
                "row_count": row_count,
                "columns": []
            }
            
            # 添加列信息
            for column_name in table_info["columns"]:
                column_type = table_info["column_types"].get(column_name, {})
                column_info = {
                    "name": column_name,
                    "type": column_type.get("type", ""),
                    "nullable": column_type.get("nullable", True),
                    "default": column_type.get("default", None),
                    "is_primary": table_info.get("primary_key") == column_name,
                    "comment": table_info.get("column_comments", {}).get(column_name, "")
                }
                table_structure["columns"].append(column_info)
            
            tables_info.append(table_structure)
        
        logger.info(f"describe_tables: 成功获取 {len(tables_info)} 个表的信息")
        
        return {
            "database": DB_CONFIG["database"],
            "table_count": len(tables_info),
            "tables": tables_info
        }
    except Exception as e:
        logger.error(f"describe_tables: 获取表结构失败: {str(e)}", exc_info=True)
        return {"error": f"获取表结构失败: {str(e)}"}


@mcp.tool()
async def describe_table(table_name: str = "") -> Dict[str, Any]:
    """
    获取指定表的结构信息，如果不指定表名则返回第一个表
    :param table_name: 表名，可选
    :return: 表结构信息
    """
    try:
        # 检查数据库连接
        if not db_pool:
            logger.info(f"describe_table: 数据库连接未初始化，尝试初始化")
            initialized = await init_db_pool()
            if not initialized or not db_pool:
                logger.error(f"describe_table: 数据库连接初始化失败")
                return {"error": "数据库连接失败，请检查数据库配置和连接"}
        
        # 日志：开始加载元数据
        logger.info(f"describe_table: 开始加载数据库元数据，请求表名='{table_name}'")
        
        # 加载元数据（强制刷新）
        try:
            global db_metadata
            db_metadata["last_updated"] = 0  # 强制刷新
            metadata = await load_database_metadata()
            
            # 检查是否有表
            if not metadata["tables"]:
                logger.warning(f"describe_table: 数据库中没有找到任何表")
                return {
                    "error": "数据库中没有表，请先创建表",
                    "database": DB_CONFIG["database"],
                    "table_count": 0
                }
                
            # 日志：发现的表
            table_list = list(metadata["tables"].keys())
            logger.info(f"describe_table: 在数据库中发现表: {table_list}")
        except Exception as e:
            logger.error(f"describe_table: 加载元数据失败: {str(e)}")
            return {"error": f"加载数据库元数据失败: {str(e)}"}
        
        # 如果没有指定表名，使用第一个表
        if not table_name:
            table_name = next(iter(metadata["tables"].keys()))
            logger.info(f"describe_table: 未指定表名，默认选择第一个表 '{table_name}'")
        
        # 检查表是否存在
        if table_name not in metadata["tables"]:
            available_tables = list(metadata["tables"].keys())
            logger.warning(f"describe_table: 请求的表 '{table_name}' 不存在，可用表: {available_tables}")
            return {
                "error": f"表 '{table_name}' 不存在",
                "available_tables": available_tables,
                "database": DB_CONFIG["database"]
            }
        
        # 获取表信息
        table_info = metadata["tables"][table_name]
        logger.info(f"describe_table: 成功获取表 '{table_name}' 的元数据")
        
        # 获取表的行数
        row_count = table_info.get("row_count", 0)
        
        # 构建表的结构信息
        table_structure = {
            "table_name": table_name,
            "comment": table_info.get("comment", ""),
            "row_count": row_count,
            "database": DB_CONFIG["database"],
            "columns": []
        }
        
        # 添加列信息
        for column_name in table_info["columns"]:
            column_type = table_info["column_types"].get(column_name, {})
            column_info = {
                "name": column_name,
                "type": column_type.get("type", ""),
                "nullable": column_type.get("nullable", True),
                "default": column_type.get("default", None),
                "is_primary": table_info.get("primary_key") == column_name,
                "comment": table_info.get("column_comments", {}).get(column_name, "")
            }
            table_structure["columns"].append(column_info)
        
        # 如果有足够权限，尝试获取表的前5条记录作为示例
        sample_data = []
        try:
            logger.info(f"describe_table: 尝试获取 '{table_name}' 的样本数据")
            async with db_pool.acquire() as conn:
                async with conn.cursor(aiomysql.DictCursor) as cursor:
                    await cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                    sample_records = await cursor.fetchall()
                    # 转换为可序列化格式
                    for record in sample_records:
                        sample_record = {}
                        for key, value in record.items():
                            if hasattr(value, 'isoformat'):  # 处理日期时间
                                sample_record[key] = value.isoformat()
                            else:
                                sample_record[key] = value
                        sample_data.append(sample_record)
            logger.info(f"describe_table: 成功获取 {len(sample_data)} 条样本数据")
        except Exception as e:
            logger.warning(f"describe_table: 获取表 '{table_name}' 的样本数据失败: {str(e)}")
        
        table_structure["sample_data"] = sample_data
        
        logger.info(f"describe_table: 成功处理表 '{table_name}' 的结构信息，包含 {len(table_structure['columns'])} 列")
        
        return table_structure
    except Exception as e:
        logger.error(f"describe_table: 获取表结构失败: {str(e)}", exc_info=True)
        return {"error": f"获取表结构失败: {str(e)}"}


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
        
        # 获取表的数量
        table_count = 0
        if db_status:
            metadata = db_metadata
            table_count = len(metadata["tables"])
        
        return {
            "status": "ok" if db_status else "error",
            "services": {
                "database": "ok" if db_status else "error"
            },
            "timestamp": time.time(),
            "service": "SakuraText2SqlService",
            "version": "2.0.0",  # 更新版本号
            "database": DB_CONFIG["database"],
            "table_count": table_count,
            "features": ["Streaming", "SSE", "DynamicTableStructure"]  # 添加新特性
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
    # 预加载数据库元数据
    metadata = await load_database_metadata()
    table_count = len(metadata["tables"])
    logger.info(f"Text2SQL MCP服务初始化完成: 发现{table_count}个表, 支持动态表结构")


# 服务器启动入口点
if __name__ == "__main__":
    # 注册事件
    mcp.on_start(init_server)
    mcp.on_shutdown(cleanup)
    
    # 启动服务器
    mcp.run()
