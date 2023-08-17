#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : crud.py
# @Software: PyCharm
# @desc    : 增删改查
import copy
from typing import Any

from aioredis import Redis
from fastapi import UploadFile
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from application import settings
from apps.vadmin.system import crud as vadminSystemCRUD
from core.crud import DalBase
from core.exception import CustomException
from core.validator import vali_telephone
from utils import status
from utils.aliyun_sms import AliyunSMS
from utils.excel.excel_manage import ExcelManage
from utils.excel.import_manage import ImportManage, FieldType
from utils.excel.write_xlsx import WriteXlsx
from utils.file.aliyun_oss import AliyunOSS, BucketConf
from utils.send_email import EmailSender
from utils.tools import test_password
from utils.wx.oauth import WXOAuth
from . import models, schemas
from .params import UserParams


class UserDal(DalBase):
    import_headers = [
        {"label": "姓名", "field": "name", "required": True},
        {"label": "昵称", "field": "nickname", "required": False},
        {"label": "手机号", "field": "telephone", "required": True, "rules": [vali_telephone]},
        {"label": "性别", "field": "gender", "required": False},
        {"label": "关联角色", "field": "role_ids", "required": True, "type": FieldType.list},
    ]

    def __init__(self, db: AsyncSession):
        super(UserDal, self).__init__(db, models.VadminUser, schemas.UserSimpleOut)

    async def create_data(
            self,
            data: schemas.UserIn,
            v_options: list = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ):
        """
        创建用户
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        代码解释：
        首先调用异步方法get_data，并传入参数telephone=data.telephone和v_return_none=True，以获取指定手机号的用户数据。
        如果能够获取到该手机号的用户数据unique，则抛出CustomException异常，提示手机号已存在。
        如果该手机号没有被占用，则接着从data参数中获取密码明文或settings.DEFAULT_PASSWORD默认密码，并使用密码哈希方法加密得到密码hash值。
        之后，将data参数中除去role_ids字段之外的所有数据构造成一个UserIn模型对象obj，然后从角色表中获取id在data.role_ids列表中的角色数据并添加到obj.roles中。
        最后，调用self.flush方法将obj写入数据库，并通过调用self.out_dict方法输出dict类型的数据，其中包含了新建用户的信息和响应状态码等信息。
        """
        unique = await self.get_data(telephone=data.telephone, v_return_none=True)
        if unique:
            raise CustomException("手机号已存在！", code=status.HTTP_ERROR)
        password = data.telephone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
        data.password = self.model.get_password_hash(password)
        data.avatar = data.avatar if data.avatar else settings.DEFAULT_AVATAR
        obj = self.model(**data.model_dump(exclude={'role_ids'}))
        if data.role_ids:
            roles = await RoleDal(self.db).get_datas(limit=0, id=("in", data.role_ids), v_return_objs=True)
            for role in roles:
                obj.roles.append(role)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.UserUpdate,
            v_options: list = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ):
        """
        更新用户信息
        :param v_return_obj: 一个布尔值，用于控制是否直接返回输出的dict类型数据，还是返回更新成功的对象实例。
        :param data_id:
        :param data:
        :param v_options: 用于控制输出的dict类型数据中包含哪些字段。
        :param v_schema: 用于控制输出的dict类型数据的格式。
        :return:
        代码解释：
        首先调用异步方法get_data，并传入参数data_id和v_options=[joinedload(self.model.roles)]，以获取指定id的用户数据，
        同时通过joinedload方法预加载roles字段。之后，将data参数编码为可JSON序列化的Python对象，并将其转换为字典类型，存储在data_dict变量中。
        接着，该方法遍历data_dict字典中的每个键值对，如果键名为"role_ids"，则将obj.roles中的所有角色清空，并根据data_dict中的value值重新添加相关的角色；
        否则，直接通过setattr方法将obj对象的对应属性设置为data_dict中的对应值。
        最后，调用self.flush方法将更新后的obj对象写入数据库，并通过self.out_dict方法输出dict类型的数据，其中包含了更新后的用户信息以及响应状态码等信息。
        """
        obj = await self.get_data(data_id, v_options=[joinedload(self.model.roles)])
        data_dict = jsonable_encoder(data)
        for key, value in data_dict.items():
            if key == "role_ids":
                if obj.roles:
                    obj.roles.clear()
                if value:
                    roles = await RoleDal(self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
                    for role in roles:
                        obj.roles.append(role)
                continue
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def reset_current_password(self, user: models.VadminUser, data: schemas.ResetPwd):
        """
        重置当前用户的密码
        :param user:
        :param data:
        :return:
        代码解释：
        首先检查data参数中的password和password_two字段是否一致，如果不一致，则抛出CustomException异常，提示两次输入的密码不一致。
        接着，调用test_password方法对password进行复杂度检查，如果返回值是字符串类型，则说明密码不符合规范，此时抛出CustomException异常并提示对应信息。
        如果密码符合要求，则利用user对象所属的self.model调用get_password_hash方法，将data.password加密得到密码hash，并将其赋值给user对象的password属性。
        之后，将user对象的is_reset_password属性设置为True，并通过调用self.flush方法将其写入数据库。最后，该方法返回一个True值，表示密码重置成功。
        """
        if data.password != data.password_two:
            raise CustomException(msg="两次密码不一致", code=400)
        result = test_password(data.password)
        if isinstance(result, str):
            raise CustomException(msg=result, code=400)
        user.password = self.model.get_password_hash(data.password)
        user.is_reset_password = True
        await self.flush(user)
        return True

    async def update_current_info(self, user: models.VadminUser, data: schemas.UserUpdateBaseInfo):
        """
        更新当前用户基本信息
        :param user:
        :param data:
        :return:
        代码解释：
        首先判断传入的新手机号码是否与当前用户的手机号码相同，如果不同，则通过调用 get_data 方法查询数据库，判断新的手机号码是否已经存在于数据库中，如果存在则抛出 CustomException 异常；
        否则将用户对象的手机号码更新为新的手机号码。
        然后，通过访问 data 对象的属性，更新当前用户的姓名、昵称和性别信息。接着，通过调用 flush 方法，将更新后的用户对象存储到数据库中。
        最后，通过调用 out_dict 方法将更新后的用户对象转换成一个 JSON 格式的字典，并将这个字典作为函数的返回值。
        """
        if data.telephone != user.telephone:
            unique = await self.get_data(telephone=data.telephone, v_return_none=True)
            if unique:
                raise CustomException("手机号已存在！", code=status.HTTP_ERROR)
            else:
                user.telephone = data.telephone
        user.name = data.name
        user.nickname = data.nickname
        user.gender = data.gender
        await self.flush(user)
        return await self.out_dict(user)

    async def export_query_list(self, header: list, params: UserParams):
        """
        导出 Excel 表格的表头和查询条件
        :param header:
        :param params:
        :return:
        代码解释：
        首先通过调用 get_datas 方法，根据传入的查询条件获取用户列表，并存储到 datas 变量中。接着，通过遍历 header 列表，获取表头信息，并将其存储到 row 列表中。
        然后，通过调用 DictTypeDal 方法获取一个字典类型信息的 CRUD 实例，并传入数据库连接对象 self.db。
        接着，通过调用 get_dicts_details 方法获取性别字典对应的详细信息并存储到 options 变量中。
        接下来，通过遍历 datas 列表，依次访问用户对象的属性，并根据属性的值进行相应的转换。
        例如，如果属性为 "is_active"，则将属性值为 True 的转换成 "可用"，将属性值为 False 的转换成 "停用"；
        如果属性为 "gender"，则将属性值对应的标签信息存储到变量 value 中。
        最后，通过调用 ExcelManage 类创建一个 Excel 表格对象，并将表格标题设置为 "用户列表"。
        接着，通过调用 write_list 方法将行数据写入到 Excel 表格中，并通过调用 save_excel 方法将表格保存到磁盘上。
        最后，通过字典对象将导出的 Excel 表格的 URL 和文件名
        """
        datas = await self.get_datas(**params.dict(), v_return_objs=True)
        # 获取表头
        row = list(map(lambda i: i.get("label"), header))
        rows = []
        options = await vadminSystemCRUD.DictTypeDal(self.db).get_dicts_details(["sys_vadmin_gender"])
        for user in datas:
            data = []
            for item in header:
                field = item.get("field")
                # 通过反射获取对应的属性值
                value = getattr(user, field, "")
                if field == "is_active":
                    value = "可用" if value else "停用"
                elif field == "gender":
                    result = list(filter(lambda i: i["value"] == value, options["sys_vadmin_gender"]))
                    value = result[0]["label"] if result else ""
                data.append(value)
            rows.append(data)
        em = ExcelManage()
        em.create_excel("用户列表")
        em.write_list(rows, row)
        file_url = em.save_excel()
        em.close()
        return {"url": file_url, "filename": "用户列表.xlsx"}

    async def get_import_headers_options(self):
        """
        导入数据时的表头选项进行数据补全
        :return:
        代码解释：
        通过 RoleDal 类获取角色列表，并将列表存储到 roles 变量中。
        从 import_headers 列表中取出角色选项和性别选项，并将其存储到变量 role_options 和 gender_options 中。
        然后，通过对 role_options 和 gender_options 的操作，为这两个选项添加选项值。
        例如，在 role_options 中添加了 options 字段，该字段对应了角色选项的选项值，选项值通过列表推导式生成，其中每个选项都由一个字典元素组成，
        包括标签和值（标签表示角色名称，值表示角色 ID）。而对于 gender_options，它之前已经从数据库中获取了性别选项的详细信息，所以只需要遍历字典对象并将其转换为选项格式即可。
        """
        # 角色选择项
        roles = await RoleDal(self.db).get_datas(limit=0, v_return_objs=True, disabled=False, is_admin=False)
        role_options = self.import_headers[4]
        assert isinstance(role_options, dict)
        role_options["options"] = [{"label": role.name, "value": role.id} for role in roles]

        # 性别选择项
        dict_types = await vadminSystemCRUD.DictTypeDal(self.db).get_dicts_details(["sys_vadmin_gender"])
        gender_options = self.import_headers[3]
        assert isinstance(gender_options, dict)
        sys_vadmin_gender = dict_types.get("sys_vadmin_gender")
        gender_options["options"] = [{"label": item["label"], "value": item["value"]} for item in sys_vadmin_gender]

    async def download_import_template(self):
        """
        用户提供最新版的数据导入模块的下载
        :param self:
        :return:
        代码解释：
        调用了 get_import_headers_options 异步函数，该函数的功能是为导入模板中的表头选项进行补全。
        接着，在获取到补全后的表头选项之后，依次执行了以下操作：
            通过 WriteXlsx 类创建一个 Excel 表格对象 em，并指定表格的名称为 "用户导入模板"。
            调用 generate_template 方法，该方法会根据表头信息生成一个空白的 Excel 导入模板，并将模板存储到磁盘上。
            调用 close 方法释放表格对象所占用的资源。
            返回导出文件的 URL 和文件名
        """
        await self.get_import_headers_options()
        em = WriteXlsx(sheet_name="用户导入模板")
        em.generate_template(copy.deepcopy(self.import_headers))
        em.close()
        return {"url": em.file_url, "filename": "用户导入模板.xlsx"}

    async def import_users(self, file: UploadFile):
        """
        批量导入用户数据
        :param self:
        :param file:
        :return:
        代码解释：
        首先调用了 get_import_headers_options 异步函数，其目的是为表头选项进行补全。
        接着，创建一个 ImportManage 对象，该对象用于管理导入工作，构造函数中传入上传的文件以及表头信息（也是从 self.import_headers 中获取）。
        接下来，调用 get_table_data 方法获取上传文件中的数据并转换成对应的 Python 对象，再调用 check_table_data 方法对数据进行验证。
        然后，遍历验证后的有效数据，将每行数据转换成 schemas.UserIn 类型的 data 对象（schemas.UserIn 是一个 pydantic 模型，用于序列化和反序列化用户数据），
        再调用 create_data 方法进行数据插入操作。在插入操作过程中，如果遇到值错误，则将错误信息添加到旧数据列表中，并使用 add_error_data 方法将错误数据加入错误列表中；
        如果插入操作出现其他异常，则同样将错误信息添加到旧数据列表中，然后将错误数据加入错误列表中。
        最后，函数返回一个字典，包含了导入成功的数量、导入失败的数量，以及错误列表的 URL 地址，用于提醒用户错误记录的查看。
        """
        await self.get_import_headers_options()
        im = ImportManage(file, copy.deepcopy(self.import_headers))
        await im.get_table_data()
        im.check_table_data()
        for item in im.success:
            old_data_list = item.pop("old_data_list")
            data = schemas.UserIn(**item)
            try:
                await self.create_data(data)
            except ValueError as e:
                old_data_list.append(e.__str__())
                im.add_error_data(old_data_list)
            except Exception:
                old_data_list.append("创建失败，请联系管理员！")
                im.add_error_data(old_data_list)
        return {
            "success_number": im.success_number,
            "error_number": im.error_number,
            "error_url": im.generate_error_url()
        }

    async def init_password(self, ids: list[int]):
        """
        初始化所选用户密码
        将用户密码改为系统默认密码，并将初始化密码状态改为False
        :param ids:
        :return:
        代码解释：
        将所选用户的密码重置为系统默认密码，并将用户状态设置为已重置密码。
        在函数中，首先从数据库获取所有指定 ids 的用户数据，然后遍历每个用户进行密码重置和用户状态更新操作。具体来说：
        遍历查询到的用户数据，对每个用户执行以下操作
        - 根据用户手机号生成新密码 password（如果系统默认密码为 "0"，则使用用户手机号码中间7位作为密码；否则使用系统默认密码）。
        - 使用 self.model.get_password_hash 方法将密码进行加密并存储至该用户的 password 字段。
        - 将该用户的 is_reset_password 标记设为 False，表示密码已重置。
        - 将修改过的用户信息添加到数据库 session 中。
        - 构造返回结果 data，包括该用户的 id、telephone、name、email、reset_password_status 和 password（明文密码）。
        - 将 data 添加至结果 result 中。
        - 提交数据库事务，使修改生效。
        - 返回操作结果 result，包括重置密码的用户信息和新密码。
        """
        users = await self.get_datas(limit=0, id=("in", ids), v_return_objs=True)
        result = []
        for user in users:
            # 重置密码
            data = {"id": user.id, "telephone": user.telephone, "name": user.name, "email": user.email}
            password = user.telephone[5:12] if settings.DEFAULT_PASSWORD == "0" else settings.DEFAULT_PASSWORD
            user.password = self.model.get_password_hash(password)
            user.is_reset_password = False
            self.db.add(user)
            data["reset_password_status"] = True
            data["password"] = password
            result.append(data)
        await self.db.flush()
        return result

    async def init_password_send_sms(self, ids: list[int], rd: Redis):
        """
        初始化所选用户密码并发送通知短信
        将用户密码改为系统默认密码，并将初始化密码状态改为false
        :param ids:
        :param rd:
        :return:
        代码解释：
        1.首先调用了 init_password 函数获取到所有指定 ids 的用户，并进行密码初始化操作。然后，遍历每个用户并根据其密码初始化状态执行以下操作：
        2.如果密码未初始化成功，则将该用户的 send_sms_status 标记为 False，表示未发送通知短信；将该用户的 send_sms_msg 值设为 "重置密码失败"。
        如果密码初始化成功，则构造通知短信内容并发送短信，记录发送结果和发送信息。
        - 构造短信内容：使用 AliyunSMS.Scene.reset_password 作为短信场景，将用户新密码 password 传递给短信模板。
        - 发送短信：调用 AliyunSMS.main_async 方法异步发送短信，并获取发送结果 send_result。
        - 记录发送结果和信息：如果发送成功则将 send_sms_status 标记为 True，表示已发送通知短信；否则将 send_sms_status 标记为 False，并将发送失败信息存入 send_sms_msg 中
        3.将修改过的用户信息添加至结果列表 result 中。
        4，提交数据库事务，使修改生效。
        5.返回操作结果 result，包括初始化密码的用户信息、新密码和通知短信的发送状态和信息。
        """
        result = await self.init_password(ids)
        for user in result:
            if not user["reset_password_status"]:
                user["send_sms_status"] = False
                user["send_sms_msg"] = "重置密码失败"
                continue
            password = user.pop("password")
            sms = AliyunSMS(rd, user.get("telephone"))
            try:
                send_result = await sms.main_async(AliyunSMS.Scene.reset_password, password=password)
                user["send_sms_status"] = send_result
                user["send_sms_msg"] = "" if send_result else "发送失败，请联系管理员"
            except CustomException as e:
                user["send_sms_status"] = False
                user["send_sms_msg"] = e.msg
        return result

    async def init_password_send_email(self, ids: list[int], rd: Redis):
        """
        初始化所选用户密码并发送通知邮件
        将用户密码改为系统默认密码，并将初始化密码状态改为false
        :param ids:
        :param rd:
        :return:
        代码解释：
        首先调用了 init_password 函数获取到所有指定 ids 的用户，并进行密码初始化操作。然后，遍历每个用户并根据其密码初始化状态执行以下操作：
        1.如果密码未初始化成功，则将该用户的 send_sms_status 标记为 False，表示未发送通知邮件；将该用户的 send_sms_msg 值设为 "重置密码失败"。
        2.如果密码初始化成功，则构造通知邮件信息并发送邮件，记录发送结果和发送信息。
        - 构造邮件内容：包括邮件主题 subject 和邮件正文 body，其中正文使用新密码 password 替换掉原来的密码。
        - 发送邮件：调用 EmailSender.send_email 方法异步发送邮件，并获取发送结果 send_result。
        - 记录发送结果和信息：如果发送成功则将 send_sms_status 标记为 True，表示已发送通知邮件；否则将 send_sms_status 标记为 False，并将发送失败信息存入 send_sms_msg 中。
        3.将修改过的用户信息添加至结果列表 result 中。
        4，提交数据库事务，使修改生效。
        5.返回操作结果 result，包括初始化密码的用户信息、新密码和通知邮件的发送状态和信息。
        """
        result = await self.init_password(ids)
        for user in result:
            if not user["reset_password_status"]:
                user["send_sms_status"] = False
                user["send_sms_msg"] = "重置密码失败"
                continue
            password: str = user.pop("password")
            email: str = user.get("email", None)
            if email:
                subject = "密码已重置"
                body = f"您好，您的密码已经重置为{password}，请及时登录并修改密码。"
                es = EmailSender(rd)
                try:
                    send_result = await es.send_email([email], subject, body)
                    user["send_sms_status"] = send_result
                    user["send_sms_msg"] = "" if send_result else "发送失败，请联系管理员"
                except CustomException as e:
                    user["send_sms_status"] = False
                    user["send_sms_msg"] = e.msg
            else:
                user["send_sms_status"] = False
                user["send_sms_msg"] = "未获取到邮箱地址"
        return result

    async def update_current_avatar(self, user: models.VadminUser, file: UploadFile):
        """
        更新当前用户头像
        :param user:
        :param file:
        :return:
        代码解释：
        调用了 AliyunOSS 类中的 upload_image 方法上传头像图片至阿里云OSS，并获取上传结果 result。
        如果上传失败，则会抛出自定义异常 CustomException，并返回错误码 status.HTTP_ERROR。
        将上传成功后的图片地址 result 赋值给当前用户的 avatar 字段，并将用户信息更新到数据库中，使用 flush 方法提交事务，使修改生效。
        返回上传成功后的图片地址 result。
        """
        result = await AliyunOSS(BucketConf(**settings.ALIYUN_OSS)).upload_image("avatar", file)
        user.avatar = result
        await self.flush(user)
        return result

    async def update_wx_server_openid(self, code: str, user: models.VadminUser, redis: Redis):
        """
        更新用户服务端微信平台openid
        :param code:
        :param user:
        :param rd:
        :return:
        代码解释：
        实例化 WXOAuth 类的实例，并调用其 parsing_openid 方法传入 code 以获取 openid 值。如果获取不到 openid，则返回 False。
        将获取到的 openid 值赋值给当前用户的 wx_server_openid 字段，并将 is_wx_server_openid 标志设置为 True，表示用户已经在服务端微信平台授权。
        使用 flush 方法提交事务，使修改生效，同时返回 True 表示操作成功。
        调用该函数即可更新用户的服务端微信平台 openid。
        """
        wx = WXOAuth(redis, 0)
        openid = await wx.parsing_openid(code)
        if not openid:
            return False
        user.is_wx_server_openid = True
        user.wx_server_openid = openid
        await self.flush(user)
        return True

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs):
        """
        删除多个用户，软删除
        :param ids:
        :param v_soft:
        :param kwargs:
        :return:
        代码解释：
        调用 self.get_datas 方法获取指定 ids 的用户对象列表，并使用 joinedload 方法将用户关联的角色信息预加载，提高查询性能。
        遍历每个用户对象，将其关联的角色信息清空，以解除与角色之间的关联关系。
        调用父类中的 delete_datas 方法将指定 ids 的用户对象进行软删除，返回操作结果。
        调用该函数即可对指定的多个用户进行软删除，并解除角色关联关系。
        """
        options = [joinedload(self.model.roles)]
        objs = await self.get_datas(limit=0, id=("in", ids), v_options=options, v_return_objs=True)
        for obj in objs:
            if obj.roles:
                obj.roles.clear()
        return await super(UserDal, self).delete_datas(ids, v_soft, **kwargs)


class RoleDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(RoleDal, self).__init__(db, models.VadminRole, schemas.RoleSimpleOut)

    async def create_data(
            self,
            data: schemas.RoleIn,
            v_options: list = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ):
        """
        创建一个新的角色实例
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        代码解释:
        从传入的参数 data 中排除 menu_ids 字段，使用 dict 方法将除menu_ids以外的数据转换为字典格式。
        然后，根据角色模型类 self.model 和转换后的字典构建一个新的角色实例对象 obj。
        查询菜单数据，通过 MenuDal 类的 get_datas 方法获取所有 ID 在 data.menu_ids 列表中的菜单对象，预加载菜单关联的权限数据，提高查询性能。
        然后，遍历列表中的菜单对象，将其添加到 obj.menus 属性中。
        通过 flush 方法将新增记录同步到数据库中，使新创建的角色实例生效。
        如果需要返回新创建的角色实例，则调用 out_dict 方法将其转换为 dict，并根据传入参数返回结果。
        """
        obj = self.model(**data.model_dump(exclude={'menu_ids'}))
        menus = await MenuDal(db=self.db).get_datas(limit=0, id=("in", data.menu_ids), v_return_objs=True)
        if data.menu_ids:
            for menu in menus:
                obj.menus.append(menu)
        await self.flush(obj)
        return await self.out_dict(obj, v_options, v_return_obj, v_schema)

    async def put_data(
            self,
            data_id: int,
            data: schemas.RoleIn,
            v_options: list = None,
            v_return_obj: bool = False,
            v_schema: Any = None
    ):
        """
        更新指定 ID 的角色实例
        :param data_id:
        :param data:
        :param v_options:
        :param v_return_obj:
        :param v_schema:
        :return:
        代码解释：
        调用 get_data 方法获取指定 ID 的角色实例对象，并使用 joinedload 方法将数据关联的菜单信息预加载，提高查询性能。
        然后，使用 jsonable_encoder 方法将传入的 data 转换为字典格式。
        遍历 obj_dict 字典中的键值对，检查是否有待更新的菜单信息。
        如果存在待更新菜单信息，则对 obj 对象的 menus 属性进行处理，清除原有的关联关系并重新关联新的菜单对象；
        如果不存在，则直接设置相应属性的值为传入的数据值。
        通过 flush 方法将修改记录同步到数据库中，使更新的角色实例生效。
        如果需要返回更新后的角色实例，则调用 out_dict 方法将其转换为 dict，并根据传入参数返回结果。
        """
        obj = await self.get_data(data_id, v_options=[joinedload(self.model.menus)])
        obj_dict = jsonable_encoder(data)
        for key, value in obj_dict.items():
            if key == "menu_ids":
                if obj.menus:
                    obj.menus.clear()
                if value:
                    menus = await MenuDal(db=self.db).get_datas(limit=0, id=("in", value), v_return_objs=True)
                    for menu in menus:
                        obj.menus.append(menu)
                continue
            setattr(obj, key, value)
        await self.flush(obj)
        return await self.out_dict(obj, None, v_return_obj, v_schema)

    async def get_role_menu_tree(self, role_id: int):
        role = await self.get_data(role_id, v_options=[joinedload(self.model.menus)])
        return [i.id for i in role.menus]

    async def get_select_datas(self):
        """
        获取所有角色实例对象的选择数据
        :return:
        代码解释：
        使用 select 方法构建一个查询表达式，查询角色模型类 self.model 所有的数据。
        然后，使用 await self.db.execute(sql) 方法执行查询，并将结果集保存在 queryset 变量中。
        使用 queryset.scalars().all() 方法将结果集转换为包含所有实例对象的列表，遍历列表中的实例对象，
        使用 from_orm 方法将每个实例对象转换为 RoleSelectOut 模型类的对象，并使用 dict 方法生成对应的字典格式。最后，将字典格式数据组成的列表作为函数的返回值。
        """
        sql = select(self.model)
        queryset = await self.db.execute(sql)
        return [schemas.RoleSelectOut.model_validate(i).model_dump() for i in queryset.scalars().all()]

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs):
        """
        删除多个角色，硬删除
        :param ids:
        :param v_soft:
        :param kwargs:
        :return:
        代码解释：
        调用 get_datas 方法，查询 ID 在 ids 列表中的所有角色实例对象，并添加过滤条件 user_total_number > 0，以确保角色实例对象没有关联的用户。
        如果查询到至少一个符合条件的角色实例对象，抛出一个自定义异常 "无法删除存在用户关联的角色"。
        调用父类 super(RoleDal, self).delete_datas(ids, v_soft, **kwargs) 的 delete_datas 方法，将符合条件的角色实例对象从数据库中删除，并返回删除操作影响到的记录数
        """
        objs = await self.get_datas(limit=0, id=("in", ids), user_total_number=(">", 0), v_return_objs=True)
        if objs:
            raise CustomException("无法删除存在用户关联的角色", code=400)
        return await super(RoleDal, self).delete_datas(ids, v_soft, **kwargs)


