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
from . import schemas, crud, params, models

app = APIRouter()


###########################################################
#                  小红书图片资源管理                        #
###########################################################

@app.get('/redbookimages', summary="获取小红书图片列表")
async def get_redbook_images_list(p: params.RedBookParams = Depends(), auth: Auth = Depends(FullAdminAuth())):
    # todo:查询有问题
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
    #todo:写库有些值要必填
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
