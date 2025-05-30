#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-05-28 18:00:00
# @Author   : 冉勇
# @File     : vanna_text2sql.py
# @Software : PyCharm
# @Desc     : Text2SQL核心实现类
import os
import json
import hashlib
import traceback
from pathlib import Path
from chromadb import EmbeddingFunction, Documents, Embeddings
from plugin.module_text2sql.core.rewrite_ask import ask
from plugin.module_text2sql.core.embedding import SiliconflowEmbedding
from plugin.module_text2sql.core.custom_chat import CustomChat
from vanna.chromadb import ChromaDB_VectorStore
from dotenv import load_dotenv


def load_env_file():
    """
    加载环境变量文件，优先加载.env.dev文件
    如果存在APP_ENV环境变量，则加载对应的环境文件
    """
    # 获取运行环境变量
    app_env = os.environ.get('APP_ENV', 'dev')

    # 确定环境文件路径
    env_files = [
        f".env.{app_env}",  # 优先加载指定环境
        ".env.dev"  # 其次加载开发环境
    ]

    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent.parent.absolute()

    # 尝试加载环境文件
    for env_file in env_files:
        env_path = project_root / env_file
        if env_path.exists():
            print(f"加载环境文件: {env_path}")
            load_dotenv(dotenv_path=str(env_path))
            return

    print("警告: 未找到任何环境文件，使用默认环境变量")


# 加载环境变量
load_env_file()


class CustomEmbeddingFunction(EmbeddingFunction[Documents]):
    """
    自定义嵌入函数类，用于生成可在 chromadb 中使用的嵌入向量。
    该类接收文档文本，并通过指定的嵌入模型生成对应的向量表示。
    """

    def __init__(self, config=None):
        """
        初始化嵌入函数

        Args:
            config: 包含API密钥和模型配置的字典
        """
        # 验证配置中是否包含API密钥
        if config is None or "api_key" not in config:
            raise ValueError("Missing 'api_key' in config")

        self.api_key = config["api_key"]
        # 默认使用 BAAI/bge-m3 模型，可在配置中指定其他模型
        self.model = config.get("model", "BAAI/bge-m3")

        try:
            # 初始化嵌入客户端
            self.client = config["embedding_client"](api_key=self.api_key)
        except Exception as e:
            raise ValueError(f"Error initializing client: {e}")

    def __call__(self, input: Documents) -> Embeddings:
        """
        将文档转换为嵌入向量

        Args:
            input: 要转换为向量的文档列表

        Returns:
            文档的嵌入向量列表
        """
        # 将换行符替换为空格，这有助于提高嵌入质量
        input = [t.replace("\n", " ") for t in input]
        all_embeddings = []
        print(f"Generating embeddings for {len(input)} documents")

        # 逐个文档生成嵌入向量
        for document in input:
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=document
                )
                embedding = response.data[0].embedding
                all_embeddings.append(embedding)
            except Exception as e:
                raise ValueError(f"Error generating embedding for document: {e}")

        return all_embeddings


