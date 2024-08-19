```python
# 安装项目依赖环境
pip3 install -r requirements.txt

# 配置环境
根目录复制 .env.dev.example -> .env.dev
在.env.dev文件中配置开发环境的数据库和redis
## 数据库
############################################
# 数据库主机
DB_HOST = '127.0.0.1'
# 数据库端口
DB_PORT = 3306
# 数据库用户名
DB_USERNAME = 'root'
# 数据库密码
DB_PASSWORD = 'Ranyong_520'
# 数据库名称
DB_DATABASE = 'Sakura_K_fastapi'
############################################

## redis
############################################
# Redis主机
REDIS_HOST = '127.0.0.1'
# Redis端口
REDIS_PORT = 6379
# Redis用户名
REDIS_USERNAME = ''
# Redis密码
REDIS_PASSWORD = ''
# Redis数据库
REDIS_DATABASE = 11
############################################

# 运行sql文件
1.新建数据库Sakura_K_fastapi(默认，可修改)
2.使用命令或数据库连接工具运行sql文件夹下的Sakura_K_fastapi.sql

# 运行后端
## 运行 cli
python3 app.py -h
## 测试环境
python3 app.py --env=dev
## 生产环境
python3 app.py --env=prod
```

# 接口编写顺序

## 第一步:先去`module_admin/entity/do`写表结构

```python
from sqlalchemy import Column, Integer, String, LargeBinary
from config.database import Base


class SysNotice(Base):
    """
    通知公告表
    """
    __tablename__ = 'sys_notice'
    __table_args__ = ({'comment': '通知公告表'})

    notice_id = Column(Integer, primary_key=True, autoincrement=True, comment='公告ID')
    notice_title = Column(String(50, collation='utf8_general_ci'), nullable=False, comment='公告标题')
    notice_type = Column(String(1, collation='utf8_general_ci'), nullable=False, comment='公告类型（1通知 2公告）')
    notice_content = Column(LargeBinary, comment='公告内容')
    status = Column(String(1, collation='utf8_general_ci'), default='0', comment='公告状态（0正常 1关闭）')
```

## 第二步:再去`module_admin/entity/vo`写 pydantic 模型

```python
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from pydantic_validation_decorator import NotBlank, Size, Xss
from typing import Literal, Optional
from module_admin.annotation.pydantic_annotation import as_form, as_query


class NoticeModel(BaseModel):
    """
    通知公告表对应pydantic模型
    """
    model_config = ConfigDict(alias_generator=to_camel, from_attributes=True)

    notice_id: Optional[int] = Field(default=None, description='公告ID')
    notice_title: Optional[str] = Field(default=None, description='公告标题')
    notice_type: Optional[Literal['1', '2']] = Field(default=None, description='公告类型（1通知 2公告）')
    notice_content: Optional[bytes] = Field(default=None, description='公告内容')
    status: Optional[Literal['0', '1']] = Field(default=None, description='公告状态（0正常 1关闭）')
    create_by: Optional[str] = Field(default=None, description='创建者')
    create_time: Optional[datetime] = Field(default=None, description='创建时间')
    update_by: Optional[str] = Field(default=None, description='更新者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    remark: Optional[str] = Field(default=None, description='备注')

    @Xss(field_name='notice_title', message='公告标题不能包含脚本字符')
    @NotBlank(field_name='notice_title', message='公告标题不能为空')
    @Size(field_name='notice_title', min_length=0, max_length=50, message='公告标题不能超过50个字符')
    def get_notice_title(self):
        return self.notice_title

    def validate_fields(self):
        self.get_notice_title()


class NoticeQueryModel(NoticeModel):
    """
    通知公告管理不分页查询模型
    """
    begin_time: Optional[str] = Field(default=None, description='开始时间')
    end_time: Optional[str] = Field(default=None, description='结束时间')


@as_query
@as_form
class NoticePageQueryModel(NoticeQueryModel):
    """
    通知公告管理分页查询模型
    """
    page_num: int = Field(default=1, description='当前页码')
    page_size: int = Field(default=10, description='每页记录数')


class DeleteNoticeModel(BaseModel):
    """
    删除通知公告模型
    """
    model_config = ConfigDict(alias_generator=to_camel)

    notice_ids: str = Field(description='需要删除的公告ID')

```

## 第三步:再去`module_admin/dao`写对数据库crud操作

