# 引入python版本
# [Mac用slim会报错]
#FROM python:3.10
FROM python:3.10
# 设置编码格式
ENV LANG=C.UTF-8
#作者信息
MAINTAINER 冉勇 ranyong1209@gmail.com
# 开始构建
RUN echo 'Start building.............'
# 设置时间
RUN ln -sf /usr/share/zoneinfo/Asia/Beijing/etc/localtime
#设置环境变量，否则docker里容易出现找不到模块
ENV PYTHONPATH "${PYTHONPATH}:/Sakura_K"
# 复制该文件到工作目录中
COPY requirements.txt .
# 升级pip并禁用缓存并批量安装包(后面的链接是利用镜像源安装，速度会加快)
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# RUN pip install --no-cache-dir -r requirements.txt
# 复制工作目录
COPY . /Sakura_K
# 设置工作目录
WORKDIR /Sakura_K
# 结束构建
RUN echo 'End building.............'
# 命令行运行，启动uvicorn服务
RUN python main.py run
#CMD [ "python", "main.py", "run"]