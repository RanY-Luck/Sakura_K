#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/24 11:30
# @Author  : 冉勇
# @Site    : 
# @File    : redis.py
# @Software: PyCharm
# @desc    : redis 监控
from fastapi import APIRouter, Depends
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from utils.redis_info import redis_info
from utils.response import SuccessResponse

app = APIRouter()


###########################################################
#                    redis 监控                            #
###########################################################
@app.get("/redis", summary="redis 监控")
async def get_redis_info(auth: Auth = Depends(AllUserAuth())):
    """IO密集型任务，使用线程池尽量减少性能损耗"""
    data = {'info': await redis_info.get_info(), 'stats': await redis_info.get_stats()}
    return SuccessResponse(data=data)
