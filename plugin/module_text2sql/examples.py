#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @desc    : Text2SQL模块使用示例

from plugin.module_text2sql.core.text2sql_client import Text2SQLClient
from plugin.module_text2sql.service.text2sql_service import Text2SQLService


def example_generate_sql():
    """示例：生成SQL查询"""
    # 获取Text2SQL服务实例
    text2sql_service = Text2SQLService.get_instance()
    
    # 将自然语言问题转换为SQL查询
    result = text2sql_service.generate_sql("显示所有用户表的数据")
    
    print("生成的SQL查询:")
    if result["success"]:
        print(f"SQL: {result['sql']}")
    else:
        print(f"错误: {result['message']}")


def example_execute_query():
    """示例：执行查询"""
    # 获取Text2SQL服务实例
    text2sql_service = Text2SQLService.get_instance()
    
    # 执行自然语言查询
    result = text2sql_service.execute_query(question="统计用户表中的记录数量")
    
    print("\n执行查询结果:")
    if result["success"]:
        print(f"SQL: {result['sql']}")
        print(f"行数: {result['row_count']}")
        print("数据:")
        for row in result["data"][:5]:  # 显示前5行
            print(row)
    else:
        print(f"错误: {result['message']}")


def example_train_with_example():
    """示例：使用示例训练模型"""
    # 获取Text2SQL服务实例
    text2sql_service = Text2SQLService.get_instance()
    
    # 训练一个问题-SQL对
    result = text2sql_service.train_with_example(
        question="显示最近注册的10个用户", 
        sql="SELECT * FROM users ORDER BY created_at DESC LIMIT 10;"
    )
    
    print("\n训练结果:")
    print(f"状态: {'成功' if result['success'] else '失败'}")
    print(f"消息: {result['message']}")


def example_get_all_tables():
    """示例：获取所有表信息"""
    # 获取Text2SQL服务实例
    text2sql_service = Text2SQLService.get_instance()
    
    # 获取所有表
    result = text2sql_service.get_all_tables()
    
    print("\n数据库表:")
    if result["success"]:
        print(f"表数量: {result['count']}")
        print("表名列表:")
        for table in result["tables"]:
            print(f"- {table}")
    else:
        print(f"错误: {result['message']}")


def example_get_table_info():
    """示例：获取表详细信息"""
    # 获取Text2SQL服务实例
    text2sql_service = Text2SQLService.get_instance()
    
    # 获取表的详细信息
    # 注意：需要替换为实际存在的表名
    result = text2sql_service.get_table_info("users")
    
    print("\n表详细信息:")
    if result["success"]:
        print(f"表名: {result['table_name']}")
        print(f"行数: {result['row_count']}")
        print("字段:")
        for column in result["columns"]:
            print(f"- {column}")
        print("示例数据:")
        for row in result["sample_data"][:3]:  # 显示前3行
            print(row)
    else:
        print(f"错误: {result['message']}")


if __name__ == "__main__":
    # 依次运行各个示例
    example_generate_sql()
    example_execute_query()
    example_train_with_example()
    example_get_all_tables()
    example_get_table_info() 