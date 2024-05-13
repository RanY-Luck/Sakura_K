#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/5/11 22:20
# @Author  : 冉勇
# @Site    : 
# @File    : server_status.py
# @Software: PyCharm
# @desc    : 服务器状态
import psutil
import time

# 全局变量
EXPAND = 1024 * 1024


# 获取 CPU 当前状态
def get_cpu_status():
    status_infos = {}
    # 当前 CPU 占用率
    status_infos["percent"] = str(psutil.cpu_percent(0)) + "%"
    return status_infos


# 获取内存使用状态
def get_memory_status():
    status_infos = {}
    mem = psutil.virtual_memory()
    # 当前内存使用量
    status_infos["used"] = str(round(mem.used / EXPAND, 2)) + " Mb"
    # 当前内存总量
    status_infos["total"] = str(round(mem.total / EXPAND, 2)) + " Mb"
    # 当前内存占用率
    status_infos["percent"] = str(psutil.virtual_memory().percent) + "%"
    return status_infos


# 获取硬盘使用情况
def get_disk_status():
    status_infos = {}
    # 计算总磁盘量
    status_infos["used"] = 0
    status_infos["total"] = 0
    status_infos["free"] = 0
    # 获取所有磁盘
    disks = psutil.disk_partitions()
    status_infos["disks"] = {}
    for disk in disks:
        disk_key = disk.device
        # 初始化这个磁盘的所有信息
        status_infos["disks"][disk_key] = {}
        disk = psutil.disk_usage(disk_key)
        # 当前该磁盘使用量
        status_infos["disks"][disk_key]["used"] = str(
            round(disk.used / EXPAND, 2)
        ) + " Mb"
        # 当前该磁盘总量
        status_infos["disks"][disk_key]["total"] = str(
            round(disk.total / EXPAND, 2)
        ) + " Mb"
        # 当前该磁盘剩余空间
        status_infos["disks"][disk_key]["free"] = str(
            round(disk.free / EXPAND, 2)
        ) + " Mb"
        # 磁盘利用率
        status_infos["disks"][disk_key]["percent"] = str(
            round((disk.used / disk.total) * 100, 2)
        ) + "%"
        # 最后计入总量
        status_infos["used"] += round(disk.used / EXPAND, 2)
        status_infos["total"] += round(disk.total / EXPAND, 2)
        status_infos["free"] += round(disk.free / EXPAND, 2)
    # 算出总磁盘使用率
    per = status_infos["used"] / status_infos["total"]
    status_infos["percent"] = str(round(per * 100, 2)) + "%"
    status_infos["used"] = str(round(status_infos["used"])) + " Mb"
    status_infos["total"] = str(round(status_infos["total"])) + " Mb"
    status_infos["free"] = str(round(status_infos["free"])) + " Mb"
    return status_infos


# 获取所有状态
def get_all():
    server_status_infos = {}
    server_status_infos["cpu"] = get_cpu_status()
    server_status_infos["memory"] = get_memory_status()
    server_status_infos["disk"] = get_disk_status()
    return server_status_infos


if __name__ == "__main__":
    for _ in range(0, 100):
        print(f"获取 CPU:{get_cpu_status()}")
        print(f"获取内存:{get_memory_status()}")
        print(f"获取硬盘使用情况:{get_disk_status()}")
        time.sleep(1)
