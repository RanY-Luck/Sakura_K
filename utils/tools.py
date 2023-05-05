#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 15:00
# @Author  : 冉勇
# @Site    : 
# @File    : tools.py
# @Software: PyCharm
# @desc    : 工具类
import datetime
import random
import re
import string
import importlib
from typing import List, Union
from core.logger import logger


def test_password(password: str) -> Union[str, bool]:
    """
    检测密码强度
    :param password:
    :return:
    解释代码：
    1、密码长度需为 8-16 个字符。
    2、密码不能包含空格或中文字符。
    3、密码必须至少包含数字、大小写字母和字符中的两种组合。
    首先判断密码长度是否在 8-16 个字符之间，如果不在这个范围内，则直接返回相应的错误信息。
    然后开始进行密码字符的遍历，判断是否包含中文字符或空格。
    通过 ord() 函数将字符转换为 unicode 编码，判断编码是否处于中文字符或者空格的范围内，如果是则返回相应的错误信息。
    接下来使用正则表达式判断密码是否包含数字、大小写字母和字符。
    通过 re.search() 函数在密码中搜索符合条件的字符，结果为 None 则表示未找到，反之则表示找到了符合条件的字符。
    根据符合条件的字符个数确定 key 的值。
    最后，判断 key 是否大于等于 2，如果是则返回 True 表示密码符合要求，反之则返回相应的错误信息。
    """
    if len(password) < 8 or len(password) > 16:
        return "长度需为8-16个字符，请重新输入~"
    else:
        for i in password:
            if 0x4e00 <= ord(i) <= 0x9fa5 or ord(i) == 0x20:  # Ox4e00等十六进制数分别为中文字符和空格的Unicode编码
                return "不能使用空格、中文，请重新输入~"
        else:
            key = 0
            key += 1 if bool(re.search(r'\d', password)) else 0
            key += 1 if bool(re.search(r'[A-Za-z]', password)) else 0
            key += 1 if bool(re.search(f"\W", password)) else 0
            if key >= 2:
                return True
            else:
                return "至少含数字、字母、字符两种组合，请重新输入~"


def list_dict_find(options: List[dict], key: str, value: any) -> Union[dict, None]:
    """
    字典列表中通过指定的 key 和 value 查找符合条件的字典，并返回这个字典。如果列表中没有符合条件的字典，函数将返回 None。
    :param options: 需要查找的包含多个字典的列表
    :param key: 要匹配的键值对的键名
    :param value: 要匹配的键值对的值
    :return:
    代码解释：
    函数使用 for 循环遍历 options 列表中的每个字典对象 item。
    在循环中，对于每个字典对象，使用字典的 get() 方法通过 key 获取 value，与传入的 value 进行比较，判断是否相等。
    如果相等，说明已经找到符合条件的字典对象，直接返回该字典对象。
    如果循环中没有找到符合条件的字典对象，则说明 options 中没有包含指定的 key 和 value 的字典，此时函数返回 None。
    """
    for item in options:
        if item.get(key) == value:
            return item
    return None


def get_item_interval(start_time: str, end_time: str, interval: int, time_format: str = "%H:%M:%S") -> List:
    """
    获取时间间隔
    :param start_time: 起始时间
    :param end_time: 结束时间
    :param interval: 时间间隔
    :param time_format: 时间格式
    :return:
    代码解释：
    首先对起始时间和结束时间做一些格式调整处理：如果起始时间或结束时间仅给出了小时和分钟，缺少秒数，则在字符串末尾补充 ":00"。
    然后使用 datetime.datetime.strptime() 方法将起始时间和结束时间从字符串格式转换为 datetime.datetime 类型。
    然后建立一个空列表 time_range 用于存放按指定时间间隔划分后的时间点。
    在 while 循环中，每次将当前时间点通过 start_time.strftime() 方法转换成字符串格式，添加到 time_range 列表中，
    然后将当前时间点加上 timedelta(minutes=interval) 进行时间间隔的跳跃。
    最后返回 time_range 列表即可。
    需要注意的是，时间格式的默认值为 "%H:%M:%S"，即时分秒的格式
    """
    if start_time.count(":") == 1:
        start_time = f"{start_time}:00"
    if end_time.count(":") == 1:
        end_time = f"{end_time}:00"
    start_time = datetime.datetime.strptime(start_time, "%H:%M:%S")
    end_time = datetime.datetime.strptime(end_time, "%H:%M:%S")
    time_range = []
    while end_time > start_time:
        time_range.append(start_time.strftime(time_format))
        start_time = start_time + datetime.timedelta(minutes=interval)
    return time_range


def generate_string(length: int = 8) -> str:
    """
    生成指定长度的随机字符串
    :param length:
    :return:
    代码解释：
    首先调用了 random.sample() 方法，从 string.ascii_letters 和 string.digits 中各取出 length 个字符，并随机打乱它们的顺序。
    这样就得到了一个包含 length 个不同字符的列表。
    然后函数使用 "".join() 方法将这些字符拼接成一个字符串，返回给调用者。
    需要注意的是，string.ascii_letters 变量包含了所有的 ASCII 字母（包括大小写），而 string.digits 包含了所有的数字字符。
    因此生成的随机字符串中只包含字母和数字字符，不包含其他特殊字符。
    """
    return ''.join(random.sample(string.ascii_letters + string.digits, length))


def import_modules(modules: list, desc: str, **kwargs):
    """
    动态导入指定模块，并调用模块中的函数
    :param modules:
    :param desc:
    :param kwargs:
    :return:
    代码解释：
    该函数使用 for 循环遍历模块列表 modules 中的每一个模块。在循环体内，首先判断当前模块是否存在，若不存在则跳过这个模块的导入。
    然后使用 importlib.import_module() 方法动态导入模块，该方法的输入为模块名称的字符串。
    由于模块名称可能包含多级文件夹，因此需要使用 str.rindex() 方法找到最后一个句号（"."）的位置，将模块名称分解为模块路径和模块名称两部分。
    接下来使用 getattr() 方法从导入的模块中获取模块名称中最后一部分所代表的函数对象，并调用该函数并传入其他参数。kwargs 参数是一个关键字参数字典，
    可以使用 **kwargs 的形式将其展开为多个关键字参数传入函数中。
    如果在导入过程中发生了 ModuleNotFoundError 或 AttributeError 异常，则记录错误日志并继续导入下一个模块。
    最后，该函数并没有返回任何值，仅仅是在运行过程中动态导入了一些模块，调用了一些函数。
    """
    for module in modules:
        if not module:
            continue
        try:
            # 动态导入模块
            module_pag = importlib.import_module(module[0:module.rindex(".")])
            getattr(module_pag, module[module.rindex(".") + 1:])(**kwargs)
        except ModuleNotFoundError:
            logger.error(f"AttributeError：导入{desc}失败，未找到该模块：{module}")
        except AttributeError:
            logger.error(f"ModuleNotFoundError：导入{desc}失败，未找到该模块下的方法：{module}")


async def import_modules_async(modules: list, desc: str, **kwargs):
    """

    :param modules:
    :param desc:
    :param kwargs:
    :return:
    """
    for module in modules:
        if not module:
            continue
        try:
            # 动态导入模块
            module_pag = importlib.import_module(module[0:module.rindex(".")])
            await getattr(module_pag, module[module.rindex(".") + 1:])(**kwargs)
        except ModuleNotFoundError:
            logger.error(f"AttributeError：导入{desc}失败，未找到该模块：{module}")
        except AttributeError:
            logger.error(f"ModuleNotFoundError：导入{desc}失败，未找到该模块下的方法：{module}")
