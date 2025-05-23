# import base64
import os
import sys

# 获取项目根目录路径
project_root = os.path.abspath(os.path.dirname(__file__))
# 将项目根目录添加到 sys.path
sys.path.insert(0, project_root)

from flask import Flask, request, jsonify
from siliconflow_api import SiliconflowEmbedding
from vanna_text2sql import VannaServer
import plotly.io as pio

from functools import lru_cache
from werkzeug.exceptions import BadRequest
import logging
from dotenv import load_dotenv

# 加载环境变量文件
load_dotenv()

# 设置日志配置
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 创建Flask应用
app = Flask(__name__)


# 集中配置管理类
class Config:
    """
    集中配置管理类，用于管理和提供应用程序的配置参数
    """
    def __init__(self, supplier):
        """
        初始化配置

        Args:
            supplier: AI服务提供商标识
        """
        # 嵌入模型提供商，默认为SiliconFlow
        self.embedding_supplier = "SiliconFlow"
        # 嵌入类，用于将文本转换为向量
        self.EmbeddingClass = SiliconflowEmbedding
        # 向量数据库路径
        self.vector_db_path = os.getenv("VECTOR_DB_PATH")
        # AI服务提供商
        self.supplier = supplier
        # MySQL数据库配置
        self.mysql_config = {
            "host": os.getenv("DB_HOST"),
            "dbname": os.getenv("DB_NAME"),
            "user": os.getenv("DB_USER"),
            "password": os.getenv("DB_PASSWORD"),
            "port": int(os.getenv("DB_PORT"))
        }


# 存储不同的 VannaServer 实例
vn_instances = {}


def get_vn_instance(supplier=""):
    """
    获取或创建VannaServer实例，实现单例模式

    Args:
        supplier: AI服务提供商标识，默认从环境变量中获取

    Returns:
        对应提供商的VannaServer实例
    """
    if supplier == "":
        supplier = os.getenv("SUPPLIER", "GITEE")
    if supplier not in vn_instances:
        config = Config(supplier)
        # 合并配置
        combined_config = {**config.__dict__, **config.mysql_config}
        vn_instances[supplier] = VannaServer(combined_config)
    return vn_instances[supplier]


def validate_input(data, required_fields):
    """
    输入验证函数，检查请求数据中是否包含所有必需字段

    Args:
        data: 请求数据
        required_fields: 必需字段列表

    Raises:
        BadRequest: 如果缺少必需字段
    """
    for field in required_fields:
        if field not in data or not data[field]:
            raise BadRequest(f"Missing required field: {field}")


@app.route('/vn_train', methods=['POST'])
def vn_train_route():
    """
    训练接口，用于接收训练数据并训练文本到SQL模型

    支持以下训练方式：
    - 问题和SQL对：通过示例教导模型如何将问题转换为SQL
    - 仅SQL：通过现有SQL示例学习查询模式
    - 文档：通过业务文档学习领域术语
    - DDL：通过数据定义语句学习数据库结构
    - 模式：通过数据库信息模式学习表结构

    Returns:
        训练结果的JSON响应
    """
    data = request.json
    # required_fields = ['question', 'sql']
    # validate_input(data, required_fields)

    supplier = data.get('supplier', "")
    question = data.get('question', '')
    sql = data.get('sql', '')
    documentation = data.get('documentation', '')
    ddl = data.get('ddl', '')
    schema = data.get('schema', False)

    # 验证至少有一个参数不为空
    if not any([question, sql, documentation, ddl, schema]):
        return jsonify(
        {'error': 'At least one of the parameters (question, sql, documentation, ddl, schema) must be provided'}), 400

    server = get_vn_instance(supplier)
    server.vn_train(question=question, sql=sql, documentation=documentation, ddl=ddl)
    if schema:
        try:
            server.schema_train()
        except Exception as e:
            logging.info(f"Error initializing vector store: {e}")

    logging.info("Training completed successfully")
    return jsonify({'status': 'success'}), 200


@app.route('/get_training_data', methods=['GET'])
def get_training_data_route():
    """
    获取训练数据接口，返回模型当前的训练数据

    Returns:
        包含训练数据的JSON响应
    """
    supplier = request.args.get('supplier', "")
    server = get_vn_instance(supplier)

    @lru_cache(maxsize=128)  # 添加缓存机制，避免频繁重复请求
    def cached_get_training_data():
        return server.get_training_data()

    training_data = cached_get_training_data()
    logging.info("Fetched training data successfully")

    return jsonify(training_data), 200


@app.route('/ask', methods=['POST'])
def ask_route():
    """
    提问接口，将自然语言问题转换为SQL查询并执行

    接收JSON请求，包含以下字段：
    - question: 自然语言问题
    - visualize: 是否生成可视化（默认为True）
    - auto_train: 是否自动训练成功的查询（默认为True）
    - supplier: AI服务提供商（默认从环境变量获取）

    Returns:
        包含SQL查询、数据结果和可视化的JSON响应
    """
    data = request.json
    question = data.get('question', '')
    visualize = data.get('visualize', True)
    auto_train = data.get('auto_train', True)
    supplier = data.get('supplier', "")  # GITEE, ZHIPU, SiliconFlow

    if not question:
        raise BadRequest("Question is required")

    server = get_vn_instance(supplier)
    try:
        # 调用Vanna服务处理问题
        sql, df, fig = server.ask(question=question, visualize=visualize, auto_train=auto_train)

        # 将DataFrame转换为JSON
        df_json = df.to_json(orient='records', force_ascii=False)

        # 将Plotly图表转换为JSON
        # 注意：之前的base64编码方法会卡住，已禁用
        # img_bytes = pio.to_image(fig, format="png", scale=2)
        # img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        """
        <img id="plotly-image" src="data:image/png;base64,{{ img_base64 }}" alt="Plotly Image">
        """

        # 将Plotly图表保存为JS文件，以便在前端展示
        fig_js_path = '../output/html/vanna_fig.js'
        fig_html_path = 'http://localhost:5000/html/vanna_fig.html'
        figure_json = pio.to_json(fig)
        with open(fig_js_path, 'w', encoding='utf-8') as f:
            f.write(figure_json)
        """
          <div id="plotly-div"></div>
          <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
          <script>
              var fig_json = {{ fig_json }};
              Plotly.newPlot('plotly-div', fig_json.data, fig_json.layout);
          </script>
        """

        logging.info("Query processed successfully")
        return jsonify({
            'sql': sql,
            'data': df_json,
            # 'img_base64': img_base64,
            'plotly_figure': fig_html_path
        }), 200
    except Exception as e:
        logging.error(f"Error processing request: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # 启动Flask应用，监听所有网络接口的5000端口
    app.run(host='0.0.0.0', port=5000)
