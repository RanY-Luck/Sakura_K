#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/2/8 10:17
# @Author   : 冉勇
# @File     : utils.py
# @Software : PyCharm
# @Desc     :
import re
from datetime import datetime
from bs4 import BeautifulSoup


def format_date(value, date_format="%m-%d"):
    """ 将日期字符串转换为指定格式 """
    if isinstance(value, str):
        try:
            date_obj = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            return date_obj.strftime(date_format)
        except ValueError:
            return value  # 如果格式不对，返回原始值
    return value


# def remove_html_tags(text):
#     # 正则表达式去掉 HTML 标签
#     clean_text = re.sub(r'<.*?>', '', text)
#     return clean_text

def remove_html_tags(text):
    # 正则表达式去掉 HTML 标签
    soup = BeautifulSoup(text, "html.parser")
    # 获取纯文本
    plain_text = soup.get_text()
    return plain_text


