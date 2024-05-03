db = db.getSiblingDB('admin');

db.createUser({
    user: 'admin',
    pwd: '123456',
    roles: ["readWrite", "dbAdmin"]
});