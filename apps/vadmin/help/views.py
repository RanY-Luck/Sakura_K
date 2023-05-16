#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    : 帮助中心视图
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from core.database import db_getter
from utils.response import SuccessResponse
from . import schemas, crud, params, models
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth
from apps.vadmin.auth.utils.validation.auth import Auth

app = APIRouter()


###########################################################
#                     类别管理                             #
###########################################################
@app.get("/issue/categorys", summary="获取类别列表")
async def get_issue_categorys(
        p: params.IssueCategoryParams = Depends(),  # 传递请求的查询参数
        auth: Auth = Depends(AllUserAuth())  # 进行身份验
):
    # 定义了model，它是models.VadminIssueCategory的一个实例，表示“VadminIssueCategory”表的ORM模型。
    model = models.VadminIssueCategory
    # 定义了options，它是一个列表，包含一个joinedload对象，用于在查询类别列表数据时同时查询其关联的用户数据。
    options = [joinedload(model.create_user)]
    # schema定义了返回数据的格式，它是schemas.IssueCategoryListOut类型。
    schema = schemas.IssueCategoryListOut
    # 通过crud.IssueCategoryDal实例的get_datas()方法获取类别列表数据，传递的参数是通过p.dict()获取的查询参数、options和schema。
    # get_datas()返回一个列表，其中每个元素是一个字典，表示一条类别数据。
    datas = await crud.IssueCategoryDal(auth.db).get_datas(**p.dict(), v_options=options, v_schema=schema)
    # count则是通过crud.IssueCategoryDal实例的get_count()方法获取的记录总数。
    count = await crud.IssueCategoryDal(auth.db).get_count(**p.to_count())
    # 路由函数返回一个SuccessResponse对象，其中包含查询到的类别列表数据和总记录数。
    # SuccessResponse是一个自定义的响应类，它包含两个属性：data和count，分别表示查询到的数据和记录总数。
    return SuccessResponse(datas, count=count)


@app.get("/issue/categorys/options", summary="获取类别选择项")
async def get_issue_categorys_options(
        auth: Auth = Depends(AllUserAuth())  # 进行身份验
):
    # 首先定义了返回数据的格式，它是schemas.IssueCategoryOptionsOut类型
    schema = schemas.IssueCategoryOptionsOut
    # 通过crud.IssueCategoryDal实例的get_datas()方法获取类别选择项数据，传递的参数是limit=0（表示查询所有记录）、
    # is_active=True（表示只查询已激活的记录）和v_schema=schema（表示使用schemas.IssueCategoryOptionsOut格式返回数据）。
    # get_datas()返回一个列表，其中每个元素是一个字典，表示一个类别选择项。
    # 最后，路由函数返回一个SuccessResponse对象，其中包含查询到的类别选择项数据。
    # SuccessResponse是一个自定义的响应类，它包含一个属性data，表示查询到的数据。
    return SuccessResponse(await crud.IssueCategoryDal(auth.db).get_datas(limit=0, is_active=True, v_schema=schema))


@app.post("/issue/categorys", summary="创建类别")
async def create_issue_category(
        data: schemas.IssueCategory,  # 创建类别的数据
        auth: Auth = Depends(AllUserAuth())  # 进行身份验证
):
    # 将data中的user_id属性设置为auth.user.id，表示创建该类别的用户ID为当前认证用户的ID。
    data.create_user_id  = auth.user.id
    # 通过crud.IssueCategoryDal实例的create_data()方法创建类别数据，传递的参数是data。create_data()返回一个字典，表示创建的类别数据。
    # 最后，路由函数返回一个SuccessResponse对象，其中包含创建的类别数据。
    # SuccessResponse是一个自定义的响应类，它包含一个属性data，表示返回的数据。
    return SuccessResponse(await crud.IssueCategoryDal(auth.db).create_data(data=data))


@app.delete("/issue/categorys", summary="批量删除类别", description="硬删除")
async def delete_issue_categorys(
        ids: IdList = Depends(),  # 自定义的参数类型IdList，包含要删除的类别ID列表
        auth: Auth = Depends(AllUserAuth())  # 进行身份验证
):
    # 通过crud.IssueCategoryDal实例的delete_datas()方法删除类别数据，传递的参数是ids.ids（表示要删除的类别ID列表）和v_soft=False（表示使用硬删除方式）。
    # delete_datas()是一个异步方法，使用await关键字等待它执行完成。
    # 然后，路由函数返回一个SuccessResponse对象，其中包含一个字符串表示删除成功的消息。
    # SuccessResponse是一个自定义的响应类，它包含一个属性data，表示返回的数据。
    await crud.IssueCategoryDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/issue/categorys/{data_id}", summary="更新类别信息")
async def put_issue_category(
        data_id: int,  # 路径参数，表示要更新的类别ID
        data: schemas.IssueCategory,  # schemas.IssueCategory类型的参数，包含更新后的类别信息
        auth: Auth = Depends(AllUserAuth())  # 进行身份验证
):
    # 通过crud.IssueCategoryDal实例的put_data()方法更新类别数据，传递的参数是data_id（表示要更新的类别ID）和data（表示更新后的类别信息）。
    # put_data()返回一个字典，表示更新后的类别数据。
    # 最后，路由函数返回一个SuccessResponse对象，其中包含更新后的类别数据。
    # SuccessResponse是一个自定义的响应类，它包含一个属性data，表示返回的数据。
    return SuccessResponse(await crud.IssueCategoryDal(auth.db).put_data(data_id, data))


