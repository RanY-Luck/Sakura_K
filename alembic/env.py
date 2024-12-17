from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from db.db_base import BaseModel

config = context.config

# 导入项目中的基本映射类，与 需要迁移的 ORM 模型，不添加会初始化失败
from module_admin.entity.do import *

target_metadata = BaseModel.metadata


def run_migrations_offline():
    """
    # 离线运行
    :return:
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """
    # 在线运行
    :return:
    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    print("离线")
    run_migrations_offline()
else:
    print("在线")
    run_migrations_online()
