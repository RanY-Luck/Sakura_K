'''
Descripttion: Text2SQL MCP服务器
version: 1.0.0
Author: 冉勇
Date: 2025-06-20 15:00:00
LastEditTime: 2025-06-20 15:00:00
'''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc    : Text2SQL MCP服务器实现

import os
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from dotenv import load_dotenv

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

# 导入Text2SQL服务
from plugin.module_text2sql.service.text2sql_service import Text2SQLService

# 创建FastAPI应用
app = FastAPI(title="Text2SQL MCP Server", description="Text2SQL MCP服务器")

# 获取Text2SQL服务实例
text2sql_service = Text2SQLService.get_instance()


# WebSocket路由
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket连接已建立")
    
    try:
        while True:
            # 接收客户端消息
            message = await websocket.receive_text()
            logger.info(f"收到消息: {message}")
            
            try:
                # 解析JSON消息
                data = json.loads(message)
                command = data.get("command")
                params = data.get("params", {})
                
                # 处理不同的命令
                if command == "generate_sql":
                    result = text2sql_service.generate_sql(params.get("question", ""))
                    await websocket.send_json({"success": True, "result": result})
                
                elif command == "execute_query":
                    result = text2sql_service.execute_query(
                        question=params.get("question"),
                        sql=params.get("sql")
                    )
                    await websocket.send_json({"success": True, "result": result})
                
                elif command == "train_example":
                    result = text2sql_service.train_with_example(
                        question=params.get("question", ""),
                        sql=params.get("sql", "")
                    )
                    await websocket.send_json({"success": True, "result": result})
                
                elif command == "train_schema":
                    result = text2sql_service.train_database_schema()
                    await websocket.send_json({"success": True, "result": result})
                
                elif command == "full_training":
                    result = text2sql_service.run_full_training()
                    await websocket.send_json({"success": True, "result": result})
                
                elif command == "get_tables":
                    result = text2sql_service.get_all_tables()
                    await websocket.send_json({"success": True, "result": result})
                
                elif command == "get_table_info":
                    result = text2sql_service.get_table_info(params.get("table_name", ""))
                    await websocket.send_json({"success": True, "result": result})
                
                else:
                    await websocket.send_json({
                        "success": False, 
                        "error": f"未知命令: {command}"
                    })
            
            except json.JSONDecodeError:
                await websocket.send_json({
                    "success": False, 
                    "error": "无效的JSON消息"
                })
            except Exception as e:
                logger.error(f"处理消息时出错: {str(e)}")
                await websocket.send_json({
                    "success": False, 
                    "error": f"处理请求时发生错误: {str(e)}"
                })
    
    except WebSocketDisconnect:
        logger.info("WebSocket连接已关闭")


# HTTP健康检查端点
@app.get("/health")
def health_check():
    """健康检查端点"""
    return {"status": "ok"}


# 启动服务器
if __name__ == "__main__":
    import uvicorn
    
    # 获取端口，默认为8765
    port = int(os.getenv("TEXT2SQL_MCP_PORT", "8765"))
    
    print(f"🚀 Text2SQL MCP服务器启动在端口 {port}")
    uvicorn.run(app, host="0.0.0.0", port=port) 