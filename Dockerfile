FROM tiangolo/uvicorn-gunicorn:python3.10-slim

LABEL maintainer="ranyong"

WORKDIR /Sakura_k

COPY pyproject.toml poetry.lock ./

RUN pip3 install --upgrade pip && \
    pip3 install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev

COPY . .
COPY .env.docker ./.env

CMD ["poetry", "run", "python", "app.py"]