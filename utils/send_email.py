#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/20 15:06
# @Author  : 冉勇
# @Site    : 
# @File    : send_email.py
# @Software: PyCharm
# @desc    : 发送邮件封装
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List
from aioredis import Redis
from core.exception import CustomException
from utils.cache import Cache


class EmailSender:
    def __init__(self, rd: Redis):
        self.email = None
        self.password = None
        self.smtp_server = None
        self.smtp_port = None
        self.server = None
        self.rd = rd

    async def __get_settings(self, retry: int = 3):
        """
        获取配置信息
        :param retry:
        :return:
        代码解释：
        首先调用Cache类的实例rd的get_tab_name方法，从缓存中获取名为“web_email”的配置信息。如果获取失败，则将会重试retry次，直至成功获取信息为止。
        然后，该方法从获取到的“web_email”配置信息中获取一些邮件相关的配置参数，包括email、password、smtp_server和smtp_port，分别表示发件邮箱、发件人密码、SMTP服务器地址和SMTP端口号。
        接着，该方法使用smtplib库中的SMTP类，以获取到的SMTP服务器地址和SMTP端口号为参数，创建了一个SMTP实例对象self.server，并调用starttls方法启动TLS加密连接。
        最后，该方法使用SMTP实例对象self.server的login方法进行认证，以email和password分别作为用户名和密码。如果认证失败，则抛出自定义异常CustomException，提示“邮箱服务器认证失败！”。
        """
        web_email = await Cache(self.rd).get_tab_name("web_email", retry)
        self.email = web_email.get("email_access")
        self.password = web_email.get("email_password")
        self.smtp_server = web_email.get("smtp_server")
        self.smtp_port = int(web_email.get("smtp_port"))
        self.server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        self.server.starttls()
        try:
            self.server.login(self.email, self.password)
        except smtplib.SMTPAuthenticationError:
            raise CustomException("邮箱服务器认证失败！")

    async def send_email(self, to_emails: List[str], subject: str, body: str, attachments: List[str] = None):
        """
        发送邮件
        :param to_emails: 收件人，一个或多个
        :param subject: 主题
        :param body: 内容
        :param attachments: 附件
        :return:
        代码解释：
        首先调用类的私有方法__get_settings，从缓存中获取邮件相关的配置信息，并创建了一个MIMEMultipart实例对象message，用于构建邮件消息体。
        接着，该方法设置了邮件的发件人、收件人、主题等信息，并使用MIMEText类创建了一个纯文本类型的邮件正文，将其添加至message中。
        如果存在附件，该方法遍历附件列表，逐个将文件读取为二进制数据，并使用MIMEApplication类创建了一个表示附件的实例对象attachment，并将其添加至message中。
        接下来，该方法使用SMTP实例对象self.server的sendmail方法发送邮件，并将发送结果保存至变量result中。
        如果发送成功，则调用self.server的quit方法，关闭SMTP连接，并返回True；否则，输出错误信息，并关闭SMTP连接，返回False。
        """
        await self.__get_settings()
        message = MIMEMultipart()
        message["From"] = self.email
        message["To"] = ",".join(to_emails)
        message["Subject"] = subject
        body = MIMEText(body)
        message.attach(body)
        if attachments:
            for attachment in attachments:
                with open(attachment, "rb") as f:
                    file_data = f.read()
                filename = attachment.split("/")[-1]
                attachment = MIMEApplication(file_data, Name=filename)
                attachment['Content-Disposition'] = f'attachment; filename="{filename}"'
                message.attach(attachment)
        try:
            result = self.server.sendmail(self.email, to_emails, message.as_string())
            self.server.quit()
            print("邮件发送结果", result)
            if result:
                return False
            else:
                return True
        except smtplib.SMTPException as e:
            self.server.quit()
            print("邮件发送失败！错误信息：", e)
            return False