```python
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from module_admin.entity.do.notice_do import SysNotice
from module_admin.entity.vo.notice_vo import *
from utils.page_util import PageUtil
from datetime import datetime, time


class NoticeDao:
    """
    通知公告管理模块数据库操作层
    """

    @classmethod
    async def get_notice_detail_by_id(cls, db: AsyncSession, notice_id: int):
        """
        根据通知公告id获取通知公告详细信息
        :param db: orm对象
        :param notice_id: 通知公告id
        :return: 通知公告信息对象
        """
        notice_info = (await db.execute(
            select(SysNotice)
                .where(SysNotice.notice_id == notice_id)
        )).scalars().first()

        return notice_info

    @classmethod
    async def get_notice_detail_by_info(cls, db: AsyncSession, notice: NoticeModel):
        """
        根据通知公告参数获取通知公告信息
        :param db: orm对象
        :param notice: 通知公告参数对象
        :return: 通知公告信息对象
        """
        notice_info = (await db.execute(
            select(SysNotice)
                .where(
                SysNotice.notice_title == notice.notice_title if notice.notice_title else True,
                SysNotice.notice_type == notice.notice_type if notice.notice_type else True,
                SysNotice.notice_content == notice.notice_content if notice.notice_content else True
            )
        )).scalars().first()

        return notice_info

    @classmethod
    async def get_notice_list(cls, db: AsyncSession, query_object: NoticePageQueryModel, is_page: bool = False):
        """
        根据查询参数获取通知公告列表信息

        :param db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 通知公告列表信息对象
        """
        query = (
            select(SysNotice)
                .where(
                SysNotice.notice_title.like(f'%{query_object.notice_title}%') if query_object.notice_title else True,
                SysNotice.create_by.like(f'%{query_object.create_by}%') if query_object.create_by else True,
                SysNotice.notice_type == query_object.notice_type if query_object.notice_type else True,
                SysNotice.create_time.between(
                    datetime.combine(datetime.strptime(query_object.begin_time, '%Y-%m-%d'), time(00, 00, 00)),
                    datetime.combine(datetime.strptime(query_object.end_time, '%Y-%m-%d'), time(23, 59, 59)),
                )
                if query_object.begin_time and query_object.end_time
                else True,
            )
                .distinct()
        )
        notice_list = await PageUtil.paginate(db, query, query_object.page_num, query_object.page_size, is_page)

        return notice_list

    @classmethod
    async def add_notice_dao(cls, db: AsyncSession, notice: NoticeModel):
        """
        新增通知公告数据库操作
        :param db: orm对象
        :param notice: 通知公告对象
        :return:
        """
        db_notice = SysNotice(**notice.model_dump())
        db.add(db_notice)
        await db.flush()

        return db_notice

    @classmethod
    async def edit_notice_dao(cls, db: AsyncSession, notice: dict):
        """
        编辑通知公告数据库操作
        :param db: orm对象
        :param notice: 需要更新的通知公告字典
        :return:
        """
        await db.execute(
            update(SysNotice),
            [notice]
        )

    @classmethod
    async def delete_notice_dao(cls, db: AsyncSession, notice: NoticeModel):
        """
        删除通知公告数据库操作
        :param db: orm对象
        :param notice: 通知公告对象
        :return:
        """
        await db.execute(
            delete(SysNotice)
                .where(SysNotice.notice_id.in_([notice.notice_id]))
        )
```

## 第四步:再去`module_admin/service`写接口crud服务

```python
from module_admin.dao.notice_dao import *
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.common_util import CamelCaseUtil


class NoticeService:
    """
    通知公告管理模块服务层
    """

    @classmethod
    async def get_notice_list_services(
            cls,
            query_db: AsyncSession,
            query_object: NoticePageQueryModel,
            is_page: bool = True
    ):
        """
        获取通知公告列表信息service
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 通知公告列表信息对象
        """
        notice_list_result = await NoticeDao.get_notice_list(query_db, query_object, is_page)

        return notice_list_result

    @classmethod
    async def add_notice_services(cls, query_db: AsyncSession, page_object: NoticeModel):
        """
        新增通知公告信息service
        :param query_db: orm对象
        :param page_object: 新增通知公告对象
        :return: 新增通知公告校验结果
        """
        notice = await NoticeDao.get_notice_detail_by_info(query_db, page_object)
        if notice:
            result = dict(is_success=False, message='通知公告已存在')
        else:
            try:
                await NoticeDao.add_notice_dao(query_db, page_object)
                await query_db.commit()
                result = dict(is_success=True, message='新增成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        return CrudResponseModel(**result)

    @classmethod
    async def edit_notice_services(cls, query_db: AsyncSession, page_object: NoticeModel):
        """
        编辑通知公告信息service
        :param query_db: orm对象
        :param page_object: 编辑通知公告对象
        :return: 编辑通知公告校验结果
        """
        edit_notice = page_object.model_dump(exclude_unset=True)
        notice_info = await cls.notice_detail_services(query_db, edit_notice.get('notice_id'))
        if notice_info:
            if notice_info.notice_title != page_object.notice_title or notice_info.notice_type != page_object.notice_type or notice_info.notice_content != page_object.notice_content:
                notice = await NoticeDao.get_notice_detail_by_info(query_db, page_object)
                if notice:
                    result = dict(is_success=False, message='通知公告已存在')
                    return CrudResponseModel(**result)
            try:
                await NoticeDao.edit_notice_dao(query_db, edit_notice)
                await query_db.commit()
                result = dict(is_success=True, message='通知公告更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='通知公告不存在')

        return CrudResponseModel(**result)

    @classmethod
    async def delete_notice_services(cls, query_db: AsyncSession, page_object: DeleteNoticeModel):
        """
        删除通知公告信息service
        :param query_db: orm对象
        :param page_object: 删除通知公告对象
        :return: 删除通知公告校验结果
        """
        if page_object.notice_ids.split(','):
            notice_id_list = page_object.notice_ids.split(',')
            try:
                for notice_id in notice_id_list:
                    await NoticeDao.delete_notice_dao(query_db, NoticeModel(noticeId=notice_id))
                await query_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='传入通知公告id为空')
        return CrudResponseModel(**result)

    @classmethod
    async def notice_detail_services(cls, query_db: AsyncSession, notice_id: int):
        """
        获取通知公告详细信息service
        :param query_db: orm对象
        :param notice_id: 通知公告id
        :return: 通知公告id对应的信息
        """
        notice = await NoticeDao.get_notice_detail_by_id(query_db, notice_id=notice_id)
        result = NoticeModel(**CamelCaseUtil.transform_result(notice))

        return result
```

