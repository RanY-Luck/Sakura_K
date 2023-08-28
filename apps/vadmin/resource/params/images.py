"""
@Project : Sakura_K
@File    : images.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/8/28 16:20
@Desc    : 
"""
from fastapi import Depends

from core.dependencies import Paging, QueryParams


class ImagesParams(QueryParams):
    """
    列表分页
    """

    def __init__(self, filename: str = None, params: Paging = Depends()):
        super().__init__(params)
        self.filename = ("like", filename)
        self.v_order = "desc"
        self.v_order_field = "create_datetime"
