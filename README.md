### 后端技术

- [Python3](https://www.python.org/downloads/windows/)：熟悉 python3 基础语法
- [FastAPI](https://fastapi.tiangolo.com/zh/) - 熟悉后台接口 Web 框架.
- [Typer](https://typer.tiangolo.com/) - 熟悉命令行工具的使用
- [MySQL](https://www.mysql.com/) 和 [MongoDB](https://www.mongodb.com/) 和 [Redis](https://redis.io/)  - 熟悉数据存储数据库
- [iP查询接口文档](https://user.ip138.com/ip/doc)：IP查询第三方服务，有1000次的免费次数

### PC端

- [node](https://gitee.com/link?target=http%3A%2F%2Fnodejs.org%2F)
  和 [git](https://gitee.com/link?target=https%3A%2F%2Fgit-scm.com%2F) - 项目开发环境
- [Vite](https://gitee.com/link?target=https%3A%2F%2Fvitejs.dev%2F) - 熟悉 vite 特性
- [Vue3](https://gitee.com/link?target=https%3A%2F%2Fv3.vuejs.org%2F) - 熟悉 Vue 基础语法
- [TypeScript](https://gitee.com/link?target=https%3A%2F%2Fwww.typescriptlang.org%2F) - 熟悉 `TypeScript` 基本语法
- [Es6+](https://gitee.com/link?target=http%3A%2F%2Fes6.ruanyifeng.com%2F) - 熟悉 es6 基本语法
- [Vue-Router-Next](https://gitee.com/link?target=https%3A%2F%2Fnext.router.vuejs.org%2F) - 熟悉 vue-router 基本使用
- [Element-Plus](https://gitee.com/link?target=https%3A%2F%2Felement-plus.org%2F) - element-plus 基本使用
- [Mock.js](https://gitee.com/link?target=https%3A%2F%2Fgithub.com%2Fnuysoft%2FMock) - mockjs 基本语法
- [vue3-json-viewer](https://gitee.com/isfive/vue3-json-viewer)：简单易用的json内容展示组件,适配vue3和vite。
- [SortableJS/vue.draggable.next](https://github.com/SortableJS/vue.draggable.next)：Vue 组件 （Vue.js 3.0）
  允许拖放和与视图模型数组同步。
- [高德地图API (amap.com)](https://lbs.amap.com/api/jsapi-v2/guide/webcli/map-vue1)：地图 JSAPI 2.0 是高德开放平台免费提供的第四代
  Web 地图渲染引擎。

### 定时任务

- [Python3](https://www.python.org/downloads/windows/) -熟悉 python3 基础语法
- [APScheduler](https://github.com/agronholm/apscheduler) - 熟悉定时任务框架
- [MongoDB](https://www.mongodb.com/) 和 [Redis](https://redis.io/)  - 熟悉数据存储数据库

### 准备工作

```
Python == 3.10 (其他版本均未测试)
nodejs >= 14.0 (推荐使用最新稳定版)
Mysql >= 8.0
MongoDB (推荐使用最新稳定版)
Redis (推荐使用最新稳定版)
```

### 后端

1. 安装依赖

```

pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/
```

2. 修改项目数据库配置信息
   在 `application/config` 目录中

- development_example.py：开发环境填写模板，需要单独复制出来删除**_example**

- production_example.py：生产环境填写模板，需要单独复制出来删除**_example**

```python
"""
Mysql 数据库配置项
连接引擎官方文档：https://www.osgeo.cn/sqlalchemy/core/engines.html
数据库链接配置说明：mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
"""
SQLALCHEMY_DATABASE_URL = "mysql+asyncmy://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称"
SQLALCHEMY_DATABASE_TYPE = "mysql"

"""
Redis 数据库配置
"""
REDIS_DB_ENABLE = True
REDIS_DB_URL = "redis://:密码@地址:端口/数据库"

"""
MongoDB 数据库配置
"""
MONGO_DB_ENABLE = True
MONGO_DB_NAME = "数据库名称"
MONGO_DB_URL = f"mongodb://用户名:密码@地址:端口/?authSource={MONGO_DB_NAME}"

"""
阿里云对象存储OSS配置
阿里云账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM用户进行API访问或日常运维，请登录RAM控制台创建RAM用户。
yourEndpoint填写Bucket所在地域对应的Endpoint。以华东1（杭州）为例，Endpoint填写为https://oss-cn-hangzhou.aliyuncs.com。
*  [accessKeyId] {String}：通过阿里云控制台创建的AccessKey。
*  [accessKeySecret] {String}：通过阿里云控制台创建的AccessSecret。
*  [bucket] {String}：通过控制台或PutBucket创建的bucket。
*  [endpoint] {String}：bucket所在的区域， 默认oss-cn-hangzhou。
"""
ALIYUN_OSS = {
    "accessKeyId": "accessKeyId",
    "accessKeySecret": "accessKeySecret",
    "endpoint": "endpoint",
    "bucket": "bucket",
    "baseUrl": "baseUrl"
}

"""
获取IP地址归属地
文档：https://user.ip138.com/ip/doc
"""
IP_PARSE_ENABLE = True
IP_PARSE_TOKEN = "IP_PARSE_TOKEN"
```

并在`alembic.ini`文件中配置数据库信息，用于数据库映射

```python
# mysql+pymysql://数据库用户名:数据库密码@数据库地址:数据库端口/数据库名称
[dev]
# 开发环境
version_locations = % (here)
s / alembic / versions_dev
sqlalchemy.url = sqlalchemy.url = mysql + pymysql: // root: 123456 @ 127.0
.0
.1 / kinit

[pro]
# 生产环境
version_locations = % (here)
s / alembic / versions_pro
sqlalchemy.url = sqlalchemy.url = mysql + pymysql: // root: 123456 @ 127.0
.0
.1 / kinit
```

3. 创建数据库

```
mysql> create database kinit;  # 创建数据库
mysql> use sakura_k;           # 使用已创建的数据库 
mysql> set names utf8;         # 设置编码
```

4. 初始化数据库数据

```
# 项目根目录下执行，需提前创建好数据库
# 会自动将模型迁移到数据库，并生成初始化数据
# 执行前请确认执行的环境与settings.py文件中配置的DEBUG一致

# （生产环境）
python3 main.py init

# （开发环境）
python3 main.py init --env dev
```

5. 修改项目基本配置信息
   修改数据库表 - vadmin_system_settings 中的关键信息

```python
# 阿里云短信配置
sms_access_key
sms_access_key_secret
sms_sign_name_1
sms_template_code_1
sms_sign_name_2
sms_template_code_2

# 高德地图配置
map_key

# 微信小程序配置
wx_server_app_id
wx_server_app_secret

# 邮箱配置
email_access
email_password
email_server
email_port
```

6. 启动

```
# 进入项目根目录下执行,初始化数据: 这里执行dev环境
python3 main.py init --env dev
#运行程序
python3 main.py run
```


mac系统安装虚拟环境和激活虚拟环境
一、安装virtualenv
> sudo pip install virtualenv

二、创建虚拟环境
> virtualenv venv  # venv为虚拟环境的名称，可以根据需要自定义

注意，如果你想使用Python3创建虚拟环境，需要添加--python选项：
> virtualenv --python=python3 env

三、激活虚拟环境
> source env/bin/activate
