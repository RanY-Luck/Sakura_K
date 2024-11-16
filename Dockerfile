FROM tiangolo/uvicorn-gunicorn:python3.10-slim

LABEL maintainer="ranyong"

WORKDIR /Sakura_k

COPY pyproject.toml poetry.lock /Sakura_k/

RUN pip3 install --no-cache-dir  --upgrade pip

RUN pip3 install --no-cache-dir poetry

RUN poetry install

COPY . /Sakura_k

COPY .env.docker /Sakura_K/.env

# 不写这个不会加载 .env.docker环境（勿动）
RUN if [ -f ".env.docker" ]; then mv .env.docker .env; fi

CMD ["poetry", "run", "python", "app.py"]