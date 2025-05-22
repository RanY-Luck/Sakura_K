import os
import shutil
import plotly.io as pio
from chromadb import EmbeddingFunction, Documents, Embeddings
from rewrite_ask import ask
from siliconflow_api import SiliconflowEmbedding
from custom_chat import CustomChat
from vanna.chromadb import ChromaDB_VectorStore
from dotenv import load_dotenv

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
            "VECTOR_DB_PATH",
            "../storage/chromadb"
        )
        EmbeddingClass = config["EmbeddingClass"] if "EmbeddingClass" in config else SiliconflowEmbedding
        ChatClass = config["ChatClass"] if "ChatClass" in config else CustomChat
        host = config["host"] if "host" in config else os.getenv("DB_HOST")
        dbname = config["db_name"] if "db_name" in config else os.getenv("DB_NAME")
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
        vn.connect_to_mysql(host=host, dbname=dbname, user=user, password=password, port=port)

        # 复制图表 HTML 文件
        self._copy_fig_html()

        return vn

    def _copy_fig_html(self):
        """
        复制图表 HTML 文件到输出目录，用于在浏览器中显示可视化结果
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

    def vn_train(self, question="", sql="", documentation="", ddl=""):
        """
        使用不同类型的输入训练 Vanna 模型

        Args:
            question: 示例问题文本
            sql: 对应的 SQL 查询或独立 SQL 查询
            documentation: 业务术语或定义的文档
            ddl: 数据定义语言语句（如 CREATE TABLE）
        """
        if question and sql:
            # 训练问答对，帮助模型理解如何将问题转换为 SQL
            self.vn.train(
                question=question,
                sql=sql
            )
        elif sql:
            # 单独添加 SQL 查询到训练数据中，有助于模型了解可能的查询模式
            self.vn.train(sql=sql)

        if documentation:
            # 添加业务术语或定义文档，帮助模型理解领域特定的概念
            self.vn.train(documentation=documentation)

        if ddl:
            # 添加数据定义语言语句，帮助模型理解表结构
            self.vn.train(ddl=ddl)

    def get_training_data(self):
        """
        获取当前训练数据

        Returns:
            当前训练数据的列表
        """
        training_data = self.vn.get_training_data()
        # print(training_data)
        return training_data

    def ask(self, question, visualize=True, auto_train=True, *args, **kwargs):
        """
        向 Vanna 提问并获取 SQL 结果及可视化

        Args:
            question: 用自然语言表达的问题
            visualize: 是否生成可视化
            auto_train: 是否自动训练成功的查询
            *args, **kwargs: 传递给 ask 函数的额外参数

        Returns:
            sql: 生成的 SQL 查询
            df: 查询结果数据框
            fig: Plotly 可视化图表
        """
        # 下面是生成SQL、运行查询和创建可视化的原始实现
        # sql = self.vn.generate_sql(question=question)
        # print("这里是生成的sql语句： ", sql)
        # df = self.vn.run_sql(sql)
        # print("\n这里是查询的数据： ", df)
        # plotly_code = self.vn.generate_plotly_code(question=question, sql=sql, df_metadata=df)
        # print("\n这里是生成的plotly代码： ", plotly_code)
        # figure = self.vn.get_plotly_figure(plotly_code, df=df)
        # # figure.show()
        # sql, df, fig = self.vn.ask(question, visualize=visualize, auto_train=auto_train)

        # 使用自定义 ask 函数处理问题
        sql, df, fig = ask(self.vn, question, visualize=visualize, auto_train=auto_train, *args, **kwargs)
        # fig.show()
        return sql, df, fig


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
    # server.schema_train()
    # 示例查询：按销售量降序排列的类别销售汇总
    server.ask("查询sys_user表中有多少条数据")
