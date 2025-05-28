import os
import shutil
import plotly.io as pio
import json
import hashlib
from chromadb import EmbeddingFunction, Documents, Embeddings
from mcp_server.text2sql.rewrite_ask import ask
from mcp_server.text2sql.siliconflow_api import SiliconflowEmbedding
from mcp_server.text2sql.custom_chat import CustomChat
from vanna.chromadb import ChromaDB_VectorStore
from dotenv import load_dotenv
import pandas as pd

# 加载环境变量
load_dotenv()
# 设置显示后端为浏览器
pio.renderers.default = 'browser'


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
                # print(response)
                embedding = response.data[0].embedding
                all_embeddings.append(embedding)
                # print(f"Cost required: {response.usage.total_tokens}")
            except Exception as e:
                raise ValueError(f"Error generating embedding for document: {e}")

        return all_embeddings


class VannaServer:
    """
    Vanna 服务器类，封装了 Vanna 文本到 SQL 的核心功能。
    负责初始化 Vanna 实例、连接数据库、训练模型和处理问题。
    """

    def __init__(self, config):
        """
        初始化 VannaServer 实例

        Args:
            config: 包含各种配置参数的字典，如供应商、嵌入模型、数据库连接信息等
        """
        self.config = config
        self.vn = self._initialize_vn()
        # 初始化已训练表的记录
        self.trained_tables = self._load_trained_tables()
        # 初始化已训练文档记录
        self.trained_docs = self._load_trained_docs()

    def _initialize_vn(self):
        """
        初始化 Vanna 实例，包括配置模型、向量存储和数据库连接

        Returns:
            初始化好的 Vanna 实例
        """
        config = self.config
        # 获取各种配置参数，如果未提供则使用默认值或环境变量
        supplier = config["supplier"]
        embedding_supplier = config["embedding_supplier"] if "embedding_supplier" in config else "SiliconFlow"
        vector_db_path = config["vector_db_path"] if "vector_db_path" in config else os.getenv(
            "VECTOR_DB_PATH"
        )
        EmbeddingClass = config["EmbeddingClass"] if "EmbeddingClass" in config else SiliconflowEmbedding
        ChatClass = config["ChatClass"] if "ChatClass" in config else CustomChat
        host = config["host"] if "host" in config else os.getenv("DB_HOST")
        dbname = config["database"] if "database" in config else (config["db_name"] if "db_name" in config else os.getenv("DB_NAME"))
        user = config["user"] if "user" in config else os.getenv("DB_USER")
        password = config["password"] if "password" in config else os.getenv("DB_PASSWORD")
        port = config["port"] if "port" in config else int(os.getenv("DB_PORT"))

        # 创建向量数据库存储目录
        os.makedirs(vector_db_path, exist_ok=True)

        # 配置嵌入功能
        config = {"api_key": os.getenv(f"{embedding_supplier}_EMBEDDING_API_KEY"),
                  "model": os.getenv(f"{embedding_supplier}_EMBEDDING_MODEL"), "embedding_client": EmbeddingClass}

        # 配置 Vanna 实例
        config = {"api_key": os.getenv(f"{supplier}_API_KEY"), "model": os.getenv(f"{supplier}_CHAT_MODEL"),
                  "api_base": os.getenv(f"{supplier}_API_BASE"),
                  "path": vector_db_path, "embedding_function": CustomEmbeddingFunction(config)}

        # 创建自定义 Vanna 类并实例化
        MyVanna = make_vanna_class(ChatClass=ChatClass)
        vn = MyVanna(config)

        # 连接到 MySQL 数据库
        print(f"连接到MySQL数据库: host={host}, database={dbname}, user={user}, port={port}")
        try:
            # 尝试使用 database 参数
            vn.connect_to_mysql(host=host, database=dbname, user=user, password=password, port=port)
        except TypeError:
            # 如果失败，尝试使用 dbname 参数
            print("使用 database 参数连接失败，尝试使用 dbname 参数")
            vn.connect_to_mysql(host=host, dbname=dbname, user=user, password=password, port=port)

        # 复制图表 HTML 文件
        self._copy_fig_html()

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

    def _save_trained_tables(self):
        """
        保存已训练表记录
        """
        trained_tables_path = self._get_trained_tables_path()
        try:
            os.makedirs(os.path.dirname(trained_tables_path), exist_ok=True)
            with open(trained_tables_path, 'w', encoding='utf-8') as f:
                json.dump(self.trained_tables, f, ensure_ascii=False, indent=2)
            print(f"已保存训练表记录到 {trained_tables_path}")
        except Exception as e:
            print(f"保存训练表记录失败: {e}")

    def _save_trained_docs(self):
        """
        保存已训练文档记录
        """
        trained_docs_path = self._get_trained_docs_path()
        try:
            os.makedirs(os.path.dirname(trained_docs_path), exist_ok=True)
            with open(trained_docs_path, 'w', encoding='utf-8') as f:
                json.dump(self.trained_docs, f, ensure_ascii=False, indent=2)
            print(f"已保存训练文档记录到 {trained_docs_path}")
        except Exception as e:
            print(f"保存训练文档记录失败: {e}")

    def _get_trained_tables_path(self):
        """
        获取已训练表记录文件路径
        
        Returns:
            文件路径
        """
        vector_db_path = self.config.get("vector_db_path", os.getenv("VECTOR_DB_PATH", "./vector_db"))
        return os.path.join(vector_db_path, "trained_tables.json")

    def _get_trained_docs_path(self):
        """
        获取已训练文档记录文件路径
        
        Returns:
            文件路径
        """
        vector_db_path = self.config.get("vector_db_path", os.getenv("VECTOR_DB_PATH", "./vector_db"))
        return os.path.join(vector_db_path, "trained_docs.json")

    def _table_hash(self, table_ddl):
        """
        计算表DDL的哈希值，用于判断表结构是否变化
        
        Args:
            table_ddl: 表DDL语句
            
        Returns:
            哈希字符串
        """
        # 移除可能变化但不影响结构的部分，如AUTO_INCREMENT值
        normalized_ddl = table_ddl.replace("\n", " ").replace("\r", "")
        # 计算哈希值
        return hashlib.md5(normalized_ddl.encode('utf-8')).hexdigest()

    def _doc_hash(self, documentation):
        """
        计算文档的哈希值，用于判断文档内容是否变化
        
        Args:
            documentation: 文档内容
            
        Returns:
            哈希字符串
        """
        # 规范化文档内容（去除额外空格）
        normalized_doc = ' '.join(documentation.split())
        # 计算哈希值
        return hashlib.md5(normalized_doc.encode('utf-8')).hexdigest()

    def train_table_ddl(self, table_ddl, force_retrain=False):
        """
        训练表DDL，会检查表是否已存在，避免重复训练
        
        Args:
            table_ddl: 表DDL语句
            force_retrain: 是否强制重新训练
            
        Returns:
            是否进行了训练
        """
        # 提取表名
        import re
        table_name_match = re.search(r'CREATE TABLE\s+`([^`]+)`', table_ddl)
        if not table_name_match:
            print(f"无法从DDL中提取表名: {table_ddl[:100]}...")
            return False

        table_name = table_name_match.group(1)
        table_hash = self._table_hash(table_ddl)

        # 检查表是否已训练且结构未变化
        if (not force_retrain and
                table_name in self.trained_tables and
                self.trained_tables[table_name].get('hash') == table_hash):
            print(f"表 '{table_name}' 已训练过且结构未变化，跳过训练")
            return False

        # 训练表DDL
        try:
            print(f"训练表: {table_name}")
            # 向训练添加表名标注
            self.vn_train(documentation=f"表 `{table_name}` 的定义")
            # 训练DDL语句
            self.vn_train(ddl=table_ddl)

            # 记录已训练表
            self.trained_tables[table_name] = {
                'hash': table_hash,
                'timestamp': pd.Timestamp.now().isoformat()
            }
            # 每训练10个表保存一次记录
            if len(self.trained_tables) % 10 == 0:
                self._save_trained_tables()

            return True
        except Exception as e:
            import traceback
            print(f"训练表 '{table_name}' 出错: {e}")
            print(traceback.format_exc())
            return False

    def _copy_fig_html(self):
        """
        复制图表 HTML 文件 到输出目录，用于在浏览器中显示可视化结果
        """
        source_path = 'fig.html'
        target_dir = '../output/html'
        target_path = os.path.join(target_dir, 'vanna_fig.html')

        # 检查目标文件是否存在
        if os.path.exists(target_path):
            print(f"Target file {target_path} already exists. Skipping copy.")
            return

        # 确保源文件存在
        if not os.path.exists(source_path):
            print(f"Source file {source_path} does not exist.")
            return

        # 创建目标目录（如果不存在）
        os.makedirs(target_dir, exist_ok=True)

        # 复制文件
        try:
            shutil.copy(source_path, target_path)
            print(f"Successfully copied {source_path} to {target_path}")
        except Exception as e:
            print(f"Failed to copy {source_path} to {target_path}: {e}")

    def schema_train(self):
        """
        从数据库信息模式中提取并训练模型理解数据库结构
        这使 Vanna 能够了解表结构、列名和关系
        """
        # 查询数据库信息模式，获取所有表和列的元数据
        df_information_schema = self.vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")
        # 创建训练计划，将信息模式分解成 LLM 可以处理的小块
        plan = self.vn.get_training_plan_generic(df_information_schema)
        # print(plan)
        # 执行训练计划
        self.vn.train(plan=plan)

    def get_training_data(self):
        """
        获取当前训练数据，并确保其格式适合使用

        Returns:
            当前训练数据的列表或字典
        """
        try:
            training_data = self.vn.get_training_data()
            print(f"原始训练数据类型: {type(training_data)}")

            # 为保存训练数据的问题-SQL对
            formatted_data = []

            # 添加已训练的问题-SQL对到字典中
            if hasattr(self, '_trained_pairs') and self._trained_pairs:
                for pair in self._trained_pairs:
                    formatted_data.append(
                        {
                            'type': 'question',
                            'question': pair['question'],
                            'sql': pair['sql']
                        }
                    )
                print(f"已添加{len(self._trained_pairs)}个自定义训练对")

            # 尝试将原始训练数据转换为标准格式
            if isinstance(training_data, list):
                for item in training_data:
                    if isinstance(item, dict):
                        formatted_data.append(item)
                    else:
                        print(f"跳过不支持的训练数据项: {type(item)}")
            elif isinstance(training_data, pd.DataFrame):
                # 正确处理 DataFrame 类型数据
                if not training_data.empty:
                    # 检查是否有必要的列
                    columns = training_data.columns.tolist()
                    print(f"DataFrame 包含列: {columns}")

                    # 检查是否有 question 和 sql 列
                    if 'question' in columns and 'sql' in columns:
                        for _, row in training_data.iterrows():
                            formatted_data.append(
                                {
                                    'type': 'question',
                                    'question': row['question'],
                                    'sql': row['sql']
                                }
                            )
                        print(f"从 DataFrame 添加了 {len(training_data)} 个训练对")
                    else:
                        print(f"DataFrame 中没有找到 question 和 sql 列")
                        # 尝试转换为适当的格式
                        print(f"DataFrame 内容示例:\n{training_data.head()}")
                else:
                    print("训练数据 DataFrame 为空")
            elif isinstance(training_data, str):
                print("训练数据为字符串格式，无法解析为问题-SQL对")
            else:
                print(f"不支持的训练数据类型: {type(training_data)}")

            print(f"格式化后训练数据数量: {len(formatted_data)}")
            return formatted_data
        except Exception as e:
            import traceback
            print(f"获取训练数据时出错: {e}")
            print(traceback.format_exc())
            return []

    def ask(self, question, visualize=True, auto_train=True, strict_match=False, *args, **kwargs):
        """
        向 Vanna 提问并获取 SQL 结果及可视化

        Args:
            question: 用自然语言表达的问题
            visualize: 是否生成可视化
            auto_train: 是否自动训练成功的查询
            strict_match: 是否严格使用训练数据中的SQL匹配（优先使用完全匹配的问题-SQL对）
            *args, **kwargs: 传递给 ask 函数的额外参数

        Returns:
            sql: 生成的 SQL 查询
            df: 查询结果数据框
            fig: Plotly 可视化图表
        """
        # 如果启用严格匹配模式，尝试从训练数据中找到完全匹配的SQL
        if strict_match:
            try:
                training_data = self.vn.get_training_data()
                print(f"训练数据类型: {type(training_data)}")
                # 检查训练数据格式并处理
                if isinstance(training_data, list):
                    # 如果是列表，尝试遍历列表查找匹配项
                    for item in training_data:
                        if isinstance(item, dict) and 'type' in item and item[
                            'type'] == 'question' and 'question' in item and item[
                            'question'] == question and 'sql' in item:
                            # 找到完全匹配的训练数据
                            sql = item['sql']
                            print("使用严格匹配的训练SQL: ", sql)
                            df = self.vn.run_sql(sql)
                            # 如果需要可视化，则生成图表
                            if visualize:
                                plotly_code = self.vn.generate_plotly_code(question=question, sql=sql, df_metadata=df)
                                fig = self.vn.get_plotly_figure(plotly_code, df=df)
                            else:
                                fig = None
                            print("这里是生成的sql语句： ", sql)
                            print("这里是生成的df： ", df)
                            print("这里是生成的fig： ", fig)
                            return sql, df, fig
                elif isinstance(training_data, dict):
                    # 如果是字典，尝试直接从字典检索
                    if question in training_data and 'sql' in training_data[question]:
                        sql = training_data[question]['sql']
                        print("使用严格匹配的训练SQL: ", sql)
                        df = self.vn.run_sql(sql)

                        if visualize:
                            plotly_code = self.vn.generate_plotly_code(question=question, sql=sql, df_metadata=df)
                            fig = self.vn.get_plotly_figure(plotly_code, df=df)
                        else:
                            fig = None

                        print("这里是生成的sql语句： ", sql)
                        print("这里是生成的df： ", df)
                        print("这里是生成的fig： ", fig)
                        return sql, df, fig
                # 处理 DataFrame 格式的训练数据
                elif hasattr(training_data, 'to_dict') and callable(getattr(training_data, 'to_dict')):
                    print("处理 DataFrame 格式的训练数据")
                    # 遍历 DataFrame 查找匹配项
                    if 'question' in training_data.columns and 'sql' in training_data.columns:
                        matches = training_data[training_data['question'] == question]
                        if not matches.empty:
                            sql = matches.iloc[0]['sql']
                            print("使用严格匹配的训练SQL: ", sql)
                            df = self.vn.run_sql(sql)

                            if visualize:
                                plotly_code = self.vn.generate_plotly_code(question=question, sql=sql, df_metadata=df)
                                fig = self.vn.get_plotly_figure(plotly_code, df=df)
                            else:
                                fig = None
                            print("这里是生成的sql语句： ", sql)
                            print("这里是生成的df： ", df)
                            print("这里是生成的fig： ", fig)
                            return sql, df, fig
                # 检查本地训练对是否有匹配项
                if hasattr(self, '_trained_pairs') and self._trained_pairs:
                    for pair in self._trained_pairs:
                        if pair['question'] == question:
                            sql = pair['sql']
                            print("使用本地存储的训练SQL: ", sql)
                            df = self.vn.run_sql(sql)

                            if visualize:
                                plotly_code = self.vn.generate_plotly_code(question=question, sql=sql, df_metadata=df)
                                fig = self.vn.get_plotly_figure(plotly_code, df=df)
                            else:
                                fig = None
                            print("这里是生成的sql语句： ", sql)
                            print("这里是生成的df： ", df)
                            print("这里是生成的fig： ", fig)
                            return sql, df, fig
                else:
                    # 其他格式的训练数据，打印但不处理
                    print(f"不支持的训练数据格式: {type(training_data)}")

                print("没有找到严格匹配的训练数据，将使用默认生成方式")
            except Exception as e:
                import traceback
                print(f"查找训练数据时出错: {e}")
                print(traceback.format_exc())
                print("将使用默认生成方式")

        # 使用自定义 ask 函数处理问题
        try:
            result = ask(self.vn, question, visualize=visualize, auto_train=auto_train, *args, **kwargs)

            # 检查返回值
            if result is None:
                print("Ask函数返回None，创建默认返回值")
                return f"-- 无法为问题'{question}'生成SQL", pd.DataFrame(), None

            if isinstance(result, tuple) and len(result) == 3:
                sql, df, fig = result
                print("这里是生成的sql语句： ", sql)
                print("这里是生成的df： ", df)
                print("这里是生成的fig： ", fig)
                return sql, df, fig
            else:
                print(f"Ask函数返回了意外的格式: {type(result)}")
                return f"-- 无法为问题'{question}'生成SQL", pd.DataFrame(), None
        except Exception as e:
            import traceback
            print(f"调用ask函数出错: {e}")
            print(traceback.format_exc())
            return f"-- 为问题'{question}'生成SQL时出错: {str(e)}", pd.DataFrame(), None

    def vn_train(self, question="", sql="", documentation="", ddl=""):
        """
        使用不同类型的输入训练 Vanna 模型

        Args:
            question: 示例问题文本
            sql: 对应的 SQL 查询或独立 SQL 查询
            documentation: 业务术语或定义的文档
            ddl: 数据定义语言语句（如 CREATE TABLE）
        """
        # 初始化训练对存储
        if not hasattr(self, '_trained_pairs'):
            self._trained_pairs = []

        if question and sql:
            # 训练问答对，帮助模型理解如何将问题转换为 SQL
            self.vn.train(
                question=question,
                sql=sql
            )
            # 保存问答对到本地记录
            self._trained_pairs.append(
                {
                    'question': question,
                    'sql': sql
                }
            )
            print(f"已添加训练对: 问题='{question}', SQL='{sql}'")
        elif sql:
            # 单独添加 SQL 查询到训练数据中，有助于模型了解可能的查询模式
            self.vn.train(sql=sql)

        if documentation:
            # 计算文档哈希值
            doc_hash = self._doc_hash(documentation)
            # 检查是否已经训练过该文档
            if doc_hash in self.trained_docs:
                print(f"文档已训练过，跳过训练: '{documentation[:50]}...'")
            else:
                # 添加业务术语或定义文档，帮助模型理解领域特定的概念
                print(f"训练新文档: '{documentation[:50]}...'")
                self.vn.train(documentation=documentation)
                # 记录已训练的文档
                self.trained_docs[doc_hash] = {
                    'documentation': documentation[:100] + ("..." if len(documentation) > 100 else ""),
                    'timestamp': pd.Timestamp.now().isoformat()
                }
                # 每训练5个文档保存一次记录
                if len(self.trained_docs) % 5 == 0:
                    self._save_trained_docs()

        if ddl:
            # 添加数据定义语言语句，帮助模型理解表结构
            self.vn.train(ddl=ddl)

    def check_vector_store(self):
        """
        检查向量库中存储的数据情况
        
        Returns:
            向量库中存储的数据统计信息
        """
        try:
            # 获取向量库的所有集合
            collections = self.vn.collection.list_collections()
            print(f"向量库中的集合: {[c.name for c in collections]}")

            # 检查每个集合中的数据量
            stats = {}
            for collection in collections:
                coll = self.vn.collection.get_collection(name=collection.name)
                count = coll.count()
                stats[collection.name] = count
                print(f"集合 '{collection.name}' 中有 {count} 条数据")

                # 获取样本数据
                if count > 0:
                    try:
                        sample = coll.peek(10)
                        print(f"集合 '{collection.name}' 样本: {sample}")
                    except:
                        print(f"无法获取集合 '{collection.name}' 的样本数据")

            return stats
        except Exception as e:
            import traceback
            print(f"检查向量库时出错: {e}")
            print(traceback.format_exc())
            return None

    def bulk_train_examples(self):
        """
        批量添加常见问题示例以增强向量库质量
        """
        # 添加通用SQL查询的例子
        examples = [
            {
                "question": "统计所有表的行数",
                "sql": """
                SELECT 
                    table_name, 
                    table_rows
                FROM 
                    information_schema.tables
                WHERE 
                    table_schema = DATABASE()
                ORDER BY 
                    table_rows DESC;
                """
            },
            {
                "question": "显示表的所有列及其数据类型",
                "sql": """
                SELECT 
                    column_name, 
                    column_type, 
                    is_nullable,
                    column_comment
                FROM 
                    information_schema.columns
                WHERE 
                    table_schema = DATABASE()
                    AND table_name = '{table_name}'
                ORDER BY 
                    ordinal_position;
                """
            },
            {
                "question": "查询某个表最新的10条记录",
                "sql": """
                SELECT 
                    * 
                FROM 
                    {table_name} 
                ORDER BY 
                    id DESC 
                LIMIT 10;
                """
            }
        ]

        print(f"开始批量添加{len(examples)}个训练示例...")

        # 获取数据库中的表列表
        try:
            df_tables = self.vn.run_sql(
                """
                                SELECT 
                                    table_name 
                                FROM 
                                    information_schema.tables 
                                WHERE 
                                    table_schema = DATABASE()
                            """
            )

            tables = df_tables['table_name'].tolist()
            print(f"数据库中有{len(tables)}个表")

            # 为每个表生成特定的SQL训练对
            total_added = 0
            for i, table in enumerate(tables[:5]):  # 只选择前5个表进行示例训练
                print(f"为表'{table}'创建训练示例...")

                # 获取表的详细信息
                df_columns = self.vn.run_sql(
                    f"""
                    SELECT 
                        column_name, 
                        column_type,
                        column_comment
                    FROM 
                        information_schema.columns
                    WHERE 
                        table_schema = DATABASE()
                        AND table_name = '{table}'
                    ORDER BY 
                        ordinal_position;
                """
                )

                # 为每个通用示例创建表特定的训练对
                for example in examples:
                    # 替换表名占位符
                    sql = example["sql"].format(table_name=table)
                    # 创建特定于表的问题
                    question = example["question"].replace("{table_name}", table)

                    # 训练具体的问题-SQL对
                    self.vn_train(question=question, sql=sql)
                    total_added += 1

                # 为该表创建一些字段特定的查询
                if not df_columns.empty:
                    # 选择前3个列作为示例
                    sample_columns = df_columns['column_name'].tolist()[:3]
                    for col in sample_columns:
                        col_comment = df_columns[df_columns['column_name'] == col]['column_comment'].iloc[
                            0] if 'column_comment' in df_columns.columns else ''
                        if pd.notna(col_comment) and col_comment.strip():
                            field_desc = col_comment
                        else:
                            field_desc = col

                        # 创建字段特定的查询
                        question = f"查询{table}表中{field_desc}为特定值的记录"
                        sql = f"SELECT * FROM {table} WHERE {col} = '{{value}}' LIMIT 10;"
                        self.vn_train(question=question, sql=sql)
                        total_added += 1

            print(f"成功添加了{total_added}个训练示例")

        except Exception as e:
            import traceback
            print(f"批量添加训练示例时出错: {e}")
            print(traceback.format_exc())


