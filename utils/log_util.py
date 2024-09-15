#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:51
# @Author  : 冉勇
# @Site    :
# @File    : log_util.py
# @Software: PyCharm
# @desc    : 日志工具
import os
import time
import datetime
import zipfile
from loguru import logger
from functools import partial

# 日志路径
log_path = os.path.join(os.getcwd(), 'logs')
# 判断是否创建
if not os.path.exists(log_path):
    os.mkdir(log_path)


# 创建一个函数来动态生成日志文件路径
def get_log_path(log_type):
    return os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_{log_type}.log')


# 创建一个自定义的 sink 函数
def custom_sink(message, log_type):
    log_path = get_log_path(log_type)
    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(message)


# 为每种日志类型添加 logger
logger.add(partial(custom_sink, log_type="info"), level="INFO")
logger.add(partial(custom_sink, log_type="error"), level="ERROR")
logger.add(partial(custom_sink, log_type="warn"), level="WARNING")


def archive_and_delete_yesterdays_logs():
    yesterday = datetime.date.today() - datetime.timedelta(days=1)
    yesterday_str = yesterday.strftime("%Y-%m-%d")

    # 创建存档目录
    archive_dir = os.path.join(log_path, "archives")
    os.makedirs(archive_dir, exist_ok=True)

    # 查找昨天的日志文件
    log_files = [f for f in os.listdir(log_path) if f.startswith(f"{yesterday_str}") and f.endswith(".log")]

    if log_files:
        # 创建ZIP文件
        zip_filename = os.path.join(archive_dir, f"logs_{yesterday_str}.zip")
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for log_file in log_files:
                file_path = os.path.join(log_path, log_file)
                zipf.write(file_path, log_file)

        # 删除原始日志文件
        for log_file in log_files:
            file_path = os.path.join(log_path, log_file)
            os.remove(file_path)
        print(f"昨天的日志已打包到 {zip_filename}")
    else:
        print("没有找到昨天的日志文件")


# # 示例：如何使用更新后的日志系统
# if __name__ == "__main__":
#     logger.info("这是一条信息日志")
#     logger.error("这是一条错误日志")
#     logger.warning("这是一条警告日志")
#
#     # 模拟第二天的日志
#     time.sleep(2)  # 等待2秒，确保日期变更（在实际使用中不需要这行）
#     logger.info("这是第二天的信息日志")
#
#     # 执行日志归档
#     archive_and_delete_yesterdays_logs()
