FROM python:3.10

COPY ../requirements.txt ./

RUN pip3 install --upgrade pip

RUN pip3 install --no-cache-dir -r requirements.txt  -i https://mirrors.aliyun.com/pypi/simple/

WORKDIR /app


#CMD ["sh", "-c", "python /app/run.py run & python /app/utils/task/run.py"]
#CMD ["sh", "-c", "python /app/run.py run"]
CMD ["python", "main.py","run"]
