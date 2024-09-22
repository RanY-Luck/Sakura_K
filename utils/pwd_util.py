#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/7/11 12:11
# @Author  : 冉勇
# @Site    : 
# @File    : pwd_util.py
# @Software: PyCharm
# @desc    : 密码工具类
from cryptography.fernet import Fernet
from passlib.context import CryptContext

# 密码加密算法
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# 哈希加密 key
hash_key = "JQDBN6iFEnQHOGfQITbLXF_Nd-B2FFRmwa6InpIaWdc="


class PwdUtil:
    """
    密码工具类
    """

    @classmethod
    def verify_password(cls, plain_password, hashed_password):
        """
        工具方法：校验当前输入的密码与数据库存储的密码是否一致
        :param plain_password: 当前输入的密码
        :param hashed_password: 数据库存储的密码
        :return: 校验结果
        """
        return pwd_context.verify(plain_password, hashed_password)

    @classmethod
    def get_password_hash(cls, input_password):
        """
        工具方法：对当前输入的密码进行加密
        :param input_password: 输入的密码
        :return: 加密成功的密码
        """
        return pwd_context.hash(input_password)

    @classmethod
    def encrypt(cls, hash_key, plain_password):
        f = Fernet(hash_key)
        # 将plain_password转换为bytes类型
        password_bytes = plain_password.encode('utf-8')
        return f.encrypt(password_bytes)

    @classmethod
    def decrypt(cls, hash_key, hashed_password):
        f = Fernet(hash_key)
        decrypted_bytes = f.decrypt(hashed_password)
        # 将解密后的bytes转换回字符串
        return decrypted_bytes.decode('utf-8')


if __name__ == '__main__':
    cipher_text = PwdUtil.encrypt(hash_key=hash_key, plain_password="123456")
    print(cipher_text)
    plain_text = PwdUtil.decrypt(hash_key=hash_key, hashed_password=cipher_text)
    print(plain_text)
