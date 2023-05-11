#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023-04-14 16:33:42
# @Author  :
# @Site    :
# @File    : views.py
# @Software: PyCharm
# @desc    :
from aioredis import Redis
from fastapi import APIRouter, Depends, Body, UploadFile, Request
from sqlalchemy.orm import joinedload

from core.database import redis_getter
from utils.response import SuccessResponse, ErrorResponse
from . import schemas, crud, models
from core.dependencies import IdList
from apps.vadmin.auth.utils.current import AllUserAuth, FullAdminAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from .params import UserParams, RoleParams

app = APIRouter()


###########################################################
#                     用户管理                             #
###########################################################
@app.get("/users/", summary="获取用户列表")
async def get_users(
        params: UserParams = Depends(),
        # 是用于身份验证的，要求验证权限为"auth.user.list"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.list"]))
):
    # 定义了模型、查询选项和输出模式。
    model = models.VadminUser  # 指向了VadminUser模型，即用户模型
    options = [joinedload(model.roles)]  # 加载了模型中的关联数据,这里的roles是指用户拥有的角色
    schema = schemas.UserOut  # 定义了对模型查询结果的输出模式，即输出到客户端的数据格式，其类型为UserOut。
    # 使用UserDal类进行数据库操作，分别调用了get_datas()和get_count()方法，从数据库中获取用户列表数据和统计数据条数，并将结果返回给客户端。
    datas = await crud.UserDal(auth.db).get_datas(**params.dict(), v_options=options, v_schema=schema)
    count = await crud.UserDal(auth.db).get_count(**params.to_count())
    # 函数返回一个SuccessResponse对象，其中包含了datas（即查询结果data）和count两个字段。
    return SuccessResponse(datas, count=count)


@app.post("/users/", summary="创建用户")
async def create_user(
        data: schemas.UserIn,
        # 是用于身份验证的，要求验证权限为"auth.user.create"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.create"]))
):
    # 返回了一个成功响应对象（SuccessResponse），其中的data字段为await crud.UserDal(auth.db).create_data(data=data)的返回结果。
    # 这里调用了UserDal类的create_data()方法，将data作为参数传入，并使用auth.db获取数据库连接对象，将新创建的用户信息存储到数据库中。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).create_data(data=data))


@app.delete("/users/", summary="批量删除用户", description="软删除，删除后清空所关联的角色")
async def delete_users(
        ids: IdList = Depends(),
        # 是用于身份验证的，要求验证权限为"auth.user.delete"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.delete"]))
):
    # 判断了当前登录用户和超级管理员用户是否在待删除的用户ID列表中，如果是，则直接返回错误响应对象（ErrorResponse）。
    if auth.user.id in ids.ids:
        return ErrorResponse("不能删除当前登录用户")
    elif 1 in ids.ids:
        return ErrorResponse("不能删除超级管理员用户")
    # 通过传入待删除的用户ID列表、软删除标记和活动状态标记来删除用户，在执行删除操作后，返回一个成功响应对象（SuccessResponse）。
    # 需要注意的是，该接口采用了软删除方式，即不会直接从数据库中删除数据，而是将用户的is_active字段标记为False，表示用户被禁用。
    # 另外，该接口还清空了用户所关联的角色信息。
    await crud.UserDal(auth.db).delete_datas(ids=ids.ids, v_soft=True, is_active=False)
    return SuccessResponse("删除成功")


@app.put("/users/{data_id}/", summary="更新用户信息")
async def put_user(
        data_id: int,  # 从URL路径中获取的待更新用户的ID
        data: schemas.UserUpdate,  # 请求体中的数据，其类型为UserUpdate，包含了需要更新的用户信息
        # 用于身份验证
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.update"]))
):
    # 返回了一个成功响应对象（SuccessResponse），其中的data字段为await crud.UserDal(auth.db).put_data(data_id, data)的返回结果。
    # 这里调用了UserDal类的put_data()方法，将data_id和data作为参数传入，并使用auth.db获取数据库连接对象，完成用户信息的更新操作。最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).put_data(data_id, data))


