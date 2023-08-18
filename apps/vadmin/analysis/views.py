#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 16:54
# @Author  : 冉勇
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    :
from fastapi import APIRouter, Depends

from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from utils.response import SuccessResponse

app = APIRouter()


###########################################################
#                     图表数据                             #
###########################################################
@app.get("/banners", summary="轮播图")
async def get_banners(auth: Auth = Depends(AllUserAuth())):
    data = [
        {
            "id": 1,
            "image": "https://images.pexels.com/photos/2662116/pexels-photo-2662116.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        },
        {
            "id": 2,
            "image": "https://images.pexels.com/photos/4014845/pexels-photo-4014845.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        },
        {
            "id": 3,
            "image": "https://images.pexels.com/photos/1287145/pexels-photo-1287145.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=2"
        },
    ]
    return SuccessResponse(data)


@app.get("/user/access/source", summary="用户来源")
async def get_user_access_source(auth: Auth = Depends(AllUserAuth())):
    data = [
        {"value": 1000, "name": 'analysis.directAccess'},
        {"value": 310, "name": 'analysis.mailMarketing'},
        {"value": 234, "name": 'analysis.allianceAdvertising'},
        {"value": 135, "name": 'analysis.videoAdvertising'},
        {"value": 1548, "name": 'analysis.searchEngines'}
    ]
    return SuccessResponse(data)


@app.get("/weekly/user/activity", summary="每周用户活跃量")
async def get_weekly_user_activity(auth: Auth = Depends(AllUserAuth())):
    data = [
        {"value": 13253, "name": 'analysis.monday'},
        {"value": 34235, "name": 'analysis.tuesday'},
        {"value": 26321, "name": 'analysis.wednesday'},
        {"value": 12340, "name": 'analysis.thursday'},
        {"value": 24643, "name": 'analysis.friday'},
        {"value": 1322, "name": 'analysis.saturday'},
        {"value": 1324, "name": 'analysis.sunday'}
    ]
    return SuccessResponse(data)


@app.get("/monthly/sales", summary="每月销售额")
async def get_monthly_sales(auth: Auth = Depends(AllUserAuth())):
    data = [
        {"estimate": 100, "actual": 120, "name": 'analysis.january'},
        {"estimate": 120, "actual": 82, "name": 'analysis.february'},
        {"estimate": 161, "actual": 91, "name": 'analysis.march'},
        {"estimate": 134, "actual": 154, "name": 'analysis.april'},
        {"estimate": 105, "actual": 162, "name": 'analysis.may'},
        {"estimate": 160, "actual": 140, "name": 'analysis.june'},
        {"estimate": 165, "actual": 145, "name": 'analysis.july'},
        {"estimate": 114, "actual": 250, "name": 'analysis.august'},
        {"estimate": 163, "actual": 134, "name": 'analysis.september'},
        {"estimate": 185, "actual": 56, "name": 'analysis.october'},
        {"estimate": 118, "actual": 99, "name": 'analysis.november'},
        {"estimate": 123, "actual": 123, "name": 'analysis.december'}
    ]
    return SuccessResponse(data)
