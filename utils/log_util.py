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
from loguru import logger as _logger
from typing import Dict
from middlewares.trace_middleware import TraceCtx
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
    record = message.record
    if record["level"].name.lower() == log_type:
        log_path = get_log_path(log_type)
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(message)


# 为每种日志类型添加 logger
logger.add(partial(custom_sink, log_type="info"), level="INFO")
logger.add(partial(custom_sink, log_type="error"), level="ERROR")
logger.add(partial(custom_sink, log_type="warning"), level="WARNING")


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


# 示例：如何使用更新后的日志系统
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


class LoggerInitializer:
    def __init__(self):
        self.log_path = os.path.join(os.getcwd(), 'logs')
        self.__ensure_log_directory_exists()
        self.log_path_error = os.path.join(self.log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

    def __ensure_log_directory_exists(self):
        """
        确保日志目录存在，如果不存在则创建
        """
        if not os.path.exists(self.log_path):
            os.mkdir(self.log_path)

    @staticmethod
    def __filter(log: Dict):
        """
        自定义日志过滤器，添加trace_id
        """
        log['trace_id'] = TraceCtx.get_id()
        return log

    def init_log(self):
        """
        初始化日志配置
        """
        # 自定义日志格式
        format_str = (
            '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | '
            '<cyan>{trace_id}</cyan> | '
            '<level>{level: <8}</level> | '
            '<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - '
            '<level>{message}</level>'
        )
        _logger.remove()
        # 移除后重新添加sys.stderr, 目的: 控制台输出与文件日志内容和结构一致
        _logger.add(sys.stderr, filter=self.__filter, format=format_str, enqueue=True)
        _logger.add(
            self.log_path_error,
            filter=self.__filter,
            format=format_str,
            rotation='50MB',
            encoding='utf-8',
            enqueue=True,
            compression='zip',
        )

        return _logger


# 初始化日志处理器
log_initializer = LoggerInitializer()
logger = log_initializer.init_log()