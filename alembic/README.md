> 如果执行数据库迁移命令,需要去env.py中找到【# 导入项目中的基本映射类，与 需要迁移的 ORM 模型，不添加会初始化失败】并解开注释
```text
# 执行命令（生产环境）：
python main.py migrate

# 执行命令（开发环境）：
python main.py migrate --env dev

# 开发环境的原命令【非执行】
alembic --name dev revision --autogenerate -m 2.0
alembic --name dev upgrade head
```

每次新加功能都要迁移请参考这个写上
```python
from apps.vadmin.auth.models import *
from apps.vadmin.system.models import *
from apps.vadmin.record.models import *
from apps.vadmin.help.models import *
from apps.vadmin.resource.models import *
from apps.vadmin.redbook.models import *
from apps.vadmin.autotest.project.models import *
from apps.vadmin.autotest.module.models import *
from apps.vadmin.autotest.apinfo.models import *
from apps.vadmin.autotest.datasource.models import *
from apps.vadmin.autotest.env.models import *
from apps.vadmin.autotest.functions.models import *
from apps.vadmin.autotest.report.models import *
from apps.vadmin.autotest.testcase.models import *
```

