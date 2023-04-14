#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 11:04
# @Author  : 冉勇
# @Site    :
# @File    : main.py
# @Software: PyCharm
# @desc    : 创建目录
import datetime
import os.path
from application.settings import BASE_DIR


class CreateApp:
    APPS_ROOT = os.path.join(BASE_DIR, "apps")
    SCRIPT_DIR = os.path.join(BASE_DIR, "scripts", "create_app")

    def __init__(self, path: str):
        """
        :param path: app路径，根目录为apps，填写apps后面路径即可，例：root/auth
        """
        self.app_path = os.path.join(self.APPS_ROOT, path)
        self.path = path

    def run(self):
        """
        自动创建初始化APP结构，如果该路径已经存在，则不执行
        :return:
        """
        if self.exist(self.app_path):
            print(f"{self.app_path} 已经存在，无法自动创建，请删除后，重新执行")
            return False
        print("开始生成 App 目录:", self.path)
        path = []
        for item in self.path.split("/"):
            path.append(item)
            self.create_pag(os.path.join(self.APPS_ROOT, *path))
        self.create_pag(os.path.join(self.app_path, "models"))
        self.create_pag(os.path.join(self.app_path, "params"))
        self.create_pag(os.path.join(self.app_path, "schemas"))
        self.generate_file("views.py")
        self.generate_file("crud.py")
        print("App 目录生成结束", self.app_path)

    def create_pag(self, path: str) -> None:
        """
        创建python包
        :param self:
        :param path:
        :return:
        """
        if self.exist(path):
            return
        os.makedirs(path)
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = {
            "create_datetime": now,
            "filename": "__init__.py",
            "desc": "初始化文件"
        }
        self.create_file(os.path.join(path, "__init__.py"), "init.py", **params)

    def generate_file(self, name: str) -> None:
        """
        创建文件
        :param name:
        :return:
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = {
            "create_datetime": now
        }
        self.create_file(os.path.join(self.app_path, name), name, **params)

    def create_file(self, filepath: str, name: str, **kwargs):
        """
        创建文件
        :param filepath:
        :param name:
        :param kwargs:
        :return:
        """
        with open(filepath, "w", encoding="utf-8") as f:
            content = self.__get_template(name)
            f.write(content.format(**kwargs))

    @classmethod
    def exist(cls, path) -> bool:
        """
        判断是否已经存在
        :param path:
        :return:
        """
        return os.path.exists(path)

    def __get_template(self, name: str) -> str:
        """
        获取模板内容
        :param name:
        :return:
        """
        template = open(os.path.join(self.SCRIPT_DIR, "template", name), 'r')
        content = template.read()
        template.close()
        return content


if __name__ == '__main__':
    app = CreateApp("vadmin/auth")
    app.run()
