#!/bin/bash

# 设置 .env.docker 文件的路径
ENV_FILE="/usr/local/ranyong/Sakura_K/.env.docker"

# 检查 .env.docker 文件是否存在
if [ ! -f "$ENV_FILE" ]; then
    echo "Error: $ENV_FILE not found!"
    exit 1
fi

# 从 .env.docker 文件加载环境变量
while IFS= read -r line || [[ -n "$line" ]]; do
    # 忽略注释和空行
    if [[ ! "$line" =~ ^\s*# && -n "$line" ]]; then
        # 提取key和value
        if [[ "$line" =~ ^([^=]+)=(.*)$ ]]; then
            key=$(echo "${BASH_REMATCH[1]}" | xargs)  # xargs 用于去除前后空格
            value=$(echo "${BASH_REMATCH[2]}" | xargs | sed "s/^'\(.*\)'$/\1/")  # 移除单引号
            # 导出变量
            export "$key"="$value"
        fi
    fi
done < "$ENV_FILE"

# 设置备份相关变量
BACKUP_DIR="/usr/local/ranyong/Sakura_K/sql"
DATE=$(date +"%Y%m%d_%H%M%S")

# 创建备份目录（如果不存在）
mkdir -p $BACKUP_DIR

# 检查必要的变量是否已设置
if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_USERNAME" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_DATABASE" ]; then
    echo "Error: One or more required variables are not set in $ENV_FILE"
    exit 1
fi

# 执行备份
docker exec mysql mysqldump -h"$DB_HOST" -P"$DB_PORT" -u"$DB_USERNAME" -p"$DB_PASSWORD" "$DB_DATABASE" > "$BACKUP_DIR/${DB_DATABASE}_${DATE}.sql"

# 检查备份是否成功
if [ $? -eq 0 ]; then
    echo "Backup created successfully: $BACKUP_DIR/${DB_DATABASE}_${DATE}.sql"

    # 压缩备份文件
    gzip "$BACKUP_DIR/${DB_DATABASE}_${DATE}.sql"
    echo "Backup compressed: $BACKUP_DIR/${DB_DATABASE}_${DATE}.sql.gz"

#    # 删除旧的备份文件（例如：保留最近7天的备份）
#    find $BACKUP_DIR -name "*.sql.gz" -type f -mtime +7 -delete

    # 保留最近的7次备份，删除更早的备份
    cd $BACKUP_DIR
    ls -t *.sql.gz | awk 'NR>7' | xargs -r rm

    echo "Cleaned up old backups, keeping the 7 most recent."
else
    echo "Error: Backup failed"
    exit 1
fi

# 清理环境变量
unset DB_HOST DB_PORT DB_USERNAME DB_PASSWORD DB_DATABASE