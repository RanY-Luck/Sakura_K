#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/26 21:56
# @Author  : 冉勇
# @Site    : 
# @File    : api_service.py
# @Software: PyCharm
# @desc    : 接口模块服务层
import json

from module_admin.dao.api_dao import *
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.common_util import CamelCaseUtil
from utils.http_util import AsyncRequest
from utils.page_util import PageResponseModel


class ApiService:
    """
    接口管理模块服务层
    """

    @classmethod
    async def get_api_list_services(
            cls,
            query_db: AsyncSession,
            query_object: ApiPageQueryModel,
            is_page: bool = True
    ):
        """
        获取接口列表service
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 接口列表信息对象
        """
        query_result = await ApiDao.get_api_list(query_db, query_object, is_page)
        if is_page:
            api_list_result = PageResponseModel(
                **{
                    **query_result.model_dump(by_alias=True),
                    'rows': [{**row[0], 'project': row[1]} for row in query_result.rows]
                }
            )
        else:
            api_list_result = []
            if query_result:
                api_list_result = [{**row[0], 'project': row[1]} for row in query_result]

        return api_list_result

    @classmethod
    async def add_api_services(cls, query_db: AsyncSession, page_object: ApiModel):
        """
        新增接口service
        :param query_db: orm对象
        :param page_object: 新增接口对象
        :return: 新增接口校验结果
        """
        api = await ApiDao.get_api_detail_by_info(query_db, page_object)
        if api:
            result = dict(is_success=False, message=f'接口:{api.api_name} 已存在')
        else:
            try:
                await ApiDao.add_api_dao(query_db, page_object)
                await query_db.commit()
                result = dict(is_success=True, message=f'新增接口成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        return CrudResponseModel(**result)

    @classmethod
    async def edit_api_services(cls, query_db: AsyncSession, page_object: ApiModel):
        """
        编辑接口service
        :param query_db: orm对象
        :param page_object: 编辑接口对象
        :return: 编辑接口校验结果
        """
        edit_api = page_object.model_dump(exclude_unset=True)
        api_info = await cls.api_detail_services(query_db, edit_api.get('api_id'))
        if api_info:
            if api_info.api_name != page_object.api_name:
                api = await ApiDao.get_api_detail_by_info(query_db, page_object)
                if api:
                    result = dict(is_success=False, message=f'接口:{api.api_name} 已存在')
                    return CrudResponseModel(**result)
            try:
                await ApiDao.edit_api_dao(query_db, edit_api)
                await query_db.commit()
                result = dict(is_success=True, message=f'接口:{api_info.api_name} 更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='接口不存在')

        return CrudResponseModel(**result)

    @classmethod
    async def delete_api_services(cls, query_db: AsyncSession, page_object: DeleteApiModel):
        """
        删除接口service
        :param query_db: orm对象
        :param page_object: 删除接口对象
        :return: 删除接口校验结果
        """
        if page_object.api_ids.split(','):
            api_id_list = page_object.api_ids.split(',')
            try:
                for api_id in api_id_list:
                    await ApiDao.delete_api_dao(query_db, ApiModel(apiId=api_id))
                await query_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='传入接口id为空')
        return CrudResponseModel(**result)

    @classmethod
    async def api_detail_services(cls, query_db: AsyncSession, api_id: int):
        """
        获取接口详细信息service
        :param query_db: orm对象
        :param api_id: 接口id
        :return: 接口id对应的信息
        """
        api = await ApiDao.get_api_detail_by_id(query_db, api_id=api_id)
        if api is None:
            return CrudResponseModel(is_success=False, message=f'接口{api_id}不存在')
        result = ApiModel(**CamelCaseUtil.transform_result(api))

        return result

    @classmethod
    async def api_debug_services(cls, query_db: AsyncSession, api_id: int):
        """
        Debug接口service
        :param query_db: orm对象
        :param api_id: 接口id
        :return: 接口id对应的信息
        """
        api = await ApiDao.get_api_detail_by_id(query_db, api_id=api_id)
        if api is None:
            return CrudResponseModel(is_success=False, message=f'接口{api_id}不存在')
        try:
            # 处理请求头格式
            headers = {}
            if api.request_headers:
                # 假设 request_headers 是一个字典，包含 key 和 value
                if isinstance(
                        api.request_headers, dict
                ) and 'key' in api.request_headers and 'value' in api.request_headers:
                    headers[api.request_headers['key']] = api.request_headers['value']
                # 如果是字符串，尝试解析 JSON
                elif isinstance(api.request_headers, str):
                    try:
                        header_data = json.loads(api.request_headers)
                        if isinstance(header_data, dict) and 'key' in header_data and 'value' in header_data:
                            headers[header_data['key']] = header_data['value']
                    except json.JSONDecodeError:
                        pass
            # 发起请求
            api_info = await AsyncRequest.client(
                url=api.api_url,
                body=api.request_data,
                body_type=api.request_data_type,
                headers=headers  # 使用处理后的headers
            )
            response = await api_info.invoke(method=api.api_method)
            return response
        except Exception as e:
            # 处理其他未预料到的错误
            await query_db.rollback()
            return CrudResponseModel(is_success=False, message=f'发生未知错误: {str(e)}')
