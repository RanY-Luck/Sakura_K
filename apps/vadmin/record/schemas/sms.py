#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/25 19:30
# @Author  : 冉勇
# @Site    :
# @File    : sms.py
# @Software: PyCharm
# @desc    : pydantic 模型，用于数据库序列化操作
"""
pydantic 验证数据：https://blog.csdn.net/qq_44291044/article/details/104693526
代码解释：
定义了两个 Pydantic 模型，SMSSendRecord 和 SMSSendRecordSimpleOut。
SMSSendRecord 是一个基础模型，它包含了一些短信发送记录的基本信息，包括电话号码（telephone）、发送状态（status）、用户 ID（user_id）、
短信内容（content）、描述（desc）和场景（scene）。其中，telephone 和 status 属性是必需的，其他属性都是可选的。
SMSSendRecordSimpleOut 继承了 SMSSendRecord，并扩展了三个属性：id、create_datetime 和 update_datetime。
其中，id 属性表示短信发送记录的唯一标识，create_datetime 属性表示短信发送记录的创建时间，update_datetime 属性表示短信发送记录的更新时间。这三个属性都是必需的。
SMSSendRecordSimpleOut 的 Config 类中设置了 orm_mode = True，这表示该模型可以被用作 SQLAlchemy ORM 模型的返回类型。
这样可以确保返回的数据符合 SQLAlchemy ORM 模型的属性要求。
此外，该代码中还引入了 DatetimeStr 类型，它是一个自定义的 Pydantic 数据类型，用于处理日期时间字符串。
由于 SMSSendRecordSimpleOut 包含了 create_datetime 和 update_datetime 属性，因此需要使用 DatetimeStr 类型来确保这些属性的值是有效的日期时间字符串。
"""
from pydantic import BaseModel, ConfigDict

from core.data_types import DatetimeStr


class SMSSendRecord(BaseModel):
    telephone: str
    status: bool = True
    user_id: int | None = None
    content: str | None = None
    desc: str | None = None
    scene: str | None = None


class SMSSendRecordSimpleOut(SMSSendRecord):
    id: int
    create_datetime: DatetimeStr
    update_datetime: DatetimeStr

    model_config = ConfigDict(from_attributes=True)