def make_vanna_class(ChatClass=CustomChat):
    """
    创建自定义 Vanna 类，结合 ChromaDB 向量存储和聊天功能

    Args:
        ChatClass: 用于处理聊天和生成 SQL 的类，默认为 CustomChat

    Returns:
        自定义 Vanna 类
    """

    class MyVanna(ChromaDB_VectorStore, ChatClass):
        """
        结合向量存储和聊天功能的自定义 Vanna 类
        """

        def __init__(self, config=None):
            """
            初始化 MyVanna 实例

            Args:
                config: 配置参数
            """
            # 初始化向量存储和聊天组件
            ChromaDB_VectorStore.__init__(self, config=config)
            ChatClass.__init__(self, config=config)

        def is_sql_valid(self, sql: str) -> bool:
            """
            检查 SQL 是否有效（未实现）

            Args:
                sql: 要检查的 SQL 查询

            Returns:
                始终返回 False（占位函数）
            """
            # 此处可以实现 SQL 验证逻辑
            return False

        def generate_query_explanation(self, sql: str):
            """
            生成 SQL 查询的解释

            Args:
                sql: 要解释的 SQL 查询

            Returns:
                SQL 查询的自然语言解释
            """
            my_prompt = [
                self.system_message("You are a helpful assistant that will explain a SQL query"),
                self.user_message("Explain this SQL query: " + sql),
            ]

            return self.submit_prompt(prompt=my_prompt)

    return MyVanna


