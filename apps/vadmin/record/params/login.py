#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 10:47
# @Author  : 冉勇
# @Site    :
# @File    : login.py
# @Software: PyCharm
# @desc    : 查询参数-类依赖项
"""
类依赖项-官方文档：https://fastapi.tiangolo.com/zh/tutorial/dependencies/classes-as-dependencies/
"""
from fastapi import Depends

from core.dependencies import Paging, QueryParams


class LoginParams(QueryParams):
    """
    列表分页
    代码解释：
    定义了一个名为 LoginParams 的类，它继承了另外一个名为 QueryParams 的类。
    在 FastAPI 中，Depends 函数可以用于注入依赖项，例如数据库连接或配置文件等。在这个例子中，依赖项是 Paging 和 QueryParams。
    LoginParams 类的构造函数接受多个参数，其中包括 ip、address、telephone、status 和 platform。这些参数都有默认值为 None，因此它们都是可选的。
    在构造函数中，首先调用了父类 QueryParams 的构造函数，将参数 params 传递给它。
    然后，将传递进来的参数赋值给类属性 self.ip、self.telephone、self.address、self.status 和 self.platform。
    值得注意的是，telephone 属性被设置为一个元组，第一个元素是字符串 "like"，第二个元素是传递进来的 telephone 参数。
    这意味着在查询数据库时，telephone 将被用作模糊查询，以便匹配所有包含指定字符串的电话号码。
    """

    def __init__(
            self,
            ip: str = None,
            address: str = None,
            telephone: str = None,
            status: bool = None,
            platform: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.ip = ("like", ip)
        self.telephone = ("like", telephone)
        self.address = ("like", address)
        self.status = status
        self.platform = platform
