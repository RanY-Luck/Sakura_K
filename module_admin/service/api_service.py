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
from module_admin.dao.env_dao import EnvDao
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
    async def api_debug_services(cls, query_db: AsyncSession, api_id: int, env_id: int):
        """
        Debug接口service
        :param query_db: orm对象
        :param api_id: 接口id
        :param env_id: 环境id
        :return: 格式化后的接口响应
        """
        api = await ApiDao.get_api_detail_by_id(query_db, api_id=api_id)
        if api is None:
            return CrudResponseModel(is_success=False, message=f'接口{api_id}不存在')
        env = await EnvDao.get_env_detail_by_id(query_db, env_id=env_id)
        if env is None:
            return CrudResponseModel(is_success=False, message=f'环境{env_id}不存在')
        try:
            # 处理请求头格式
            headers = {}
            # 首先添加环境的通用请求头
            if env.env_headers:
                try:
                    env_headers = env.env_headers
                    if isinstance(env_headers, str):
                        env_headers = json.loads(env_headers)
                    if isinstance(env_headers, dict) and 'key' in env_headers and 'value' in env_headers:
                        headers[env_headers['key']] = env_headers['value']
                    elif isinstance(env_headers, dict):
                        headers.update(env_headers)
                except json.JSONDecodeError:
                    pass
            # 然后添加接口的请求头，如果有相同的键则覆盖环境请求头
            if api.request_headers:
                try:
                    if isinstance(api.request_headers, str):
                        header_data = json.loads(api.request_headers)
                    else:
                        header_data = api.request_headers
                    # 支持多个请求头
                    if isinstance(header_data, list):
                        for item in header_data:
                            if isinstance(item, dict) and 'key' in item and 'value' in item:
                                headers[item['key']] = item['value']
                    elif isinstance(header_data, dict):
                        if 'key' in header_data and 'value' in header_data:
                            headers[header_data['key']] = header_data['value']
                        else:
                            headers.update(header_data)
                except json.JSONDecodeError:
                    pass

            # 处理环境变量
            request_data = api.request_data
            if env.env_variables:
                try:
                    env_vars = env.env_variables
                    if isinstance(env_vars, str):
                        env_vars = json.loads(env_vars)

                    # 替换请求数据中的环境变量
                    if isinstance(request_data, str):
                        # 如果请求数据是字符串，直接替换
                        if isinstance(env_vars, dict):
                            if 'key' in env_vars and 'value' in env_vars:
                                request_data = request_data.replace(f"${{{env_vars['key']}}}", env_vars['value'])
                            else:
                                for key, value in env_vars.items():
                                    request_data = request_data.replace(f"${{{key}}}", str(value))
                    elif isinstance(request_data, dict):
                        # 如果请求数据是字典，递归替换
                        def replace_vars(data):
                            if isinstance(data, str):
                                result = data
                                if isinstance(env_vars, dict):
                                    if 'key' in env_vars and 'value' in env_vars:
                                        result = result.replace(f"${{{env_vars['key']}}}", env_vars['value'])
                                    else:
                                        for key, value in env_vars.items():
                                            result = result.replace(f"${{{key}}}", str(value))
                                return result
                            elif isinstance(data, dict):
                                return {k: replace_vars(v) for k, v in data.items()}
                            elif isinstance(data, list):
                                return [replace_vars(item) for item in data]
                            return data

                        request_data = replace_vars(request_data)
                except json.JSONDecodeError:
                    pass

            # 拼接环境URL和API URL
            base_url = env.env_url.rstrip('/')  # 移除末尾的斜杠
            api_path = api.api_url.lstrip('/')  # 移除开头的斜杠
            full_url = f"{base_url}/{api_path}"

            # 发起请求
            api_info = await AsyncRequest.client(
                url=full_url,
                body=api.request_data,
                body_type=api.request_data_type,
                headers=headers
            )
            response = await api_info.invoke(method=api.api_method)

            # 对响应进行去转义处理
            def clean_and_unescape(text):
                if not isinstance(text, str):
                    return text
                # 移除无效的控制字符
                text = ''.join(char for char in text if ord(char) >= 32 or char in '\n\r\t')
                try:
                    # 尝试去转义
                    return text.encode('raw_unicode_escape').decode('unicode_escape')
                except:
                    return text

            if isinstance(response, str):
                response = clean_and_unescape(response)
            elif isinstance(response, dict):
                try:
                    # 递归处理字典中的所有字符串值
                    def process_dict(d):
                        if not isinstance(d, dict):
                            return d
                        return {k: clean_and_unescape(v) if isinstance(v, str) else process_dict(v) if isinstance(
                            v,
                            (dict, list)
                        ) else v
                                for k, v in d.items()}

                    def process_list(l):
                        return [clean_and_unescape(item) if isinstance(item, str) else process_dict(item) if isinstance(
                            item,
                            dict
                        )
                        else process_list(item) if isinstance(item, list) else item for item in l]

                    response = process_dict(response)
                except Exception as e:
                    # 如果处理失败，返回原始响应
                    pass

            return response

        except Exception as e:
            await query_db.rollback()
            return CrudResponseModel(is_success=False, message=f'发生未知错误: {str(e)}')
