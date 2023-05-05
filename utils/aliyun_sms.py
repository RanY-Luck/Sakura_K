#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 19:37
# @Author  : 冉勇
# @Site    : 
# @File    : aliyun_sms.py
# @Software: PyCharm
# @desc    : 最新版阿里云短信服务发送程序（Python版本）【向指定手机号发送验证码短信，并校验该验证码是否正确】
"""
短信 API 官方文档：https://help.aliyun.com/document_detail/419298.html?spm=5176.25163407.help.dexternal.6ff2bb6ercg9x3
发送短信 官方文档：https://help.aliyun.com/document_detail/419273.htm?spm=a2c4g.11186623.0.0.36855d7aRBSwtP
Python SDK 官方文档：https://help.aliyun.com/document_detail/215764.html?spm=a2c4g.11186623.0.0.6a0c4198XsBJNW
安装 SDK 核心库 OpenAPI ，使用pip安装包依赖:
pip3 install alibabacloud_tea_openapi
pip3 install alibabacloud_dysmsapi20170525
代码解释：

"""
import random
import re
import datetime
from enum import Enum, unique
from core.exception import CustomException
from alibabacloud_dysmsapi20170525.client import Client as Dysmsapi20170525Client
from alibabacloud_dysmsapi20170525 import models as dysmsapi_20170525_models
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_tea_util import models as util_models
from core.logger import logger
from aioredis.client import Redis
from utils.cache import Cache
from utils import status


