FROM python:3.10

COPY ../../requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app

#CMD ["sh", "-c", "python /app/main.py run & python /app/utils/task/run.py"]
#CMD ["sh", "-c", "python /app/main.py run"]
CMD ["python", "/app/main.py"]