# 使用示例
if __name__ == '__main__':
    # 创建 VannaServer 实例，使用 GITEE 作为提供商
    config = {"supplier": "GITEE"}
    server = VannaServer(config)

    # # 清理旧数据选项（默认不执行）
    # clear_old_data = False
    # if clear_old_data:
    #     print("清理向量库中的旧数据...")
    #     try:
    #         # 获取所有集合
    #         collections = server.vn.collection.list_collections()
    #         for collection in collections:
    #             # 删除集合
    #             print(f"删除集合: {collection.name}")
    #             server.vn.collection.delete_collection(name=collection.name)
    #         print("已清理所有旧数据")
    #     except Exception as e:
    #         print(f"清理旧数据时出错: {e}")
    #
    # # 读取导出的SQL文件
    # with open('bms.sql', 'r', encoding='utf-8') as f:
    #     sql_content = f.read()
    #
    # # 将SQL内容按表划分
    # import re
    #
    # # 使用更精确的正则表达式提取完整的表定义
    # table_patterns = re.findall(r'(DROP TABLE IF EXISTS\s+`[^`]+`\s*;[\s\S]*?CREATE TABLE[\s\S]*?;)', sql_content)
    #
    # print(f"提取到{len(table_patterns)}个表定义")
    #
    # # 对每个表结构进行训练，使用新添加的方法检查是否重复
    # total_trained = 0
    # skipped = 0
    # for i, table_ddl in enumerate(table_patterns):
    #     if i < 5:  # 打印前5个表结构示例
    #         print(f"处理第{i + 1}个表结构: {table_ddl[:100]}...")
    #
    #     # 使用新方法进行训练，该方法会检查是否已存在
    #     if server.train_table_ddl(table_ddl):
    #         total_trained += 1
    #     else:
    #         skipped += 1
    #
    # # 保存训练表记录
    # server._save_trained_tables()
    # print(f"总共处理了{len(table_patterns)}个表，训练了{total_trained}个，跳过了{skipped}个")
    #
    # # 验证训练数据存储情况
    # try:
    #     print("获取训练数据...")
    #     training_data = server.get_training_data()
    #
    #     if isinstance(training_data, list):
    #         print(f"训练后数据项数量: {len(training_data)}")
    #
    #         if training_data:
    #             print(f"训练数据第一项: {training_data[0]}")
    #     else:
    #         print(f"训练数据类型: {type(training_data)}")
    #
    #     # 检查本地存储的训练对
    #     if hasattr(server, '_trained_pairs') and server._trained_pairs:
    #         print(f"本地存储的训练对: {len(server._trained_pairs)}")
    #         print(f"示例: {server._trained_pairs[0] if server._trained_pairs else '无'}")
    # except Exception as e:
    #     print(f"获取训练数据时出错: {e}")
    #     import traceback
    #
    #     print(traceback.format_exc())
    #
    # # 添加批量训练示例（可选，默认不执行）
    # add_training_examples = True
    # if add_training_examples:
    #     try:
    #         print("\n开始添加批量训练示例...")
    #         server.bulk_train_examples()
    #         print("批量训练示例添加完成")
    #     except Exception as e:
    #         print(f"添加批量训练示例出错: {e}")
    #         import traceback
    #
    #         print(traceback.format_exc())
    #
    # # 最后执行schema训练
    # print("开始执行schema训练...")
    # server.schema_train()
    # print("schema训练完成")
    #
    # # 检查向量库中的数据
    # print("检查向量库中的数据...")
    # server.check_vector_store()
    # server.vn_train(
    #     documentation="表split_table_info是一些拆表数据，每次查询时间需要来这个根据起始时间和结束时间并查询获取表名"
    # )
    #
    # # 保存一个简单的示例SQL作为测试
    # server.vn_train(
    #     question="查询sys_file_info表的第一条记录",
    #     sql="SELECT * FROM sys_file_info LIMIT 1;"
    # )
    #
    # # 验证是否可以使用训练好的模型
    # test_questions = [
    #     "sys_file_info表有哪些字段？",
    #     "file_name字段是什么含义？",
    #     "查询sys_file_info表的第一条记录",
    #     # "帮我查询设备号：BDA1220513100042的在上报类型描述数据,时间段为：2025-05-23 16:35:38,在表：packet_info_2025_11 中"
    # ]
    #
    # print("\n测试向量库效果...")
    # for question in test_questions:
    #     print(f"\n问题: {question}")
    #     try:
    #         sql, df, _ = server.ask(question, visualize=False, strict_match=False)
    #         print(f"生成的SQL: {sql}")
    #         if not df.empty:
    #             print(f"结果前5行:\n{df.head()}")
    #     except Exception as e:
    #         print(f"执行查询出错: {e}")

    server.ask(question="预警表最新的一条数据", visualize=False, strict_match=False)
