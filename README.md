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
REDIS_DB_URL = "Redis://:密码@地址:端口/数据库"

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
sqlalchemy.url = mysql + pymysql: // root: 123456 @ 127.0
.0
.1: 3306 / sakura_k

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
mysql> create database sakura_k;  # 创建数据库
mysql> use sakura_k;           # 使用已创建的数据库 
mysql> set names utf8;         # 设置编码
```

4. 初始化数据库数据

```
# 项目根目录下执行，需提前创建好数据库
# 会自动将模型迁移到数据库，并生成初始化数据
# 执行前请确认执行的环境与settings.py文件中配置的DEBUG一致
# 比如要初始化开发环境，那么env参数应该为 dev，并且 application/settings.DEBUG 应该 = True
# 比如要初始化生产环境，那么env参数应该为 pro，并且 application/settings.DEBUG 应该 = False

# （生产环境）
python3 main.py init

# （开发环境）
python3 main.py init --env dev
```

5. 修改项目基本配置信息

- 修改数据库表 - vadmin_system_settings 中的关键信息

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
#运行程序
python3 main.py run
```

## 其他操作

- 接口Swagger文档

```
#在线文档地址(在配置文件里面设置路径或者关闭)
http://127.0.0.1:9000/docs
```

- 提交代码模板

```
✨ feat:  新增
🐞 Fix: 修复
📃 docs: 文档
🦄 refactor: 重构
🎈 perf: 优化
```

- Git提交代码

Git更新ignore文件直接修改gitignore是不会生效的，需要先去掉已经托管的文件，修改完成之后再重新添加并提交。

```
第一步：
git rm -r --cached .
去掉已经托管的文件
第二步：
修改自己的igonre文件内容
第三步：
git add .
git commit -m "clear cached"
```

- 执行数据库迁移命令（终端执行）

```
# 执行命令（生产环境）：
python main.py migrate

# 执行命令（开发环境）：
python main.py migrate --env dev

# 开发环境的原命令
alembic --name dev revision --autogenerate -m 2.0
alembic --name dev upgrade head
```

## 查数据

自定义的一些查询过滤

```
# 日期查询
# 值的类型：str
# 值得格式：%Y-%m-%d：2023-05-14
字段名称=("date", 值)

# 模糊查询
# 值的类型: str
字段名称=("like", 值)

# in 查询
# 值的类型：list
字段名称=("in", 值)

# 时间区间查询
# 值的类型：tuple 或者 list
字段名称=("between", 值)

# 月份查询
# 值的类型：str
# 值的格式：%Y-%m：2023-05
字段名称=("month", 值)

# 不等于查询
字段名称=("!=", 值)

# 大于查询
字段名称=(">", 值)

# 等于 None
字段名称=("None")

# 不等于 None
字段名称=("not None")
```

代码部分：

```python
def __dict_filter(self, **kwargs) -> list[BinaryExpression]:
    """
    字典过滤
    :param model:
    :param kwargs:
    """
    conditions = []
    for field, value in kwargs.items():
        if value is not None and value != "":
            attr = getattr(self.model, field)
            if isinstance(value, tuple):
                if len(value) == 1:
                    if value[0] == "None":
                        conditions.append(attr.is_(None))
                    elif value[0] == "not None":
                        conditions.append(attr.isnot(None))
                    else:
                        raise CustomException("SQL查询语法错误")
                elif len(value) == 2 and value[1] not in [None, [], ""]:
                    if value[0] == "date":
                        # 根据日期查询， 关键函数是：func.time_format和func.date_format
                        conditions.append(func.date_format(attr, "%Y-%m-%d") == value[1])
                    elif value[0] == "like":
                        conditions.append(attr.like(f"%{value[1]}%"))
                    elif value[0] == "in":
                        conditions.append(attr.in_(value[1]))
                    elif value[0] == "between" and len(value[1]) == 2:
                        conditions.append(attr.between(value[1][0], value[1][1]))
                    elif value[0] == "month":
                        conditions.append(func.date_format(attr, "%Y-%m") == value[1])
                    elif value[0] == "!=":
                        conditions.append(attr != value[1])
                    elif value[0] == ">":
                        conditions.append(attr > value[1])
                    elif value[0] == "<=":
                        conditions.append(attr <= value[1])
                    else:
                        raise CustomException("SQL查询语法错误")
            else:
                conditions.append(attr == value)
    return conditions
```

示例：

查询所有用户id为1或2或 4或6，并且email不为空，并且名称包括李：

```python
users = UserDal(db).get_datas(limit=0, id=("in", [1, 2, 4, 6]), email=("not None",), name=("like", "李"))

# limit=0：表示返回所有结果数据
# 这里的 get_datas 默认返回的是 pydantic 模型数据
# 如果需要返回用户对象列表，使用如下语句：
users = UserDal(db).get_datas(
    limit=0,
    id=("in", [1, 2, 4, 6]),
    email=("not None",),
    name=("like", "李"),
    v_return_objs=True
)
```

查询所有用户id为1或2或 4或6，并且email不为空，并且名称包括李：

查询第一页，每页两条数据，并返回总数，同样可以通过 get_datas 实现原始查询方式：

```python
v_where = [VadminUser.id.in_([1, 2, 4, 6]), VadminUser.email.isnot(None), VadminUser.name.like(f"%李%")]
users, count = UserDal(db).get_datas(limit=2, v_where=v_where, v_return_count=True)

# 这里的 get_datas 默认返回的是 pydantic 模型数据
# 如果需要返回用户对象列表，使用如下语句：
users, count = UserDal(db).get_datas(
    limit=2,
    v_where=v_where,
    v_return_count=True,
    v_return_objs=True,
)
```

外键查询示例

以常见问题表为主表，查询出创建用户名称为kinit的用户，创建了哪些常见问题，并加载出用户信息：

```python
v_options = [joinedload(VadminIssue.create_user)]
v_join = [["create_user"]]
v_where = [VadminUser.name == "kinit"]
datas = await crud.IssueCategoryDal(auth.db).get_datas(
    limit=0,
    v_options=options,
    v_join=v_join,
    v_where=v_where,
    v_return_objs=True
)
```

mac系统安装虚拟环境和激活虚拟环境
一、安装virtualenv
> sudo pip install virtualenv

二、创建虚拟环境
> virtualenv venv # venv为虚拟环境的名称，可以根据需要自定义

注意，如果你想使用Python3创建虚拟环境，需要添加--python选项：
> virtualenv --python=python3 env

三、激活虚拟环境
> source env/bin/activate

## 如何快速开发一个接口

第一步：所有接口逻辑写在/apps/vadmin/目录下,创建一个包,然后再里面分别创建models，params，schemas包目录和crud.py,views.py文件
models包目录下是数据模型，可以自定义存什么样的数据
第二步：在models下创建个自定义的py文件

