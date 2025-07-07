#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025-05-28 18:10:00
# @Author   : 冉勇
# @File     : embedding.py
# @Software : PyCharm
# @Desc     : SiliconFlow嵌入模型API封装

import requests
from types import SimpleNamespace
from typing import Any, Union, List


def convert_to_namespace(obj: Any) -> Any:
    """Recursively convert a dictionary or list to a SimpleNamespace object."""
    if isinstance(obj, dict):
        return SimpleNamespace(**{k: convert_to_namespace(v) for k, v in obj.items()})
    elif isinstance(obj, list):
        return [convert_to_namespace(item) for item in obj]
    else:
        return obj


class SiliconFlowAI:
    def __init__(self, api_key, base_url="https://api.siliconflow.cn/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.chat = self.Chat(self)  # 初始化chat子对象

    class Chat:
        def __init__(self, outer):
            self.outer = outer  # 保存外部类的引用
            self.completions = self.Completions(self)  # 初始化completions子对象

        class Completions:
            def __init__(self, outer):
                self.outer = outer  # 保存外部类的引用

            def create(self, model, messages, **kwargs):
                """
                创建聊天补全

                参数:
                - model: 模型名称 (如 "Qwen/QwQ-32B")
                - messages: 消息列表
                - **kwargs: 其他可选参数:
                    - stream: 是否流式输出 (默认False)
                    - max_tokens: 最大token数
                    - temperature: 温度参数
                    - top_p: top_p采样参数
                    - top_k: top_k采样参数
                    - frequency_penalty: 频率惩罚
                    - response_format: 响应格式
                    - tools: 工具列表
                """
                url = f"{self.outer.outer.base_url}/chat/completions"

                payload = {
                    "model": model,
                    "messages": messages,
                    "stream": kwargs.get("stream", False),
                    "max_tokens": kwargs.get("max_tokens", 512),
                    "stop": kwargs.get("stop", None),
                    "temperature": kwargs.get("temperature", 0.7),
                    "top_p": kwargs.get("top_p", 0.7),
                    "top_k": kwargs.get("top_k", 50),
                    "frequency_penalty": kwargs.get("frequency_penalty", 0.5),
                    "n": kwargs.get("n", 1),
                    "response_format": kwargs.get("response_format", {"type": "text"}),
                    "tools": kwargs.get("tools", None)
                }

                headers = {
                    "Authorization": f"Bearer {self.outer.outer.api_key}",
                    "Content-Type": "application/json"
                }

                response = requests.post(url, json=payload, headers=headers)
                return convert_to_namespace(response.json())


class SiliconflowEmbedding:
    """A client for the Siliconflow Embeddings API with chainable call style.

    Example usage:
        >>> sf = SiliconflowEmbedding(api_key="your_api_key")
        >>> result = sf.embeddings.create(model="your_model", input="your_text")
    """

    def __init__(self, api_key: str):
        """Initialize the embedding client.

        Args:
            api_key: Your Siliconflow API key
        """
        self.api_key = api_key
        self.embeddings = self._Embeddings(self)

    class _Embeddings:
        """Inner class handling embeddings operations."""

        def __init__(self, parent):
            self._parent = parent
            self._url = "https://api.siliconflow.cn/v1/embeddings"
            self._headers = {
                "Authorization": f"Bearer {self._parent.api_key}",
                "Content-Type": "application/json"
            }

        def create(
                self,
                model: str,
                input: Union[str, List[str]],
                encoding_format: str = "float"
        ) -> SimpleNamespace:
            """Create embeddings for the input text(s).

            Args:
                model: The model ID to use for embedding
                input: Input text or list of texts to embed
                encoding_format: The format of the output embeddings

            Returns:
                API response as a dictionary
            """
            if not input:
                raise ValueError("Input cannot be empty")

            response = requests.post(
                self._url,
                json={
                    "model": model,
                    "input": input,
                    "encoding_format": encoding_format
                },
                headers=self._headers
            )

            response.raise_for_status()
            return convert_to_namespace(response.json()) 