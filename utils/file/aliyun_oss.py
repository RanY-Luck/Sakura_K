#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 18:50
# @Author  : 冉勇
# @Site    : 
# @File    : aliyun_oss.py
# @Software: PyCharm
# @desc    : 阿里云存储对象
import os.path
from fastapi import UploadFile
from pydantic import BaseModel
import oss2  # 安装依赖:pip3 install oss2
from oss2.models import PutObjectResult
from core.logger import logger
from utils.file.compress.cpressJPG import compress_jpg_png
from utils.file.file_manage import FileManage
from utils.file.file_base import FileBase

"""
代码解释：
实现了一个基于阿里云OSS的文件上传类AliyunOSS，包含两个方法：upload_image和upload_file。
该类需要传入一个BucketConf对象作为初始化参数，其中accessKeyId、accessKeySecret、endpoint、bucket和baseUrl等属性分别对应阿里云存储桶的相关配置信息。
在upload_image方法中，首先调用generate_path方法生成文件路径，然后判断是否需要压缩图片，
如果需要，则调用FileManage类的save_tmp_file方法将上传的文件保存到临时目录中，再调用compress_jpg_png方法对图片进行压缩。
最后读取压缩后的文件，并通过oss2.Bucket.put_object方法上传到OSS中。如果上传成功，则返回图片URL地址。
在upload_file方法中，同样先调用generate_path方法生成文件路径，然后读取文件内容，并通过oss2.Bucket.put_object方法上传到OSS中。
如果上传成功，则返回文件URL地址。
"""


class BucketConf(BaseModel):
    accessKeyId: str
    accessKeySecret: str
    endpoint: str
    bucket: str
    baseUrl: str


class AliyunOSS(FileBase):
    """
    阿里云存储对象
    常见报错：https://help.aliyun.com/document_detail/185228.htm?spm=a2c4g.11186623.0.0.6de530e5pxNK76#concept-1957777
    官方文档：https://help.aliyun.com/document_detail/32026.html
    使用Python SDK时，大部分操作都是通过oss2.Service和oss2.Bucket两个类进行。
    oss2.Service类用于列举存储空间。
    oss2.Bucket类用于上传、下载、删除文件以及对存储空间进行各种配置。
    """

    def __init__(self, bucket: BucketConf):
        # 阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
        auth = oss2.Auth(bucket.accessKeyId, bucket.accessKeySecret)
        # 填写Bucket名称。
        self.bucket = oss2.Bucket(auth, bucket.endpoint, bucket.bucket)
        self.baseUrl = bucket.baseUrl

    async def upload_image(self, path: str, file: UploadFile, compress: bool = False) -> str:
        """
        上传图片
        :param path:
        :param file:
        :param compress:
        :return:
        """
        path = self.generate_path(path, file.filename)
        if compress:
            # 压缩图片
            file_path = await FileManage.save_tmp_file(file)
            new_file = compress_jpg_png(file_path, originpath=os.path.abspath(file_path))
            with open(new_file, "rb") as f:
                file_data = f.read()
        else:
            file_data = await file.read()
        result = self.bucket.put_object(path, file_data)
        assert isinstance(result, PutObjectResult)
        if result.status != 200:
            logger.error(f"图片上传到OSS失败，状态码：{result.status}")
            print("图片上传路径", path)
            print(f"图片上传到OSS失败，状态码：{result.status}")
            return ""
        return self.baseUrl + path

    async def upload_file(self, path: str, file: UploadFile) -> str:
        """
        上传文件
        :param path:
        :param file:
        :return:
        """
        path = self.generate_path(path, file.filename)
        file_data = await file.read()
        result = self.bucket.put_object(path, file_data)
        assert isinstance(result, PutObjectResult)
        if result.status != 200:
            logger.error(f"文件上传到OSS失败，状态码：{result.status}")
            return ""
        return self.baseUrl + path
