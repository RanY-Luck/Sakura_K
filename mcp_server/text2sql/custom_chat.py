#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/22 17:01
# @Author   : 冉勇
# @File     : custom_chat.py
# @Software : PyCharm
# @Desc     : 重组Vanna聊天，适配多种模型
import re
from typing import List
import pandas as pd
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

        initial_prompt = CustomChat.add_ddl_to_prompt(
            initial_prompt, ddl_list, max_tokens=14000
        )

        initial_prompt = CustomChat.add_documentation_to_prompt(
            initial_prompt, doc_list, max_tokens=14000
        )

        message_log = [CustomChat.system_message(initial_prompt)]

        for example in question_sql_list:
            if example is None:
                print("example is None")
            else:
                if example is not None and "question" in example and "sql" in example:
                    message_log.append(CustomChat.user_message(example["question"]))
                    message_log.append(CustomChat.assistant_message(example["sql"]))

        message_log.append({"role": "user", "content": question})

        return message_log

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
        为生成后续问题创建提示消息

        基于原始问题和已有数据，生成用户可能的后续问题

        Args:
            question: 原始问题
            df: 查询结果数据框
            question_sql_list: 历史问题和SQL对的列表
            ddl_list: DDL语句列表
            doc_list: 文档说明列表
            **kwargs: 额外参数

        Returns:
            格式化的消息列表，用于提交给大语言模型
        """
        initial_prompt = f"The user initially asked the question: '{question}': \n\n"

        initial_prompt = CustomChat.add_ddl_to_prompt(
            initial_prompt, ddl_list, max_tokens=14000
        )

        initial_prompt = CustomChat.add_documentation_to_prompt(
            initial_prompt, doc_list, max_tokens=14000
        )

        initial_prompt = CustomChat.add_sql_to_prompt(
            initial_prompt, question_sql_list, max_tokens=14000
        )

        message_log = [CustomChat.system_message(initial_prompt)]
        message_log.append(
            CustomChat.user_message(
                "Generate a List of followup questions that the user might ask about this data. Respond with a List of questions, one per line. Do not answer with any explanations -- just the questions."
            )
        )

        return message_log

    def generate_question(self, sql: str, **kwargs) -> str:
        """
        从SQL生成对应的自然语言问题

        尝试猜测给定的SQL查询可能回答的业务问题

        Args:
            sql: SQL查询字符串
            **kwargs: 额外参数

        Returns:
            生成的自然语言问题
        """
        response = self.submit_prompt(
            [
                self.system_message(
                    "The user will give you SQL and you will try to guess what the business question this query is answering. Return just the question without any additional explanation. Do not reference the table name in the question."
                ),
                self.user_message(sql),
            ],
            **kwargs,
        )

        return response

    def _extract_python_code(self, markdown_string: str) -> str:
        """
        从markdown字符串中提取Python代码块

        Args:
            markdown_string: 包含代码块的markdown字符串

        Returns:
            提取的Python代码，如果没有找到则返回原始字符串
        """
        # 匹配Python代码块的正则表达式模式
        pattern = r"```[\w\s]*python\n([\s\S]*?)```|```([\s\S]*?)```"

        # 在markdown字符串中找到所有匹配项
        matches = re.findall(pattern, markdown_string, re.IGNORECASE)

        # 从匹配项中提取Python代码
        python_code = []
        for match in matches:
            python = match[0] if match[0] else match[1]
            python_code.append(python.strip())

        if len(python_code) == 0:
            return markdown_string

        return python_code[0]

    def _sanitize_plotly_code(self, raw_plotly_code: str) -> str:
        """
        清理Plotly代码，移除fig.show()语句

        Args:
            raw_plotly_code: 原始Plotly代码

        Returns:
            清理后的Plotly代码
        """
        # 移除fig.show()语句
        plotly_code = raw_plotly_code.replace("fig.show()", "")

        return plotly_code

    def generate_plotly_code(
            self, question: str = None, sql: str = None, df_metadata: str = None, **kwargs
    ) -> str:
        """
        生成用于可视化数据的Plotly代码

        根据问题、SQL查询和数据框元数据，生成适当的可视化代码

        Args:
            question: 原始问题
            sql: SQL查询
            df_metadata: 数据框的元数据信息
            **kwargs: 额外参数

        Returns:
            生成的Plotly代码
        """
        if question is not None:
            system_msg = f"The following is a pandas DataFrame that contains the results of the query that answers the question the user asked: '{question}'"
        else:
            system_msg = "The following is a pandas DataFrame "

        if sql is not None:
            system_msg += f"\n\nThe DataFrame was produced using this query: {sql}\n\n"

        system_msg += f"The following is information about the resulting pandas DataFrame 'df': \n{df_metadata}"

        message_log = [
            self.system_message(system_msg),
            self.user_message(
                "Can you generate the Python plotly code to chart the results of the dataframe? Assume the data is in a pandas dataframe called 'df'. If there is only one value in the dataframe, use an Indicator. Respond with only Python code. Do not answer with any explanations -- just the code."
            ),
        ]

        plotly_code = self.submit_prompt(message_log, kwargs=kwargs)

        return self._sanitize_plotly_code(self._extract_python_code(plotly_code))

    def submit_prompt(
            self, prompt, max_tokens=512, temperature=0.7, top_p=0.7, stop=None, **kwargs
    ):
        """
        向大语言模型提交提示并获取响应

        Args:
            prompt: 提示消息列表
            max_tokens: 生成的最大token数
            temperature: 采样温度
            top_p: 概率质量
            stop: 停止标记
            **kwargs: 额外参数

        Returns:
            模型生成的响应文本
        """
        if prompt is None:
            raise Exception("Prompt is None")

        if len(prompt) == 0:
            raise Exception("Prompt is empty")

        # print("prompt: ", prompt)

        # client = self.ChatAPI(api_key=self.api_key, base_url=self.api_base)
        try:
            # 尝试初始化OpenAI客户端
            client = OpenAI(api_key=self.api_key, base_url=self.api_base)
        except:
            # 如果失败，使用失效转移功能重试
            client = OpenAI(
                api_key=self.api_key,
                base_url=self.api_base,
                default_headers={"X-Failover-Enabled": "true"}
            )

        # 调用大语言模型生成回复
        response = client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            # stop=stop,
            messages=prompt,
        )

        result = response.choices[0].message.content
        # 处理结果，移除思考过程（如果存在）
        if result.find('</think>') != -1:
            start = result.find('</think>') + len('</think>')
            result = result[start:].strip()

        return result
