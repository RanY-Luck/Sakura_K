#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/4/29 22:00
# @Author  : 冉勇
# @Site    :
# @File    : ssh_controller.py
# @Software: PyCharm
# @desc    : SSH操作控制器
from fastapi import APIRouter, UploadFile, File, Form, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from utils.response_util import ResponseUtil
from module_admin.service.login_service import LoginService
from utils.ssh_operation import ssh_operation
from module_ssh.core.ssh_client import SSHClient
from module_ssh.core.ssh_operations import SSHOperations
from config.get_db import get_db
from module_ssh.service.ssh_service import get_ssh_connection_details

# 创建路由器
sshController = APIRouter(prefix="/ssh", dependencies=[Depends(LoginService.get_current_user)])


@sshController.post("/connect/test")
async def test_ssh_connection(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    测试SSH连接
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")
        host, username, password, port = connection_details
        success, error = SSHClient.test_connection(
            host=host,
            username=username,
            password=password,
            port=port
        )
        if success:
            return ResponseUtil.success(msg="连接成功")
        else:
            return ResponseUtil.error(msg=f"连接失败: {error}")
    except Exception as e:
        return ResponseUtil.error(msg=f"连接测试异常: {str(e)}")


@sshController.post("/command/execute")
async def execute_command(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        command: str = Body(..., description="要执行的命令"),
        timeout: int = Body(60, description="命令超时时间(秒)"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    执行SSH命令
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        ssh_ops = SSHOperations.from_credentials(
            host=host,
            username=username,
            password=password,
            port=port
        )

        output, error, exit_code = ssh_ops.execute_command(command, timeout)

        return ResponseUtil.success(
            data={
                "output": output,
                "error": error,
                "exit_code": exit_code
            }
        )
    except Exception as e:
        return ResponseUtil.error(msg=f"执行命令失败: {str(e)}")


@sshController.post("/script/execute")
async def execute_script(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        script_content: str = Body(..., description="脚本内容"),
        timeout: int = Body(60, description="脚本超时时间(秒)"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    执行SSH脚本
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        ssh_ops = SSHOperations.from_credentials(
            host=host,
            username=username,
            password=password,
            port=port
        )

        output, error, exit_code = ssh_ops.execute_script(script_content, timeout)

        return ResponseUtil.success(
            data={
                "output": output,
                "error": error,
                "exit_code": exit_code
            }
        )
    except Exception as e:
        return ResponseUtil.error(msg=f"执行脚本失败: {str(e)}")


@sshController.post("/file/upload")
async def upload_file(
        ssh_id: int = Form(..., description="SSH服务器ID"),
        remote_path: str = Form(..., description="远程路径"),
        file: UploadFile = File(..., description="要上传的文件"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    上传文件到远程服务器
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        # 保存上传的文件到临时目录
        import tempfile
        import os

        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, file.filename)

        with open(temp_file_path, "wb") as temp_file:
            content = await file.read()
            temp_file.write(content)

        # 使用旧接口上传文件
        result = ssh_operation(
            host=host,
            username=username,
            password=password,
            operation="upload_file",
            local_path=temp_file_path,
            remote_path=remote_path,
            port=port
        )

        # 删除临时文件
        os.unlink(temp_file_path)

        if result:
            return ResponseUtil.success(msg="文件上传成功")
        else:
            return ResponseUtil.error(msg="文件上传失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"文件上传失败: {str(e)}")


@sshController.post("/file/download")
async def download_file(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        remote_path: str = Body(..., description="远程文件路径"),
        local_path: str = Body(..., description="本地保存路径"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    从远程服务器下载文件
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        # 检查远程文件是否存在
        import os
        from utils.log_util import logger

        logger.info(f"开始下载文件: 远程路径={remote_path}, 本地路径={local_path}")

        # 确保本地目录存在
        local_dir = os.path.dirname(local_path)
        if local_dir and not os.path.exists(local_dir):
            try:
                logger.info(f"创建本地目录: {local_dir}")
                os.makedirs(local_dir, exist_ok=True)
            except Exception as dir_err:
                logger.error(f"创建本地目录失败: {str(dir_err)}")
                return ResponseUtil.error(msg=f"创建本地目录失败: {str(dir_err)}")

        # 执行下载
        result = ssh_operation(
            host=host,
            username=username,
            password=password,
            operation="download_file",
            local_path=local_path,
            remote_path=remote_path,
            port=port
        )

        if result:
            logger.info(f"文件下载成功: {local_path}")
            return ResponseUtil.success(msg="文件下载成功", data={"local_path": local_path})
        else:
            logger.error(f"文件下载失败: 远程={remote_path}, 本地={local_path}")
            return ResponseUtil.error(msg="文件下载失败，请检查远程文件是否存在")
    except Exception as e:
        logger.error(f"文件下载异常: {str(e)}")
        return ResponseUtil.error(msg=f"文件下载失败: {str(e)}")


@sshController.post("/text/write")
async def write_text(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        remote_path: str = Body(..., description="远程文件路径"),
        content: str = Body(..., description="要写入的文本内容"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    写入文本到远程文件
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        result = ssh_operation(
            host=host,
            username=username,
            password=password,
            operation="write_text",
            remote_path=remote_path,
            content=content,
            port=port
        )

        if result:
            return ResponseUtil.success(msg="文本写入成功")
        else:
            return ResponseUtil.error(msg="文本写入失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"文本写入失败: {str(e)}")


@sshController.post("/text/read")
async def read_text(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        remote_path: str = Body(..., description="远程文件路径"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    读取远程文件文本内容
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        content = ssh_operation(
            host=host,
            username=username,
            password=password,
            operation="read_text",
            remote_path=remote_path,
            port=port
        )

        if content is not None:
            return ResponseUtil.success(data={"output": content})
        else:
            return ResponseUtil.error(msg="读取文件内容失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"读取文件内容失败: {str(e)}")


@sshController.post("/dir/list")
async def list_directory(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        remote_path: str = Body(..., description="远程目录路径"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    列出远程目录内容
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        files = ssh_operation(
            host=host,
            username=username,
            password=password,
            operation="list_dir",
            remote_path=remote_path,
            port=port
        )
        return ResponseUtil.success(data={"output": files})
    except Exception as e:
        return ResponseUtil.error(msg=f"列出目录内容失败: {str(e)}")


@sshController.post("/dir/make")
async def make_directory(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        remote_path: str = Body(..., description="要创建的远程目录路径"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    创建远程目录
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        result = ssh_operation(
            host=host,
            username=username,
            password=password,
            operation="make_dir",
            remote_path=remote_path,
            port=port
        )

        if result:
            return ResponseUtil.success(msg="目录创建成功")
        else:
            return ResponseUtil.error(msg="目录创建失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"目录创建失败: {str(e)}")


@sshController.post("/file/remove")
async def remove_file(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        remote_path: str = Body(..., description="要删除的远程文件路径"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    删除远程文件
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        result = ssh_operation(
            host=host,
            username=username,
            password=password,
            operation="remove_file",
            remote_path=remote_path,
            port=port
        )

        if result:
            return ResponseUtil.success(msg="文件删除成功")
        else:
            return ResponseUtil.error(msg="文件删除失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"文件删除失败: {str(e)}")


@sshController.post("/dir/remove")
async def remove_directory(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        remote_path: str = Body(..., description="要删除的远程目录路径"),
        recursive: bool = Body(False, description="是否递归删除目录内容"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    删除远程目录
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        if recursive:
            ssh_ops = SSHOperations.from_credentials(
                host=host,
                username=username,
                password=password,
                port=port
            )
            result = ssh_ops.remove_dir(remote_path, recursive=True)
        else:
            result = ssh_operation(
                host=host,
                username=username,
                password=password,
                operation="remove_dir",
                remote_path=remote_path,
                port=port
            )

        if result:
            return ResponseUtil.success(msg="目录删除成功")
        else:
            return ResponseUtil.error(msg="目录删除失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"目录删除失败: {str(e)}")


@sshController.post("/file/info")
async def get_file_info(
        ssh_id: int = Body(..., description="SSH服务器ID"),
        remote_path: str = Body(..., description="远程文件路径"),
        query_db: AsyncSession = Depends(get_db)
):
    """
    获取远程文件信息
    """
    try:
        # 获取SSH连接详情
        connection_details = await get_ssh_connection_details(query_db, ssh_id)
        if not connection_details:
            return ResponseUtil.error(msg=f"未找到ID为{ssh_id}的SSH服务器信息")

        host, username, password, port = connection_details

        ssh_ops = SSHOperations.from_credentials(
            host=host,
            username=username,
            password=password,
            port=port
        )

        file_info = ssh_ops.get_file_info(remote_path)

        if file_info:
            # 处理时间戳为字符串格式
            import datetime
            if 'atime' in file_info:
                file_info['atime'] = datetime.datetime.fromtimestamp(file_info['atime']).strftime('%Y-%m-%d %H:%M:%S')
            if 'mtime' in file_info:
                file_info['mtime'] = datetime.datetime.fromtimestamp(file_info['mtime']).strftime('%Y-%m-%d %H:%M:%S')
            return ResponseUtil.success(data={"output": file_info})
        else:
            return ResponseUtil.error(msg="获取文件信息失败")
    except Exception as e:
        return ResponseUtil.error(msg=f"获取文件信息失败: {str(e)}")
