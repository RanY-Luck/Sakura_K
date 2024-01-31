"""
@Project : Sakura_K
@File    : views.py
@IDE     : PyCharm
@Author  : RanY
@Date    : 2023/10/13 10:45
@Desc    : 小红书图片资源管理
"""
from fastapi import APIRouter, Depends, UploadFile
from sqlalchemy.orm import joinedload

from application.settings import ALIYUN_OSS
from apps.vadmin.auth.utils.current import FullAdminAuth
from apps.vadmin.auth.utils.validation.auth import Auth
from core.dependencies import IdList
from utils.file.aliyun_oss import AliyunOSS, BucketConf
from utils.response import SuccessResponse
from utils.xhs.source import XHS
from . import schemas, crud, params, models
from .schemas import Links

app = APIRouter()


###########################################################
#                  小红书图片资源管理                        #
###########################################################

@app.put("/redbookdown", summary="获取小红书无水印文件,支持单个下载")
async def getredbookdown(link: str | None, auth: Auth = Depends(FullAdminAuth())):
    """获取小红书无水印文件,支持单个下载"""
    # 实例对象
    work_path = "G:\\"  # 作品数据/文件保存根路径，默认值：项目根路径
    folder_name = "Download"  # 作品文件储存文件夹名称（自动创建），默认值：Download
    user_agent = ""  # 请求头 User-Agent
    cookie = ""  # 小红书网页版 Cookie，无需登录
    proxy = None  # 网络代理
    timeout = 5  # 请求数据超时限制，单位：秒，默认值：10
    chunk = 1024 * 1024 * 10  # 下载文件时，每次从服务器获取的数据块大小，单位：字节
    max_retry = 5  # 请求数据失败时，重试的最大次数，单位：秒，默认值：5
    record_data = True  # 是否记录作品数据至文件
    image_format = "PNG"  # 图文作品文件下载格式，支持：PNG、WEBP
    folder_mode = True  # 是否将每个作品的文件储存至单独的文件夹
    async with XHS(
            work_path=work_path,
            folder_name=folder_name,
            user_agent=user_agent,
            cookie=cookie,
            proxy=proxy,
            timeout=timeout,
            chunk=chunk,
            max_retry=max_retry,
            record_data=record_data,
            image_format=image_format,
            folder_mode=folder_mode,
    ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        print(await xhs.extract(link, download))  # 下载单个作品
    return SuccessResponse()


@app.put("/redbookdownmultiple", summary="获取小红书无水印文件,支持批量下载")
async def getredbookdownmultiple(links: Links, auth: Auth = Depends(FullAdminAuth())):
    """获取小红书无水印文件,支持批量下载"""
    multiple_links = " ".join(links.link or [])
    # 实例对象
    work_path = "G:\\"  # 作品数据/文件保存根路径，默认值：项目根路径
    folder_name = "Download"  # 作品文件储存文件夹名称（自动创建），默认值：Download
    user_agent = ""  # 请求头 User-Agent
    cookie = ""  # 小红书网页版 Cookie，无需登录
    proxy = None  # 网络代理
    timeout = 5  # 请求数据超时限制，单位：秒，默认值：10
    chunk = 1024 * 1024 * 10  # 下载文件时，每次从服务器获取的数据块大小，单位：字节
    max_retry = 5  # 请求数据失败时，重试的最大次数，单位：秒，默认值：5
    record_data = True  # 是否记录作品数据至文件
    image_format = "PNG"  # 图文作品文件下载格式，支持：PNG、WEBP
    folder_mode = True  # 是否将每个作品的文件储存至单独的文件夹
    async with XHS(
            work_path=work_path,
            folder_name=folder_name,
            user_agent=user_agent,
            cookie=cookie,
            proxy=proxy,
            timeout=timeout,
            chunk=chunk,
            max_retry=max_retry,
            record_data=record_data,
            image_format=image_format,
            folder_mode=folder_mode,
    ) as xhs:  # 使用自定义参数
        download = True  # 是否下载作品文件，默认值：False
        # 返回作品详细信息，包括下载地址
        print(await xhs.extract(multiple_links, download))  # 支持传入多个作品链接
    return SuccessResponse()


@app.get('/redbookimages', summary="获取小红书图片列表")
async def get_redbook_images_list(p: params.RedBookParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    model = models.VadminRedBook
    v_options = [joinedload(model.create_user)]
    v_schema = schemas.RedBookImagesOut
    datas, count = await crud.RedBookDal(auth.db).get_datas(
        **p.dict(),
        v_options=v_options,
        v_schema=v_schema,
        v_return_scalars=True
    )
    return SuccessResponse(datas, count=count)


@app.post("/redbookimages", summary="创建小红书图片")
async def create_redbook_images(file: UploadFile, auth: Auth = Depends(FullAdminAuth())):
    # todo:写库有些值要必填
    filepath = f"/resource/redbookimages/"
    result = await AliyunOSS(BucketConf(**ALIYUN_OSS)).upload_image(filepath, file)
    data = schemas.RedBookImages(
        filename=file.filename,
        image_url=result,
        create_user_id=auth.user.id
    )
    return SuccessResponse(await crud.RedBookDal(auth.db).create_data(data=data))


@app.delete("/redbookimages", summary="删除图片", description="硬删除")
async def delete_redbook_images(ids: IdList = Depends(), auth: Auth = Depends(FullAdminAuth())):
    await crud.RedBookDal(auth.db).delete_datas(ids.ids, v_soft=False)
    return SuccessResponse("删除成功")


@app.get("/redbookimages", summary="获取小红书图片信息")
async def get_redbook_images(data_id: int, auth: Auth = Depends(FullAdminAuth())):
    return SuccessResponse(await crud.RedBookDal(auth.db).get_data(data_id, v_schema=schemas.RedBookImagesOut))
