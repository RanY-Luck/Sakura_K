#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025/5/1 20:54
# @Author  : 冉勇
# @Site    :
# @File    : servermanage_service.py
# @Software: PyCharm
# @desc    : 服务器管理模块服务层
import paramiko
import asyncio
import socket
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from exceptions.exception import ServiceException
from module_admin.entity.do.servermanage_do import Ssh
from module_admin.entity.vo.common_vo import CrudResponseModel
from module_admin.dao.servermanage_dao import SshDao
from module_admin.entity.vo.servermanage_vo import DeleteSshModel, SshModel, SshPageQueryModel, SshInfo
from utils.common_util import CamelCaseUtil
from utils.excel_util import ExcelUtil
from utils.pwd_util import PwdUtil, hash_key


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
                # 在这里对密码进行加密
                if 'ssh_password' in edit_ssh and edit_ssh['ssh_password']:
                    edit_ssh['ssh_password'] = PwdUtil.encrypt(
                        hash_key=hash_key,
                        plain_password=page_object.ssh_password
                    )
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

    @classmethod
    async def copy_ssh_services(cls, query_db: AsyncSession, new_ssh: SshModel):
        """
        复制service
        :param query_db: orm对象
        :param new_ssh: 新项目对象（Pydantic 模型）
        :return: 复制服务器结果
        """
        try:
            # 检查原项目是否存在
            original_ssh_id = new_ssh.ssh_id
            original_ssh = await cls.ssh_detail_services(query_db, original_ssh_id)
            if not original_ssh:
                result = dict(is_success=False, message='原服务器不存在')
                return CrudResponseModel(**result)

            # 将 Pydantic 模型转换为 SQLAlchemy 模型
            new_ssh_dict = new_ssh.model_dump(exclude_unset=True)
            new_ssh_dict.pop('ssh_id', None)  # 移除 project_id，依赖数据库自增

            # 创建 SQLAlchemy 模型实例
            db_ssh = Ssh(**new_ssh_dict)

            # 添加新项目到数据库
            query_db.add(db_ssh)

            # 提交事务
            await query_db.commit()

            # 刷新新项目对象以获取数据库生成的主键等信息
            await query_db.refresh(db_ssh)

            result = dict(is_success=True, message=f'服务器:{new_ssh.ssh_name} 复制成功')
            return CrudResponseModel(**result)
        except Exception as e:
            await query_db.rollback()
            raise e

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
            'remark': '备注'
        }
        binary_data = ExcelUtil.export_list2excel(ssh_list, mapping_dict)

        return binary_data

    @classmethod
    async def ssh_client_services(cls, query_db: AsyncSession, ssh_id: int):
        """
        测试连接服务器service
        :param query_db: orm对象
        :param ssh_id: 服务器id
        :return: 服务器连接测试结果, 包含系统信息和连接状态
        """
        # 查询服务器信息
        ssh = await SshDao.get_ssh_detail_by_id(query_db, ssh_id=ssh_id)
        if ssh is None:
            return CrudResponseModel(is_success=False, message=f'服务器{ssh_id}不存在')

        result = SshModel(**CamelCaseUtil.transform_result(ssh))

        # 最大重试次数
        max_retries = 2
        retry_count = 0
        last_error = None

        # 尝试连接，如果失败则重试
        while retry_count <= max_retries:
            try:
                # 解密密码
                decrypt_password = None
                if result.ssh_password:
                    decrypt_password = PwdUtil.decrypt(hash_key=hash_key, hashed_password=result.ssh_password)
                # 创建SshInfo对象
                ssh_info = SshInfo(
                    ssh_host=result.ssh_host,
                    ssh_username=result.ssh_username,
                    ssh_port=result.ssh_port,
                    ssh_password=decrypt_password
                )
                # 创建SSHConnection实例
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # 设置连接参数
                connect_kwargs = {
                    'hostname': ssh_info.ssh_host,
                    'username': ssh_info.ssh_username,
                    'port': ssh_info.ssh_port,
                    'timeout': 10,  # 设置超时时间
                    'allow_agent': False,
                    'look_for_keys': False
                }

                if ssh_info.ssh_password:
                    connect_kwargs['password'] = ssh_info.ssh_password
                # 连接服务器
                ssh_client.connect(**connect_kwargs)
                # 获取系统信息
                system_info = {}
                # 获取操作系统信息
                try:
                    stdin, stdout, stderr = ssh_client.exec_command('uname -a', timeout=5)
                    system_info['os_info'] = stdout.read().decode('utf-8').strip()
                    if not system_info['os_info']:
                        # 尝试Windows系统命令
                        stdin, stdout, stderr = ssh_client.exec_command(
                            'systeminfo | findstr /B /C:"OS Name" /C:"OS Version"',
                            timeout=5
                        )
                        system_info['os_info'] = stdout.read().decode('utf-8').strip()
                except Exception:
                    system_info['os_info'] = "获取操作系统信息失败"

                # 获取CPU信息
                try:
                    stdin, stdout, stderr = ssh_client.exec_command(
                        'cat /proc/cpuinfo | grep "model name" | head -1',
                        timeout=5
                    )
                    cpu_info = stdout.read().decode('utf-8').strip()
                    if cpu_info:
                        system_info['cpu_info'] = cpu_info.split(':')[1].strip() if ':' in cpu_info else cpu_info
                    else:
                        # 尝试Windows系统命令
                        stdin, stdout, stderr = ssh_client.exec_command('wmic cpu get Name', timeout=5)
                        output = stdout.read().decode('utf-8').strip()
                        if output:
                            lines = output.split('\n')
                            if len(lines) > 1:
                                system_info['cpu_info'] = lines[1].strip()
                except Exception:
                    system_info['cpu_info'] = "获取CPU信息失败"

                # 获取内存信息
                try:
                    stdin, stdout, stderr = ssh_client.exec_command('free -h', timeout=5)
                    mem_info = stdout.read().decode('utf-8').strip()
                    if mem_info:
                        system_info['memory_info'] = mem_info
                    else:
                        # 尝试Windows系统命令
                        stdin, stdout, stderr = ssh_client.exec_command(
                            'wmic OS get TotalVisibleMemorySize /Value',
                            timeout=5
                        )
                        system_info['memory_info'] = stdout.read().decode('utf-8').strip()
                except Exception:
                    system_info['memory_info'] = "获取内存信息失败"

                # 获取磁盘信息
                try:
                    stdin, stdout, stderr = ssh_client.exec_command('df -h', timeout=5)
                    disk_info = stdout.read().decode('utf-8').strip()
                    if disk_info:
                        system_info['disk_info'] = disk_info
                    else:
                        # 尝试Windows系统命令
                        stdin, stdout, stderr = ssh_client.exec_command(
                            'wmic logicaldisk get DeviceID,Size,FreeSpace',
                            timeout=5
                        )
                        system_info['disk_info'] = stdout.read().decode('utf-8').strip()
                except Exception:
                    system_info['disk_info'] = "获取磁盘信息失败"

                # 关闭连接
                ssh_client.close()

                # 返回成功结果
                return CrudResponseModel(
                    is_success=True,
                    message=f'连接服务器 {result.ssh_name}({result.ssh_host}) 成功',
                    result={
                        'server_name': result.ssh_name,
                        'server_host': result.ssh_host,
                        'server_port': result.ssh_port,
                        'username': result.ssh_username,
                        'system_info': system_info
                    }
                )

            except paramiko.AuthenticationException:
                # 身份验证错误，不再重试
                return CrudResponseModel(
                    is_success=False,
                    message=f'连接服务器 {result.ssh_name}({result.ssh_host}) 失败: 用户名或密码错误'
                )

            except paramiko.SSHException as e:
                # SSH异常，可能是临时性问题，尝试重试
                last_error = str(e)
                retry_count += 1
                if retry_count <= max_retries:
                    await asyncio.sleep(1)  # 等待1秒后重试
                    continue
                break

            except socket.timeout:
                # 连接超时，可能是网络问题，尝试重试
                last_error = "连接超时"
                retry_count += 1
                if retry_count <= max_retries:
                    await asyncio.sleep(1)  # 等待1秒后重试
                    continue
                break

            except Exception as e:
                # 其他未预期的错误
                last_error = str(e)
                retry_count += 1
                if retry_count <= max_retries:
                    await asyncio.sleep(1)  # 等待1秒后重试
                    continue
                break

        # 所有重试都失败
        await query_db.rollback()  # 回滚数据库事务
        return CrudResponseModel(
            is_success=False,
            message=f'连接服务器 {result.ssh_name}({result.ssh_host}) 失败: {last_error}',
            result={
                'server_name': result.ssh_name,
                'server_host': result.ssh_host,
                'retry_count': retry_count
            }
        )