@app.get("/users/{data_id}/", summary="获取用户信息")
async def get_user(
        data_id: int,  # 从URL路径中获取的待获取用户的ID
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.view", "auth.user.update"]))  # 身份验证
):
    # 先定义了model、options和schema三个变量，分别表示需要查询的数据表、查询选项和返回结果的数据模型。
    model = models.VadminUser
    options = [joinedload(model.roles)]
    schema = schemas.UserOut
    # 调用UserDal类的get_data()方法，传入data_id作为参数，并使用auth.db获取数据库连接对象，options指定了查询选项，v_schema指定了返回结果的数据模型。
    # 最后将查询结果构造成成功响应对象（SuccessResponse）并返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).get_data(data_id, options, v_schema=schema))


@app.post("/user/current/reset/password/", summary="重置当前用户密码")
async def user_current_reset_password(
        data: schemas.ResetPwd,  # 请求体中的数据，包括新旧密码信息
        auth: Auth = Depends(AllUserAuth())  # 身份验证,该身份验证对象的权限必须为AllUserAuth。
):
    # 返回一个成功响应对象（SuccessResponse），其中data字段为await crud.UserDal(auth.db).reset_current_password(auth.user, data)的返回结果。
    # 该语句调用了UserDal类中的reset_current_password方法，传入auth.user作为参数表示当前登录用户，data包含了需要重置的新旧密码信息，使用auth.db获取数据库连接对象。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).reset_current_password(auth.user, data))


@app.post("/user/current/update/info/", summary="更新当前用户基本信息")
async def post_user_current_update_info(
        data: schemas.UserUpdateBaseInfo,  # 请求体中的数据，包含需要更新的用户基本信息
        auth: Auth = Depends(AllUserAuth())  # 身份验证,该身份验证对象的权限必须为AllUserAuth。
):
    # 返回一个成功响应对象（SuccessResponse），其中data字段为await crud.UserDal(auth.db).update_current_info(auth.user, data)的返回结果。
    # 该语句调用了UserDal类中的update_current_info方法，传入auth.user作为参数表示当前登录用户，data为包含需要更新的用户基本信息，使用auth.db获取数据库连接对象。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).update_current_info(auth.user, data))


@app.post("/user/current/update/avatar/", summary="更新当前用户头像")
async def post_user_current_update_avatar(
        file: UploadFile,  # 上传的头像文件
        auth: Auth = Depends(AllUserAuth())  # 身份验证,该身份验证对象的权限必须为AllUserAuth。
):
    # 表示该接口返回一个成功响应对象（SuccessResponse），其中data字段为await crud.UserDal(auth.db).update_current_avatar(auth.user, file)的返回结果。
    # 该语句调用了UserDal类中的update_current_avatar方法，传入auth.user作为参数表示当前登录用户，file为上传的头像文件对象，使用auth.db获取数据库连接对象。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).update_current_avatar(auth.user, file))


@app.get("/user/admin/current/info/", summary="获取当前管理员信息")
async def get_user_admin_current_info(
        auth: Auth = Depends(FullAdminAuth())  # 身份验证，该身份验证对象的权限必须为FullAdminAuth。
):
    # 从数据库获取到的用户信息转化为输出用的UserOut模式的对象，并调用.dict()方法将对象转换为字典形式
    result = schemas.UserOut.from_orm(auth.user).dict()
    # 将当前管理员的所有权限存储在字典对象result的"permissions"字段中，
    # 使用FullAdminAuth类的get_user_permissions方法获取当前管理员的权限列表。
    result["permissions"] = list(FullAdminAuth.get_user_permissions(auth.user))
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(result)


@app.post("/user/export/query/list/to/excel/", summary="导出用户查询列表为excel")
async def post_user_export_query_list(
        header: list = Body(..., title="表头与对应字段"),  # Excel文件表头与对应字段的列表，类型为list
        params: UserParams = Depends(),  # 包含查询参数的用户参数对象，类型为UserParams
        # 用于身份验证的，要求验证权限为"auth.user.export"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.export"]))
):
    # 该接口返回一个成功响应对象（SuccessResponse），其中data字段为await crud.UserDal(auth.db).export_query_list(header, params)的返回结果。
    # 该语句调用了UserDal类中的export_query_list方法，传入header作为Excel文件的表头信息，params为用户查询的参数对象，使用auth.db获取数据库连接对象。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).export_query_list(header, params))


@app.get("/user/download/import/template/", summary="下载最新批量导入用户模板")
async def get_user_download_new_import_template(
        auth: Auth = Depends(AllUserAuth())  # 身份验证，该身份验证对象的权限必须为AllUserAuth。
):
    # 返回一个成功响应对象（SuccessResponse），其中data字段为await crud.UserDal(auth.db).download_import_template()的返回结果。
    # 该语句调用了UserDal类中的download_import_template方法，使用auth.db获取数据库连接对象，并下载最新的批量导入用户模板，最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).download_import_template())


