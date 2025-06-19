#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-05-28 18:20:00
# @Author   : 冉勇
# @File     : text2sql_controller.py
# @Software : PyCharm
# @Desc     : Text2SQL控制器，暴露API接口
from fastapi import APIRouter, Body, Query, Depends
from plugin.module_text2sql.service.text2sql_service import Text2SQLService
from plugin.module_text2sql.entity.vo.text2sql_vo import TrainRequest, AskRequest
from utils.response_util import ResponseUtil
from module_admin.service.login_service import LoginService

# 创建服务实例
service = Text2SQLService()

# 创建路由器
text2sqlController = APIRouter(prefix="/text2sql", dependencies=[Depends(LoginService.get_current_user)])


@text2sqlController.post("/train")
async def train_model(request: TrainRequest):
    """
    训练Text2SQL模型
    
    支持以下训练方式：
    - 问题和SQL对：通过示例教导模型如何将问题转换为SQL
    - 仅SQL：通过现有SQL示例学习查询模式
    - 文档：通过业务文档学习领域术语
    - DDL：通过数据定义语句学习数据库结构
    - 模式：通过数据库信息模式学习表结构
    """
    # 验证至少有一个参数不为空
    if not any([request.question, request.sql, request.documentation, request.ddl, request.schema]):
        return ResponseUtil.error(msg="至少需要提供一个参数(question, sql, documentation, ddl, schema)")

    try:
        success = service.train(
            supplier=request.supplier,
            question=request.question,
            sql=request.sql,
            documentation=request.documentation,
            ddl=request.ddl,
            schema=request.schema
        )

        if success:
            return ResponseUtil.success(msg="训练成功")
        else:
            return ResponseUtil.error(msg="训练失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"训练异常: {str(e)}")


@text2sqlController.get("/training_data")
async def get_training_data():
    """
    获取训练数据，包括问题-SQL对、文档、DDL等
    """
    try:
        training_data = service.get_training_data()
        return ResponseUtil.success(data=training_data)
    except Exception as e:
        return ResponseUtil.error(msg=f"获取训练数据失败: {str(e)}")


@text2sqlController.post("/ask")
async def ask_question(request: AskRequest):
    """
    提问接口，将自然语言问题转换为SQL查询并执行
    
    接收JSON请求，包含以下字段：
    - question: 自然语言问题
    - auto_train: 是否自动训练成功的查询（默认为True）
    - supplier: AI服务提供商（默认从环境变量获取）
    """
    if not request.question:
        return ResponseUtil.error(msg="问题不能为空")

    try:
        # 打印请求信息，便于调试
        print(f"接收到问题请求: {request.question}")
        print(f"供应商: {request.supplier or '默认'}")

        # 调用服务处理问题
        sql, df, fig = service.ask(
            question=request.question,
            auto_train=request.auto_train,
            supplier=request.supplier
        )

        print(f"生成SQL: {sql}")
        print(f"结果数据行数: {len(df)}")

        # 将DataFrame转换为JSON
        df_json = df.to_json(orient='records', force_ascii=False)

        return ResponseUtil.success(
            data={
                "sql": sql,
                "data": df_json
            }
        )
    except Exception as e:
        import traceback
        error_msg = f"处理问题失败: {str(e)}"
        print(error_msg)
        traceback.print_exc()  # 打印详细的堆栈跟踪
        return ResponseUtil.error(msg=error_msg)


@text2sqlController.post("/check_vector_store")
async def check_vector_store(supplier: str = Body("", embed=True)):
    """
    检查向量存储状态
    """
    try:
        vn_instance = service.get_vn_instance(supplier)
        status = vn_instance.check_vector_store()
        if status:
            return ResponseUtil.success(msg="向量存储正常")
        else:
            return ResponseUtil.error(msg="向量存储未初始化或异常")
    except Exception as e:
        return ResponseUtil.error(msg=f"检查向量存储失败: {str(e)}")


@text2sqlController.post("/schema_train")
async def schema_train(supplier: str = Body("", embed=True)):
    """
    训练数据库模式
    """
    try:
        vn_instance = service.get_vn_instance(supplier)
        success = vn_instance.schema_train()
        if success:
            return ResponseUtil.success(msg="数据库模式训练成功")
        else:
            return ResponseUtil.error(msg="数据库模式训练失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"训练数据库模式失败: {str(e)}")


@text2sqlController.post("/train_table")
async def train_table_ddl(
        ddl: str = Body(..., description="表DDL语句"),
        force_retrain: bool = Body(False, description="是否强制重新训练"),
        supplier: str = Body("", description="AI服务提供商")
):
    """
    训练表DDL
    """
    try:
        vn_instance = service.get_vn_instance(supplier)
        success = vn_instance.train_table_ddl(ddl, force_retrain)
        if success:
            return ResponseUtil.success(msg="表训练成功")
        else:
            return ResponseUtil.error(msg="表训练失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"训练表失败: {str(e)}")


@text2sqlController.post("/train_doc")
async def train_documentation(
        documentation: str = Body(..., description="文档内容"),
        supplier: str = Body("", description="AI服务提供商")
):
    """
    训练文档
    """
    try:
        success = service.train(
            supplier=supplier,
            documentation=documentation
        )
        if success:
            return ResponseUtil.success(msg="文档训练成功")
        else:
            return ResponseUtil.error(msg="文档训练失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"训练文档失败: {str(e)}")
