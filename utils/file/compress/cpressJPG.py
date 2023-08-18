#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 18:52
# @Author  : 冉勇
# @Site    : 
# @File    : cpressJPG.py
# @Software: PyCharm
# @desc    : JPEG和PNG图片进行压缩
import os
import time

from PIL import Image, ExifTags  # 安装依赖包：pip3 install pillow

from utils.file.compress import dynamic_quality

"""
PIL读取的图像发生自动旋转：https://blog.csdn.net/mizhenpeng/article/details/82794112
使用python批量压缩图片文件：https://blog.csdn.net/weixin_41855010/article/details/120723943
代码解释：
导入所需的依赖库，包括os、time和Pillow中的Image和ExifTags组件。
定义一个名为compress_jpg_png的函数，该函数接受两个参数，即需要处理的图片文件名和原始图片所在路径。
通过调用Image.open方法打开原始图片，并解决图像的方向问题。
由于JPEG和PNG格式图像可能存在自动旋转的情况，因此这里使用Pillow的ExifTags组件获取图片中的元数据信息，然后根据Orientation标签对图片进行旋转，以保证图片方向正确。
将原始图片转换为RGB格式，并指定其格式为JPEG。
复制原始图片，并使用thumbnail方法将其缩小至原始大小，在保存时指定一些参数，如压缩质量和是否优化等。
最后将缩小后的图片保存到新的文件中，并返回该文件的路径。
"""


def compress_jpg_png(filename, originpath):
    name = filename.rstrip('.png').rstrip('.jpg')
    im = Image.open(os.path.join(originpath, filename))
    # 解决图像方向问题
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation': break
            exif = dict(im._getexif().items())
            if exif[orientation] == 3:
                im = im.rotate(180, expand=True)
            elif exif[orientation] == 6:
                im = im.rotate(270, expand=True)
            elif exif[orientation] == 8:
                im = im.rotate(90, expand=True)
    except:
        pass
    im = im.convert('RGB')
    im.format = "JPEG"
    new_photo = im.copy()
    new_photo.thumbnail(im.size, resample=Image.ANTIALIAS)
    save_args = {'format': im.format}
    save_args['quality'], value = dynamic_quality.jpeg_dynamic_quality(im)
    save_args['optimize'] = True
    save_args['progressive=True'] = True
    new_file = os.path.join(originpath, name + str(int(time.time())) + ".jpg")
    new_photo.save(new_file, **save_args)
    return new_file
