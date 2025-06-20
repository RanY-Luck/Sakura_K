# Text2SQL2 - 自然语言到SQL查询助手

Text2SQL2是一个基于Vanna AI的自然语言到SQL查询转换工具，允许用户使用自然语言提问并自动生成和执行SQL查询。

## 功能特性

- 🔍 将自然语言问题转换为SQL查询
- 📊 执行SQL查询并返回格式化结果
- 📝 支持训练自定义问题和SQL对
- 📋 查看数据库表结构和样本数据
- 🧠 生成数据分析总结和洞察
- 📈 支持数据可视化生成（Plotly代码）

## 环境配置

1. 安装依赖项：

```bash
pip install vanna openai chromadb pandas python-dotenv
```

2. 配置环境变量（在.env文件中）：

```
# OpenAI配置
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_API_URL=https://api.openai.com/v1

# 数据库配置
DB_HOST=localhost
DB_PORT=3306
DB_NAME=your_database
DB_USER=your_username
DB_PASSWORD=your_password
```

## 使用方法

### 作为MCP服务使用

1. 启动MCP服务器：

```bash
python mcp_server/text2sql2_server.py
```

2. 在另一个终端中使用MCP客户端连接：

```bash
python mcp_server/mcp_client.py mcp_server/text2sql2_server.py
```

3. 现在可以通过MCP客户端使用自然语言进行查询：

```
你: 显示所有表
```

### 可用的MCP工具

- `sql_query(question)`: 将自然语言问题转换为SQL并执行
- `execute_sql(sql)`: 直接执行SQL语句
- `get_table_info(table_name)`: 获取指定表的详细信息
- `get_all_tables()`: 获取所有表的信息
- `train_sql_example(question, sql)`: 训练一个问题-SQL对
- `train_database_schema()`: 训练数据库模式
- `train_with_examples()`: 使用生成的示例进行训练
- `run_full_training()`: 运行完整的训练流程

### 作为Flask应用使用

text2sql.py文件中已经配置了一个Flask应用，可以直接运行：

```bash
python mcp_server/text2sql2/text2sql.py
```

访问 http://localhost:5001 即可使用Web界面。

## 训练模型

运行train.py以训练模型，使其更好地理解你的数据库结构和业务场景：

```bash
python mcp_server/text2sql2/train.py
```

## 示例问题

- "显示所有表"
- "统计用户表中的记录数量"
- "查找最近10条订单记录"
- "按时间排序显示用户活动"
- "统计每个类别的产品数量"

## 开发说明

- `text2sql.py`: 主要功能实现
- `train.py`: 训练工具和流程
- `text2sql2_server.py`: MCP服务器实现

## 注意事项

- 确保数据库连接信息正确
- OpenAI API密钥需要有效
- 对于复杂查询，可能需要进行额外的训练 