#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/14 17:37
# @Author  : 冉勇
# @Site    :
# @File    : user.py
# @Software: PyCharm
# @desc    : 用户模型
import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship
from db.db_base import BaseModel
from sqlalchemy import Column, String, Boolean, DateTime
from passlib.context import CryptContext
from .m2m import vadmin_user_roles

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class VadminUser(BaseModel):
    """
    代码解释：
    定义了一个名为 vadmin_auth_user 的用户表格
    id 列，这个列在代码中没有显示定义，但是可以默认继承自父类 BaseModel 中的主键 id 列。
    avatar 列，表示用户头像，数据类型为字符串型（String），最大长度为 500。该列可以为空（nullable=True），并且有注释 comment="头像"。
    telephone 列，表示用户手机号码，数据类型为字符串型，最大长度为 11。该列不能为空（nullable=False），并且被设置为索引（index=True），不具备唯一性（unique=False），同时有注释 comment="手机号"。
    email 列，表示用户电子邮箱地址，数据类型为字符串型，最大长度为 50。该列可以为空，并且有注释 comment="邮箱地址"。
    name 列，表示用户姓名，数据类型为字符串型，最大长度为 50。该列不能为空，并且被设置为索引（index=True），具备唯一性（unique=False），同时有注释 comment="姓名"。
    nickname 列，表示用户昵称，数据类型为字符串型，最大长度为 50。该列可以为空，并且有注释 comment="昵称"。
    password 列，表示用户密码，数据类型为字符串型，最大长度为 255。该列可以为空，并且有注释 comment="密码"。密码在数据库中应该是经过加密处理的。在代码中，通过导入 passlib.context 模块并使用 bcrypt 加密算法对密码进行处理。
    gender 列，表示用户性别，数据类型为字符串型，最大长度为 8。该列可以为空，并且有注释 comment="性别"。
    is_active 列，表示用户是否可用，数据类型为布尔型（Boolean），默认值为 True。该列有注释 comment="是否可用"。
    is_reset_password 列，表示用户是否已重置密码，数据类型为布尔型，默认值为 False。如果为 False，则用户在登录系统后必须重置密码。该列有注释 comment="是否已经重置密码，没有重置的，登录系统后必须重置密码"。
    last_ip 列，表示用户最后一次登录的 IP 地址，数据类型为字符串型，最大长度为 50。该列可以为空，并且有注释 comment="最后一次登录IP"。
    last_login 列，表示用户最后一次登录的时间，数据类型为日期时间型（DateTime）。该列可以为空，并且有注释 comment="最后一次登录时间"。
    is_staff 列，表示用户是否为工作人员，数据类型为布尔型，默认值为 False。该列有注释 comment="是否为工作人员"。
    wx_server_openid 列，表示服务端微信平台 OpenId，数据类型为字符串型，最大长度为 255。该列可以为空，并且有注释 comment="服务端微微信平台OpenId"。
    roles 列，表示用户拥有的角色，数据类型为关系型（relationship），表示该列与 VadminRole 对象之间存在着多对多的关系。这里通过关键字参数指定该关系在数据库中是由另一个名为 vadmin_user_roles 的表格维护的，这个表格定义在 m2m.py 模块中。
    """
    __tablename__ = "vadmin_auth_user"
    __table_args__ = ({'comment': '用户表'})
    avatar = Column(String(500), nullable=True, comment='头像')
    telephone = Column(String(11), nullable=False, index=True, comment="手机号", unique=False)
    email = Column(String(50), nullable=True, comment="邮箱地址")
    name = Column(String(50), index=True, nullable=False, comment="姓名")
    nickname = Column(String(50), nullable=True, comment="昵称")
    password = Column(String(255), nullable=True, comment="密码")
    gender = Column(String(8), nullable=True, comment="性别")
    is_active = Column(Boolean, default=True, comment="是否可用")
    is_reset_password = Column(Boolean, default=False, comment="是否已经重置密码，没有重置的，登陆系统后必须重置密码")
    last_ip = Column(String(50), nullable=True, comment="最后一次登录IP")
    last_login = Column(DateTime, nullable=True, comment="最近一次登录时间")
    is_staff = Column(Boolean, default=False, comment="是否为工作人员")
    wx_server_openid = Column(String(255), comment="服务端微信平台openid")
    is_wx_server_openid = Column(Boolean, default=False, comment="是否已有服务端微信平台openid")

    roles = relationship("VadminRole", back_populates='users', secondary=vadmin_user_roles)

    # generate hash password
    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    # verify login password
    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        return pwd_context.verify(password, hashed_password)

    async def update_login_info(self, db: AsyncSession, last_ip: str):
        """
        更新当前登录信息
        :param db: 数据库
        :param last_ip: 最近一次登录 IP
        :return:
        """
        self.last_ip = last_ip
        self.last_login = datetime.datetime.now()
        await db.flush()

    async def is_admin(self) -> bool:
        """
        获取该用户是否拥有最高权限
        以最高权限为准
        :return:
        """
        return any([i.is_admin for i in self.roles])