class MenuDal(DalBase):

    def __init__(self, db: AsyncSession):
        super(MenuDal, self).__init__(db, models.VadminMenu, schemas.MenuSimpleOut)

    async def get_tree_list(self, mode: int):
        """
        获取菜单树列表
        获取菜单选择项，添加、修改菜单时使用
        获取菜单树列表，角色天机菜单权限时使用
        :param mode:
        :return:
        代码解释：
        如果 mode=1，则获取菜单树列表，用于添加、修改菜单时使用。
        如果 mode=2 或 mode=3，则获取菜单选择项，用于角色天机菜单权限时使用。其中，mode=3 表示只返回可用的菜单选择项。
        如果 mode 值未在上述情况中，则抛出自定义异常 "获取菜单失败，无可用选项"。
        在函数中，根据 mode 参数的不同，构建不同的查询表达式 sql，并执行查询，将结果集保存在 queryset 变量中。
        接着，从 queryset 中获取所有实例对象并保存在 datas 变量中。
        使用 filter() 函数筛选出顶层菜单（即没有父菜单的菜单）保存在 roots 变量中。
        再根据 mode 的值，调用相应的生成树形列表方法 generate_tree_list 或 generate_tree_options 生成菜单树列表或菜单选择项。
        调用 menus_order 方法对生成的结果进行排序，最终将结果作为函数的返回值。
        """
        if mode == 3:
            sql = select(self.model).where(self.model.disabled == 0, self.model.is_delete == False)
        else:
            sql = select(self.model).where(self.model.is_delete == False)
        queryset = await self.db.execute(sql)
        datas = queryset.scalars().all()
        roots = filter(lambda i: not i.parent_id, datas)
        if mode == 1:
            menus = self.generate_tree_list(datas, roots)
        elif mode == 2 or mode == 3:
            menus = self.generate_tree_options(datas, roots)
        else:
            raise CustomException("获取菜单失败，无可用选项", code=400)
        return self.menus_order(menus)

    async def get_routers(self, user: models.VadminUser):
        """
        获取路由表
        :param user:
        :return:
        代码解释：
        如果用户拥有任意一个角色的权限为管理员权限，则查询所有没有被禁用并且不是按钮类型的菜单，并将查询结果保存在 datas 变量中。
        否则，查询用户所拥有角色中每个菜单不被禁用并且不是按钮类型的菜单，并将查询结果保存在 datas 变量中。
        使用 filter() 函数筛选出顶层路由（即没有父路由的路由）保存在 roots 变量中。
        使用 generate_router_tree 方法生成路由表，并使用 menus_order 方法对结果进行排序，最终将结果作为函数的返回值。
        """
        if any([i.is_admin for i in user.roles]):
            sql = select(self.model) \
                .where(self.model.disabled == 0, self.model.menu_type != "2", self.model.is_delete == False)
            queryset = await self.db.execute(sql)
            datas = queryset.scalars().all()
        else:
            options = [joinedload(models.VadminUser.roles), joinedload("roles.menus")]
            user = await UserDal(self.db).get_data(user.id, v_options=options)
            datas = set()
            for role in user.roles:
                for menu in role.menus:
                    # 该路由没有被禁用，并且菜单不是按钮
                    if not menu.disabled and menu.menu_type != "2":
                        datas.add(menu)
        roots = filter(lambda i: not i.parent_id, datas)
        menus = self.generate_router_tree(datas, roots)
        return self.menus_order(menus)

    def generate_router_tree(self, menus: list[models.VadminMenu], nodes: filter, name: str = "") -> list:
        """
        生成路由树
        :param menus: 总菜单列表
        :param nodes: 节点菜单列表
        :param name: name拼接，切记Name不能重复
        :return:
        代码解释：
        创建一个空列表 data 用于存储转化后的节点数据。
        然后遍历节点菜单列表 nodes，对于每个节点使用 schemas.RouterOut.from_orm() 方法根据 root 中的数据创建一个新的 RouterOut 对象 router，
        并将其 name 属性设置为 name 和路径中各个单词首字母大写的拼接结果，例如：将 path 为 "/user/setting" 的节点的 name 设为 "UserSetting"。
        同时，将其 meta 属性设置为节点在路由中的元数据，包括标题、图标、是否隐藏等信息。
        接着，判断当前节点的类型是否为菜单类型，如果是则递归调用本函数来获取与该节点相关联的子节点，并将子节点列表赋给 router.children 属性。
        最后，将转化后的节点数据以字典形式添加到 data 列表中，并将 data 列表作为函数的返回值。
        """
        data = []
        for root in nodes:
            router = schemas.RouterOut.model_validate(root)
            router.name = name + "".join(name.capitalize() for name in router.path.split("/"))
            router.meta = schemas.Meta(title=root.title, icon=root.icon, hidden=root.hidden, alwaysShow=root.alwaysShow)
            if root.menu_type == "0":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router.children = self.generate_router_tree(menus, sons, router.name)
            data.append(router.model_dump())
        return data

    def generate_tree_list(self, menus: list[models.VadminMenu], nodes: filter) -> list:
        """
        生成菜单树列表
        :param menus: 所有的菜单项
        :param nodes: 菜单树的根节点
        :return:
        代码解释：
        首先初始化一个空列表data。
        对于每个节点root遍历nodes，将节点转换为schemas.TreeListOut类型的变量router。
        如果节点的type为0或1，即为父节点，需要递归查找其所有子节点，具体操作是通过filter筛选出该节点的所有子节点，
        然后再调用generate_tree_list函数递归处理该子节点，直到处理完当前节点的所有子节点。
        将处理好的节点加入到data列表中。
        最后返回处理好的data列表，即所有的节点及其对应的子节点组成的菜单树列表。
        """
        data = []
        for root in nodes:
            router = schemas.TreeListOut.model_validate(root)
            if root.menu_type == "0" or root.menu_type == "1":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router.children = self.generate_tree_list(menus, sons)
            data.append(router.model_dump())
        return data

    def generate_tree_options(self, menus: list[models.VadminMenu], nodes: filter) -> list:
        """
        生成菜单树选择项
        :param menus: 所有菜单数据
        :param nodes: 筛选后剩余的节点信息
        :return:
        代码解释：
        首先初始化一个空列表data。
        该方法通过遍历nodes中的每一个节点，生成一个router字典对象，其中包含了该节点的id、标题和顺序等信息。
        如果该节点的menu_type属性值为0或1，则说明该节点有子节点，需要递归调用generate_tree_options方法来生成子节点的菜单树。子节点存储在router对象的children属性中。
        将生成的router对象添加到data数组中，并最终将该数组作为方法的返回值返回。
        """
        data = []
        for root in nodes:
            router = {"value": root.id, "label": root.title, "order": root.order}
            if root.menu_type == "0" or root.menu_type == "1":
                sons = filter(lambda i: i.parent_id == root.id, menus)
                router["children"] = self.generate_tree_options(menus, sons)
            data.append(router)
        return data

    @classmethod
    def menus_order(cls, datas: list, order: str = "order", children: str = "children"):
        """
        菜单排序
        :param datas: 菜单列表
        :param order: 排序的关键字
        :param children: 菜单嵌套的子菜单列表名称
        :return:
        代码解释：
        对菜单列表进行排序，首先根据输入的order参数进行一级菜单的排序，然后再遍历每个一级菜单的子菜单列表，根据order参数进行二级菜单的排序。
        最后返回排好序的菜单列表。
        """
        result = sorted(datas, key=lambda menu: menu[order])
        for item in result:
            if item[children]:
                item[children] = sorted(item[children], key=lambda menu: menu[order])
        return result

    async def delete_datas(self, ids: list[int], v_soft: bool = False, **kwargs):
        """
        删除多个菜单
        如果存在角色关联则无法删除
        :param ids: 需要删除的菜单ID列表
        :param v_soft: 是否执行软删除
        :param kwargs: 其他更新字段
        :return:
        代码解释：
        在执行删除之前，它会调用get_datas方法来获取对应的菜单数据对象，并通过joinedload方式预加载了角色关联信息。
        然后它会遍历所有要删除的菜单数据对象，检查是否存在与角色相关联的记录。如果存在，则抛出自定义异常并终止删除操作。
        如果没有存在关联的菜单数据，则调用父类的delete_datas方法来真正执行删除操作。
        其中，v_soft参数决定是进行软删除还是硬删除，其他可选字段则可以为删除操作添加其他更新字段。最终返回删除结果。
        """
        options = [joinedload(self.model.roles)]
        objs = await self.get_datas(limit=0, id=("in", ids), v_return_objs=True, v_options=options)
        for obj in objs:
            if obj.roles:
                raise CustomException("无法删除存在角色关联的菜单", code=400)
        return await super(MenuDal, self).delete_datas(ids, v_soft, **kwargs)
