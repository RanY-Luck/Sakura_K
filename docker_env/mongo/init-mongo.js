db = db.getSiblingDB('sakura'); // 切换到要创建的数据库

db.createUser({
    user: 'root',
    pwd: '123456',
    roles: ["readWrite", "dbAdmin"]
});