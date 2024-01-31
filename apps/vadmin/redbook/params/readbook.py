"""
@Project : Sakura_K
@File    : readbook.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/10/13 10:58
@Desc    : 列表分页查询1
"""
from fastapi import Depends

from core.dependencies import Paging, QueryParams


class RedBookParams(QueryParams):
    """
    列表分页
    """

    def __init__(
            self,
            filename: str = None,
            params: Paging = Depends()
    ):
        super().__init__(params)
        self.filename = ('like', filename)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
