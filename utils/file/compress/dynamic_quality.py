#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/4/18 18:54
# @Author  : 冉勇
# @Site    : 
# @File    : dynamic_quality.py
# @Software: PyCharm
# @desc    : 计算图像质量
from math import log

import PIL.Image  # 安装依赖包：pip3 install pillow
from SSIM_PIL import compare_ssim  # 安装依赖包：pip3 install SSIM-PIL

"""
代码解释：
实现了一个计算图像质量（SSIM）的函数
get_ssim_at_quality函数实现了将给定的photo对象保存为JPEG格式，并调用compare_ssim函数计算图像质量的功能。
其中，quality参数表示JPEG图片的压缩质量，progressive参数表示是否启用逐步渐进式扫描。最后返回计算出的图像质量分数。
_ssim_iteration_count函数实现了在压缩图像时要进行迭代的次数，该函数接收两个参数：压缩质量范围的下限和上限。
如果下限比上限大，则返回0。否则，根据下限和上限之间的跨度计算出需要进行迭代的次数，并返回。
"""


def get_ssim_at_quality(photo, quality):
    """

    :param photo:
    :param quality:
    :return:
    """
    ssim_photo = "tmp.jpg"
    photo.save(ssim_photo, format="JPEG", quality=quality, progressive=True)
    ssim_score = compare_ssim(photo, PIL.Image.open(ssim_photo))
    return ssim_score


def _ssim_iteration_count(lo, hi):
    """Return the depth of the binary search tree for this range"""
    if lo >= hi:
        return 0
    else:
        return int(log(hi - lo, 2)) + 1


def jpeg_dynamic_quality(original_photo):
    """
    动态计算JPEG图像的压缩质量
    代码解释：
    设定目标图像质量（SSIM值）和初始的压缩质量范围上下限（hi和lo）。
    对原始的photo对象进行缩放（resize）操作，将其大小调整为200*200。
    使用get_ssim_at_quality函数计算在压缩到10%质量时的图像质量分数（normalized_ssim）。
    迭代地尝试不同的压缩质量（curr_quality），直到达到指定的目标图像质量为止。
    具体的迭代方式是，在当前的压缩质量范围（low和hi）之间二分查找，
    计算当前质量下的图像质量分数（curr_ssim）并与normalized_ssim比较，得出当前压缩质量对应的图像质量与最初状态的比值（ssim_ratio）。
    如果该比值大于等于目标图像质量，则说明当前压缩质量可以作为最终结果，并将当前质量和对应的图像质量分数保存下来。
    同时，将压缩质量范围上限hi缩小到当前质量的位置，继续进行二分查找。
    如果该比值小于目标图像质量，则说明当前质量太低，需要将压缩质量范围下限lo增加到当前质量的位置，继续进行二分查找。
    最后根据是否找到了合适的压缩质量，返回选择的压缩质量和对应的图像质量分数，或者使用压缩质量范围上限hi计算出默认的图像质量分数并返回。
    :param original_photo:
    :return:
    """
    ssim_goal = 0.9  # the original value is 0.95
    hi = 35  # the original value is 85
    lo = 30  # the original value is 80
    photo = original_photo.resize((200, 200))
    normalized_ssim = get_ssim_at_quality(photo, 10)
    selected_quality = selected_ssim = None
    for i in range(_ssim_iteration_count(lo, hi)):
        curr_quality = (lo + hi) // 2
        curr_ssim = get_ssim_at_quality(photo, curr_quality)
        ssim_ratio = curr_ssim / normalized_ssim
        if ssim_ratio >= ssim_goal:
            selected_quality = curr_quality
            selected_ssim = curr_ssim
            hi = curr_quality
        else:
            lo = curr_quality
    if selected_quality:
        return selected_quality, selected_ssim
    else:
        default_ssim = get_ssim_at_quality(photo, hi)
        return hi, default_ssim
