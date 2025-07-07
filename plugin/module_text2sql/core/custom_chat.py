#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-05-28 18:05:00
# @Author   : 冉勇
# @File     : custom_chat.py
# @Software : PyCharm
# @Desc     : 重组Vanna聊天，适配多种模型

import re
import pandas as pd
from typing import List
from vanna.base import VannaBase
from openai import OpenAI


class CustomChat(VannaBase):
    """
    自定义聊天类，扩展 VannaBase 类，用于处理文本到 SQL 的转换过程
    该类实现了与大语言模型的交互逻辑，以便生成 SQL 查询和可视化代码
    """

    def __init__(self, config=None):
        """
        初始化自定义聊天类

        Args:
            config: 包含API密钥和模型配置的字典
        """
        VannaBase.__init__(self, config=config)
        if config is None:
            return
        if "api_key" not in config:
            raise Exception("Missing api_key in config")
        self.api_key = config["api_key"]
        self.model = config["model"] if "model" in config else "Qwen/Qwen2.5-7B-Instruct"
        self.api_base = config["api_base"]
        # self.ChatAPI = config["ChatAPI"]

    # 静态方法，用于格式化聊天消息和实用工具函数
    @staticmethod
    def system_message(message: str) -> dict:
        """
        创建系统角色的消息

        Args:
            message: 系统消息内容

        Returns:
            格式化的系统消息字典
        """
        return {"role": "system", "content": message}

    @staticmethod
    def user_message(message: str) -> dict:
        """
        创建用户角色的消息

        Args:
            message: 用户消息内容

        Returns:
            格式化的用户消息字典
        """
        return {"role": "user", "content": message}

    @staticmethod
    def assistant_message(message: str) -> dict:
        """
        创建助手角色的消息

        Args:
            message: 助手消息内容

        Returns:
            格式化的助手消息字典
        """
        return {"role": "assistant", "content": message}

    @staticmethod
    def str_to_approx_token_count(string: str) -> int:
        """
        估算字符串的大致token数量
        使用简单的启发式方法：每4个字符约等于1个token

        Args:
            string: 要估算的字符串

        Returns:
            估算的token数量
        """
        return len(string) / 4

    @staticmethod
    def add_ddl_to_prompt(
            initial_prompt: str, ddl_list: List[str], max_tokens: int = 14000
    ) -> str:
        """
        将DDL语句添加到初始提示中，同时控制总token数不超过最大限制

        Args:
            initial_prompt: 初始提示文本
            ddl_list: DDL语句列表
            max_tokens: 最大允许的token数

        Returns:
            添加了DDL语句的提示文本
        """
        if len(ddl_list) > 0:
            initial_prompt += "\nYou may use the following DDL statements as a reference for what tables might be available. Use responses to past questions also to guide you:\n\n"

            for ddl in ddl_list:
                if (
                        CustomChat.str_to_approx_token_count(initial_prompt)
                        + CustomChat.str_to_approx_token_count(ddl)
                        < max_tokens
                ):
                    initial_prompt += f"{ddl}\n\n"

        return initial_prompt

    @staticmethod
    def add_documentation_to_prompt(
            initial_prompt: str, documentation_List: List[str], max_tokens: int = 14000
    ) -> str:
        """
        将文档说明添加到初始提示中，同时控制总token数不超过最大限制

        Args:
            initial_prompt: 初始提示文本
            documentation_List: 文档说明列表
            max_tokens: 最大允许的token数

        Returns:
            添加了文档说明的提示文本
        """
        if len(documentation_List) > 0:
            initial_prompt += "\nYou may use the following documentation as a reference for what tables might be available. Use responses to past questions also to guide you:\n\n"

            for documentation in documentation_List:
                if (
                        CustomChat.str_to_approx_token_count(initial_prompt)
                        + CustomChat.str_to_approx_token_count(documentation)
                        < max_tokens
                ):
                    initial_prompt += f"{documentation}\n\n"

        return initial_prompt

    @staticmethod
    def add_sql_to_prompt(
            initial_prompt: str, sql_List: List[str], max_tokens: int = 14000
    ) -> str:
        """
        将SQL语句添加到初始提示中，同时控制总token数不超过最大限制

        Args:
            initial_prompt: 初始提示文本
            sql_List: SQL语句列表，每项包含问题和SQL
            max_tokens: 最大允许的token数

        Returns:
            添加了SQL语句的提示文本
        """
        if len(sql_List) > 0:
            initial_prompt += "\nYou may use the following SQL statements as a reference for what tables might be available. Use responses to past questions also to guide you:\n\n"

            for question in sql_List:
                if (
                        CustomChat.str_to_approx_token_count(initial_prompt)
                        + CustomChat.str_to_approx_token_count(question["sql"])
                        < max_tokens
                ):
                    initial_prompt += f"{question['question']}\n{question['sql']}\n\n"

        return initial_prompt

    def get_sql_prompt(
            self,
            question: str,
            question_sql_list: List,
            ddl_list: List,
            doc_list: List,
            **kwargs,
    ):
        """
        为SQL生成创建提示消息

        组合问题、历史示例、数据库结构等，形成完整的提示

        Args:
            question: 当前问题
            question_sql_list: 历史问题和SQL对的列表
            ddl_list: DDL语句列表
            doc_list: 文档说明列表
            **kwargs: 额外参数

        Returns:
            格式化的消息列表，用于提交给大语言模型
        """
        initial_prompt = "The user provides a question and you provide SQL. You will only respond with SQL code and not with any explanations.\n\nRespond with only SQL code. Do not answer with any explanations -- just the code.\n"

        # 添加DDL语句到提示中
        initial_prompt = self.add_ddl_to_prompt(
            initial_prompt=initial_prompt, ddl_list=ddl_list
        )

        # 添加文档说明到提示中
        initial_prompt = self.add_documentation_to_prompt(
            initial_prompt=initial_prompt, documentation_List=doc_list
        )

        # 添加SQL语句到提示中
        initial_prompt = self.add_sql_to_prompt(
            initial_prompt=initial_prompt, sql_List=question_sql_list
        )

        # 构建消息列表
        messages = [
            self.system_message(initial_prompt),
            self.user_message(f"Question: {question}\n\nSQL:"),
        ]

        return messages

    def get_followup_questions_prompt(
            self,
            question: str,
            df: pd.DataFrame,
            question_sql_list: List,
            ddl_list: List,
            doc_list: List,
            **kwargs,
    ):
        """
        为后续问题生成提示消息

        Args:
            question: 当前问题
            df: 查询结果数据框
            question_sql_list: 历史问题和SQL对的列表
            ddl_list: DDL语句列表
            doc_list: 文档说明列表
            **kwargs: 额外参数

        Returns:
            格式化的消息列表，用于提交给大语言模型
        """
        initial_prompt = "The user asked a question and got some results. Based on the results, suggest 3 follow-up questions that the user might want to ask. Make the questions specific and directly related to the data that was returned.\n\n"

        # 添加DDL语句到提示中
        initial_prompt = self.add_ddl_to_prompt(
            initial_prompt=initial_prompt, ddl_list=ddl_list
        )

        # 添加文档说明到提示中
        initial_prompt = self.add_documentation_to_prompt(
            initial_prompt=initial_prompt, documentation_List=doc_list
        )

        # 添加SQL语句到提示中
        initial_prompt = self.add_sql_to_prompt(
            initial_prompt=initial_prompt, sql_List=question_sql_list
        )

        # 构建消息列表
        messages = [
            self.system_message(initial_prompt),
            self.user_message(
                f"Question: {question}\n\nResults (first 5 rows):\n{df.head().to_string()}\n\nSuggest 3 follow-up questions:"
            ),
        ]

        return messages

    def generate_question(self, sql: str, **kwargs) -> str:
        """
        根据SQL生成自然语言问题

        Args:
            sql: SQL查询语句
            **kwargs: 额外参数

        Returns:
            生成的自然语言问题
        """
        try:
            # 构建消息列表
            messages = [
                self.system_message(
                    "Given an SQL query, generate a natural language question that the SQL query might be answering. Focus on the business meaning of the query."
                ),
                self.user_message(f"SQL: {sql}\n\nQuestion:"),
            ]

            # 提交到大语言模型
            question = self.submit_prompt(prompt=messages, max_tokens=100)
            return question
        except Exception as e:
            print(f"生成问题失败: {str(e)}")
            return "What does this query show?"

    def _extract_python_code(self, markdown_string: str) -> str:
        """
        从Markdown字符串中提取Python代码块

        Args:
            markdown_string: 包含代码块的Markdown字符串

        Returns:
            提取的Python代码
        """
        # 尝试匹配带有Python标记的代码块
        python_code_match = re.search(
            r"```(?:python|py)(.*?)```", markdown_string, re.DOTALL
        )
        if python_code_match:
            return python_code_match.group(1).strip()

        # 尝试匹配任何代码块
        code_match = re.search(r"```(.*?)```", markdown_string, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        # 如果没有找到代码块，返回原始字符串
        return markdown_string.strip()

    def _sanitize_plotly_code(self, raw_plotly_code: str) -> str:
        """
        清理和标准化Plotly代码

        Args:
            raw_plotly_code: 原始Plotly代码

        Returns:
            清理后的Plotly代码
        """
        # 如果代码以 import 开头，直接返回
        if raw_plotly_code.strip().startswith("import"):
            return raw_plotly_code

        # 添加必要的导入语句
        return "import plotly.express as px\nimport plotly.graph_objects as go\n\n" + raw_plotly_code

    def generate_plotly_code(
            self, question: str = None, sql: str = None, df_metadata: str = None, **kwargs
    ) -> str:
        """
        生成Plotly可视化代码

        Args:
            question: 用户问题
            sql: SQL查询
            df_metadata: 数据框元数据
            **kwargs: 额外参数

        Returns:
            Plotly可视化代码
        """
        try:
            # 构建消息列表
            messages = [
                self.system_message(
                    "You are an expert at data visualization using Plotly. Given a question, SQL query, and dataframe metadata, generate Python code using Plotly to visualize the data. Only respond with the Python code, no explanations."
                ),
                self.user_message(
                    f"Question: {question}\n\nSQL: {sql}\n\n{df_metadata}\n\nWrite Python code using Plotly to visualize this data:"
                ),
            ]

            # 提交到大语言模型
            plotly_code = self.submit_prompt(prompt=messages, max_tokens=1000)

            # 提取和清理代码
            extracted_code = self._extract_python_code(plotly_code)
            sanitized_code = self._sanitize_plotly_code(extracted_code)

            return sanitized_code
        except Exception as e:
            print(f"生成Plotly代码失败: {str(e)}")
            return "import plotly.express as px\n\nfig = px.bar(df, title='Data Visualization')\n"

    def submit_prompt(
            self, prompt, max_tokens=512, temperature=0.7, top_p=0.7, stop=None, **kwargs
    ):
        """
        提交提示到大语言模型并获取响应

        Args:
            prompt: 提示消息列表
            max_tokens: 最大生成token数
            temperature: 温度参数
            top_p: 核采样参数
            stop: 停止序列
            **kwargs: 额外参数

        Returns:
            模型生成的响应文本
        """
        try:
            # 创建OpenAI客户端
            client = OpenAI(api_key=self.api_key, base_url=self.api_base)
            
            # 确保模型名称不为空
            model = self.model if self.model else "gpt-3.5-turbo"
            
            # 打印提交的提示，便于调试
            print(f"提交提示: {prompt}")
            
            # 确保所有参数都有效
            params = {
                "model": model,
                "messages": prompt,
                "temperature": temperature,
                "top_p": top_p
            }
            
            # 只添加非空参数
            if max_tokens and max_tokens > 0:
                params["max_tokens"] = max_tokens
            
            if stop:
                params["stop"] = stop
                
            # 添加额外参数
            for k, v in kwargs.items():
                if v is not None:
                    params[k] = v

            # 提交请求
            response = client.chat.completions.create(**params)

            # 返回生成的文本
            return response.choices[0].message.content
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise Exception(f"提交提示失败: {str(e)}") 