class VannaServer:
    """
    Vanna 服务器类，封装了 Vanna 文本到 SQL 的核心功能。
    负责初始化 Vanna 实例、连接数据库、训练模型和处理问题。
    """

    def __init__(self, config=None):
        """
        初始化 VannaServer 实例

        Args:
            config: 包含各种配置参数的字典，如供应商、嵌入模型、数据库连接信息等
        """
        # 确保配置存在
        self.config = config or {}
        self.vn = self._initialize_vn()
        # 初始化已训练表的记录
        self.trained_tables = self._load_trained_tables()
        # 初始化已训练文档记录
        self.trained_docs = self._load_trained_docs()
        # 初始化已训练问题-SQL对记录
        self.trained_pairs = self._load_trained_pairs()
        # 初始化schema训练状态
        self.schema_trained = self._load_schema_trained()

    def _initialize_vn(self):
        """
        初始化 Vanna 实例，包括配置模型、向量存储和数据库连接

        Returns:
            初始化好的 Vanna 实例
        """
        config = self.config
        # 从配置或环境变量获取参数
        supplier = config.get("supplier", os.getenv("SUPPLIER", "GITEE"))
        embedding_supplier = config.get("embedding_supplier", os.getenv("TEXT2SQL_EMBEDDING_SUPPLIER", "SiliconFlow"))
        vector_db_path = config.get("vector_db_path", os.getenv("VECTOR_DB_PATH", "vector_db"))

        # 确保向量存储路径是绝对路径
        if not os.path.isabs(vector_db_path):
            vector_db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), vector_db_path)

        # 配置类
        EmbeddingClass = config.get("EmbeddingClass", SiliconflowEmbedding)
        ChatClass = config.get("ChatClass", CustomChat)

        # 数据库配置
        host = config.get("host", os.getenv("DB_HOST1"))
        dbname = config.get("dbname", os.getenv("DB_NAME1"))
        user = config.get("user", os.getenv("DB_USER1"))
        password = config.get("password", os.getenv("DB_PASSWORD1"))
        port = config.get("port", int(os.getenv("DB_PORT1", "3306")))

        # 创建向量数据库存储目录
        os.makedirs(vector_db_path, exist_ok=True)

        # 获取API密钥和模型名称
        api_key = os.getenv(f"{supplier}_API_KEY")
        chat_model = os.getenv(f"{supplier}_CHAT_MODEL", "gpt-3.5-turbo")
        api_base = os.getenv(f"{supplier}_API_BASE")

        # 打印关键配置信息，便于调试
        print(f"当前使用的LLM供应商: {supplier}")
        print(f"当前使用的模型: {chat_model}")
        print(f"API基础URL: {api_base}")
        print(f"API密钥是否存在: {'是' if api_key else '否'}")

        # 配置嵌入功能
        embedding_api_key = os.getenv(f"{embedding_supplier}_EMBEDDING_API_KEY")
        embedding_model = os.getenv(f"{embedding_supplier}_EMBEDDING_MODEL", "BAAI/bge-m3")

        print(f"当前使用的嵌入供应商: {embedding_supplier}")
        print(f"当前使用的嵌入模型: {embedding_model}")
        print(f"嵌入API密钥是否存在: {'是' if embedding_api_key else '否'}")

        embedding_config = {
            "api_key": embedding_api_key,
            "model": embedding_model,
            "embedding_client": EmbeddingClass
        }

        # 配置 Vanna 实例
        vanna_config = {
            "api_key": api_key,
            "model": chat_model,
            "api_base": api_base,
            "path": vector_db_path,
            "embedding_function": CustomEmbeddingFunction(embedding_config)
        }

        # 创建自定义 Vanna 类并实例化
        MyVanna = make_vanna_class(ChatClass=ChatClass)
        vn = MyVanna(vanna_config)

        # 连接到 MySQL 数据库
        if all([host, dbname, user, password]):
            vn.connect_to_mysql(host=host, dbname=dbname, user=user, password=password, port=port)
        else:
            print("警告: 数据库连接信息不完整，请检查环境变量或配置")

        return vn

    def _load_trained_tables(self):
        """
        加载已训练表记录

        Returns:
            已训练表的记录字典
        """
        trained_tables_path = self._get_trained_tables_path()
        if os.path.exists(trained_tables_path):
            try:
                with open(trained_tables_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载已训练表记录失败: {e}")
                return {}
        return {}

    def _load_trained_docs(self):
        """
        加载已训练文档记录

        Returns:
            已训练文档的记录字典
        """
        trained_docs_path = self._get_trained_docs_path()
        if os.path.exists(trained_docs_path):
            try:
                with open(trained_docs_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载已训练文档记录失败: {e}")
                return {}
        return {}

    def _load_trained_pairs(self):
        """
        加载已训练问题-SQL对记录
        
        Returns:
            已训练问题-SQL对的记录字典
        """
        trained_pairs_path = self._get_trained_pairs_path()
        if os.path.exists(trained_pairs_path):
            try:
                with open(trained_pairs_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载已训练问题-SQL对记录失败: {e}")
                return {}
        return {}

    def _load_schema_trained(self):
        """
        加载schema训练状态
        
        Returns:
            schema是否已训练的状态信息字典
        """
        schema_trained_path = self._get_schema_trained_path()
        if os.path.exists(schema_trained_path):
            try:
                with open(schema_trained_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"加载schema训练状态失败: {e}")
                return {}
        return {}

    def _save_trained_tables(self):
        """保存已训练表记录到文件"""
        trained_tables_path = self._get_trained_tables_path()
        try:
            with open(trained_tables_path, 'w', encoding='utf-8') as f:
                json.dump(self.trained_tables, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存已训练表记录失败: {e}")

    def _save_trained_docs(self):
        """保存已训练文档记录到文件"""
        trained_docs_path = self._get_trained_docs_path()
        try:
            with open(trained_docs_path, 'w', encoding='utf-8') as f:
                json.dump(self.trained_docs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存已训练文档记录失败: {e}")

    def _save_trained_pairs(self):
        """保存已训练问题-SQL对记录到文件"""
        trained_pairs_path = self._get_trained_pairs_path()
        try:
            with open(trained_pairs_path, 'w', encoding='utf-8') as f:
                json.dump(self.trained_pairs, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存已训练问题-SQL对记录失败: {e}")

    def _save_schema_trained(self):
        """保存schema训练状态到文件"""
        schema_trained_path = self._get_schema_trained_path()
        try:
            with open(schema_trained_path, 'w', encoding='utf-8') as f:
                json.dump(self.schema_trained, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"保存schema训练状态失败: {e}")

    def _get_trained_tables_path(self):
        """
        获取已训练表记录文件路径

        Returns:
            已训练表记录文件的完整路径
        """
        vector_db_path = self.config.get("vector_db_path")
        if vector_db_path is None:
            vector_db_path = os.getenv("VECTOR_DB_PATH", "vector_db")
            if not os.path.isabs(vector_db_path):
                vector_db_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    vector_db_path
                )
        return os.path.join(vector_db_path, "trained_tables.json")

    def _get_trained_docs_path(self):
        """
        获取已训练文档记录文件路径

        Returns:
            已训练文档记录文件的完整路径
        """
        vector_db_path = self.config.get("vector_db_path")
        if vector_db_path is None:
            vector_db_path = os.getenv("VECTOR_DB_PATH", "vector_db")
            if not os.path.isabs(vector_db_path):
                vector_db_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    vector_db_path
                )
        return os.path.join(vector_db_path, "trained_docs.json")

    def _get_trained_pairs_path(self):
        """
        获取已训练问题-SQL对记录文件路径

        Returns:
            已训练问题-SQL对记录文件的完整路径
        """
        vector_db_path = self.config.get("vector_db_path")
        if vector_db_path is None:
            vector_db_path = os.getenv("VECTOR_DB_PATH", "vector_db")
            if not os.path.isabs(vector_db_path):
                vector_db_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    vector_db_path
                )
        return os.path.join(vector_db_path, "trained_pairs.json")

    def _get_schema_trained_path(self):
        """
        获取schema训练状态文件路径
        
        Returns:
            schema训练状态文件的完整路径
        """
        vector_db_path = self.config.get("vector_db_path")
        if vector_db_path is None:
            vector_db_path = os.getenv("VECTOR_DB_PATH", "vector_db")
            if not os.path.isabs(vector_db_path):
                vector_db_path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    vector_db_path
                )
        return os.path.join(vector_db_path, "schema_trained.json")

    def _table_hash(self, table_ddl):
        """
        计算表DDL的哈希值，用于确定表是否已训练

        Args:
            table_ddl: 表的DDL语句

        Returns:
            DDL的MD5哈希值
        """
        return hashlib.md5(table_ddl.encode()).hexdigest()

    def _doc_hash(self, documentation):
        """
        计算文档的哈希值，用于确定文档是否已训练

        Args:
            documentation: 文档文本

        Returns:
            文档的MD5哈希值
        """
        return hashlib.md5(documentation.encode()).hexdigest()

    def _pair_hash(self, question, sql):
        """
        计算问题-SQL对的哈希值，用于确定对是否已训练
        
        Args:
            question: 问题文本
            sql: SQL查询
            
        Returns:
            问题-SQL对的MD5哈希值
        """
        # 结合问题和SQL计算哈希值
        pair_text = f"{question.strip()}||{sql.strip()}"
        return hashlib.md5(pair_text.encode()).hexdigest()

    def train_table_ddl(self, table_ddl, force_retrain=False):
        """
        训练表DDL，如果之前已训练且未指定强制重新训练，则跳过

        Args:
            table_ddl: 表的DDL语句
            force_retrain: 是否强制重新训练

        Returns:
            训练是否成功的布尔值
        """
        # 计算DDL的哈希值
        ddl_hash = self._table_hash(table_ddl)

        # 如果已经训练过且不需要重新训练，则跳过
        if ddl_hash in self.trained_tables and not force_retrain:
            print(f"表已训练过，跳过训练: {self.trained_tables[ddl_hash]}")
            return True

        try:
            # 向Vanna添加DDL
            self.vn.add_ddl(ddl=table_ddl)

            # 提取表名（简单实现，实际应根据DDL语法进行更精确的解析）
            import re
            table_match = re.search(r'CREATE\s+TABLE\s+[`"]?(\w+)[`"]?', table_ddl, re.IGNORECASE)
            if table_match:
                table_name = table_match.group(1)
            else:
                table_name = "未知表"

            # 记录已训练的表
            self.trained_tables[ddl_hash] = table_name
            self._save_trained_tables()
            print(f"成功训练表: {table_name}")
            return True
        except Exception as e:
            print(f"训练表失败: {str(e)}")
            return False

    def schema_train(self, force_retrain=False):
        """
        训练数据库模式信息
        
        Args:
            force_retrain: 是否强制重新训练
            
        Returns:
            训练是否成功的布尔值
        """
        # 获取当前连接的数据库名称
        try:
            db_name = self.vn.config.get("database", "unknown")
            db_hash = hashlib.md5(db_name.encode()).hexdigest()
            
            # 检查是否已经训练过该数据库架构
            if db_hash in self.schema_trained and not force_retrain:
                last_trained = self.schema_trained[db_hash].get("last_trained", "未知时间")
                print(f"数据库架构已训练过(于 {last_trained}), 跳过训练")
                return True
                
            # 查询数据库信息模式，获取所有表和列的元数据
            df_information_schema = self.vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
            # 创建训练计划，将信息模式分解成 LLM 可以处理的小块
            plan = self.vn.get_training_plan_generic(df_information_schema)
            # 执行训练计划
            self.vn.train(plan=plan)
            
            # 记录训练时间
            import datetime
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.schema_trained[db_hash] = {
                "database": db_name,
                "last_trained": now,
                "tables_count": len(df_information_schema)
            }
            self._save_schema_trained()
            
            print(f"成功训练数据库 '{db_name}' 架构，包含 {len(df_information_schema)} 行模式数据")
            return True
        except Exception as e:
            print(f"训练数据库模式失败: {str(e)}")
            return False

    def get_training_data(self):
        """
        获取训练数据，包括问题-SQL对、文档、DDL等

        Returns:
            包含所有训练数据的字典
        """
        # 获取Vanna实例的配置信息
        config = self.vn.get_config()

        # 初始化结果字典
        result = {
            "training_data": {
                "question_sql": [],
                "ddl": [],
                "documentation": []
            }
        }

        # 获取向量存储中的所有文档
        if hasattr(self.vn, "vector_store") and self.vn.vector_store is not None:
            if hasattr(self.vn.vector_store, "get_all_documents"):
                all_documents = self.vn.vector_store.get_all_documents()

                # 分类文档
                for doc in all_documents:
                    doc_type = doc.get("type")
                    if doc_type == "question_sql":
                        # 问题-SQL对
                        question = doc.get("question", "")
                        sql = doc.get("sql", "")
                        if question and sql:
                            result["training_data"]["question_sql"].append(
                                {
                                    "question": question,
                                    "sql": sql
                                }
                            )
                    elif doc_type == "ddl":
                        # DDL语句
                        ddl = doc.get("ddl", "")
                        if ddl:
                            result["training_data"]["ddl"].append(ddl)
                    elif doc_type == "documentation":
                        # 文档说明
                        documentation = doc.get("documentation", "")
                        if documentation:
                            result["training_data"]["documentation"].append(documentation)

        # 如果配置中包含数据库连接信息，添加到结果中
        db_config = {}
        for key in ["host", "user", "password", "port", "database"]:
            if key in config and config[key]:
                # 密码特殊处理，不直接返回
                if key == "password" and config[key]:
                    db_config[key] = "******"  # 隐藏密码
                else:
                    db_config[key] = config[key]

        # 如果有数据库配置，添加到结果中
        if db_config:
            result["db_config"] = db_config

        return result

    def ask(self, question, auto_train=True, strict_match=False, *args, **kwargs):
        """
        处理自然语言问题，生成SQL并执行

        Args:
            question: 自然语言问题
            auto_train: 是否自动训练成功的查询
            strict_match: 是否使用严格匹配

        Returns:
            SQL查询、结果数据和可视化图表的元组
        """
        try:
            # 调用ask帮助函数处理问题
            return ask(
                vanna_instance=self.vn,
                question=question,
                print_results=False,
                auto_train=auto_train,
                *args,
                **kwargs
            )
        except Exception as e:
            import traceback
            print(f"处理问题时出错: {str(e)}")
            traceback.print_exc()
            return f"-- Error: {str(e)}", None

    def vn_train(self, question="", sql="", documentation="", ddl=""):
        """
        训练Vanna模型

        Args:
            question: 问题文本
            sql: SQL查询
            documentation: 文档说明
            ddl: DDL语句

        Returns:
            训练是否成功的布尔值
        """
        try:
            # 如果提供了问题和SQL，添加问题-SQL对
            if question and sql:
                # 计算问题-SQL对的哈希值
                pair_hash = self._pair_hash(question, sql)
                
                # 检查是否已经训练过该问题-SQL对
                if pair_hash not in self.trained_pairs:
                    self.vn.add_question_sql(question=question, sql=sql)
                    self.trained_pairs[pair_hash] = {
                        "question": question[:50] + ("..." if len(question) > 50 else ""),
                        "sql": sql[:50] + ("..." if len(sql) > 50 else "")
                    }
                    self._save_trained_pairs()
                    print(f"成功添加问题-SQL对: {question}")
                else:
                    print(f"问题-SQL对已存在，跳过训练: {self.trained_pairs[pair_hash]['question']}")

            # 如果提供了文档，添加文档
            if documentation:
                doc_hash = self._doc_hash(documentation)
                if doc_hash not in self.trained_docs:
                    self.vn.add_documentation(documentation=documentation)
                    self.trained_docs[doc_hash] = documentation[:50] + "..."  # 保存文档前50个字符作为标识
                    self._save_trained_docs()
                    print(f"成功添加文档: {self.trained_docs[doc_hash]}")
                else:
                    print(f"文档已存在，跳过训练: {self.trained_docs[doc_hash]}")

            # 如果提供了DDL，训练表
            if ddl:
                self.train_table_ddl(ddl)

            return True
        except Exception as e:
            print(f"训练失败: {str(e)}")
            return False

    def check_vector_store(self):
        """
        检查向量存储是否已初始化

        Returns:
            向量存储初始化状态的布尔值
        """
        try:
            if not hasattr(self.vn, "vector_store") or self.vn.vector_store is None:
                print("警告: 向量存储未初始化")
                return False

            # 尝试获取所有文档，验证向量存储是否正常工作
            docs = self.vn.vector_store.get_all_documents()
            print(f"向量存储已正确初始化，包含 {len(docs)} 条记录")

            # 显示各类型文档的数量
            type_counts = {}
            for doc in docs:
                doc_type = doc.get("type", "unknown")
                type_counts[doc_type] = type_counts.get(doc_type, 0) + 1

            for doc_type, count in type_counts.items():
                print(f"  - {doc_type}: {count} 条记录")

            return True
        except Exception as e:
            print(f"检查向量存储时出错: {str(e)}")
            return False

    def bulk_train_tables(self, table_ddls, force_retrain=False):
        """
        批量训练表DDL
        
        Args:
            table_ddls: 表DDL列表
            force_retrain: 是否强制重新训练
            
        Returns:
            (成功训练的表数量, 跳过的表数量)
        """
        if not table_ddls:
            print("没有提供表DDL进行训练")
            return 0, 0
            
        # 统计训练结果
        trained_count = 0
        skipped_count = 0
        
        # 批量处理表DDL
        for table_ddl in table_ddls:
            if self.train_table_ddl(table_ddl, force_retrain):
                trained_count += 1
            else:
                skipped_count += 1
                
        print(f"批量训练完成: 成功训练 {trained_count} 个表, 跳过 {skipped_count} 个表")
        return trained_count, skipped_count
        
    def bulk_train_pairs(self, question_sql_pairs, force_retrain=False):
        """
        批量训练问题-SQL对
        
        Args:
            question_sql_pairs: 包含问题和SQL的字典列表，每个字典需要有'question'和'sql'键
            force_retrain: 是否强制重新训练
            
        Returns:
            (成功训练的对数量, 跳过的对数量)
        """
        if not question_sql_pairs:
            print("没有提供问题-SQL对进行训练")
            return 0, 0
            
        # 统计训练结果
        trained_count = 0
        skipped_count = 0
        
        # 批量处理问题-SQL对
        for pair in question_sql_pairs:
            question = pair.get('question', '')
            sql = pair.get('sql', '')
            
            if not question or not sql:
                print("跳过无效的问题-SQL对")
                skipped_count += 1
                continue
                
            # 计算问题-SQL对的哈希值
            pair_hash = self._pair_hash(question, sql)
            
            # 检查是否需要训练
            if pair_hash not in self.trained_pairs or force_retrain:
                try:
                    self.vn.add_question_sql(question=question, sql=sql)
                    self.trained_pairs[pair_hash] = {
                        "question": question[:50] + ("..." if len(question) > 50 else ""),
                        "sql": sql[:50] + ("..." if len(sql) > 50 else "")
                    }
                    trained_count += 1
                except Exception as e:
                    print(f"训练问题-SQL对失败: {e}")
                    skipped_count += 1
            else:
                print(f"问题已存在，跳过: {question[:50]}...")
                skipped_count += 1
                
        # 保存训练记录
        if trained_count > 0:
            self._save_trained_pairs()
            
        print(f"批量训练完成: 成功训练 {trained_count} 个问题-SQL对, 跳过 {skipped_count} 个")
        return trained_count, skipped_count
        
    def bulk_train_docs(self, docs, force_retrain=False):
        """
        批量训练文档
        
        Args:
            docs: 文档文本列表
            force_retrain: 是否强制重新训练
            
        Returns:
            (成功训练的文档数量, 跳过的文档数量)
        """
        if not docs:
            print("没有提供文档进行训练")
            return 0, 0
            
        # 统计训练结果
        trained_count = 0
        skipped_count = 0
        
        # 批量处理文档
        for doc in docs:
            if not doc:
                skipped_count += 1
                continue
                
            doc_hash = self._doc_hash(doc)
            
            # 检查是否需要训练
            if doc_hash not in self.trained_docs or force_retrain:
                try:
                    self.vn.add_documentation(documentation=doc)
                    self.trained_docs[doc_hash] = doc[:50] + "..."
                    trained_count += 1
                except Exception as e:
                    print(f"训练文档失败: {e}")
                    skipped_count += 1
            else:
                print(f"文档已存在，跳过: {self.trained_docs[doc_hash]}")
                skipped_count += 1
                
        # 保存训练记录
        if trained_count > 0:
            self._save_trained_docs()
            
        print(f"批量训练完成: 成功训练 {trained_count} 个文档, 跳过 {skipped_count} 个")
        return trained_count, skipped_count

    def bulk_train_examples(self):
        """
        添加一些预定义的训练示例
        
        Returns:
            训练是否成功的布尔值
        """
        try:
            # 示例问题-SQL对
            example_pairs = [
                {
                    "question": "获取最新的10条预警记录",
                    "sql": "SELECT * FROM warn_info ORDER BY warn_time DESC LIMIT 10;"
                },
                {
                    "question": "统计各种预警类型的数量",
                    "sql": "SELECT warn_type, COUNT(*) as count FROM warn_info GROUP BY warn_type ORDER BY count DESC;"
                },
                {
                    "question": "查找高严重性的预警",
                    "sql": "SELECT * FROM warn_info WHERE warn_level = 'high' ORDER BY warn_time DESC LIMIT 20;"
                }
            ]
            
            # 添加示例文档
            example_docs = [
                "预警表warn_info存储系统中所有的预警信息，包括预警时间(warn_time)、预警类型(warn_type)、预警级别(warn_level)等字段",
                "表split_table_info是拆表数据，查询时需要根据起始时间和结束时间获取表名",
                "系统日志存储在sys_log表中，包含操作时间(operation_time)、操作用户(username)、操作类型(operation_type)等信息"
            ]
            
            # 批量训练问题-SQL对
            pairs_trained, pairs_skipped = self.bulk_train_pairs(example_pairs)
            
            # 批量训练文档
            docs_trained, docs_skipped = self.bulk_train_docs(example_docs)
            
            print(f"批量训练示例完成: 训练了 {pairs_trained} 个问题-SQL对，{docs_trained} 个文档")
            return True
        except Exception as e:
            print(f"批量训练示例失败: {str(e)}")
            return False


def make_vanna_class(ChatClass=CustomChat):
    """
    创建自定义Vanna类

    Args:
        ChatClass: 用于聊天的类

    Returns:
        组合了向量存储和聊天功能的Vanna类
    """

    class MyVanna(ChromaDB_VectorStore, ChatClass):
        """
        自定义Vanna类，结合向量存储和聊天功能
        """

        def __init__(self, config=None):
            """初始化Vanna实例"""
            ChromaDB_VectorStore.__init__(self, config=config)
            ChatClass.__init__(self, config=config)

        def is_sql_valid(self, sql: str) -> bool:
            """
            检查SQL是否有效

            Args:
                sql: 待检查的SQL语句

            Returns:
                SQL是否有效的布尔值
            """
            # 简单验证，可根据需要扩展
            if not sql or len(sql.strip()) < 5:  # 太短的SQL可能无效
                return False
            return True

        def generate_query_explanation(self, sql: str) -> str:
            """
            生成SQL查询的解释

            Args:
                sql: SQL查询

            Returns:
                SQL查询的自然语言解释
            """
            try:
                # 使用大语言模型生成解释
                explanation = self.submit_prompt(
                    prompt=[
                        self.system_message(
                            "你是一个SQL专家，请对下面的SQL查询进行简短清晰的解释，只描述它的功能，不需要逐行分析。"
                        ),
                        self.user_message(f"请解释这个SQL查询的功能: \n\n{sql}")
                    ],
                    max_tokens=150
                )
                return explanation
            except Exception as e:
                return f"无法生成解释: {str(e)}"

    return MyVanna


# 使用示例
if __name__ == '__main__':
    try:
        # 创建 VannaServer 实例，使用环境变量配置
        config = {}
        # 如果需要指定供应商，可以通过配置或环境变量设置
        supplier = "GITEE"
        if supplier:
            config["supplier"] = supplier

        print(f"初始化 VannaServer，使用配置: {config}")
        server = VannaServer(config)

        # 清理旧数据选项（默认不执行）
        clear_old_data = False
        if clear_old_data:
            print("清理向量库中的旧数据...")
            try:
                # 获取所有集合
                collections = server.vn.collection.list_collections()
                for collection in collections:
                    # 删除集合
                    print(f"删除集合: {collection.name}")
                    server.vn.collection.delete_collection(name=collection.name)
                print("已清理所有旧数据")
            except Exception as e:
                print(f"清理旧数据时出错: {e}")

        # 读取导出的SQL文件
        with open('bms.sql', 'r', encoding='utf-8') as f:
            sql_content = f.read()

        # 将SQL内容按表划分
        import re

        # 使用更精确的正则表达式提取完整的表定义
        table_patterns = re.findall(r'(DROP TABLE IF EXISTS\s+`[^`]+`\s*;[\s\S]*?CREATE TABLE[\s\S]*?;)', sql_content)

        print(f"提取到{len(table_patterns)}个表定义")

        # 使用批量训练接口训练表结构
        trained_count, skipped_count = server.bulk_train_tables(table_patterns)
        print(f"表结构训练完成: 训练了 {trained_count} 个表，跳过了 {skipped_count} 个表")

        # 验证训练数据存储情况
        try:
            print("获取训练数据...")
            training_data = server.get_training_data()

            if isinstance(training_data, dict) and "training_data" in training_data:
                print(f"DDL数量: {len(training_data['training_data']['ddl'])}")
                print(f"文档数量: {len(training_data['training_data']['documentation'])}")
                print(f"问题-SQL对数量: {len(training_data['training_data']['question_sql'])}")
            else:
                print(f"训练数据类型: {type(training_data)}")
        except Exception as e:
            print(f"获取训练数据时出错: {e}")
            print(traceback.format_exc())

        # 添加批量训练示例
        add_training_examples = True
        if add_training_examples:
            try:
                print("\n开始添加批量训练示例...")
                server.bulk_train_examples()
                print("批量训练示例添加完成")
            except Exception as e:
                print(f"添加批量训练示例出错: {e}")
                print(traceback.format_exc())
                
        # 执行schema训练，如果之前已训练过则会跳过
        print("开始执行schema训练...")
        server.schema_train(force_retrain=False)
        print("schema训练完成")

        # 检查向量库中的数据
        print("检查向量库中的数据...")
        server.check_vector_store()
        
        # 添加单个文档示例（无需重复添加相同内容）
        server.vn_train(
            documentation="表split_table_info是一些拆表数据，每次查询时间需要来这个根据起始时间和结束时间并查询获取表名"
        )
        
        # 添加单个问题-SQL对示例（无需重复添加相同内容）
        server.vn_train(
            question="查询sys_file_info表的第一条记录",
            sql="SELECT * FROM sys_file_info LIMIT 1;"
        )
        
        # 验证是否可以使用训练好的模型
        test_questions = [
            "sys_file_info表有哪些字段？",
            "file_name字段是什么含义？",
            "查询sys_file_info表的第一条记录"
        ]
        print("\n测试向量库效果...")
        for question in test_questions:
            print(f"\n问题: {question}")
            try:
                sql, df, _ = server.ask(question, visualize=False, strict_match=False)
                print(f"生成的SQL: {sql}")
                if df is not None and not df.empty:
                    print(f"结果前5行:\n{df.head()}")
                else:
                    print("查询结果为空")
            except Exception as e:
                print(f"执行查询出错: {e}")
                
        # 测试一个简单的问题
        try:
            print("\n测试问题: 预警表最新的一条数据")
            sql, df, _ = server.ask(question="预警表最新的一条数据", visualize=False, strict_match=False)
            print(f"生成的SQL: {sql}")
            if df is not None and not df.empty:
                print(f"结果前5行:\n{df.head()}")
            else:
                print("查询结果为空")
        except Exception as e:
            print(f"执行查询出错: {e}")
    except Exception as e:
        print(f"程序执行出错: {e}")
        print(traceback.format_exc())
