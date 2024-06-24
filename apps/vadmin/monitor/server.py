#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/6/24 11:30
# @Author  : 冉勇
# @Site    : 
# @File    : server.py
# @Software: PyCharm
# @desc    : server 监控
from fastapi import APIRouter, Depends
from starlette.concurrency import run_in_threadpool
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from utils.response import SuccessResponse
from utils.server_info import server_info

app = APIRouter()


###########################################################
#                   server 监控                           #
###########################################################
@app.get("/server", summary="server 监控")
async def get_server_info(auth: Auth = Depends(AllUserAuth())):
    """IO密集型任务，使用线程池尽量减少性能损耗"""
    data = {
        'cpu': await run_in_threadpool(server_info.get_cpu_info),
        'mem': await run_in_threadpool(server_info.get_mem_info),
        'sys': await run_in_threadpool(server_info.get_sys_info),
        'disk': await run_in_threadpool(server_info.get_disk_info),
        'service': await run_in_threadpool(server_info.get_service_info)
    }
    return SuccessResponse(data=data)
