#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/13 18:59
# @Author  : 冉勇
# @Site    : 
# @File    : file_manage.py
# @Software: PyCharm
# @desc    : 保存图片到本地
import datetime
import shutil
import sys
from pathlib import Path

import aioshutil
from aiopathlib import AsyncPath
from fastapi import UploadFile

from application.settings import TEMP_DIR, STATIC_ROOT, BASE_DIR, STATIC_URL, STATIC_DIR
from core.exception import CustomException
from utils.file.file_base import FileBase


class FileManage(FileBase):
    """
    上传文件管理
    """

    def __init__(self, file: UploadFile, path: str):
        self.path = self.generate_path(path, file.filename)
        self.file = file

    async def save_image_local(self, accept: list = None) -> dict:
        """
        将上传的图片文件保存到本地
        :param accept: 允许上传的图片类型
        :return:
        代码解释：
        该方法首先判断是否指定了可接受的图片类型 accept，如果没有指定则使用 self.IMAGE_ACCEPT 中定义的默认值。
        然后调用 validate_file 方法验证上传的文件是否符合指定格式，其中 max_size 参数表示文件的最大尺寸，mime_types 表示可接受的文件类型。
        如果文件不符合指定的格式，则会抛出自定义异常 CustomException 并附带相应的错误提示信息和状态码。
        如果上传的图片符合指定的格式，则调用 save_local 方法将图片保存到本地，并返回一个字典，表示保存成功的相关信息，例如文件名、文件路径等。
        """
        if accept is None:
            accept = self.IMAGE_ACCEPT
        await self.validate_file(self.file, max_size=5, mime_types=accept)
        return await self.save_local()

    async def save_local(self) -> dict:
        """
        保存文件到本地
        :return:
        """
        path = self.path
        if sys.platform == "win32":
            path = self.path.replace("/", "\\")
        save_path = AsyncPath(STATIC_ROOT) / path
        if not await save_path.parent.exists():
            await save_path.parent.mkdir(parents=True, exist_ok=True)
        await save_path.write_bytes(await self.file.read())
        return {
            "local_path": f"{STATIC_DIR}/{self.path}",
            "remote_path": f"{STATIC_URL}/{self.path}"
        }

    @staticmethod
    async def save_tmp_file(file: UploadFile) -> str:
        """
        上传的文件保存到临时文件夹中
        :param file: 待上传的文件对象
        :return:
        代码解释：
        该方法首先获取当前日期（格式为 %Y%m%d），并将其作为临时文件夹名称。如果不存在该文件夹，则创建该文件夹。
        然后生成唯一的文件名，包含当前时间戳和文件原始名称。需要注意的是，如果上传多个文件，并且它们恰好在同一秒内上传，则需要保证它们的文件名不同，因此需要使用当前时间戳生成唯一名称。
        接着使用 with open(...) as f 语句打开文件，并将文件内容写入到指定文件中。需要注意的是，读取文件内容时需要使用 await file.read() 方法。
        最后返回保存的文件名（包括路径）。
        """
        date = datetime.datetime.strftime(datetime.datetime.now(), "%Y%m%d")
        file_dir = AsyncPath(TEMP_DIR) / date
        if not await file_dir.exists():
            await file_dir.mkdir(parents=True, exist_ok=True)
        filename = file_dir / (str(int(datetime.datetime.now().timestamp())) + file.filename)
        await filename.write_bytes(await file.read())
        return str(filename)

    @staticmethod
    def copy(src: str, dst: str) -> None:
        """
        复制文件
        :param src: 源文件的路径，根据 BASE_DIR 来确定相对基础目录的路径。
        :param dst: 目标文件的绝对路径。
        :return:
        代码解释：
        首先判断源文件路径是否以斜杠 / 开头，如果是则去掉前导斜杠。接着判断操作系统是否为 Windows，如果是则将路径中的正斜杠 / 替换为反斜杠 \。
        接着使用 os.path.join(BASE_DIR, src) 方法将相对路径转换为绝对路径，并检查目标路径上级目录是否存在，如果不存在则创建该目录。最后使用 shutil.copyfile 方法将源文件复制到目标文件。
        """
        if src[0] == "/":
            src = src.lstrip("/")
        if sys.platform == "win32":
            src = src.replace("/", "\\")
            dst = dst.replace("/", "\\")
        src = Path(BASE_DIR) / src
        dst = Path(dst)
        if not src.exists():
            raise CustomException("源文件不存在！")
        if not dst.parent.exists():
            dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)

    @staticmethod
    async def async_copy(src: str, dst: str) -> None:
        """
        异步复制文件
        根目录为项目根目录，传过来的文件路径均为相对路径
        :param src: 原始文件
        :param dst: 目标路径。绝对路径
        :return:
        """
        if src[0] == "/":
            src = src.lstrip("/")
        if sys.platform == "win32":
            src = src.replace("/", "\\")
            dst = dst.replace("/", "\\")
        src = AsyncPath(BASE_DIR) / src
        if not await src.exists():
            raise CustomException("源文件不存在！")
        dst = AsyncPath(dst)
        if not await dst.parent.exists():
            await dst.parent.mkdir(parents=True, exist_ok=True)
        await aioshutil.copyfile(src, dst)
