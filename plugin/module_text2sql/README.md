# Text2SQL 模块

本模块提供自然语言到SQL查询的转换功能，通过MCP服务将已有的text2sql2功能进行封装，提供Web接口供前端调用。

## 功能简介

- 🔍 将自然语言问题转换为SQL查询
- 📊 执行SQL查询并返回格式化结果
- 📝 支持训练自定义问题和SQL对
- 📋 查看数据库表结构和样本数据
- 🧠 生成数据分析总结和洞察

## 接口说明

### 1. 生成SQL查询

```
POST /text2sql/generate
```

**请求参数：**
```json
{
  "question": "显示所有用户表的数据"
}
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "success": true,
    "sql": "SELECT * FROM users LIMIT 100;",
    "message": "SQL生成成功"
  }
}
```

### 2. 执行查询

```
POST /text2sql/execute
```

**请求参数：**
```json
{
  "question": "显示所有用户表的数据"
}
```

或者：
```json
{
  "sql": "SELECT * FROM users LIMIT 100;"
}
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "success": true,
    "sql": "SELECT * FROM users LIMIT 100;",
    "data": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      ...
    ],
    "columns": ["id", "username", "email"],
    "row_count": 10,
    "summary": "查询返回了10行数据，包含3个字段。",
    "message": "查询执行成功"
  }
}
```

### 3. 训练示例

```
POST /text2sql/train/example
```

**请求参数：**
```json
{
  "question": "显示最近注册的用户",
  "sql": "SELECT * FROM users ORDER BY created_at DESC LIMIT 10;"
}
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "示例训练成功"
}
```

### 4. 训练数据库架构

```
POST /text2sql/train/schema
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "数据库架构训练成功"
}
```

### 5. 运行完整训练流程

```
POST /text2sql/train/full
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "完整训练流程执行成功"
}
```

### 6. 获取所有表信息

```
GET /text2sql/tables
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "success": true,
    "tables": ["users", "products", "orders"],
    "count": 3,
    "message": "成功获取表信息"
  }
}
```

### 7. 获取表详细信息

```
GET /text2sql/tables/{table_name}
```

**响应示例：**
```json
{
  "code": 200,
  "msg": "操作成功",
  "data": {
    "success": true,
    "table_name": "users",
    "structure": [
      {
        "Field": "id",
        "Type": "int(11)",
        "Null": "NO",
        "Key": "PRI",
        "Default": null,
        "Extra": "auto_increment"
      },
      ...
    ],
    "columns": ["id", "username", "email"],
    "row_count": 100,
    "sample_data": [
      {
        "id": 1,
        "username": "admin",
        "email": "admin@example.com"
      },
      ...
    ],
    "message": "成功获取表 users 的信息"
  }
}
```

## 前端调用示例

### Vue.js 示例

```javascript
// 生成SQL
async function generateSQL(question) {
  const response = await axios.post('/text2sql/generate', {
    question: question
  });
  return response.data.data;
}

// 执行查询
async function executeQuery(question) {
  const response = await axios.post('/text2sql/execute', {
    question: question
  });
  return response.data.data;
}
```

### 界面示例

1. 输入自然语言问题
2. 系统生成SQL查询并展示
3. 执行SQL获取结果
4. 展示结果表格和可视化图表
5. 提供训练功能按钮

## 注意事项

1. 确保系统已正确配置数据库连接信息
2. 初始使用时建议先运行完整训练流程
3. 复杂查询可能需要额外的训练示例
4. 请避免在生产环境中执行非查询类SQL操作 