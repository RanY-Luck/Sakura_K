# 开发环境的原命令【非执行】
alembic --name dev revision --autogenerate -m "描述"
alembic --name dev upgrade head
# 回滚上一次版本
alembic --name dev downgrade -1
每次新加功能都要迁移请参考这个写上
```python
from module_admin.entity.do import *
```
