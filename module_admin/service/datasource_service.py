#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/17 16:31
# @Author  : 冉勇
# @Site    : 
# @File    : datasource_service.py
# @Software: PyCharm
# @desc    : 数据源模块服务层
from module_admin.dao.datasource_dao import *
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.entity.vo.datasource_vo import DataSourceModel
from utils.common_util import CamelCaseUtil


class DataSourceService:
    """
    数据源模块服务层
    """

    @classmethod
    async def get_datasource_list_services(
            cls,
            query_db: AsyncSession,
            query_object: DataSourcePageQueryModel,
            is_page: bool = True
    ):
        """
        获取数据源列表service
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 数据源列表信息对象
        """
        datasource_list_result = await DataSourceDao.get_datasource_list(query_db, query_object, is_page)

        return datasource_list_result

    @classmethod
    async def add_datasource_services(cls, query_db: AsyncSession, page_object: DataSourceModel):
        """
        新增数据源service
        :param query_db: orm对象
        :param page_object: 新增数据源对象
        :return: 新增数据源校验结果
        """
        datasource = await DataSourceDao.get_datasource_detail_by_info(query_db, page_object)
        if datasource:
            result = dict(is_success=False, message=f'数据源:{datasource.datasource_name} 已存在')
        else:
            try:
                await DataSourceDao.add_datasource_dao(query_db, page_object)
                await query_db.commit()
                result = dict(is_success=True, message=f'新增数据源成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        return CrudResponseModel(**result)

    @classmethod
    async def edit_datasource_services(cls, query_db: AsyncSession, page_object: DataSourceModel):
        """
        编辑数据源service
        :param query_db: orm对象
        :param page_object: 编辑数据源对象
        :return: 编辑数据源校验结果
        """
        edit_datasource = page_object.model_dump(exclude_unset=True)
        datasource_info = await cls.datasource_detail_services(query_db, edit_datasource.get('datasource_id'))
        if datasource_info:
            if datasource_info.datasource_name != page_object.datasource_name:
                datasource = await DataSourceDao.get_datasource_detail_by_info(query_db, page_object)
                if datasource:
                    result = dict(is_success=False, message=f'数据源:{datasource.datasource_name} 已存在')
                    return CrudResponseModel(**result)
            try:
                await DataSourceDao.edit_datasource_dao(query_db, edit_datasource)
                await query_db.commit()
                result = dict(is_success=True, message=f'数据源:{datasource_info.datasource_name} 更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='数据源不存在')

        return CrudResponseModel(**result)

    @classmethod
    async def delete_datasource_services(cls, query_db: AsyncSession, page_object: DeleteDataSourceModel):
        """
        删除数据源service
        :param query_db: orm对象
        :param page_object: 删除项目对象
        :return: 删除项目校验结果
        """
        if page_object.datasource_ids.split(','):
            datasource_id_list = page_object.datasource_ids.split(',')
            try:
                for datasource_id in datasource_id_list:
                    await DataSourceDao.delete_datasource_dao(query_db, DataSourceModel(datasourceId=datasource_id))
                await query_db.commit()
                result = dict(is_success=True, message='删除数据源成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='传入数据源id为空')
        return CrudResponseModel(**result)

    @classmethod
    async def datasource_detail_services(cls, query_db: AsyncSession, datasource_id: int):
        """
        获取数据源详细信息service
        :param query_db: orm对象
        :param datasource_id: 数据源id
        :return: 数据源id对应的信息
        """
        datasource = await DataSourceDao.get_datasource_detail_by_id(query_db, datasource_id=datasource_id)
        if datasource is None:
            return CrudResponseModel(is_success=False, message=f'数据源{datasource_id}不存在')
        result = DataSourceModel(**CamelCaseUtil.transform_result(datasource))

        return result
