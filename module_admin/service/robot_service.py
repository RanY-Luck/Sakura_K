#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Create Time    : 2024/09/15 12:42
# @Author         : 
# @File           : robot_service.py
# @Software       : PyCharm
# @desc           : 机器人模块服务层
import json
from requests.exceptions import RequestException
from module_admin.dao.robot_dao import *
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.bot_util import WxWebhookNotify
from utils.common_util import CamelCaseUtil


class RobotService:
    """
    机器人配置模块服务层
    """

    @classmethod
    async def get_robot_list_services(
            cls,
            query_db: AsyncSession,
            query_object: RobotPageQueryModel,
            is_page: bool = True
    ):
        """
        获取项目列表service
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目列表信息对象
        """
        robot_list_result = await RobotDao.get_robot_list(query_db, query_object, is_page)

        return robot_list_result

    @classmethod
    async def add_robot_services(cls, query_db: AsyncSession, page_object: RobotModel):
        """
        新增机器人service
        :param query_db: orm对象
        :param page_object: 新增机器人对象
        :return: 新增机器人校验结果
        """
        robot = await RobotDao.get_robot_detail_by_info(query_db, page_object)
        if robot:
            result = dict(is_success=False, message=f'机器人:{robot.robot_name} 已存在')
        else:
            try:
                await RobotDao.add_robot_dao(query_db, page_object)
                await query_db.commit()
                result = dict(is_success=True, message=f'新增机器人成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        return CrudResponseModel(**result)

    @classmethod
    async def edit_robot_services(cls, query_db: AsyncSession, page_object: RobotModel):
        """
        编辑机器人service
        :param query_db: orm对象
        :param page_object: 编辑机器人对象
        :return: 编辑机器人校验结果
        """
        edit_robot = page_object.model_dump(exclude_unset=True)
        robot_info = await cls.robot_detail_services(query_db, edit_robot.get('robot_id'))
        if robot_info:
            if robot_info.robot_name != page_object.robot_name:
                robot = await RobotDao.get_robot_detail_by_info(query_db, page_object)
                if robot:
                    result = dict(is_success=False, message=f'机器人:{robot.robot_name} 已存在')
                    return CrudResponseModel(**result)
            try:
                await RobotDao.edit_robot_dao(query_db, edit_robot)
                await query_db.commit()
                result = dict(is_success=True, message=f'机器人:{robot_info.robot_name} 更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='机器人不存在')

        return CrudResponseModel(**result)

    @classmethod
    async def delete_robot_services(cls, query_db: AsyncSession, page_object: DeleteRobotModel):
        """
        删除机器人service
        :param query_db: orm对象
        :param page_object: 删除机器人对象
        :return: 删除校机器人验结果
        """
        if page_object.robot_ids.split(','):
            robot_id_list = page_object.robot_ids.split(',')
            try:
                for robot_id in robot_id_list:
                    await RobotDao.delete_robot_dao(query_db, RobotModel(robotId=robot_id))
                await query_db.commit()
                result = dict(is_success=True, message='机器人删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='传入机器人id为空')
        return CrudResponseModel(**result)

    @classmethod
    async def robot_detail_services(cls, query_db: AsyncSession, robot_id: int):
        """
        获取机器人详细信息service
        :param query_db: orm对象
        :param robot_id: 机器人id
        :return: 机器人id对应的信息
        """
        robot = await RobotDao.get_robot_detail_by_id(query_db, robot_id=robot_id)
        if robot is None:
            return CrudResponseModel(is_success=False, message=f'机器人{robot_id}不存在')
        result = RobotModel(**CamelCaseUtil.transform_result(robot))

        return result

    @classmethod
    async def robot_client_services(cls, query_db: AsyncSession, robot_id: int):
        """
        测试连接机器人service
        :param query_db: orm对象
        :param robot_id: 机器人id
        :return: 机器人id对应的信息
        """
        robot = await RobotDao.get_robot_detail_by_id(query_db, robot_id=robot_id)
        if robot is None:
            return CrudResponseModel(is_success=False, message=f'机器人{robot_id}不存在')
        try:
            wn_webhook = WxWebhookNotify(webhook_url=robot.robot_webhook)
            response = wn_webhook.send_msg_markdown(msg=robot.robot_template)
            # 检查响应内容
            if response.get('errcode') == 0:
                return CrudResponseModel(is_success=True, message='机器人测试已成功发送')
            else:
                return CrudResponseModel(
                    is_success=False,
                    message=f'机器人测试发送失败。错误码: {response.get("errcode")}, 错误信息: {response.get("errmsg")}'
                )
        except RequestException as e:
            # 处理网络相关错误
            return CrudResponseModel(is_success=False, message=f'网络错误: {str(e)}')
        except json.JSONDecodeError:
            # 处理JSON解析错误
            return CrudResponseModel(is_success=False, message='响应格式错误，无法解析JSON')
        except Exception as e:
            # 处理其他未预料到的错误
            await query_db.rollback()
            return CrudResponseModel(is_success=False, message=f'发生未知错误: {str(e)}')
