#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/8 10:00
# @Author  : 冉勇
# @Site    :
# @File    : text2sql_controller.py
# @Software: PyCharm
# @desc    : 文本转SQL控制器
from fastapi import APIRouter, Depends
from utils.response_util import ResponseUtil
from utils.log_util import logger
from module_admin.service.login_service import LoginService
from plugin.module_text2sql.entity.vo.text2sql_vo import TrainRequest, AskRequest
from plugin.module_text2sql.service.text2sql_service import Text2SqlService

# 创建路由器
text2sqlController = APIRouter(prefix="/text2sql", dependencies=[Depends(LoginService.get_current_user)])


@text2sqlController.post("/train")
async def train_route(request: TrainRequest):
    """
    训练接口，用于接收训练数据并训练文本到SQL模型

    支持以下训练方式：
    - 问题和SQL对：通过示例教导模型如何将问题转换为SQL
    - 仅SQL：通过现有SQL示例学习查询模式
    - 文档：通过业务文档学习领域术语
    - DDL：通过数据定义语句学习数据库结构
    - 模式：通过数据库信息模式学习表结构
    """
    try:
        result = await Text2SqlService.train_service(
            question=request.question,
            sql=request.sql,
            documentation=request.documentation,
            ddl=request.ddl,
            schema=request.use_schema,
            supplier=request.supplier
        )
        logger.info(f"训练成功: {result}")
        return ResponseUtil.success(msg="训练成功")
    except Exception as e:
        logger.error(f"训练失败: {str(e)}")
        return ResponseUtil.error(msg=str(e))


@text2sqlController.get("/training_data")
async def get_training_data_route(supplier: str = ""):
    """
    获取训练数据接口
    
    Args:
        supplier: AI服务提供商
    """
    try:
        training_data = await Text2SqlService.get_training_data_service(supplier)
        logger.info("成功获取训练数据")
        return ResponseUtil.success(data=training_data)
    except Exception as e:
        logger.error(f"获取训练数据失败: {str(e)}")
        return ResponseUtil.error(msg=str(e))


@text2sqlController.post("/ask")
async def ask_route(request: AskRequest):
    """
    提问接口，将自然语言问题转换为SQL查询并执行
    
    接收请求，包含以下字段：
    - question: 自然语言问题
    - visualize: 是否生成可视化（默认为True）
    - auto_train: 是否自动训练成功的查询（默认为True）
    - supplier: AI服务提供商（默认从环境变量获取）
    """
    try:
        result = await Text2SqlService.ask_service(
            question=request.question,
            visualize=request.visualize,
            auto_train=request.auto_train,
            supplier=request.supplier
        )
        logger.info(f"成功处理问题: {request.question}")
        return ResponseUtil.success(data=result)
    except Exception as e:
        logger.error(f"处理问题失败: {str(e)}")
        return ResponseUtil.error(msg=str(e)) 