@app.post("/import/users/", summary="批量导入用户")
async def post_import_users(
        file: UploadFile,  # 上传的Excel文件对象
        # 身份验证，要求验证权限为"auth.user.import"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.import"]))
):
    # 返回一个成功响应对象（SuccessResponse），其中data字段为await crud.UserDal(auth.db).import_users(file)的返回结果。
    # 该语句调用了UserDal类中的import_users方法，传入file作为上传的Excel文件对象，使用auth.db获取数据库连接对象，并进行用户的批量导入。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).import_users(file))


@app.post("/users/init/password/send/sms/", summary="初始化所选用户密码并发送通知短信")
async def post_users_init_password(
        request: Request,  # 请求对象
        ids: IdList = Depends(),  # 解析出的包含待初始化密码用户ID列表的对象
        # 身份验证，要求验证权限为"auth.user.reset"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.reset"])),
        rd: Redis = Depends(redis_getter)
):
    # 返回一个成功响应对象（SuccessResponse），
    # 其中data字段为await crud.UserDal(auth.db).init_password_send_sms(ids.ids, request.app.state.redis)的返回结果。
    # 该语句调用了UserDal类中的init_password_send_sms方法，传入ids.ids作为待初始化密码的用户ID列表，
    # 传入request.app.state.redis作为Redis数据库连接对象，使用auth.db获取数据库连接对象，并进行密码初始化和发送通知短信。最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).init_password_send_sms(ids.ids, rd))


@app.post("/users/init/password/send/email/", summary="初始化所选用户密码并发送通知邮件")
async def post_users_init_password_send_email(
        request: Request,  # 请求对象
        ids: IdList = Depends(),  # 解析出的包含待初始化密码用户ID列表的对象
        # 身份验证，要求验证权限为"auth.user.reset"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.reset"])),
        rd: Redis = Depends(redis_getter)
):
    # 返回一个成功响应对象（SuccessResponse），
    # 其中data字段为await crud.UserDal(auth.db).init_password_send_email(ids.ids, request.app.state.redis)的返回结果。
    # 该语句调用了UserDal类中的init_password_send_email方法，传入ids.ids作为待初始化密码的用户ID列表，
    # 传入request.app.state.redis作为Redis数据库连接对象，使用auth.db获取数据库连接对象，并进行密码初始化和发送通知邮件。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.UserDal(auth.db).init_password_send_email(ids.ids, rd))


@app.put("/users/wx/server/openid/", summary="更新当前用户服务端微信平台openid")
async def put_user_wx_server_openid(
        code: str,  # 客户端传入的微信临时凭证code
        auth: Auth = Depends(AllUserAuth()),  # 身份验证的，要求为AllUserAuth，表示所有用户都可以访问该接口。
        rd: Redis = Depends(redis_getter)
):
    # 返回一个成功响应对象（SuccessResponse），
    # 其中data字段为await crud.UserDal(auth.db).update_wx_server_openid(code, auth.user, request.app.state.redis)的返回结果。
    # 该语句调用了UserDal类中的update_wx_server_openid方法，传入code作为微信临时凭证code，传入auth.user表示当前用户，
    # 传入request.app.state.redis作为Redis数据库连接对象，更新当前用户的服务端微信平台OpenId，并将成功标志True或False返回给客户端。
    # 最终将成功响应对象返回给客户端。
    result = await crud.UserDal(auth.db).update_wx_server_openid(code, auth.user, rd)
    return SuccessResponse(result)


###########################################################
#                     角色管理                             #
###########################################################
@app.get("/roles/", summary="获取角色列表")
async def get_roles(
        params: RoleParams = Depends(),  # 解析出的包含查询条件的对象
        # 身份验证，要求验证权限为"auth.role.list"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.role.list"]))
):
    # 返回一个成功响应对象（SuccessResponse），其中data字段为await crud.RoleDal(auth.db).get_datas(**params.dict())的返回结果，即符合查询条件的角色数据列表。
    # 同时，还在响应中返回了角色总数count，该值被传入到成功响应对象的count字段中。
    # RoleDal类中的get_datas方法和get_count方法分别用于获取符合条件的角色数据列表和角色总数，这两个方法均接受以键值对形式传入的查询条件，
    # 因此我们对params对象使用**操作符将其解包成键值对，用于向这两个方法传递查询条件。
    # 最终将成功响应对象返回给客户端。
    datas = await crud.RoleDal(auth.db).get_datas(**params.dict())
    count = await crud.RoleDal(auth.db).get_count(**params.to_count())
    return SuccessResponse(datas, count=count)


