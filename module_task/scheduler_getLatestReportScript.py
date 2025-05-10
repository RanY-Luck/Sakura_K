#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/10 16:59
# @Author  : 冉勇
# @Site    : 
# @File    : scheduler_getLatestReportScript.py
# @Software: PyCharm
# @desc    : 每1分钟监控正式服数据上报
from module_task.scheduler_getLatestReport import monitor_api, send_webhook_notification


async def monitor():
    success, result = monitor_api()
    # 控制台输出结果
    if success:
        pass
    else:
        # 只在异常时发送企业微信通知
        send_webhook_notification(success, result)
