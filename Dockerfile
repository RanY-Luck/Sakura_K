# Select the image to build based on SERVER_TYPE, defaulting to fastapi_server
ARG SERVER_TYPE=fastapi_server

# === Python environment from uv ===
FROM tiangolo/uvicorn-gunicorn:python3.10-slim AS builder

LABEL maintainer="ranyong"

WORKDIR /Sakura_K

# 更新 pip
RUN pip3 install --no-cache-dir --upgrade pip

# 复制 requirements.txt 并安装依赖
COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt
# 复制项目文件
COPY . .

# 处理 .env 文件
COPY .env.docker .env
RUN if [ -f ".env.docker" ]; then mv .env.docker .env; fi

# 启动命令
CMD ["python", "app.py"]