from datetime import datetime
from fastapi import APIRouter, Depends, Form, Request
from pydantic_validation_decorator import ValidateFields
from sqlalchemy.ext.asyncio import AsyncSession
from config.enums import BusinessType
from config.get_db import get_db
from module_admin.annotation.log_annotation import Log
from module_admin.aspect.interface_auth import CheckUserInterfaceAuth
from module_admin.entity.vo.user_vo import CurrentUserModel
from module_admin.service.login_service import LoginService
from module_admin.service.info_service import InfoService
from module_admin.entity.vo.info_vo import DeleteInfoModel, InfoModel, InfoPageQueryModel
from utils.common_util import bytes2file_response
from utils.log_util import logger
from utils.page_util import PageResponseModel
from utils.response_util import ResponseUtil

infoController = APIRouter(prefix='/system/info', dependencies=[Depends(LoginService.get_current_user)])


@infoController.get(
    '/list', response_model=PageResponseModel, dependencies=[Depends(CheckUserInterfaceAuth('ssh:info:list'))]
)
async def get_system_info_list(
        request: Request,
        info_page_query: InfoPageQueryModel = Depends(InfoPageQueryModel.as_query),
        query_db: AsyncSession = Depends(get_db),
):
    """
    获取服务器列表
    :param request:
    :param info_page_query:
    :param query_db:
    :return:
    """
    # 获取分页数据
    info_page_query_result = await InfoService.get_info_list_services(query_db, info_page_query, is_page=True)
    logger.info('获取成功')

    return ResponseUtil.success(model_content=info_page_query_result)


@infoController.post('', dependencies=[Depends(CheckUserInterfaceAuth('ssh:info:add'))])
@ValidateFields(validate_model='add_info')
@Log(title='服务器', business_type=BusinessType.INSERT)
async def add_system_info(
        request: Request,
        add_info: InfoModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    新增服务器
    :param request:
    :param add_info:
    :param query_db:
    :param current_user:
    :return:
    """
    add_info.create_by = current_user.user.user_name
    add_info.create_time = datetime.now()
    add_info.update_by = current_user.user.user_name
    add_info.update_time = datetime.now()
    add_info_result = await InfoService.add_info_services(query_db, add_info)
    logger.info(add_info_result.message)

    return ResponseUtil.success(msg=add_info_result.message)


@infoController.put('', dependencies=[Depends(CheckUserInterfaceAuth('ssh:info:edit'))])
@ValidateFields(validate_model='edit_info')
@Log(title='服务器', business_type=BusinessType.UPDATE)
async def edit_system_info(
        request: Request,
        edit_info: InfoModel,
        query_db: AsyncSession = Depends(get_db),
        current_user: CurrentUserModel = Depends(LoginService.get_current_user),
):
    """
    编辑服务器
    :param request:
    :param edit_info:
    :param query_db:
    :param current_user:
    :return:
    """
    edit_info.update_by = current_user.user.user_name
    edit_info.update_time = datetime.now()
    edit_info_result = await InfoService.edit_info_services(query_db, edit_info)
    logger.info(edit_info_result.message)

    return ResponseUtil.success(msg=edit_info_result.message)


@infoController.delete('/{ssh_ids}', dependencies=[Depends(CheckUserInterfaceAuth('ssh:info:remove'))])
@Log(title='服务器', business_type=BusinessType.DELETE)
async def delete_system_info(request: Request, ssh_ids: str, query_db: AsyncSession = Depends(get_db)):
    """
    硬删除服务器
    :param request:
    :param ssh_ids:
    :param query_db:
    :return:
    """
    delete_info = DeleteInfoModel(sshIds=ssh_ids)
    delete_info_result = await InfoService.delete_info_services(query_db, delete_info)
    logger.info(delete_info_result.message)

    return ResponseUtil.success(msg=delete_info_result.message)


@infoController.get(
    '/{ssh_id}', response_model=InfoModel, dependencies=[Depends(CheckUserInterfaceAuth('ssh:info:query'))]
)
async def query_detail_system_info(request: Request, ssh_id: int, query_db: AsyncSession = Depends(get_db)):
    """
    根据ID获取服务器信息
    :param request:
    :param ssh_id:
    :param query_db:
    :return:
    """
    info_detail_result = await InfoService.info_detail_services(query_db, ssh_id)
    logger.info(f'获取ssh_id为{ssh_id}的信息成功')

    return ResponseUtil.success(data=info_detail_result)


@infoController.post('/export', dependencies=[Depends(CheckUserInterfaceAuth('ssh:info:export'))])
@Log(title='服务器', business_type=BusinessType.EXPORT)
async def export_system_info_list(
        request: Request,
        info_page_query: InfoPageQueryModel = Form(),
        query_db: AsyncSession = Depends(get_db),
):
    """
    导出服务器信息
    :param request:
    :param info_page_query:
    :param query_db:
    :return:
    """
    # 获取全量数据
    info_query_result = await InfoService.get_info_list_services(query_db, info_page_query, is_page=False)
    info_export_result = await InfoService.export_info_list_services(info_query_result)
    logger.info('导出成功')

    return ResponseUtil.streaming(data=bytes2file_response(info_export_result))
