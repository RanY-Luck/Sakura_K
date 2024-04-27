#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 11:04
# @Author  : 冉勇
# @Site    :
# @File    : run.py
# @Software: PyCharm
# @desc    : 创建目录
import datetime
import os.path

from application.settings import BASE_DIR


class CreateApp:
    """
    代码解释：
    定义了一个 CreateApp 类，并创建了两个常量：APPS_ROOT 和 SCRIPT_DIR。APPS_ROOT
    """
    APPS_ROOT = os.path.join(BASE_DIR, "apps")
    SCRIPT_DIR = os.path.join(BASE_DIR, "scripts", "create_app")

    def __init__(self, path: str):
        """
        :param path: app 路径，根目录为apps，填写apps后面路径即可，例子：vadmin/auth
        """
        self.app_path = os.path.join(self.APPS_ROOT, path)
        self.path = path

    def run(self):
        """
        自动创建初始化APP结构，如果该路径已经存在，则不执行
        :return:
        代码解释：
        1、检查应用程序目录是否已存在；
        2、如果应用程序目录已经存在，则打印出错误信息，并返回 False 来结束该方法；
        3、如果应用程序目录不存在，程序会依次创建以下目录：
        - models 目录
        - params 目录
        - schemas 目录
        4、然后程序会调用 generate_file 方法生成 views.py 和 crud.py 文件。
        5、最后，程序会打印出提示信息，表示应用程序目录已经创建完成。
        """
        if self.exist(self.app_path):
            print(f"{self.app_path} 已经存在，无法自动创建，请删除后，重新执行。")
            return False
        print("开始生成 App 目录：", self.path)
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
        用于创建一个 Python 包（package），并为其添加一个初始化文件。
        :param self:
        :param path: 绝对路径
        :return:
        代码解释：
        定义了一个名为 create_pag 的方法，用于创建一个 Python 包（package）
        首先会检查指定路径是否已存在，如果已经存在，则直接返回；
        如果路径不存在，则会调用 os.makedirs 方法递归地创建该路径所需的所有目录；
        接着，程序会获取当前时间并将其格式化成字符串，并设置一些参数；
        然后，程序会调用 create_file 方法来创建一个名为 __init__.py 的文件，该文件用于初始化新建的 Python 包；
        最后，程序会在 path 目录下创建一个名为 __init__.py 的文件。
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
        创建一个新文件
        :param name:
        :return:
        代码解释：
        首先，程序会获取当前时间并将其格式化成字符串，并设置一些参数；
        然后，程序会调用 create_file 方法来创建一个名为 name 的文件，路径是应用程序目录下的 name 文件；
        最后，该方法完成操作。
        """
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = {
            "create_datetime": now
        }
        self.create_file(os.path.join(self.app_path, name), name, **params)

    def create_file(self, filepath: str, name: str, **kwargs):
        """
        创建一个新文件并写入内容
        :param filepath:
        :param name:
        :param kwargs:
        :return:
        代码解释：
        首先，程序会打开指定名称的文件并以写入模式（"w"）打开。如果该文件不存在，则会创建该文件；
        然后，程序会调用 __get_template 方法获取指定名称文件的模板内容，并使用传递给该方法的参数更新占位符；
        最后，程序会将更新后的模板内容写入到打开的文件中，并关闭文件。
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
        代码解释：
        程序会调用 os.path.exists 方法来检查指定路径是否存在；
        如果指定路径存在，则该方法返回 True，否则返回 False。
        """
        return os.path.exists(path)

    def __get_template(self, name: str) -> str:
        """
        获取指定名称文件的模板内容
        :param name:
        :return:
        代码解释：
        首先，程序会打开位于脚本目录下的 template 目录中的指定名称文件，并以只读（"r"）模式打开；
        然后，程序会读取文件的内容并将其保存到变量 content 中；
        最后，程序会关闭打开的文件，并返回读取到的内容。
        """
        template = open(os.path.join(self.SCRIPT_DIR, "template", name), 'r')
        content = template.read()
        template.close()
        return content