## 第五步:再去`module_admin/controller`写接口

```python
from datetime import datetime
from fastapi import APIRouter, Depends, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.notice_vo import DeleteNoticeModel, NoticeModel, NoticePageQueryModel
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.notice_service import NoticeService
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

noticeController = APIRouter(prefix='/system/notice', dependencies=[Depends(LoginService.get_current_user)])


@noticeController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:list'))]
)
async def get_system_notice_list(
        request: Request,
        notice_page_query: NoticePageQueryModel = Depends(NoticePageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    """
    获取系统通知公告列表
    """
    # 获取分页数据
    notice_page_query_result = await NoticeService.get_notice_list_services(query_db, notice_page_query, is_page=True)
    logger.info('系统通知公告获取成功')

    return ResponseUtil.success(model_content=notice_page_query_result)


@noticeController.post('', dependencies=[Depends(CheckUserInterfaceAuth('system:notice:add'))])
@ValidateFields(validate_model='add_notice')
@Log(title='通知公告', business_type=BusinessType.INSERT)
async def add_system_notice(
        request: Request,
        add_notice: NoticeModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    新增通知公告
    """
    add_notice.create_by = current_user.user.user_name
    add_notice.create_time = datetime.now()
    add_notice.update_by = current_user.user.user_name
    add_notice.update_time = datetime.now()
    add_notice_result = await NoticeService.add_notice_services(query_db, add_notice)
    logger.info(add_notice_result.message)

    return ResponseUtil.success(msg=add_notice_result.message)


@noticeController.put('', dependencies=[Depends(CheckUserInterfaceAuth('system:notice:edit'))])
@ValidateFields(validate_model='edit_notice')
@Log(title='通知公告', business_type=BusinessType.UPDATE)
async def edit_system_notice(
        request: Request,
        edit_notice: NoticeModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user)
):
    """
    编辑通知公告
    """
    edit_notice.update_by = current_user.user.user_name
    edit_notice.update_time = datetime.now()
    edit_notice_result = await NoticeService.edit_notice_services(query_db, edit_notice)
    logger.info(edit_notice_result.message)

    return ResponseUtil.success(msg=edit_notice_result.message)


@noticeController.delete('/{notice_ids}', dependencies=[Depends(CheckUserInterfaceAuth('system:notice:remove'))])
@Log(title='通知公告', business_type=BusinessType.DELETE)
async def delete_system_notice(request: Request, notice_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    删除系统通知公告
    """
    delete_notice = DeleteNoticeModel(noticeIds=notice_ids)
    delete_notice_result = await NoticeService.delete_notice_services(query_db, delete_notice)
    logger.info(delete_notice_result.message)

    return ResponseUtil.success(msg=delete_notice_result.message)


@noticeController.get(
    '/{notice_id}', response_model=NoticeModel, dependencies=[Depends(CheckUserInterfaceAuth('system:notice:query'))]
)
async def query_detail_system_post(request: Request, notice_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    获取系统通知公告信息
    """
    notice_detail_result = await NoticeService.notice_detail_services(query_db, notice_id)
    logger.info(f'获取notice_id为{notice_id}的信息成功')

    return ResponseUtil.success(data=notice_detail_result)
```

## 第六步:最后去`server.py`写路由挂载

```python
# 导入接口
from module_admin.controller.notice_controller import noticeController

# 引入接口,并写好tags
controller_list = [
    {'router': noticeController, 'tags': ['系统管理-通知公告管理']},
]
```