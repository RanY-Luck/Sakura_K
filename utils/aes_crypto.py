#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 14:03
# @Author  : 冉勇
# @Site    : 
# @File    : aes_crypto.py
# @Software: PyCharm
# @desc    : AES对称加、解密
"""
安装：pip install pycryptodome
密钥（key）, 密斯偏移量（iv） CBC模式加密
base64 详解：https://cloud.tencent.com/developer/article/1099008
"""

import base64
from Crypto.Cipher import AES

# 自己秘钥
_key = "0CoJUm6Qywm6ts68"


def aes_encrypt(data: str):
    """
    AES 对称加密
    :param data:
    :return:
    解释代码：
    首先声明了一个自己设置的密钥，然后定义了一个 aes_encrypt 方法。
    该方法的作用是将传入的数据进行补位，然后用密钥和固定的 vi 值生成一个 AES 加密器，使用 CBC 模式对数据进行加密，最后使用 base64 编码将加密后的数据转换成可打印的字符串。
    """
    vi = "0102030405060708"
    pad = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
    data = pad(data)
    # 字符串补位
    cipher = AES.new(_key.encode("utf8"), AES.MODE_CBC, vi.encode("utf8"))
    encrypted_bytes = cipher.encrypt(data.encode("utf8"))
    # 加密后得到的bytes类型的数据
    encode_strs = base64.urlsafe_b64encode(encrypted_bytes)
    # 使用Base64进行编码，返回byte字符串
    # 对byte字符串按utf-8进行编码
    return encode_strs.decode("utf8")


def aes_decrypt(data):
    """
    对 AES 对称加密后的数据进行解密，返回原始数据字符串。
    :param data:
    :return:
    代码解释：
    在函数中，首先声明了一个固定的 vi（Initialization Vector）值，然后将传入的加密数据字符串编码成字节类型，
    并使用 base64 库的 urlsafe_b64encode() 方法将编码后的字节数据转换成 URL 安全的 Base64 编码形式。
    接着，使用 AES 库的 new() 方法以指定密钥和 CBC 模式生成一个 AES 解密器，使用解密器的 decrypt() 方法对传入的 Base64 编码数据进行解密。
    由于加密过程中存在补位操作，所以解密后的数据需要进行补位还原，这里定义了一个 lambda 表达式来实现补位操作。最后将还原后的字节数据解码成字符串，返回解密后的原始数据。
    """
    vi = "0102030405060708"
    data = data.encode("utf8")
    encode_bytes = base64.urlsafe_b64encode(data)
    # 将加密数据转换为bytes类型数据
    cipher = AES.new(_key.encode("utf8"), AES.MODE_CBC, vi.encode("utf8"))
    text_decrypted = cipher.decrypt(encode_bytes)
    unpad = lambda s: s[0:-s[-1]]
    text_decrypted = unpad(text_decrypted)
    # 补位
    text_decrypted = text_decrypted.decode("utf8")
    return text_decrypted


if __name__ == '__main__':
    _data = '123456'  # 需要加密的内容
    enctext = aes_encrypt(_data)
    print(enctext)
