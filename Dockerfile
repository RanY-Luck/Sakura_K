FROM python:3.10-slim

LABEL maintainer="ranyong"

WORKDIR /Sakura_K

ENV PYTHONUNBUFFERED=1

ENV APP_ENV=docker

EXPOSE 9099

COPY ./requirements.txt ./

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . /Sakura_K

CMD ["python", "-m", "uvicorn", "app:app","--host", "0.0.0.0", "--port", "9099"]