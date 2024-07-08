```text
# 安装项目依赖环境
pip3 install -r requirements.txt

# 配置环境
根目录复制 .env.dev.example -> .env.dev
在.env.dev文件中配置开发环境的数据库和redis
## 数据库
############################################
# 数据库主机
DB_HOST = '127.0.0.1'
# 数据库端口
DB_PORT = 3306
# 数据库用户名
DB_USERNAME = 'root'
# 数据库密码
DB_PASSWORD = 'Ranyong_520'
# 数据库名称
DB_DATABASE = 'Sakura_K_fastapi'
############################################

## redis
############################################
# Redis主机
REDIS_HOST = '127.0.0.1'
# Redis端口
REDIS_PORT = 6379
# Redis用户名
REDIS_USERNAME = ''
# Redis密码
REDIS_PASSWORD = ''
# Redis数据库
REDIS_DATABASE = 11
############################################

# 运行sql文件
1.新建数据库Sakura_K_fastapi(默认，可修改)
2.使用命令或数据库连接工具运行sql文件夹下的Sakura_K_fastapi.sql

# 运行后端
## 测试环境
python3 app.py --env=dev
## 正事环境
python3 app.py --env=prod
```