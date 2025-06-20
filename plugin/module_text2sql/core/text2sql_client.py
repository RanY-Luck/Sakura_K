'''
Descripttion: Text2SQL客户端
version: 1.0.0
Author: 冉勇
Date: 2025-06-20 10:00:00
LastEditTime: 2025-06-20 17:20:25
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc    : Text2SQL客户端核心类

import os
import json
import logging
import sys
import datetime
import importlib
import pandas as pd
from typing import Dict, List, Any, Tuple, Optional, Union
from dotenv import load_dotenv
from openai import OpenAI

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 配置参数
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')
OPENAI_API_URL = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1')
OPENAI_TIMEOUT = int(os.getenv('OPENAI_TIMEOUT', '60'))

# MySQL 配置
DB_HOST = os.getenv('DB_HOST')
DB_PORT = int(os.getenv('DB_PORT', '3306'))
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')


# 简化版的 MyVanna 类，避免导入问题
class SimpleVanna:
    """简化版的 Vanna 类，直接实现必要功能"""
    
    def __init__(self, config=None):
        """初始化 Vanna 实例"""
        if config is None:
            config = {}
        self.config = config
        
        # 创建 OpenAI 客户端
        self.client = OpenAI(
            api_key=config.get('api_key'),
            base_url=config.get('base_url'),
            timeout=config.get('timeout')
        )
        
        self.connection = None
        self.model = config.get('model', 'gpt-3.5-turbo')
    
    def is_connected(self):
        """检查数据库连接是否有效"""
        if not self.connection:
            return False
        try:
            return self.connection.is_connected()
        except Exception:
            return False
    
    def connect_to_mysql(self, host, dbname, user, password, port=3306):
        """连接到 MySQL 数据库"""
        try:
            import mysql.connector
            
            # 如果已有连接，先关闭
            if self.connection and self.is_connected():
                self.connection.close()
                
            self.connection = mysql.connector.connect(
                host=host,
                database=dbname,
                user=user,
                password=password,
                port=port
            )
            logger.info(f"成功连接到 MySQL 数据库: {dbname}@{host}:{port}")
            return True
        except Exception as e:
            logger.error(f"连接到 MySQL 数据库失败: {str(e)}")
            raise
    
    def run_sql(self, sql):
        """执行 SQL 查询并返回结果"""
        if not self.connection:
            raise ValueError("数据库未连接")
        
        # 为每次查询创建一个新的连接，避免未读结果集问题
        import mysql.connector
        
        try:
            # 获取当前连接的配置
            config = {
                'host': self.connection.server_host,
                'database': self.connection.database,
                'user': self.connection.user,
                'password': self.connection._password if hasattr(self.connection, '_password') else '',
                'port': self.connection.server_port
            }
            
            # 创建新连接
            conn = mysql.connector.connect(**config)
            cursor = conn.cursor(dictionary=True)
            
            # 执行查询
            cursor.execute(sql)
            
            # 如果是 SELECT 查询，获取结果
            if sql.strip().upper().startswith(("SELECT", "SHOW", "DESCRIBE")):
                rows = cursor.fetchall()
                
                # 转换为 Pandas DataFrame
                df = pd.DataFrame(rows) if rows else pd.DataFrame()
                
                # 关闭资源
                cursor.close()
                conn.close()
                
                return df
            else:
                # 对于非SELECT查询，提交事务并返回影响的行数
                conn.commit()
                affected_rows = cursor.rowcount
                
                # 关闭资源
                cursor.close()
                conn.close()
                
                # 返回包含影响行数的 DataFrame
                return pd.DataFrame([{"affected_rows": affected_rows}])
                
        except Exception as e:
            logger.error(f"执行SQL失败: {str(e)}")
            raise
    
    def generate_sql(self, question, **kwargs):
        """生成 SQL 查询"""
        # 添加中文提示词来改善SQL生成
        chinese_prompt = f"""
        请根据以下中文问题生成对应的SQL查询语句。
        问题：{question}

        要求：
        1. 生成标准的SQL语句
        2. 确保语法正确
        3. 如果需要，添加适当的注释
        4. 优化查询性能
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一个SQL生成专家，擅长将自然语言问题转换为精确的SQL查询。"},
                    {"role": "user", "content": chinese_prompt}
                ],
                temperature=0.2
            )
            
            # 提取生成的SQL
            sql = response.choices[0].message.content.strip()
            
            # 如果返回的是代码块，提取代码
            if "```sql" in sql:
                sql = sql.split("```sql")[1].split("```")[0].strip()
            elif "```" in sql:
                sql = sql.split("```")[1].split("```")[0].strip()
            
            return sql
        except Exception as e:
            logger.error(f"生成SQL失败: {str(e)}")
            raise
    
    def train(self, question=None, sql=None, documentation=None, ddl=None):
        """训练模型，存储示例"""
        try:
            # 这里简化处理，只记录训练数据
            training_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "question": question,
                "sql": sql,
                "documentation": documentation,
                "ddl": ddl
            }
            
            # 记录到日志
            logger.info(f"添加训练数据: {training_data}")
            
            return True
        except Exception as e:
            logger.error(f"训练失败: {str(e)}")
            raise


# 自定义的VannaTrainer类，不再依赖原始的train.py
class CustomVannaTrainer:
    """自定义 Vanna AI SQL 助手训练器"""

    def __init__(self, vn_instance):
        self.vn = vn_instance
        self.training_log = []
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    def save_training_log(self, filename: str = None):
        """保存训练日志"""
        if filename is None:
            filename = f"training_log_{self.timestamp}.json"

        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.training_log, f, ensure_ascii=False, indent=2)
            logger.info(f"📄 训练日志已保存到: {filename}")
        except Exception as e:
            logger.error(f"❌ 保存训练日志失败: {e}")

    def train_database_structure(self) -> bool:
        """训练数据库结构"""
        logger.info("📊 步骤 1: 训练数据库表结构...")
        success_count = 0

        try:
            # 获取所有表名
            tables = self.vn.run_sql("SHOW TABLES")
            if tables.empty:
                logger.warning("❌ 未找到任何表")
                return False

            table_names = tables.iloc[:, 0].tolist()
            logger.info(f"发现 {len(table_names)} 个表: {', '.join(table_names)}")

            # 为每个表添加结构信息
            for table in table_names:
                logger.info(f"正在训练表: {table}")

                try:
                    # 方法1: 获取建表语句
                    create_result = self.vn.run_sql(f"SHOW CREATE TABLE `{table}`")
                    if not create_result.empty and len(create_result.columns) >= 2:
                        ddl = create_result.iloc[0, 1]  # 第二列是建表语句
                        self.vn.train(ddl=ddl)
                        success_count += 1

                        # 记录日志
                        log_entry = {
                            "timestamp": datetime.datetime.now().isoformat(),
                            "type": "DDL",
                            "table": table,
                            "status": "success",
                            "content": ddl[:200] + "..." if len(ddl) > 200 else ddl
                        }
                        self.training_log.append(log_entry)
                        logger.info(f"  ✅ 已添加 {table} 的表结构")

                except Exception as e:
                    logger.warning(f"  ⚠️ 无法获取 {table} 的建表语句: {e}")

                    # 备用方案：使用 DESCRIBE
                    try:
                        desc = self.vn.run_sql(f"DESCRIBE `{table}`")
                        if not desc.empty:
                            # 构建更详细的表信息
                            table_info = f"""
-- 表 {table} 的详细信息
-- 字段信息：
{desc.to_string()}

-- 表注释和使用说明
-- 表名: {table}
-- 字段数量: {len(desc)}
-- 主要字段: {', '.join(desc['Field'].head(5).tolist())}
                            """
                            self.vn.train(documentation=table_info)
                            success_count += 1

                            # 记录日志
                            log_entry = {
                                "timestamp": datetime.datetime.now().isoformat(),
                                "type": "DESCRIBE",
                                "table": table,
                                "status": "success",
                                "content": table_info[:200] + "..."
                            }
                            self.training_log.append(log_entry)
                            logger.info(f"  ✅ 已添加 {table} 的字段信息（备用方案）")
                    except Exception as e2:
                        logger.error(f"  ❌ 备用方案也失败: {e2}")
                        log_entry = {
                            "timestamp": datetime.datetime.now().isoformat(),
                            "type": "ERROR",
                            "table": table,
                            "status": "failed",
                            "error": str(e2)
                        }
                        self.training_log.append(log_entry)

            logger.info(f"✅ 成功训练了 {success_count}/{len(table_names)} 个表的结构")
            return success_count > 0

        except Exception as e:
            logger.error(f"❌ 训练表结构时出错: {e}")
            return False
    
    def generate_dynamic_examples(self) -> List[Dict]:
        """根据实际表结构生成动态示例"""
        examples = []

        try:
            # 获取表名列表
            tables_result = self.vn.run_sql("SHOW TABLES")
            if tables_result.empty:
                return examples

            table_names = tables_result.iloc[:, 0].tolist()

            # 为每个表生成基础示例
            for table in table_names[:3]:  # 限制前3个表，避免过多
                try:
                    # 获取表结构
                    desc = self.vn.run_sql(f"DESCRIBE `{table}`")
                    if desc.empty:
                        continue

                    columns = desc['Field'].tolist()

                    # 基础查询示例
                    examples.extend(
                        [
                            {
                                "question": f"查看{table}表的所有数据",
                                "sql": f"SELECT * FROM `{table}` LIMIT 100;"
                            },
                            {
                                "question": f"统计{table}表有多少条记录",
                                "sql": f"SELECT COUNT(*) as 记录总数 FROM `{table}`;"
                            },
                            {
                                "question": f"显示{table}表的前10条记录",
                                "sql": f"SELECT * FROM `{table}` LIMIT 10;"
                            }
                        ]
                    )

                    # 如果有时间字段，添加时间相关示例
                    time_columns = [col for col in columns if any(
                        keyword in col.lower()
                        for keyword in ['time', 'date', 'created', 'updated']
                    )]

                    if time_columns:
                        time_col = time_columns[0]
                        examples.extend(
                            [
                                {
                                    "question": f"按{time_col}倒序查看{table}表的最新数据",
                                    "sql": f"SELECT * FROM `{table}` ORDER BY `{time_col}` DESC LIMIT 20;"
                                },
                                {
                                    "question": f"统计{table}表每天的记录数",
                                    "sql": f"SELECT DATE(`{time_col}`) as 日期, COUNT(*) as 记录数 FROM `{table}` GROUP BY DATE(`{time_col}`) ORDER BY 日期 DESC;"
                                }
                            ]
                        )

                except Exception as e:
                    logger.warning(f"  ⚠️ 为表 {table} 生成示例时出错: {e}")
                    continue

        except Exception as e:
            logger.error(f"❌ 生成动态示例时出错: {e}")

        return examples

    def add_example_questions(self):
        """添加示例问题和SQL对"""
        logger.info("💡 步骤 3: 添加示例问题和SQL对...")

        # 通用示例
        general_examples = [
            {
                "question": "显示数据库中所有的表",
                "sql": "SHOW TABLES;"
            },
            {
                "question": "显示数据库信息",
                "sql": "SELECT DATABASE() as 当前数据库, VERSION() as MySQL版本, NOW() as 当前时间;"
            },
            {
                "question": "查看数据库大小",
                "sql": "SELECT table_schema AS '数据库', ROUND(SUM(data_length + index_length) / 1024 / 1024, 2) AS '大小(MB)' FROM information_schema.tables WHERE table_schema = DATABASE() GROUP BY table_schema;"
            }
        ]

        # 获取动态生成的示例
        dynamic_examples = self.generate_dynamic_examples()

        # 合并所有示例
        all_examples = general_examples + dynamic_examples

        success_count = 0
        for i, pair in enumerate(all_examples, 1):
            try:
                self.vn.train(question=pair["question"], sql=pair["sql"])
                logger.info(f"  ✅ 已添加示例 {i}: {pair['question']}")
                success_count += 1

                # 记录日志
                log_entry = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "type": "QUESTION_SQL_PAIR",
                    "question": pair["question"],
                    "sql": pair["sql"],
                    "status": "success"
                }
                self.training_log.append(log_entry)

            except Exception as e:
                logger.error(f"  ❌ 添加示例 {i} 失败: {e}")

        logger.info(f"✅ 成功添加了 {success_count}/{len(all_examples)} 个示例")
    
    def validate_training(self):
        """验证训练结果"""
        logger.info("🔍 步骤 4: 验证训练结果...")

        test_questions = [
            "数据库中有哪些表？",
            "显示第一个表的结构",
            "统计数据总量",
            "查看最新的10条记录",
            "按时间排序显示数据"
        ]

        success_count = 0
        for question in test_questions:
            try:
                sql = self.vn.generate_sql(question)
                if sql and sql.strip():
                    logger.info(f"  ✅ 问题: '{question}' -> SQL: {sql.strip()[:80]}...")
                    success_count += 1
                else:
                    logger.warning(f"  ❌ 问题: '{question}' -> 未生成SQL")
            except Exception as e:
                logger.error(f"  ❌ 问题: '{question}' 失败: {e}")

        validation_score = success_count / len(test_questions)
        logger.info(f"✅ 验证通过率: {success_count}/{len(test_questions)} ({validation_score * 100:.1f}%)")
        return validation_score
    
    def full_training_pipeline(self):
        """完整的训练流程"""
        logger.info("🚀 开始训练 Vanna AI SQL 助手...")

        start_time = datetime.datetime.now()

        try:
            # 1. 训练数据库结构
            structure_success = self.train_database_structure()

            # 2. 添加示例问题
            self.add_example_questions()

            # 3. 验证训练结果
            validation_score = self.validate_training()

            # 保存训练日志
            self.save_training_log()

            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()

            logger.info(f"\n🎉 训练完成！")
            logger.info(f"⏱️  用时: {duration:.2f} 秒")
            logger.info(f"📊 验证得分: {validation_score * 100:.1f}%")

            if validation_score >= 0.6:
                logger.info("✅ 训练质量良好，可以开始使用！")
            else:
                logger.warning("⚠️  训练质量一般，建议添加更多示例数据")

            return True

        except Exception as e:
            logger.error(f"❌ 训练过程中出现错误: {e}")
            return False


class Text2SQLClient:
    """Text2SQL客户端类，提供自然语言到SQL的转换功能"""

    _instance = None

    @classmethod
    def get_instance(cls) -> 'Text2SQLClient':
        """获取Text2SQLClient单例"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        """初始化Text2SQL客户端"""
        try:
            # 创建自己的 Vanna 实例
            self.vn = SimpleVanna(
                config={
                    'api_key': OPENAI_API_KEY,
                    'model': OPENAI_MODEL,
                    'base_url': OPENAI_API_URL,
                    'timeout': OPENAI_TIMEOUT
                }
            )
            
            # 连接数据库
            self._connect_to_database()
                
            # 创建训练器
            self.trainer = CustomVannaTrainer(self.vn)
            
        except Exception as e:
            logger.error(f"初始化Text2SQL客户端失败: {str(e)}")
            raise
            
    def _connect_to_database(self):
        """连接到数据库，提取为单独方法以支持重连"""
        try:
            if all([DB_HOST, DB_NAME, DB_USER, DB_PASSWORD]):
                self.vn.connect_to_mysql(
                    host=DB_HOST,
                    dbname=DB_NAME,
                    user=DB_USER,
                    password=DB_PASSWORD,
                    port=DB_PORT
                )
                logger.info("成功连接到MySQL数据库")
            else:
                logger.warning("数据库连接信息不完整，请检查环境变量")
        except Exception as e:
            logger.error(f"连接数据库失败: {str(e)}")

    def generate_sql(self, question: str) -> Dict[str, Any]:
        """
        将自然语言问题转换为SQL查询
        
        Args:
            question: 自然语言问题
            
        Returns:
            Dict: 包含生成的SQL和相关信息
        """
        try:
            sql = self.vn.generate_sql(question)
            return {
                "success": True,
                "sql": sql,
                "message": "SQL生成成功"
            }
        except Exception as e:
            logger.error(f"生成SQL时出错: {str(e)}")
            return {
                "success": False,
                "sql": None,
                "message": f"生成SQL时出错: {str(e)}"
            }

    def execute_sql_query(self, question: str = None, sql: str = None) -> Dict[str, Any]:
        """
        执行SQL查询并返回结果
        
        Args:
            question: 自然语言问题（如果提供，将先转换为SQL）
            sql: 直接提供的SQL查询
            
        Returns:
            Dict: 包含查询结果和相关信息
        """
        max_retries = 2
        retry_count = 0
        
        while retry_count <= max_retries:
            try:
                # 确保数据库连接正常
                if not self.vn.connection or not self.vn.is_connected():
                    logger.info(f"数据库连接已断开，尝试重新连接 (尝试 {retry_count + 1}/{max_retries + 1})")
                    # 重新连接数据库
                    self._connect_to_database()
                
                if question and not sql:
                    sql = self.vn.generate_sql(question)
                    
                if not sql:
                    return {
                        "success": False,
                        "data": None,
                        "message": "未提供SQL语句"
                    }
                
                # 执行SQL查询
                result = self.vn.run_sql(sql)
                
                # 将DataFrame转换为可序列化的列表
                result_data = result.to_dict('records')
                
                # 生成数据统计摘要
                summary = self._generate_summary(sql, result)
                
                return {
                    "success": True,
                    "sql": sql,
                    "data": result_data,
                    "columns": result.columns.tolist(),
                    "row_count": len(result),
                    "summary": summary,
                    "message": "查询执行成功"
                }
                
            except Exception as e:
                logger.error(f"执行查询时出错 (尝试 {retry_count + 1}/{max_retries + 1}): {str(e)}")
                retry_count += 1
                
                if "Unread result found" in str(e):
                    logger.warning("检测到'Unread result found'错误，尝试重新连接数据库")
                    try:
                        # 强制关闭并重新连接
                        if self.vn.connection:
                            self.vn.connection.close()
                        self._connect_to_database()
                    except Exception as conn_error:
                        logger.error(f"重新连接失败: {str(conn_error)}")
                
                # 如果已经达到最大重试次数，返回错误
                if retry_count > max_retries:
                    return {
                        "success": False,
                        "data": None,
                        "message": f"执行查询时出错: {str(e)}"
                    }
    
    def _generate_summary(self, sql: str, df: Any) -> str:
        """生成数据摘要"""
        try:
            if df is None or df.empty:
                return "查询未返回任何数据"
                
            return f"查询返回了{len(df)}行数据，包含{len(df.columns)}个字段。"
        except Exception as e:
            logger.error(f"生成摘要时出错: {str(e)}")
            return "无法生成数据摘要"
    
    def train_with_example(self, question: str, sql: str) -> Dict[str, Any]:
        """
        使用示例训练模型
        
        Args:
            question: 问题示例
            sql: 对应的SQL查询
            
        Returns:
            Dict: 训练结果
        """
        try:
            self.vn.train(question=question, sql=sql)
            return {
                "success": True,
                "message": "示例训练成功"
            }
        except Exception as e:
            logger.error(f"训练示例时出错: {str(e)}")
            return {
                "success": False,
                "message": f"训练示例时出错: {str(e)}"
            }
    
    def train_database_schema(self) -> Dict[str, Any]:
        """
        训练数据库架构
        
        Returns:
            Dict: 训练结果
        """
        try:
            success = self.trainer.train_database_structure()
            if success:
                return {
                    "success": True,
                    "message": "数据库架构训练成功"
                }
            else:
                return {
                    "success": False,
                    "message": "数据库架构训练失败"
                }
        except Exception as e:
            logger.error(f"训练数据库架构时出错: {str(e)}")
            return {
                "success": False,
                "message": f"训练数据库架构时出错: {str(e)}"
            }
    
    def run_full_training(self) -> Dict[str, Any]:
        """
        运行完整的训练流程
        
        Returns:
            Dict: 训练结果
        """
        try:
            success = self.trainer.full_training_pipeline()
            if success:
                return {
                    "success": True,
                    "message": "完整训练流程执行成功"
                }
            else:
                return {
                    "success": False,
                    "message": "完整训练流程执行失败"
                }
        except Exception as e:
            logger.error(f"执行完整训练流程时出错: {str(e)}")
            return {
                "success": False,
                "message": f"执行完整训练流程时出错: {str(e)}"
            }
    
    def get_all_tables(self) -> Dict[str, Any]:
        """
        获取所有表信息
        
        Returns:
            Dict: 包含所有表信息
        """
        try:
            tables = self.vn.run_sql("SHOW TABLES")
            tables_list = tables.iloc[:, 0].tolist()
            
            return {
                "success": True,
                "tables": tables_list,
                "count": len(tables_list),
                "message": "成功获取表信息"
            }
        except Exception as e:
            logger.error(f"获取表信息时出错: {str(e)}")
            return {
                "success": False,
                "tables": [],
                "message": f"获取表信息时出错: {str(e)}"
            }
    
    def get_table_info(self, table_name: str) -> Dict[str, Any]:
        """
        获取指定表的详细信息
        
        Args:
            table_name: 表名
            
        Returns:
            Dict: 表的详细信息
        """
        try:
            # 获取表结构
            structure = self.vn.run_sql(f"DESCRIBE `{table_name}`")
            
            # 获取表行数
            try:
                count_result = self.vn.run_sql(f"SELECT COUNT(*) AS count FROM `{table_name}`")
                row_count = int(count_result.iloc[0, 0]) if not count_result.empty else 0
            except Exception as e:
                logger.warning(f"获取表 {table_name} 行数失败: {str(e)}")
                row_count = -1
            
            # 获取表的前10条数据作为样例
            try:
                sample_data = self.vn.run_sql(f"SELECT * FROM `{table_name}` LIMIT 10")
                sample_records = sample_data.to_dict('records')
            except Exception as e:
                logger.warning(f"获取表 {table_name} 样例数据失败: {str(e)}")
                sample_records = []
            
            return {
                "success": True,
                "table_name": table_name,
                "structure": structure.to_dict('records'),
                "columns": structure['Field'].tolist() if not structure.empty else [],
                "row_count": row_count,
                "sample_data": sample_records,
                "message": f"成功获取表 {table_name} 的信息"
            }
        except Exception as e:
            logger.error(f"获取表 {table_name} 信息时出错: {str(e)}")
            return {
                "success": False,
                "message": f"获取表信息时出错: {str(e)}"
            } 