FROM tiangolo/uvicorn-gunicorn:python3.10-slim

LABEL maintainer="ranyong"

COPY requirements.txt /Sakura_K/requirements.txt

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r /Sakura_K/requirements.txt

COPY . /Sakura_K

COPY .env.docker /Sakura_K/.env
# 不写这个不会加载 .env.docker环境（勿动）
RUN if [ -f ".env.docker" ]; then mv .env.docker .env; fi

CMD ["python", "app.py"]