class AliyunSMS:
    # 返回错误码对应：
    doc = "https://help.aliyun.com/document_detail/101346.html"

    @unique
    class Scene(Enum):
        login = "sms_template_code_1"
        reset_password = "sms_template_code_2"

    def __init__(self, rd: Redis, telephone: str):
        self.check_telephone_format(telephone)
        self.telephone = telephone
        self.rd = rd
        self.code = None
        self.scene = None

    async def __get_settings(self, retry: int = 3):
        """
        获取阿里云短信服务配置信息
        :param retry:
        :return:
        代码解释：
        该方法会从Redis数据库中获取适用于短信服务的Access Key ID、Access Key Secret、发送间隔、验证码有效时间、短信签名和短信模版编码等配置信息，然后将其存储在类实例的属性中以便其他方法使用。
        具体来说，该方法有一个可选参数retry，表示从Redis数据库中获取配置信息的最大重试次数，默认为3。
        在方法内部，它首先通过调用Cache类的get_tab_name方法，从Redis数据库中获取aliyun_sms表的内容，并将结果存储在一个字典对象aliyun_sms中。
        然后，它通过访问字典对象获取适用于短信服务的Access Key ID、Access Key Secret、发送间隔、验证码有效时间、短信签名和短信模版编码等配置信息，
        并将这些值分别赋值给类实例的属性access_key、access_key_secret、send_interval、valid_time、sign_name和template_code。
        其中，根据当前场景值（self.scene），选择不同的短信签名（sms_sign_name_1或者sms_sign_name_2）。
        """
        aliyun_sms = await Cache(self.rd).get_tab_name("aliyun_sms", retry)
        self.access_key = aliyun_sms.get("sms_access_key")
        self.access_key_secret = aliyun_sms.get("sms_access_key_secret")
        self.send_interval = int(aliyun_sms.get("sms_send_interval"))
        self.valid_time = int(aliyun_sms.get("sms_valid_time"))
        if self.scene == self.Scene.login:
            self.sign_name = aliyun_sms.get("sms_sign_name_1")
        else:
            self.sign_name = aliyun_sms.get("sms_sign_name_2")
        self.template_code = aliyun_sms.get(self.scene.value)

    async def main_async(self, scene: Scene, **kwargs) -> bool:
        """
        主程入口，异步方式
        :param scene:
        :param kwargs:
        :return:
        代码解释：
        这是一个用于发送短信的方法main_async。该方法接受一个Scene类型的参数scene作为短信场景，以及任意数量的关键字参数kwargs，这些参数包含了短信模版所需的动态参数。返回值为bool类型，表示短信是否发送成功。
        具体来说，该方法会首先获取当前时间，并检查Redis数据库中是否存在指定手机号加上"flag"后缀的键。如果存在，则表示该手机号最近已经发送过短信，无法再次发送。
        此时，该方法会将错误信息记录到日志中，并抛出自定义异常CustomException，其中msg为"短信发送频繁"，code为status.HTTP_ERROR表示请求无效。
        如果Redis中不存在指定手机号的标记，则会将类实例属性self.scene设置为参数scene，然后调用__get_settings方法获取短信服务的配置信息。
        最后，调用__send方法发送短信，传入关键字参数kwargs。如果__send方法返回True，则表示短信发送成功，该方法也会返回True。否则，该方法返回False。
        """
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if await self.rd.get(self.telephone + "_flag_"):
            logger.error(f"{send_time} {self.telephone} 短信发送失败，短信发送过于频繁")
            print(f"{self.telephone} 短信发送频繁")
            raise CustomException(msg="短信发送频繁", code=status.HTTP_ERROR)
        self.scene = scene
        await self.__get_settings()
        return await self.__send(**kwargs)

    async def __send(self, **kwargs) -> bool:
        """
        发送短信
        :param kwargs:
        :return:
        代码解释：
        这是一个用于发送短信的私有方法__send。该方法接受任意数量的关键字参数kwargs，这些参数包含了短信模版所需的动态参数。返回值为bool类型，表示短信是否发送成功。
        具体来说，该方法首先调用create_client方法创建一个阿里云短信服务客户端client，并使用类实例对象中存储的Access Key ID和Access Key Secret作为参数。
        然后，该方法创建一个dysmsapi_20170525_models.SendSmsRequest对象send_sms_request，其中包含了短信发送所需的手机号、签名、短信模版编码和动态参数等信息。
        其中self.telephone表示接收短信的手机号，self.sign_name表示短信签名，self.template_code表示短信模版编码，self.__get_template_parm(**kwargs)表示获取短信模版所需的动态参数。
        接下来，该方法创建一个util_models.RuntimeOptions对象runtime，用于设置短信发送的运行时选项。
        最后，该方法调用client的send_sms_with_options_async方法发送短信，并捕获任何异常。如果发送成功，则返回True，否则返回False。
        """
        client = self.create_client(self.access_key, self.access_key_secret)
        send_sms_request = dysmsapi_20170525_models.SendSmsRequest(
            phone_numbers=self.telephone,
            sign_name=self.sign_name,
            template_code=self.template_code,
            template_param=self.__get_template_parm(**kwargs)
        )
        runtime = util_models.RuntimeOptions()
        try:
            resp = await client.send_sms_with_options_async(send_sms_request, runtime)
            return await self.__validation(resp)
        except Exception as e:
            print(e.__str__())
            return False

    def __get_template_parm(self, **kwargs) -> str:
        """
        获取短信模版参数
        :param kwargs:
        :return:
        代码解释：
        该方法首先检查实例属性self.scene的值，以确定当前的短信场景是登录还是重置密码。
        如果self.scene等于Scene.login枚举值，则认为当前场景为登录，并使用kwargs中获取或调用get_code方法生成验证码，将其作为模版参数code的值，组成一个JSON字符串template_param。
        如果self.scene等于Scene.reset_password枚举值，则认为当前场景为重置密码，并使用kwargs中获取的password作为模版参数code的值，组成一个JSON字符串template_param。
        如果self.scene既不等于Scene.login也不等于Scene.reset_password，则表示发送场景不明确，此时将抛出自定义异常CustomException，其中msg为"获取发送场景失败"，code为status.HTTP_ERROR表示请求无效。
        最后，该方法返回组装好的短信模版参数template_param字符串。
        """
        if self.scene == self.Scene.login:
            self.code = kwargs.get("code", self.get_code())
            template_param = '{"code":"%s"}' % self.code
        elif self.scene == self.Scene.reset_password:
            self.code = kwargs.get("password")
            template_param = '{"password":"%s"}' % self.code
        else:
            raise CustomException(msg="获取发送场景失败", code=status.HTTP_ERROR)
        return template_param

    async def __validation(self, resp: dysmsapi_20170525_models.SendSmsResponse) -> bool:
        """
        验证短信发送结果
        :param resp:
        :return:
        代码解释：
        首先获取当前时间，并将其格式化为"%Y-%m-%d %H:%M:%S"的字符串形式，存储在变量send_time中。
        然后，该方法检查resp.body.code属性的值是否为"OK"，如果是，则表示短信发送成功，此时将调用日志记录器logger的info方法，记录短信发送成功的日志信息，
        并将验证码及过期时间存储在Redis数据库中，分别使用await self.rd.set(self.telephone, self.code, self.valid_time)
        和await self.rd.set(self.telephone + "flag", self.code, self.send_interval)方法实现，并返回True表示发送成功。
        如果resp.body.code属性的值不为"OK"，则表示短信发送失败，此时将调用日志记录器logger的error方法，记录短信发送失败的日志信息，
        并将错误码及参考文档链接存储在变量logger.error中，返回False表示发送失败。
        """
        send_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if resp.body.code == "OK":
            logger.info(f"{send_time}{self.telephone} 短信发送成功，返回code：{resp.body.code}")
            await self.rd.set(self.telephone, self.code, self.valid_time)
            await self.rd.set(self.telephone + "_flag_", self.code, self.send_interval)
            return True
        else:
            logger.error(f"{send_time}{self.telephone}短信发送失败，返回code：{resp.body.code}，请参考文档：{self.doc}")
            return False

    async def check_sms_code(self, code: str) -> bool:
        """
        检查短信验证码是否正确
        :param code:
        :return:
        代码解释：
        首先判断传入的验证码code是否存在且与Redis数据库中对应手机号码的验证码相同，
        如果相同，则使用await self.rd.delete(self.telephone)和await self.rd.delete(self.telephone + "flag")分别删除Redis数据库中该手机号码对应的验证码及发送间隔标记，并返回True表示验证码正确。
        如果传入的验证码code不存在、与Redis数据库中对应手机号码的验证码不同，或者Redis数据库中不存在该手机号码对应的验证码，则直接返回False表示验证码错误。
        """
        if code and code == await self.rd.get(self.telephone):
            await self.rd.delete(self.telephone)
            await self.rd.delete(self.telephone + "_flag_")
            return True
        return False

    @staticmethod
    def get_code(length: int = 6, blend: bool = False) -> str:
        """
        生成短信验证码
        短信验证码仅支持数字，不支持字母及其他字符
        :param length:
        :param blend:
        :return:
        代码解释：
        首先创建一个空字符串变量code，用于存储生成的验证码。
        然后，该方法通过for循环控制生成验证码的位数，每次循环随机生成一个0-9之间的数字，并根据blend参数决定是否需要添加字母验证码。
        如果需要添加字母验证码，将随机生成一个大写字母（ASCII码为65-90之间）与一个小写字母（ASCII码为97-122之间），并从这三个字符中随机选择一个，更新num变量的值。
        最后，将生成的num转换为字符串类型，并添加到code变量中，直到code变量的长度达到设定的长度。最终将code作为方法的输出返回。
        """
        code = ""  # 创建字符串变量，存储生成的验证码
        for i in range(length):  # 通过for循环控制验证码位数
            num = random.randint(0, 9)
            if blend:  # 需要字母验证码,不用传参,如果不需要字母的,关键字alpha=False
                upper_alpha = chr(random.randint(65, 90))
                lower_alpha = chr(random.randint(97, 122))
                # 随机选择其中一位
                num = random.choice([num, upper_alpha, lower_alpha])
            code = code + str(num)
        return code

    @staticmethod
    def check_telephone_format(telephone: str) -> bool:
        """
        检查手机号格式是否合法
        :param telephone:
        :return:
        代码解释：
        该方法首先定义了一个正则表达式REGEX_TELEPHONE，用来匹配符合条件的手机号码格式。
        其中，手机号码必须以1开头，第二位数字必须为3、4、5、6、7、8、9中的一个，其余9位数字任意组合。如果待检查的手机号码不符合该正则表达式，则认为该手机号码格式不正确。
        然后，该方法通过一系列判断来确定手机号码的合法性，如果手机号码为空，则抛出自定义异常CustomException，提示“手机号不能为空”，异常代码为400；
        如果手机号码不符合正则表达式，同样抛出CustomException，提示“手机号码格式不正确”，异常代码为400。
        如果以上两个判断条件都不成立，则表明该手机号码格式合法，返回True表示验证通过。
        """
        REGEX_TELEPHONE = r'^1(3\d|4[4-9]|5[0-35-9]|6[67]|7[013-8]|8[0-9]|9[0-9])\d{8}$'
        if not telephone:
            raise CustomException(msg="手机号不能为空", code=400)
        elif not re.match(REGEX_TELEPHONE, telephone):
            raise CustomException(msg="手机号码格式不正确", code=400)
        return True

    @staticmethod
    def create_client(
            access_key_id: str,
            access_key_secret: str,
    ) -> Dysmsapi20170525Client:
        """
        创建阿里云短信服务
        :param access_key_id:
        :param access_key_secret:
        :return:
        代码解释：
        首先通过传入的access_key_id和access_key_secret初始化open_api_models.Config类的实例config，即生成了一个访问阿里云API所需的配置信息。
        然后，将访问域名设置为'dysmsapi.aliyuncs.com'，即使用阿里云短信服务的API接口。
        最后，将config作为参数传入Dysmsapi20170525Client类的构造方法中，完成了客户端实例的创建，将其返回。
        需要注意的是，该方法在代码中并没有进行异常处理，因此在调用该方法时需要确保输入正确的access_key_id和access_key_secret，避免抛出异常。
        """
        config = open_api_models.Config(
            # 您的AccessKey ID
            access_key_id=access_key_id,
            # 您的AccessKey Secret
            access_key_secret=access_key_secret
        )
        # 访问域名
        config.endpoint = 'dysmsapi.aliyuncs.com'
        return Dysmsapi20170525Client(config)
