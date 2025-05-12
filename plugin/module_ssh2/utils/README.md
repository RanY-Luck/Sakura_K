# SSH模块使用文档

## 1. 模块简介

SSH模块提供了对远程服务器的SSH操作功能，包括文件上传下载、命令执行、文本读写等。该模块使用了Paramiko库，实现了稳定高效的SSH连接管理，同时提供了一组RESTful API接口，方便在Web界面中进行远程服务器操作。

## 2. 核心功能

- SSH连接管理：建立、测试、维护SSH连接
- 文件操作：上传、下载、删除文件
- 目录操作：列出目录内容、创建目录、删除目录
- 文本操作：读取、写入文本内容
- 命令执行：执行Shell命令、执行脚本文件
- 文件信息：获取文件/目录属性信息

## 3. API接口

模块提供了以下RESTful API接口：

### 3.1 测试SSH连接

```
POST /ssh/connect/test
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）

### 3.2 执行远程命令

```
POST /ssh/command/execute
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- command: 要执行的命令
- timeout: 超时时间（默认60秒）

### 3.3 执行远程脚本

```
POST /ssh/script/execute
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- script_content: 脚本内容
- timeout: 超时时间（默认60秒）

### 3.4 上传文件

```
POST /ssh/file/upload
```

请求参数（multipart/form-data）：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 远程路径
- file: 要上传的文件

### 3.5 下载文件

```
POST /ssh/file/download
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 远程文件路径
- local_path: 本地保存路径

### 3.6 写入文本

```
POST /ssh/text/write
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 远程文件路径
- content: 要写入的文本内容

### 3.7 读取文本

```
POST /ssh/text/read
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 远程文件路径

### 3.8 列出目录内容

```
POST /ssh/dir/list
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 远程目录路径

### 3.9 创建目录

```
POST /ssh/dir/make
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 要创建的远程目录路径

### 3.10 删除文件

```
POST /ssh/file/remove
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 要删除的远程文件路径

### 3.11 删除目录

```
POST /ssh/dir/remove
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 要删除的远程目录路径
- recursive: 是否递归删除（默认false）

### 3.12 获取文件信息

```
POST /ssh/file/info
```

请求参数：
- host: 主机地址
- username: 用户名
- password: 密码
- port: SSH端口（默认22）
- remote_path: 远程文件路径

## 4. 使用示例

### 4.1 测试连接

```javascript
// 前端示例代码（使用Axios）
async function testConnection() {
  try {
    const response = await axios.post('/ssh/connect/test', {
      host: '192.168.1.100',
      username: 'root',
      password: 'your_password'
    });
    
    if (response.data.code === 200) {
      console.log('连接成功');
    } else {
      console.error('连接失败:', response.data.msg);
    }
  } catch (error) {
    console.error('请求异常:', error);
  }
}
```

### 4.2 执行命令

```javascript
// 前端示例代码（使用Axios）
async function executeCommand() {
  try {
    const response = await axios.post('/ssh/command/execute', {
      host: '192.168.1.100',
      username: 'root',
      password: 'your_password',
      command: 'ls -la /home'
    });
    
    if (response.data.code === 200) {
      console.log('命令输出:', response.data.data.output);
    } else {
      console.error('执行失败:', response.data.msg);
    }
  } catch (error) {
    console.error('请求异常:', error);
  }
}
```

## 5. 注意事项

1. 目前仅支持密码验证方式
2. 上传和下载大文件时需要考虑超时设置
3. 执行命令时建议设置合理的超时时间
4. 递归删除目录操作需谨慎，确认路径正确 