@app.get("/issue/categorys/{data_id}", summary="获取类别信息")
async def get_issue_category(
        data_id: int,  # 路径参数，表示要获取的类别ID
        auth: Auth = Depends(AllUserAuth())  # 进行身份验证
):
    # 通过schemas.IssueCategorySimpleOut定义一个输出的数据模式
    schema = schemas.IssueCategorySimpleOut
    # 然后调用crud.IssueCategoryDal实例的get_data()方法获取类别数据，传递的参数是data_id（表示要获取的类别ID）和v_schema=schema（表示使用定义的数据模式）。
    # get_data()返回一个字典，表示获取到的类别数据。最后，路由函数返回一个SuccessResponse对象，其中包含获取到的类别数据。
    # SuccessResponse是一个自定义的响应类，它包含一个属性data，表示返回的数据。
    return SuccessResponse(await crud.IssueCategoryDal(auth.db).get_data(data_id, v_schema=schema))


@app.get("/issue/categorys/platform/{platform}", summary="获取平台中的常见问题类别列表")
async def get_issue_category_platform(
        platform: str,  # 路径参数，表示要获取类别列表的平台名称
        db: AsyncSession = Depends(db_getter)  # 异步会话依赖项，用于从数据库中获取数据
):
    model = models.VadminIssueCategory
    options = [joinedload(model.issues)]
    # 通过schemas.IssueCategoryPlatformOut定义一个输出的数据模式，然后调用crud.IssueCategoryDal实例的get_datas()方法获取类别数据，
    # 传递的参数是platform（表示要获取类别列表的平台名称）、is_active=True（表示只获取状态为“激活”的类别）、v_schema=schema（表示使用定义的数据模式）
    # 和v_options=options（表示使用joinedload来优化查询性能）。
    # get_datas()返回一个列表，表示获取到的类别数据。
    # 最后，路由函数返回一个SuccessResponse对象，其中包含获取到的类别数据。
    # SuccessResponse是一个自定义的响应类，它包含一个属性data，表示返回的数据。
    schema = schemas.IssueCategoryPlatformOut
    result = await crud.IssueCategoryDal(db).get_datas(
        platform=platform,
        is_active=True,
        v_schema=schema,
        v_options=options
    )
    return SuccessResponse(result)


###########################################################
#                     问题管理                             #
###########################################################
@app.get("/issues", summary="获取问题列表")
async def get_issues(
        p: params.IssueParams = Depends(),  # 自定义的参数类型params.IssueParams，包含获取问题列表所需的各种参数，如分页、排序等
        auth: Auth = Depends(AllUserAuth())  # 身份验证
):
    model = models.VadminIssue
    options = [joinedload(model.create_user), joinedload(model.category)]
    # 通过schemas.IssueListOut定义一个输出的数据模式
    schema = schemas.IssueListOut
    # 然后调用crud.IssueDal实例的get_datas()方法获取问题数据，传递的参数是**p.dict()（表示将p对象转换成字典，
    # 并将其作为关键字参数传递给get_datas()方法）、v_options=options（表示使用joinedload来优化查询性能）和v_schema=schema（表示使用定义的数据模式）。
    # get_datas()返回一个列表，表示获取到的问题数据。
    datas = await crud.IssueDal(auth.db).get_datas(**p.dict(), v_options=options, v_schema=schema)
    # 调用crud.IssueDal实例的get_count()方法获取满足条件的问题总数，传递的参数是**p.to_count()（表示将p对象转换成字典，
    # 并将其作为关键字参数传递给get_count()方法）。get_count()返回一个整数，表示满足条件的问题总数。
    count = await crud.IssueDal(auth.db).get_count(**p.to_count())
    # 最后，路由函数返回一个SuccessResponse对象，其中包含获取到的问题数据和问题总数。
    # SuccessResponse是一个自定义的响应类，它包含一个属性data，表示返回的数据，和一个属性count，表示问题总数。
    return SuccessResponse(datas, count=count)


@app.post("/issues", summary="创建问题")
async def create_issue(
        data: schemas.Issue,
        auth: Auth = Depends(AllUserAuth())  # 身份验证
):
    data.create_user_id = auth.user.id
    return SuccessResponse(await crud.IssueDal(auth.db).create_data(data=data))


@app.delete("/issues", summary="批量删除问题", description="硬删除")
async def delete_issues(ids: IdList = Depends(), auth: Auth = Depends(AllUserAuth())):
    await crud.IssueDal(auth.db).delete_datas(ids=ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/issues/{data_id}", summary="更新问题信息")
async def put_issue(data_id: int, data: schemas.Issue, auth: Auth = Depends(AllUserAuth())):
    return SuccessResponse(await crud.IssueDal(auth.db).put_data(data_id, data))


@app.get("/issues/{data_id}", summary="获取问题信息")
async def get_issue(data_id: int, db: AsyncSession = Depends(db_getter)):
    schema = schemas.IssueSimpleOut
    return SuccessResponse(await crud.IssueDal(db).get_data(data_id, v_schema=schema))


@app.get("/issues/add/view/number/{data_id}", summary="更新常见问题查看次数+1")
async def issue_add_view_number(data_id: int, db: AsyncSession = Depends(db_getter)):
    return SuccessResponse(await crud.IssueDal(db).add_view_number(data_id))
