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
            "VECTOR_DB_PATH"
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
                    formatted_data.append({
                        'type': 'question',
                        'question': pair['question'],
                        'sql': pair['sql']
                    })
                print(f"已添加{len(self._trained_pairs)}个自定义训练对")
            
            # 尝试将原始训练数据转换为标准格式
            if training_data:
                if isinstance(training_data, list):
                    for item in training_data:
                        if isinstance(item, dict):
                            formatted_data.append(item)
                        else:
                            print(f"跳过不支持的训练数据项: {type(item)}")
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
                        if isinstance(item, dict) and 'type' in item and item['type'] == 'question' and 'question' in item and item['question'] == question and 'sql' in item:
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
        sql, df, fig = ask(self.vn, question, visualize=visualize, auto_train=auto_train, *args, **kwargs)
        # fig.show()
        print("这里是生成的sql语句： ", sql)
        print("这里是生成的df： ", df)
        print("这里是生成的fig： ", fig)
        return sql, df, fig

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
            self._trained_pairs.append({
                'question': question,
                'sql': sql
            })
            print(f"已添加训练对: 问题='{question}', SQL='{sql}'")
        elif sql:
            # 单独添加 SQL 查询到训练数据中，有助于模型了解可能的查询模式
            self.vn.train(sql=sql)

        if documentation:
            # 添加业务术语或定义文档，帮助模型理解领域特定的概念
            self.vn.train(documentation=documentation)

        if ddl:
            # 添加数据定义语言语句，帮助模型理解表结构
            self.vn.train(ddl=ddl)


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
    server.vn_train(
        ddl="""CREATE TABLE `alarm` (
  `id` bigint(50) NOT NULL AUTO_INCREMENT,
  `imei` varchar(50) NOT NULL COMMENT 'imei',
  `alarm_status` tinyint(1) DEFAULT NULL COMMENT '报警处理状态（未处理、处理中、已处理）',
  `alarm_result` tinyint(1) DEFAULT NULL COMMENT '处理结果/设备状态（正常、修复、报警、拆除）',
  `charge_man` varchar(512) DEFAULT NULL COMMENT '负责人',
  `charge_phone` varchar(255) DEFAULT NULL COMMENT '电话号码',
  `predict_complete_time` datetime DEFAULT NULL COMMENT '预计完成时间',
  `real_complete_time` datetime DEFAULT NULL COMMENT '完成时间',
  `danger_score` bigint(10) DEFAULT NULL COMMENT '危险评分',
  `duration` int(10) DEFAULT NULL COMMENT '处理耗时（分钟）',
  `fall_index` tinyint(1) DEFAULT NULL COMMENT '跌落报警',
  `swing_index` tinyint(1) DEFAULT NULL COMMENT '摇摆报警',
  `lean_index` decimal(10,5) DEFAULT NULL COMMENT '倾斜度数',
  `alarm_desc` varchar(255) DEFAULT NULL COMMENT '报警细节描述',
  `remark` varchar(512) DEFAULT NULL COMMENT '备注',
  `handle_type` tinyint(2) DEFAULT NULL COMMENT '处理类型',
  `crt_time` datetime DEFAULT NULL COMMENT '创建时间',
  `crt_user` varchar(255) DEFAULT NULL COMMENT '创建人',
  `crt_name` varchar(255) DEFAULT NULL COMMENT '创建人姓名',
  `crt_host` varchar(255) DEFAULT NULL COMMENT '创建主机',
  `upd_time` datetime DEFAULT NULL COMMENT '更新时间',
  `upd_user` varchar(255) DEFAULT NULL COMMENT '更新人',
  `upd_name` varchar(255) DEFAULT NULL COMMENT '更新姓名',
  `upd_host` varchar(255) DEFAULT NULL COMMENT '更新主机',
  `year` varchar(20) DEFAULT NULL COMMENT '冗余字段（年：yyyy）',
  `month` varchar(20) DEFAULT NULL COMMENT '冗余字段（月：yyyy-MM）',
  `day` varchar(255) DEFAULT NULL COMMENT '冗余字段（日：yyyy-MM-dd）',
  `time` varchar(20) DEFAULT NULL COMMENT '冗余字段（时间：yyyy-MM-dd hh:mm）',
  `danger_level` tinyint(1) DEFAULT NULL COMMENT '危险等级(1~29低级1 30~59中级2 60~100高级3 )',
  `alarm_type_number` int(50) DEFAULT NULL COMMENT '报警类型10进制表示',
  `lean_value` varchar(512) DEFAULT NULL COMMENT '倾斜报警值',
  `distance_x_value` varchar(512) DEFAULT NULL COMMENT '三角位移报警值',
  `distance_y_value` varchar(512) DEFAULT NULL COMMENT '三角沉降报警值',
  `gap_value` varchar(512) DEFAULT NULL COMMENT '裂缝报警值',
  `water_value` varchar(512) DEFAULT NULL COMMENT '水位报警值',
  `gradienter_value` varchar(512) DEFAULT NULL COMMENT '水准仪沉降报警值',
  `displacement_value` varchar(512) DEFAULT NULL COMMENT '位移报警值',
  `deep_displacement_value` varchar(512) DEFAULT NULL COMMENT '深度位移报警值',
  `rtk_distance_x_value` varchar(512) DEFAULT NULL COMMENT 'rtk位移报警值',
  `rtk_distance_y_value` varchar(512) DEFAULT NULL COMMENT 'rtk沉降报警值',
  `srx` varchar(512) DEFAULT NULL COMMENT '振动频率',
  `sry` varchar(512) DEFAULT NULL COMMENT '振动幅度mm/s',
  `total_alarm_type_number` int(50) DEFAULT NULL COMMENT '总报警类型',
  `day_alarm_type_number` int(50) DEFAULT NULL COMMENT '日变化报警类型',
  `month_alarm_type_number` int(50) DEFAULT NULL COMMENT '月变化报警类型',
  `total_alarm_desc` varchar(512) DEFAULT NULL COMMENT '总报警描述',
  `day_alarm_desc` varchar(512) DEFAULT NULL COMMENT '日变化报警描述',
  `month_alarm_desc` varchar(512) DEFAULT NULL COMMENT '月变化报警描述',
  `alarm_level` varchar(256) DEFAULT NULL COMMENT '报警等级json',
  `device_alarm_level` tinyint(2) DEFAULT NULL COMMENT '设备报警等级',
  `pre_device_alarm_level` tinyint(2) DEFAULT NULL COMMENT '设备原报警等级',
  `update_level` tinyint(2) DEFAULT '0' COMMENT '报警等级升级数',
  `data_id` char(10) NOT NULL DEFAULT '0000000000' COMMENT '数据标识',
  `day_average_alarm_type_number` int(50) DEFAULT NULL COMMENT '日均报警类型',
  `day_average_alarm_desc` varchar(512) DEFAULT NULL COMMENT '日均报警描述',
  `rebar_stress_meter_value` varchar(512) DEFAULT NULL COMMENT '钢筋应力报警值',
  `rebar_strain_gauge_value` varchar(512) DEFAULT NULL COMMENT '钢筋应变报警值',
  `surface_strain_gauge_value` varchar(512) DEFAULT NULL COMMENT '表面应变报警值',
  `wind_speed_direction_value` varchar(512) DEFAULT NULL COMMENT '风速风向报警值',
  `vibration_value` varchar(20) DEFAULT NULL COMMENT '振动报警值',
  `newest_time` datetime DEFAULT NULL COMMENT '最新预警时间',
  `earth_pressure_meter_value` varchar(512) DEFAULT NULL COMMENT '土压力计报警值',
  `rainfall_value` varchar(512) DEFAULT NULL COMMENT '雨量报警值',
  `soil_value` varchar(512) DEFAULT NULL COMMENT '土壤报警值',
  `slope_meter_value` varchar(50) DEFAULT NULL COMMENT '测斜仪报警值',
  `water_pressure_meter_value` text COMMENT '水压力计报警值',
  PRIMARY KEY (`id`) USING BTREE,
  KEY `idx_imei_time` (`imei`,`crt_time`),
  KEY `idx_did_time` (`data_id`,`crt_time`) USING BTREE,
  KEY `idx_did_imei_time` (`data_id`,`imei`,`crt_time`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1120753465950482441 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=DYNAMIC COMMENT='警报表';"""
    )
    # server.vn_train(documentation='"累计值"是指报告期内最新的一条数据减最旧的一条数据')
    # server.vn_train(sql='SELECT * FROM alarm WHERE imei = "BDA1220513100042";')
    server.vn_train(question="查询'BDA1220513100042'设备的第一条预警",sql='SELECT * FROM alarm WHERE imei = "BDA1220513100042" LIMIT 1;')
    # server.get_training_data()
    # server.schema_train()
    # 示例查询：
    server.ask(question="查询'BDA1220513100042'设备的第一条预警", strict_match=True)