@app.post("/roles/", summary="创建角色信息")
async def create_role(
        role: schemas.RoleIn,  # 客户端传入的角色信息
        # 身份验证，要求验证权限为"auth.role.create"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.role.create"]))
):
    # 返回一个成功响应对象（SuccessResponse），其中data字段为await crud.RoleDal(auth.db).create_data(data=role)的返回结果，即新创建的角色信息。
    # RoleDal类中的create_data方法用于将传入的角色信息插入到数据库中，并返回插入后的完整数据。
    # 该方法被传入data=role参数，表示以role中的数据作为新记录插入到数据库中。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.RoleDal(auth.db).create_data(data=role))


@app.delete("/roles/", summary="批量删除角色", description="硬删除, 如果存在用户关联则无法删除")
async def delete_roles(
        ids: IdList = Depends(),  # 客户端传入的待删除角色ID列表
        # 身份验证，要求验证权限为"auth.role.delete"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.role.delete"]))
):
    # 如果待删除的角色中包含ID为1的管理员角色，则直接返回错误响应对象（ErrorResponse），提示无法删除管理员角色。
    if 1 in ids.ids:
        return ErrorResponse("不能删除管理员角色")
    # 如果全部待删除的角色都不是管理员角色，则调用RoleDal类中的delete_datas方法，将待删除角色的ID列表传入，并将v_soft参数设置为False（表示硬删除）。
    await crud.RoleDal(auth.db).delete_datas(ids.ids, v_soft=False)
    # 返回一个成功响应对象（SuccessResponse），其中data字段为字符串"删除成功"。
    return SuccessResponse("删除成功")


@app.put("/roles/{data_id}/", summary="更新角色信息")
async def put_role(
        data_id: int,  # 客户端传入的待更新角色的ID
        data: schemas.RoleIn,  # 客户端传入的新的角色信息
        # 身份验证，要求验证权限为"auth.role.update"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.role.update"]))
):
    # 如果待更新的角色是管理员角色（即ID为1的角色），则直接返回错误响应对象（ErrorResponse），提示无法修改管理员角色。
    # 如果待更新的角色不是管理员角色，则调用RoleDal类中的put_data方法，将待更新角色的ID和新的角色信息作为参数传入。
    # put_data方法用于将指定ID的角色信息更新为新的角色信息，并返回更新后的完整数据。最终将成功响应对象返回给客户端。
    if 1 == data_id:
        return ErrorResponse("不能修改管理员角色")
    # 返回一个成功响应对象，其中data字段为await crud.RoleDal(auth.db).put_data(data_id, data)的返回结果，即更新后的完整角色信息
    return SuccessResponse(await crud.RoleDal(auth.db).put_data(data_id, data))


@app.get("/roles/options/", summary="获取角色选择项")
async def get_role_options(
        # 身份验证，要求验证权限为"auth.role.create"或"auth.user.update"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.user.create", "auth.user.update"]))
):
    # 返回一个成功响应对象（SuccessResponse），其中data字段为await crud.RoleDal(auth.db).get_select_datas()的返回结果，即数据库中所有角色的选择项列表。
    # 在获取前，该代码会根据Auth中的验证信息，判断该用户是否具有"auth.role.create"或"auth.user.update"的权限。
    # 如果验证通过，则调用RoleDal类中的get_select_datas方法，用于从数据库中获取所有角色的选择项列表，并返回给客户端。
    # 最终将成功响应对象返回给客户端。
    return SuccessResponse(await crud.RoleDal(auth.db).get_select_datas())


