# Text2SQL 模块

## 简介

Text2SQL 模块是一个自然语言转 SQL 查询的插件，允许用户使用自然语言提问，系统自动生成并执行 SQL 查询，返回结果。

## 功能特点

- 自然语言转 SQL 查询
- 支持多种 AI 服务提供商
- 支持模型训练，不断提升转换精度
- 支持数据库模式训练，自动学习表结构
- 支持文档训练，理解业务术语

## 安装方法

### 依赖项

安装所需依赖：

```bash
pip install -r plugin/module_text2sql/requirements.txt
```

### 环境变量配置

在 `.env.dev` 或其他环境文件中配置以下变量：

```
# 数据库配置
DB_HOST1=your_db_host
DB_NAME1=your_db_name
DB_USER1=your_db_user
DB_PASSWORD1=your_db_password
DB_PORT1=3306

# AI 服务提供商配置
SUPPLIER=GITEE  # 或其他支持的提供商
GITEE_API_KEY=your_api_key
GITEE_API_BASE=your_api_base_url
GITEE_CHAT_MODEL=your_chat_model

# 嵌入模型配置
TEXT2SQL_EMBEDDING_SUPPLIER=SiliconFlow
SiliconFlow_EMBEDDING_API_KEY=your_embedding_api_key
SiliconFlow_EMBEDDING_MODEL=your_embedding_model

# 向量数据库路径
VECTOR_DB_PATH=vector_db
```

## 使用方法

### API 接口

模块提供以下 API 接口：

1. **训练模型**
    - 路径: `/text2sql/train`
    - 方法: POST
    - 功能: 训练模型理解自然语言和 SQL 的对应关系

2. **提问**
    - 路径: `/text2sql/ask`
    - 方法: POST
    - 功能: 将自然语言问题转换为 SQL 并执行

3. **训练数据库模式**
    - 路径: `/text2sql/schema_train`
    - 方法: POST
    - 功能: 训练模型理解数据库结构

4. **训练表 DDL**
    - 路径: `/text2sql/train_table`
    - 方法: POST
    - 功能: 训练模型理解表结构

5. **训练文档**
    - 路径: `/text2sql/train_doc`
    - 方法: POST
    - 功能: 训练模型理解业务术语和概念

### 示例请求

#### 训练模型

```json
POST /text2sql/train
{
  "question": "有多少用户注册了我们的系统？",
  "sql": "SELECT COUNT(*) FROM sys_user WHERE del_flag = 0"
}
```

#### 提问

```json
POST /text2sql/ask
{
  "question": "有多少用户注册了我们的系统？",
  "visualize": true,
  "auto_train": true
}
```

## 故障排除

### 常见问题

1. **模块无法加载**
    - 检查是否安装了所有依赖
    - 确认目录结构是否正确
    - 检查 `__init__.py` 文件是否存在

2. **API 调用失败**
    - 检查环境变量配置
    - 确认 AI 服务提供商 API 密钥是否有效
    - 检查数据库连接信息是否正确

3. **SQL 生成不准确**
    - 增加更多训练数据
    - 确保已训练数据库模式
    - 添加相关业务文档进行训练
