#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time     : 2025/5/13 09:49
# @Author   : 冉勇
# @File     : tools.py
# @Software : PyCharm
# @Desc     : 下载、解压、移动插件
import os
import requests
import zipfile
import shutil
from urllib.parse import urlparse
from utils.log_util import logger
from tqdm import tqdm


def download_github_repo(repo_url: str) -> bool:
    """
    下载github仓库
    :param repo_url: github地址：「https://github.com/ranyong1997/Sakura_K_plugin」
    :return:
    """
    try:
        # 解析仓库URL
        parsed_url = urlparse(repo_url)
        if not parsed_url.netloc == 'github.com':
            logger.error("错误: 不是一个有效的GitHub URL")
            return False
        # 构建ZIP下载URL
        repo_path = parsed_url.path.strip('/')
        zip_url = f"https://github.com/{repo_path}/archive/refs/heads/main.zip"
        # 从URL中获取存储库名称
        repo_name = repo_path.split('/')[-1]
        # 为ZIP文件创建一个临时目录
        temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        # 下载ZIP文件
        logger.info(f"下载 {repo_name}...")
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()

        # 获取文件总大小
        total_size = int(response.headers.get('content-length', 0))
        
        zip_path = os.path.join(temp_dir, f"{repo_name}.zip")
        with open(zip_path, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=f"下载 {repo_name}",
                ncols=100
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        # 解压缩ZIP文件
        logger.info(f"解压 {repo_name}...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        # 在提取的文件中找到插件目录
        extracted_dir = os.path.join(temp_dir, f"{repo_name}-main")
        plugin_dir = os.path.join(extracted_dir, "plugin")
        if not os.path.exists(plugin_dir):
            logger.error("错误: 仓库中没有找到插件目录")
            shutil.rmtree(temp_dir)
            return False
        # 找到所有的module *目录
        module_dirs = [d for d in os.listdir(plugin_dir)
                       if os.path.isdir(os.path.join(plugin_dir, d)) and d.startswith('module_')]
        if not module_dirs:
            logger.error("错误: 在插件目录中找不到module_xxx目录")
            shutil.rmtree(temp_dir)
            return False
        # 将每个模块目录移动到目标位置
        for module_name in module_dirs:
            source_dir = os.path.join(plugin_dir, module_name)
            target_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), module_name)
            # 如果存在，则删除现有目录
            if os.path.exists(target_dir):
                shutil.rmtree(target_dir)
            # 移动模块目录
            shutil.move(source_dir, target_dir)
            logger.success(f"成功移动 {module_name} 到 plugin 目录")
        # Clean up
        shutil.rmtree(temp_dir)
        return True
    except requests.exceptions.RequestException as e:
        logger.error(f"下载错误存储库: {str(e)}")
        return False
    except zipfile.BadZipFile:
        logger.error("错误: 无效的ZIP文件")
        return False
    except Exception as e:
        logger.error(f"其他错误: {str(e)}")
        return False


if __name__ == '__main__':
    download_github_repo('https://github.com/ranyong1997/Sakura_K_plugin')
