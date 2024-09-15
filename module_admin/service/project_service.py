#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/9/3 16:48
# @Author  : 冉勇
# @Site    : 
# @File    : project_service.py
# @Software: PyCharm
# @desc    : 项目模块服务层
from module_admin.dao.project_dao import *
from module_admin.entity.vo.common_vo import CrudResponseModel
from utils.common_util import CamelCaseUtil


class ProjectService:
    """
    项目管理模块服务层
    """

    @classmethod
    async def get_project_list_services(
            cls,
            query_db: AsyncSession,
            query_object: ProjectPageQueryModel,
            is_page: bool = True
    ):
        """
        获取项目列表service
        :param query_db: orm对象
        :param query_object: 查询参数对象
        :param is_page: 是否开启分页
        :return: 项目列表信息对象
        """
        project_list_result = await ProjectDao.get_project_list(query_db, query_object, is_page)

        return project_list_result

    @classmethod
    async def add_project_services(cls, query_db: AsyncSession, page_object: ProjectModel):
        """
        新增项目service
        :param query_db: orm对象
        :param page_object: 新增项目对象
        :return: 新增项目校验结果
        """
        project = await ProjectDao.get_project_detail_by_info(query_db, page_object)
        if project:
            result = dict(is_success=False, message=f'项目:{project.project_name} 已存在')
        else:
            try:
                await ProjectDao.add_project_dao(query_db, page_object)
                await query_db.commit()
                result = dict(is_success=True, message=f'新增项目成功')
            except Exception as e:
                await query_db.rollback()
                raise e

        return CrudResponseModel(**result)

    @classmethod
    async def edit_project_services(cls, query_db: AsyncSession, page_object: ProjectModel):
        """
        编辑项目service
        :param query_db: orm对象
        :param page_object: 编辑项目对象
        :return: 编辑项目校验结果
        """
        edit_project = page_object.model_dump(exclude_unset=True)
        project_info = await cls.project_detail_services(query_db, edit_project.get('project_id'))
        if project_info:
            if project_info.project_name != page_object.project_name:
                project = await ProjectDao.get_project_detail_by_info(query_db, page_object)
                if project:
                    result = dict(is_success=False, message=f'项目:{project.project_name} 已存在')
                    return CrudResponseModel(**result)
            try:
                await ProjectDao.edit_project_dao(query_db, edit_project)
                await query_db.commit()
                result = dict(is_success=True, message=f'项目:{project_info.project_name} 更新成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='项目不存在')

        return CrudResponseModel(**result)

    @classmethod
    async def delete_project_services(cls, query_db: AsyncSession, page_object: DeleteProjectModel):
        """
        删除项目service
        :param query_db: orm对象
        :param page_object: 删除项目对象
        :return: 删除项目校验结果
        """
        if page_object.project_ids.split(','):
            project_id_list = page_object.project_ids.split(',')
            try:
                for project_id in project_id_list:
                    await ProjectDao.delete_project_dao(query_db, ProjectModel(projectId=project_id))
                await query_db.commit()
                result = dict(is_success=True, message='删除成功')
            except Exception as e:
                await query_db.rollback()
                raise e
        else:
            result = dict(is_success=False, message='传入项目id为空')
        return CrudResponseModel(**result)

    @classmethod
    async def project_detail_services(cls, query_db: AsyncSession, project_id: int):
        """
        获取通知公告详细信息service
        :param query_db: orm对象
        :param project_id: 通知公告id
        :return: 通知公告id对应的信息
        """
        project = await ProjectDao.get_project_detail_by_id(query_db, project_id=project_id)
        if project is None:
            return CrudResponseModel(is_success=False, message=f'项目{project_id}不存在')
        result = ProjectModel(**CamelCaseUtil.transform_result(project))

        return result
