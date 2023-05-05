#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : {create_datetime}
# @Author  :
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    :
from fastapi import APIRouter, Depends
from utils.response import SuccessResponse
from . import crud
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import Auth

app = APIRouter()
