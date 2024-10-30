#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/10/30 21:37
# @Author  : 冉勇
# @Site    : 
# @File    : env_service.py
# @Software: PyCharm
# @desc    : 环境管理模块服务层
from module_admin.dao.env_dao import *
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.common_util import CamelCaseUtil


class EnvService:
    """
    环境管理模块服务层
    """

    @classmethod
    async def get_env_list_services(
            cls,
            query_db: AsyncSession,
            query_object: EnvPageQueryModel,
            is_page: bool = True
    ):
        """
        获取环境列表service
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 环境列表信息对象
        """
        env_list_result = await EnvDao.get_env_list(query_db, query_object, is_page)

        return env_list_result

    @classmethod
    async def add_env_services(cls, query_db: AsyncSession, page_object: EnvModel):
        """
        新增环境service
        :param query_db: orm对象
        :param page_object: 新增接口对象
        :return: 新增环境校验结果
        """
        env = await EnvDao.get_env_detail_by_info(query_db, page_object)
        if env:
            result = dict(is_success=False, message=f'环境:{env.env_name} 已存在')
        else:
            try:
                await EnvDao.add_env_dao(query_db, page_object)
                await query_db.commit()
                result = dict(is_success=True, message=f'新增环境成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        return CrudResponseModel(**result)

    @classmethod
    async def edit_env_services(cls, query_db: AsyncSession, page_object: EnvModel):
        """
        编辑环境service
        :param query_db: orm对象
        :param page_object: 编辑环境对象
        :return: 编辑环境校验结果
        """
        edit_env = page_object.model_dump(exclude_unset=True)
        env_info = await cls.env_detail_services(query_db, edit_env.get('env_id'))
        if env_info:
            if env_info.env_name != page_object.env_name:
                env = await EnvDao.get_env_detail_by_info(query_db, page_object)
                if env:
                    result = dict(is_success=False, message=f'环境:{env.env_name} 已存在')
                    return CrudResponseModel(**result)
            try:
                await EnvDao.edit_env_dao(query_db, edit_env)
                await query_db.commit()
                result = dict(is_success=True, message=f'接口:{env_info.env_name} 更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='接口不存在')

        return CrudResponseModel(**result)

    @classmethod
    async def delete_env_services(cls, query_db: AsyncSession, page_object: DeleteEnvModel):
        """
        删除环境service
        :param query_db: orm对象
        :param page_object: 删除环境对象
        :return: 删除环境校验结果
        """
        if page_object.env_ids.split(','):
            env_id_list = page_object.env_ids.split(',')
            try:
                for env_id in env_id_list:
                    await EnvDao.delete_env_dao(query_db, EnvModel(envId=env_id))
                await query_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='传入环境id为空')
        return CrudResponseModel(**result)

    @classmethod
    async def env_detail_services(cls, query_db: AsyncSession, env_id: int):
        """
        获取环境详细信息service
        :param query_db: orm对象
        :param env_id: 环境id
        :return: 环境id对应的信息
        """
        env = await EnvDao.get_env_detail_by_id(query_db, env_id=env_id)
        if env is None:
            return CrudResponseModel(is_success=False, message=f'环境{env_id}不存在')
        result = EnvModel(**CamelCaseUtil.transform_result(env))

        return result
