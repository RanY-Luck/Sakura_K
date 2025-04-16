FROM tiangolo/uvicorn-gunicorn:python3.10-slim

LABEL maintainer="ranyong"

WORKDIR /Sakura_k

# 安装必要的构建工具
RUN apt-get update && apt-get install -y g++ && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY pyproject.toml uv.lock ./

# 安装 uv 并使用它来安装依赖
RUN pip3 install --upgrade pip && \
    pip3 install uv && \
    uv venv && \
    # 先将 pyproject.toml 转换为 requirements.txt
    uv pip compile pyproject.toml -o requirements.txt && \
    # 然后使用 requirements.txt 安装依赖
    uv pip install -r requirements.txt \
    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# 复制剩余文件
COPY . .
COPY .env.docker ./.env

RUN if [ -f ".env.docker" ]; then mv .env.docker .env; fi
# 使用 python 直接运行应用
CMD ["uv","run", "app.py"]