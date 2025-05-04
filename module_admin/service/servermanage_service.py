#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/1 20:54
# @Author  : 冉勇
# @Site    :
# @File    : servermanage_service.py
# @Software: PyCharm
# @desc    : 服务器管理模块服务层
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from exceptions.exception import ServiceException
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.servermanage_dao import SshDao
from module_admin.entity.vo.servermanage_vo import DeleteSshModel, SshModel, SshPageQueryModel
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil


class SshService:
    """
    服务器管理模块服务层
    """

    @classmethod
    async def get_ssh_list_services(
            cls,
            query_db: AsyncSession,
            query_object: SshPageQueryModel,
            is_page: bool = False
    ):
        """
        获取服务器列表信息service

        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 服务器列表信息对象
        """
        ssh_list_result = await SshDao.get_ssh_list(query_db, query_object, is_page)

        return ssh_list_result

    @classmethod
    async def add_ssh_services(cls, query_db: AsyncSession, page_object: SshModel):
        """
        新增服务器service
        :param query_db: orm对象
        :param page_object: 新增服务器对象
        :return: 新增服务器校验结果
        """
        ssh = await SshDao.get_ssh_detail_by_info(query_db, page_object)
        if ssh:
            result = dict(is_success=False, message=f'服务器:{page_object.ssh_name} 已存在')
        else:
            try:
                await SshDao.add_ssh_dao(query_db, page_object)
                await query_db.commit()
                result = dict(is_success=True, message='新增服务器成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        return CrudResponseModel(**result)

    @classmethod
    async def edit_ssh_services(cls, query_db: AsyncSession, page_object: SshModel):
        """
        编辑服务器service
        :param query_db: orm对象
        :param page_object: 编辑服务器对象
        :return: 编辑服务器校验结果
        """
        edit_ssh = page_object.model_dump(exclude_unset=True)
        ssh_info = await cls.ssh_detail_services(query_db, edit_ssh.get('ssh_id'))
        if ssh_info:
            if ssh_info.ssh_name != page_object.ssh_name:
                ssh = await SshDao.get_ssh_detail_by_info(query_db, page_object)
                if ssh:
                    result = dict(is_success=False, message=f'服务器:{page_object.ssh_name} 已存在')
                    return CrudResponseModel(**result)
            try:
                await SshDao.edit_ssh_dao(query_db, edit_ssh)
                await query_db.commit()
                result = dict(is_success=True, message=f'服务器:{ssh_info.ssh_name} 更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='服务器不存在')

        return CrudResponseModel(**result)

    @classmethod
    async def delete_ssh_services(cls, query_db: AsyncSession, page_object: DeleteSshModel):
        """
        删除服务器信息service

        :param query_db: orm对象
        :param page_object: 删除服务器对象
        :return: 删除服务器校验结果
        """
        if page_object.ssh_ids:
            ssh_id_list = page_object.ssh_ids.split(',')
            try:
                for ssh_id in ssh_id_list:
                    await SshDao.delete_ssh_dao(query_db, SshModel(sshId=ssh_id))
                await query_db.commit()
                return CrudResponseModel(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            raise ServiceException(message='传入服务器ID为空')

    @classmethod
    async def ssh_detail_services(cls, query_db: AsyncSession, ssh_id: int):
        """
        获取服务器详细信息service

        :param query_db: orm对象
        :param ssh_id: 服务器ID
        :return: 服务器ID对应的信息
        """
        ssh = await SshDao.get_ssh_detail_by_id(query_db, ssh_id=ssh_id)
        if ssh:
            result = SshModel(**CamelCaseUtil.transform_result(ssh))
        else:
            result = SshModel(**dict())

        return result

    @staticmethod
    async def export_ssh_list_services(ssh_list: List):
        """
        导出服务器信息service

        :param ssh_list: 服务器信息列表
        :return: 服务器信息对应excel的二进制数据
        """
        # 创建一个映射字典，将英文键映射到中文键
        mapping_dict = {
            'sshId': '服务器编号',
            'sshName': '服务器名称',
            'sshHost': '服务器地址',
            'sshUsername': '服务器用户名',
            'sshPassword': '服务器密码',
            'sshPort': '服务器端口',
            'createBy': '创建者',
            'createTime': '创建时间',
            'updateBy': '更新者',
            'updateTime': '更新时间',
            'remark': '备注',
            'delFlag': '删除标志',
        }
        binary_data = ExcelUtil.export_list2excel(ssh_list, mapping_dict)

        return binary_data
