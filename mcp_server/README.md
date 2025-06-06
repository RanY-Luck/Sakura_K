# MCP服务 StreamableHTTP 客户端示例

这个目录包含了使用 MCP（Model Control Protocol）服务的 `streamablehttp_client` 方法的示例代码。这是最新的HTTP连接方式，用于与MCP服务进行通信。

## 文件说明

本项目包含以下示例文件：

1. `streamable_http_demo.py` - 基本的streamablehttp_client使用示例
2. `streamable_http_advanced_demo.py` - 高级示例，展示流式处理功能
3. `streamable_http_websocket.py` - WebSocket服务器示例，用于在Web应用中使用MCP服务

## 环境要求

- Python 3.8+
- MCP库
- FastAPI (用于WebSocket示例)
- uvicorn (用于WebSocket示例)

## 安装依赖

```bash
pip install mcp fastapi uvicorn
```

## 基本示例 (streamable_http_demo.py)

这个示例展示了如何使用 `streamablehttp_client` 连接到MCP服务器并调用工具。

### 功能特点

- 连接到MCP服务器
- 列出可用工具
- 调用工具
- 调用资源
- 错误处理和重试机制

### 使用方法

```bash
python streamable_http_demo.py
```

## 高级示例 (streamable_http_advanced_demo.py)

这个示例展示了如何使用 `streamablehttp_client` 进行流式处理，适用于需要实时处理大量数据的场景。

### 功能特点

- 流式调用工具
- 流式调用资源
- 实时处理数据块
- 命令行参数配置

### 使用方法

```bash
python streamable_http_advanced_demo.py --url http://localhost:8000 --prompt "介绍一下Python的异步编程"
```

### 命令行参数

- `--url`: MCP服务器URL，默认为 `http://localhost:8000`
- `--prompt`: Ollama生成提示，默认为 "介绍一下Python的异步编程特性"
- `--sql-question`: Text2SQL问题，默认为 "查询所有销售额超过1000元的订单"

## WebSocket服务器示例 (streamable_http_websocket.py)

这个示例展示了如何创建一个WebSocket服务器，允许Web应用程序通过WebSocket连接使用MCP服务。

### 功能特点

- WebSocket服务器
- 多客户端支持
- 流式响应
- 内置HTML测试页面

### 使用方法

```bash
python streamable_http_websocket.py --host 127.0.0.1 --port 8080
```

然后在浏览器中访问 `http://127.0.0.1:8080` 使用测试页面。

### 命令行参数

- `--host`: 监听主机，默认为 `127.0.0.1`
- `--port`: 监听端口，默认为 `8080`

## 使用说明

### 1. 确保MCP服务器正在运行

在使用这些示例之前，确保您的MCP服务器已经启动。例如，如果您使用的是FastMCP服务器，可以这样启动：

```bash
uvicorn mcp_server:app --host 0.0.0.0 --port 8000
```

### 2. 运行基本示例

运行基本示例以测试连接和基本功能：

```bash
python streamable_http_demo.py
```

这将连接到MCP服务器，列出可用工具，并演示调用天气查询工具和Ollama生成工具。

### 3. 尝试高级流式示例

如果您需要处理大量数据或需要实时响应，可以运行高级流式示例：

```bash
python streamable_http_advanced_demo.py
```

这将展示如何流式调用工具并处理流式响应。您可以通过命令行参数自定义请求：

```bash
python streamable_http_advanced_demo.py --prompt "解释量子计算的基本原理"
```

### 4. 在Web应用中使用WebSocket示例

如果您想在Web应用中使用MCP服务，可以启动WebSocket服务器：

```bash
python streamable_http_websocket.py
```

然后在浏览器中访问 `http://127.0.0.1:8080`，您将看到一个测试页面，可以：

1. 连接WebSocket
2. 连接MCP服务器
3. 调用工具
4. 流式调用工具
5. 断开连接

## API说明

### StreamableHttpDemo 类 (基本示例)

```python
# 创建客户端实例
client = StreamableHttpDemo(server_url="http://localhost:8000")

# 连接到服务器
await client.connect_to_server()

# 调用工具
result = await client.call_tool("query_weather", {"city": "Shanghai"})
print(result)

# 调用资源
health_info = await client.call_resource("sakura://health")
print(health_info)

# 清理资源
await client.cleanup()
```

### StreamableHttpAdvancedDemo 类 (高级示例)

```python
# 创建客户端实例
client = StreamableHttpAdvancedDemo(server_url="http://localhost:8000")

# 连接到服务器
await client.connect_to_server()

# 流式调用工具
print("生成结果: ", end="")
async for chunk in client.stream_tool("ollama_generate", {
    "model": "llama3", 
    "prompt": "介绍Python"
}):
    if isinstance(chunk, str):
        print(chunk, end="")
    elif isinstance(chunk, dict) and "text" in chunk:
        print(chunk["text"], end="")
print("\n")

# 清理资源
await client.cleanup()
```

### WebSocket API (WebSocket示例)

WebSocket客户端可以发送以下JSON消息：

1. 连接到MCP服务器：
```json
{
    "action": "connect_mcp",
    "server_url": "http://localhost:8000"
}
```

2. 调用工具：
```json
{
    "action": "call_tool",
    "tool_name": "query_weather",
    "args": {"city": "Shanghai"}
}
```

3. 流式调用工具：
```json
{
    "action": "stream_tool",
    "tool_name": "ollama_generate",
    "args": {"model": "llama3", "prompt": "介绍Python"}
}
```

## 常见问题

### 1. 连接超时

如果遇到连接超时，请检查：
- MCP服务器是否正在运行
- 服务器URL是否正确
- 网络连接是否正常

可以通过设置环境变量增加超时时间：
```bash
export MCP_CONNECTION_TIMEOUT=60.0  # 设置为60秒
```

### 2. 工具不可用

如果提示工具不可用，请先使用`list_tools`方法检查服务器上可用的工具列表。您可以在代码中打印：
```python
print(f"可用工具: {[tool.name for tool in client.available_tools]}")
```

### 3. 流式调用失败

流式调用需要服务器端支持流式响应。如果流式调用失败，可能是因为：
- 服务器不支持流式响应
- 工具不支持流式调用
- 网络不稳定

## 定制开发

您可以基于这些示例进行定制开发：

1. 创建自己的工具调用类
2. 集成到现有项目中
3. 添加更多错误处理和重试逻辑
4. 增加用户界面

## 贡献

欢迎提交问题和改进建议！

## 许可证

[MIT License](LICENSE) 