@app.get("/roles/{data_id}/", summary="获取角色信息")
async def get_role(
        data_id: int, # 客户端传入的待获取角色的ID
        # 身份验证，要求验证权限为"auth.role.view"或"auth.role.update"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.role.view", "auth.role.update"]))
):
    # 该代码会根据Auth中的验证信息，判断该用户是否具有"auth.role.view"或"auth.role.update"的权限。
    # 如果验证通过，则调用RoleDal类中的get_data方法，用于从数据库中获取指定ID的完整角色信息，并返回给客户端。
    model = models.VadminRole
    # 在执行get_data方法时，该代码定义了一个选项列表(options)，用于指定需要同时查询的关联表（这里指定查询menus表），以便一次性获取所有相关数据。
    options = [joinedload(model.menus)]
    # 此外，还指定了一个输出模型(schema)，用于将查询结果转换为json格式的数据。
    # 最终将成功响应对象返回给客户端。
    schema = schemas.RoleOut
    # 返回一个成功响应对象,其中data字段为await crud.RoleDal(auth.db).get_data(data_id, options, v_schema=schema)的返回结果
    # 指定ID的完整角色信息
    return SuccessResponse(await crud.RoleDal(auth.db).get_data(data_id, options, v_schema=schema))


###########################################################
#                     菜单管理                             #
###########################################################
@app.get("/menus/", summary="获取菜单列表")
async def get_menus(
        # 身份验证，要求验证权限为"auth.menu.create"或"auth.menu.update"的FullAdminAuth。
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.menu.list"]))
):
    # 返回一个成功响应对象（SuccessResponse），其中data字段为await crud.MenuDal(auth.db).get_tree_list(mode=3)的返回结果，即所有菜单的树形结构列表。
    # 在获取前，该代码会根据Auth中的验证信息，判断该用户是否具有"auth.menu.create"或"auth.menu.update"的权限。
    # 如果验证通过，则调用crud.MenuDal类中的get_tree_list方法，用于从数据库中获取所有菜单的树形结构列表，并返回给客户端。
    # 在执行get_tree_list方法时，该代码指定mode参数为3，表示返回所有菜单的完整信息，包括每个菜单的所有父级菜单和子级菜单。
    # 最终将成功响应对象返回给客户端。
    datas = await crud.MenuDal(auth.db).get_tree_list(mode=1)
    return SuccessResponse(datas)


@app.get("/menus/tree/options/", summary="获取菜单树选择项，添加/修改菜单时使用")
async def get_menus_options(auth: Auth = Depends(FullAdminAuth(permissions=["auth.menu.create", "auth.menu.update"]))):
    datas = await crud.MenuDal(auth.db).get_tree_list(mode=2)
    return SuccessResponse(datas)


@app.get("/menus/role/tree/options/", summary="获取菜单列表树信息，角色权限使用")
async def get_menus_treeselect(
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.role.create", "auth.role.update"]))
):
    return SuccessResponse(await crud.MenuDal(auth.db).get_tree_list(mode=3))


@app.post("/menus/", summary="创建菜单信息")
async def create_menu(menu: schemas.Menu, auth: Auth = Depends(FullAdminAuth(permissions=["auth.menu.create"]))):
    if menu.parent_id:
        menu.alwaysShow = False
    return SuccessResponse(await crud.MenuDal(auth.db).create_data(data=menu))


@app.delete("/menus/", summary="批量删除菜单", description="硬删除, 如果存在角色关联则无法删除")
async def delete_menus(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth(permissions=["auth.menu.delete"]))):
    await crud.MenuDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.put("/menus/{data_id}/", summary="更新菜单信息")
async def put_menus(
        data_id: int,
        data: schemas.Menu, auth: Auth = Depends(FullAdminAuth(permissions=["auth.menu.update"]))
):
    return SuccessResponse(await crud.MenuDal(auth.db).put_data(data_id, data))


@app.get("/menus/{data_id}/", summary="获取菜单信息")
async def put_menus(
        data_id: int,
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.menu.view", "auth.menu.update"]))
):
    schema = schemas.MenuSimpleOut
    return SuccessResponse(await crud.MenuDal(auth.db).get_data(data_id, None, v_schema=schema))


@app.get("/role/menus/tree/{role_id}/", summary="获取菜单列表树信息以及角色菜单权限ID，角色权限使用")
async def get_role_menu_tree(
        role_id: int,
        auth: Auth = Depends(FullAdminAuth(permissions=["auth.role.create", "auth.role.update"]))
):
    treeselect = await crud.MenuDal(auth.db).get_tree_list(mode=3)
    role_menu_tree = await crud.RoleDal(auth.db).get_role_menu_tree(role_id)
    return SuccessResponse({"role_menu_tree": role_menu_tree, "menus": treeselect})
