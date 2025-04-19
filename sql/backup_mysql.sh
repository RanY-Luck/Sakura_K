#!/bin/bash
# MySQL Docker 数据库备份脚本（修复版）
# 作用：从Docker容器中备份MySQL数据库，压缩并管理备份文件

# 设置颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 配置参数
ENV_FILE="/usr/local/ranyong/Sakura_K/.env.docker"
BACKUP_DIR="/usr/local/ranyong/Sakura_K/sql"
DOCKER_CONTAINER="sakura_mysql"  # Docker 容器名称
KEEP_DAYS=7               # 保留最近几天的备份
DATE=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="$BACKUP_DIR/backup_log.txt"

# 记录日志函数
log() {
    echo -e "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

log "${GREEN}开始数据库备份流程${NC}"

# 检查 .env.docker 文件是否存在
if [ ! -f "$ENV_FILE" ]; then
    log "${RED}错误: $ENV_FILE 文件不存在!${NC}"
    exit 1
fi

# 创建备份目录（如果不存在）
mkdir -p $BACKUP_DIR
log "${YELLOW}备份目录: $BACKUP_DIR${NC}"

# 从 .env.docker 文件加载环境变量
log "加载配置文件 $ENV_FILE"

# 使用更安全的方式解析配置文件，处理空格和Windows回车符
while IFS= read -r line || [[ -n "$line" ]]; do
    # 移除Windows风格的回车符
    line=$(echo "$line" | tr -d '\r')

    # 跳过注释和空行
    [[ "$line" =~ ^#.*$ || -z "$line" ]] && continue

    # 提取键值对
    if [[ "$line" =~ (.+)=(.+) ]]; then
        key=$(echo "${BASH_REMATCH[1]}" | xargs)
        value=$(echo "${BASH_REMATCH[2]}" | xargs)

        # 移除引号
        value="${value%\'}"
        value="${value#\'}"
        value="${value%\"}"
        value="${value#\"}"

        # 设置变量
        declare "$key=$value"
        #log "读取配置: $key = [已设置]"
    fi
done < "$ENV_FILE"

# 显示数据库连接信息（隐藏密码）
log "数据库信息: 主机=$DB_HOST, 端口=$DB_PORT, 用户=$DB_USERNAME, 数据库=$DB_DATABASE"

# 检查必要的变量是否已设置
if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_USERNAME" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_DATABASE" ]; then
    log "${RED}错误: 配置文件中缺少必要的数据库配置参数${NC}"
    log "DB_HOST=${DB_HOST:-未设置}"
    log "DB_PORT=${DB_PORT:-未设置}"
    log "DB_USERNAME=${DB_USERNAME:-未设置}"
    log "DB_DATABASE=${DB_DATABASE:-未设置}"
    exit 1
fi

# 检查Docker容器是否运行
if ! docker ps | grep -q "$DOCKER_CONTAINER"; then
    log "${RED}错误: Docker容器 $DOCKER_CONTAINER 未运行!${NC}"
    exit 1
fi

# 设置备份文件名
BACKUP_FILE="$BACKUP_DIR/${DB_DATABASE}_${DATE}.sql"
COMPRESSED_FILE="${BACKUP_FILE}.gz"

log "${YELLOW}准备备份数据库: $DB_DATABASE${NC}"
log "备份文件: $BACKUP_FILE"

# 执行备份 - 不使用配置文件，而是直接在容器内执行命令
log "执行数据库备份..."

# 使用环境变量而不是配置文件
if docker exec -i $DOCKER_CONTAINER sh -c "MYSQL_PWD='$DB_PASSWORD' mysqldump -h'$DB_HOST' -P'$DB_PORT' -u'$DB_USERNAME' '$DB_DATABASE'" > "$BACKUP_FILE" 2>/tmp/mysql_error; then
    log "${GREEN}数据库备份成功完成!${NC}"

    # 压缩备份文件
    log "压缩备份文件..."
    gzip -f "$BACKUP_FILE"
    log "${GREEN}备份文件已压缩: $COMPRESSED_FILE${NC}"

    # 检查压缩文件大小
    FILESIZE=$(du -h "$COMPRESSED_FILE" | cut -f1)
    log "备份文件大小: $FILESIZE"

    # 清理旧的备份文件
    log "清理旧备份文件, 保留最近 $KEEP_DAYS 天的备份..."
    find $BACKUP_DIR -name "*.sql.gz" -type f -mtime +$KEEP_DAYS -delete
    DELETED=$(find $BACKUP_DIR -name "*.sql.gz" -type f -mtime +$KEEP_DAYS | wc -l)
    log "已删除 $DELETED 个过期备份文件"

    # 列出当前备份文件
    BACKUP_COUNT=$(ls -l $BACKUP_DIR/*.sql.gz 2>/dev/null | wc -l)
    log "${GREEN}当前共有 $BACKUP_COUNT 个备份文件${NC}"
else
    ERROR=$(cat /tmp/mysql_error)
    log "${RED}备份失败! 错误信息: $ERROR${NC}"
    rm -f "$BACKUP_FILE"  # 移除可能的部分备份文件
    exit 1
fi

# 展示保留的备份文件
log "${GREEN}备份完成! 当前保留的备份文件:${NC}"
ls -lh $BACKUP_DIR/*.sql.gz | awk '{print $9, $5}'

exit 0