FROM python:3.10

COPY ./Sakura_K/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app

CMD ["sh", "-c", "python main.py run & python /utils/task/run.py"]
