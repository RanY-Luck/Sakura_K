#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 19:03
# @Author  : 冉勇
# @Site    : 
# @File    : file_base.py
# @Software: PyCharm
# @desc    : 文件基类
import datetime
import os
import uuid
from fastapi import UploadFile
from core.exception import CustomException
from utils import status


class FileBase:
    IMAGE_ACCEPT = ["image/png", "image/jpeg", "image/gif", "image/x-icon"]
    VIDEO_ACCEPT = ["audio/mp4", "video/mp4", "video/mpeg"]
    ALL_ACCEPT = [*IMAGE_ACCEPT, *VIDEO_ACCEPT]

    @classmethod
    def generate_path(cls, path: str, filename):
        """
        生成文件路径
        :param path: 文件路径中的目录部分
        :param filename: 文件名部分
        :return:
        代码解释：
        该方法首先对 path 进行处理，如果 path 的第一个字符是斜杠（/），则去掉它；如果 path 的最后一个字符也是斜杠，则也去掉它。这样可以确保 path 的格式是正确的。
        然后获取当前日期，并将日期对象转换成字符串，作为文件路径的一部分。使用 datetime.datetime.now().date() 方法获取当前日期，然后将其转换成字符串类型。
        接下来使用 datetime.datetime.now().timestamp() 方法获取当前时间的时间戳，并将其转换成整数，作为文件名的一部分。
        再次生成一个随机字符串，并取其中前 8 个字符，作为文件名的一部分。
        最后使用 os.path.splitext() 方法获取 filename 的扩展名（即文件类型），然后将完整的文件路径拼接成一个字符串，并返回给调用者。
        """
        if path[0] == "/":
            path = path[1:]
        if path[-1] == "/":
            path = path[:-1]
        full_data = datetime.datetime.now().date()
        _filename = str(int(datetime.datetime.now().timestamp())) + str(uuid.uuid4())[:8]
        return f"{path}/{full_data}/{_filename}{os.path.splitext(filename)[-1]}"

    @classmethod
    async def validate_file(cls, file: UploadFile, max_size: int = None, mime_types: list = None) -> bool:
        """
        验证文件是否符合格式
        :param file: 验证的文件对象
        :param max_size: 文件的最大尺寸，单位MB
        :param mime_types: 允许上传的文件类型
        :return:
        代码解释：
        该方法首先判断参数中是否指定了文件的最大尺寸 max_size。
        如果指定了最大尺寸，则使用 await file.read() 方法读取整个文件，并计算文件大小（单位为 MB）。
        如果文件大小超过了指定的最大值，则抛出自定义异常 CustomException 并附带错误提示信息和状态码 status.HTTP_ERROR。
        如果设置了最大尺寸限制，则需要将文件对象的读取位置重置为 0，以便后续操作能够正确读取文件内容。
        接着判断参数中是否指定了文件类型列表 mime_types。
        如果指定了文件类型列表，则需要判断待验证文件的类型是否在此列表中。
        判断方法是通过 file.content_type 属性获取文件的 MIME 类型，然后判断该值是否在 mime_types 列表中。
        如果文件类型不在指定的类型列表中，则同样抛出自定义异常 CustomException 并附带错误提示信息和状态码 status.HTTP_ERROR。
        最后，如果文件符合指定格式，则返回 True 表示验证通过。需要注意的是，该方法是一个异步方法，因此需要使用关键字 async 声明该方法，并且需要使用 await 关键字等待异步操作完成。
        """
        if max_size:
            size = len(await file.read()) / 1024 / 1024
            if size > max_size:
                raise CustomException(f"上传文件过大，不能超过{max_size}MB", status.HTTP_ERROR)
            await file.seek(0)
        if mime_types:
            if file.content_type not in mime_types:
                raise CustomException(f"上传文件格式错误，只支持 {'/'.join(mime_types)} 格式!", status.HTTP_ERROR)
        return True

    @classmethod
    def get_file_type(cls, content_type: str) -> str | None:
        """
        获取文件类型
        :param content_type:
        :return:
        0： 图片
        1：视屏
        """
        if content_type in cls.IMAGE_ACCEPT:
            return "0"
        elif content_type in cls.VIDEO_ACCEPT:
            return "1"
        else:
            return None
