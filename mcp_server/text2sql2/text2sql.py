import logging
import os
from dotenv import load_dotenv
from vanna.chromadb import ChromaDB_VectorStore
from vanna.flask import VannaFlaskApp
from vanna.openai import OpenAI_Chat
from openai import OpenAI

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

# OpenAI配置
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable is not set")
OPENAI_MODEL = os.getenv('OPENAI_MODEL', 'gpt-3.5-turbo')  # 添加默认值
OPENAI_API_URL = os.getenv('OPENAI_API_URL', 'https://api.openai.com/v1')  # 添加默认值
OPENAI_TIMEOUT = 60  # 增加超时时间到60秒

# MySQL 配置
DB_HOST = os.getenv('DB_HOST')  # 添加默认值
DB_PORT = os.getenv('DB_PORT')  # 添加默认值
DB_NAME = os.getenv('DB_NAME')  # 添加默认值
DB_USER = os.getenv('DB_USER')  # 添加默认值
DB_PASSWORD = os.getenv('DB_PASSWORD')  # 添加默认值


class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        if config is None:
            config = {}
        logger.info("正在初始化 ChromaDB_VectorStore...")
        ChromaDB_VectorStore.__init__(self, config=config)
        logger.info("正在初始化 OpenAI_Chat...")

        # 创建 OpenAI 客户端
        self.client = OpenAI(
            api_key=config.get('api_key'),
            base_url=config.get('base_url'),
            timeout=config.get('timeout')
        )

        OpenAI_Chat.__init__(self, config={'client': self.client, 'model': config.get('model')})

    def generate_questions(self):
        """生成中文问题"""
        questions = [
            "数据库中有哪些表？",
            "显示最近10条记录",
            "统计每个类别的数量",
            "查找重复的记录",
            "按日期排序显示数据",
            "统计总记录数",
            "显示数据表结构",
            "查询最新更新的数据"
        ]
        return questions

    def generate_sql(self, question, **kwargs):
        """处理中文问题并生成SQL"""
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

        return super().generate_sql(question=chinese_prompt, **kwargs)

    def generate_followup_questions(self, question, sql, df):
        """生成中文后续问题"""
        if df is not None and not df.empty:
            followup_questions = [
                "这些数据有什么特点？",
                "能否按时间维度进行分析？",
                "哪些类别或字段的占比最大？",
                "数据中是否存在异常值？",
                "能否进行趋势分析？",
                "如何进一步筛选这些数据？",
                "相关数据的统计信息如何？"
            ]
        else:
            followup_questions = [
                "请尝试其他查询条件",
                "检查数据表是否存在",
                "确认查询语法是否正确"
            ]
        return followup_questions

    def generate_summary(self, question, df):
        """生成中文总结"""
        if df is None or df.empty:
            return "查询未返回任何数据，请检查查询条件或数据表。"

        # 构建详细的中文提示词
        prompt = f"""
        请作为专业的数据分析师，用中文分析以下查询结果，并提供简洁明了的总结。

        原始问题：{question}

        数据概览：
        - 总行数：{len(df)}
        - 总列数：{len(df.columns)}
        - 列名：{', '.join(df.columns.tolist())}

        数据样本：
        {df.head(10).to_string()}

        请提供：
        1. 数据的基本概况
        2. 主要发现和洞察
        3. 数据质量评估
        4. 可能的后续分析建议

        请用专业但通俗易懂的中文回答。
        """

        try:
            response = self.client.chat.completions.create(
                model=self.config.get('model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system",
                     "content": "你是一个专业的数据分析师，擅长用中文进行数据分析和洞察总结。请用简洁明了的中文回答用户的问题。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"生成总结时出错: {str(e)}")
            return f"数据查询成功，共返回 {len(df)} 行数据，包含 {len(df.columns)} 个字段。由于技术原因，无法生成详细总结，请查看上方的数据结果。"

    def ask(self, question, **kwargs):
        """重写 ask 方法以确保中文响应"""
        # 添加中文上下文
        chinese_context = f"""
        请用中文回答以下问题。如果需要生成SQL，请确保SQL语句正确且高效。

        用户问题：{question}
        """

        return super().ask(question=chinese_context, **kwargs)

    def generate_plotly_code(self, question, sql, df):
        """生成中文图表代码"""
        if df is None or df.empty:
            return None

        prompt = f"""
        请根据以下信息生成Plotly图表的Python代码，要求：
        1. 图表标题、轴标签等都使用中文
        2. 选择合适的图表类型
        3. 代码要完整可运行
        4. 添加必要的中文注释

        问题：{question}
        SQL：{sql}
        数据列：{df.columns.tolist()}
        数据类型：{df.dtypes.to_dict()}
        数据样本：{df.head().to_string()}
        """

        try:
            response = self.client.chat.completions.create(
                model=self.config.get('model', 'gpt-3.5-turbo'),
                messages=[
                    {"role": "system", "content": "你是一个数据可视化专家，请生成中文标注的Plotly图表代码。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"生成图表代码时出错: {str(e)}")
            return None


# 创建 Vanna 实例
vn = MyVanna(
    config={
        'api_key': OPENAI_API_KEY,
        'model': OPENAI_MODEL,
        'base_url': OPENAI_API_URL,
        'timeout': OPENAI_TIMEOUT
    }
)

# 连接到MySQL数据库
try:
    vn.connect_to_mysql(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=int(DB_PORT)
    )
    logger.info("成功连接到MySQL数据库")
except Exception as e:
    logger.error(f"连接数据库失败: {str(e)}")
    raise


# 训练模型使用中文语境
# def setup_chinese_training():
#     """设置中文训练数据"""
#     try:
#         # 添加一些中文问题和对应的SQL示例
#         chinese_training_data = [
#             {
#                 "question": "显示所有表",
#                 "sql": "SHOW TABLES;"
#             },
#             {
#                 "question": "查询用户表的结构",
#                 "sql": "DESCRIBE users;"
#             },
#             {
#                 "question": "统计用户总数",
#                 "sql": "SELECT COUNT(*) as 用户总数 FROM users;"
#             },
#             {
#                 "question": "按创建时间排序显示最新的10条记录",
#                 "sql": "SELECT * FROM users ORDER BY created_at DESC LIMIT 10;"
#             }
#         ]
#
#         for item in chinese_training_data:
#             vn.train(question=item["question"], sql=item["sql"])
#
#         logger.info("中文训练数据添加完成")
#     except Exception as e:
#         logger.warning(f"添加训练数据时出现错误: {str(e)}")
#
#
# # 设置中文训练
# setup_chinese_training()

# 创建 Flask 应用 - 只使用 VannaFlaskApp 支持的参数
app = VannaFlaskApp(
    vn=vn,
    logo="https://www.reshot.com/preview-assets/icons/RVTB9HNE4Z/innovation-RVTB9HNE4Z.svg",
    title="AI SQL 智能助手",
    subtitle="您的专属 AI 数据查询分析师",
    debug=True,
    allow_llm_to_see_data=True
)

if __name__ == '__main__':
    print("正在启动 AI SQL 智能助手...")
    print("访问地址: http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)