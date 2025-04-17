# Select the image to build based on SERVER_TYPE, defaulting to fastapi_server, or docker-compose build args
ARG SERVER_TYPE=fastapi_server

# === Python environment from uv ===
FROM tiangolo/uvicorn-gunicorn:python3.10-slim AS builder

LABEL maintainer="ranyong"

WORKDIR /Sakura_k

COPY requirements.txt /Sakura_K/requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r /Sakura_K/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY . /Sakura_k

COPY .env.docker /Sakura_K/.env

# 不写这个不会加载 .env.docker环境（勿动）
RUN if [ -f ".env.docker" ]; then mv .env.docker .env; fi

CMD ["python", "app.py"]