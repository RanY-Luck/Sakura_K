如果执行数据库迁移命令,需要去env.py中找到【# 导入项目中的基本映射类，与 需要迁移的 ORM 模型，不添加会初始化失败】并解开注释

# 执行命令（生产环境）：
```python
python main.py migrate

```

# 执行命令（开发环境）：
```python
python main.py migrate --env dev
```

# 开发环境的原命令【非执行】
alembic --name dev revision --autogenerate -m "描述"
alembic --name dev upgrade head
# 回滚上一次版本
alembic --name dev downgrade -1
每次新加功能都要迁移请参考这个写上
```python
from module_admin.entity.do import *
```
