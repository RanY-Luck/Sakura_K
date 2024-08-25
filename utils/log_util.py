#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/5 10:51
# @Author  : 冉勇
# @Site    : 
# @File    : log_util.py
# @Software: PyCharm
# @desc    : 日志工具
import os
import sys
import time
import datetime
import zipfile
from loguru import logger

# 日志路径
log_path = os.path.join(os.getcwd(), 'logs')
# 判断是否创建
if not os.path.exists(log_path):
    os.mkdir(log_path)

# 日志名称
log_path_info = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_info.log')
log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')
log_path_warn = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_warn.log')

# 移除默认的处理器
logger.remove()

# 添加控制台输出，保留颜色
logger.add(
    sys.stderr,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)
logger.add(
    sys.stderr,
    format="<red>{time:YYYY-MM-DD HH:mm:ss}</red> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="ERROR"
)
logger.add(
    sys.stderr,
    format="<yellow>{time:YYYY-MM-DD HH:mm:ss}</yellow> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="ERROR"
)

# 保留你原有的文件输出配置
logger.add(
    log_path_info,
    retention=10,
    enqueue=True,
    encoding="UTF-8",
    level="INFO"
)
logger.add(
    log_path_error,
    retention=10,
    enqueue=True,
    encoding="UTF-8",
    level="ERROR"
)
logger.add(
    log_path_warn,
    retention=10,
    enqueue=True,
    encoding="UTF-8",
    level="WARNING"
)


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

# 调用函数来打包并删除昨天的日志
# archive_and_delete_yesterdays_logs()
