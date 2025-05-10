#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/10 15:38
# @Author  : 冉勇
# @Site    : 
# @File    : scheduler_getLatestReport.py
# @Software: PyCharm
# @desc    : 监控正式服上报数据
import requests
import json
from datetime import datetime

# 企业微信机器人webhook URL，请替换为你的实际URL
WEBHOOK = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=ce91ea89-0fc4-43b2-9584-aefc9324a17f"

# 需要@的人员手机号列表，示例格式
AT_MOBILES = ["13206269804", "15112673242"]


def monitor_api():
    """监控接口是否有数据上报"""
    url = "https://www.convercomm.com/api/admin/openapi/getLatestReport?pwd=CEmA2ynTA6%29ia&minutes=15"

    payload = {}
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Accept': '*/*',
        'Host': 'www.convercomm.com',
        'Connection': 'keep-alive'
    }

    try:
        # 发送请求
        response = requests.request("GET", url, headers=headers, data=payload)

        # 检查HTTP状态码
        if response.status_code != 200:
            return False, f"HTTP请求失败，状态码: {response.status_code}"

        # 解析响应
        try:
            data = json.loads(response.text)

            # 检查API返回的状态码
            if "statusCode" in data:
                if data["statusCode"] == 500:
                    error_msg = f"无数据上报: {data.get('data')}"
                    print("error_msg-->", error_msg)
                    return False, error_msg
                elif data["statusCode"] == 200:
                    return True, "数据上报正常"
                else:
                    error_msg = f"未知状态码: {data['statusCode']}"
                    return False, error_msg
            else:
                error_msg = "响应中缺少statusCode字段"
                return False, error_msg

        except json.JSONDecodeError:
            error_msg = "响应不是有效的JSON格式"
            return False, error_msg

    except requests.exceptions.RequestException as e:
        error_msg = f"请求异常: {str(e)}"
        return False, error_msg
    except Exception as e:
        return False, str(e)


def send_webhook_notification(success, message):
    """发送企业微信通知"""
    # 只在数据上报异常时发送通知
    if success:
        return

    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    title = "❌ 异动通正式服数据上报异常警报"
    content = f"[{current_time}] 数据上报警报：{message}"

    # 构建通知消息
    headers = {"Content-Type": "application/json"}

    # 企业微信机器人消息格式
    send_data = {
        "msgtype": "text",
        "text": {
            "content": f"{title}\n{content}\n请相关同事注意检查。",
            "mentioned_mobile_list": AT_MOBILES
        }
    }
    requests.post(url=WEBHOOK, headers=headers, json=send_data)


# if __name__ == "__main__":
#     # 监控API
#     success, result = monitor_api()
#
#     # 控制台输出结果
#     if success:
#         print("✓ API数据上报正常")
#     else:
#         print(f"✗ API数据上报异常: {result}")
#         # 只在异常时发送企业微信通知
#         send_webhook_notification(success, result)
