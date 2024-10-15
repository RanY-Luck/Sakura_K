#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2024/10/15 10:40
# @Author   : 冉勇
# @File     : hooks.py
# @Software : PyCharm
# @Desc     : 一些常用的Hook函数
import datetime
import random
import string

from faker import Faker

faker = Faker(locale='zh_CN')


def current_time(strf: str = '%Y-%m-%d %H:%M:%S') -> str:
    """
    :return: 获取当前时间
    """
    return datetime.datetime.now().strftime(strf)


def random_phone() -> str:
    """
    :return: 随机手机号
    """
    return faker.phone_number()


def random_name() -> str:
    """
    :return: 随机中文名
    """
    return faker.name()


def sum_a_b(a: int, b: int) -> int:
    return a + b


def generate_random_password(length=12) -> string:
    """
    随机密码
    """
    # 定义包含大小写字母、数字和特殊字符的字符集合
    characters = string.ascii_letters + string.digits + string.punctuation
    # 生成随机密码
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_random_name(length=6, syllables=2) -> string:
    """
    随机英文名
    """
    # 定义音节
    vowels = 'aeiou'
    consonants = 'bcdfghjklmnpqrstvwxyz'
    # 生成随机名字
    name = ''.join(
        random.choice(consonants) + random.choice(vowels)
        for _ in range(length // syllables)
    )
    # 如果长度不是音节的整数倍，添加剩余字符
    name += ''.join(random.choice(consonants + vowels) for _ in range(length % syllables))
    return name.capitalize()


def random_password() -> string:
    """
    随机密码
    """
    return faker.password()


if __name__ == '__main__':
    print(current_time())
    print(random_phone())
    print(random_name())
    print(sum_a_b(1, 1))
    print(generate_random_password())
    print(generate_random_name())
    print(random_password())
