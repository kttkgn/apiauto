# Docker 部署指南

本文档介绍如何使用 Docker 和 Docker Compose 部署接口自动化平台。

## 📋 系统要求

- Docker 20.10+
- Docker Compose 2.0+
- 至少 2GB 可用内存
- 至少 5GB 可用磁盘空间

## 🚀 快速启动

### 方式一：使用启动脚本（推荐）

```bash
# 给脚本执行权限
chmod +x docker-start.sh

# 运行启动脚本
./docker-start.sh
```

### 方式二：手动启动

#### 简化模式（推荐用于开发）

```bash
# 启动核心服务
docker-compose -f docker-compose.simple.yml up -d

# 查看服务状态
docker-compose -f docker-compose.simple.yml ps
```

#### 完整模式（推荐用于生产）

```bash
# 启动所有服务（包含 Nginx）
docker-compose up -d

# 查看服务状态
docker-compose ps
```

## 📦 服务说明

### 核心服务

| 服务名 | 端口 | 说明 |
|--------|------|------|
| `api` | 8001 | FastAPI 应用 |
| `mysql` | 3306 | MySQL 数据库 |
| `redis` | 6379 | Redis 缓存 |

### 可选服务

| 服务名 | 端口 | 说明 |
|--------|------|------|
| `nginx` | 80, 443 | Nginx 反向代理 |

## 🔧 配置说明

### 环境变量

应用通过环境变量进行配置，主要配置项：

```yaml
# 数据库配置
MYSQL_HOST: mysql          # 数据库主机
MYSQL_PORT: 3306           # 数据库端口
MYSQL_USER: api_user       # 数据库用户名
MYSQL_PASSWORD: ApiUser123 # 数据库密码
MYSQL_DB: api_auto         # 数据库名

# Redis 配置
REDIS_HOST: redis          # Redis 主机
REDIS_PORT: 6379           # Redis 端口
REDIS_DB: 0                # Redis 数据库
REDIS_PASSWORD: null       # Redis 密码
```

### 数据持久化

- **MySQL 数据**: `mysql_data` 卷
- **Redis 数据**: `redis_data` 卷
- **应用日志**: `./logs` 目录

## 📊 访问地址

启动成功后，可以通过以下地址访问：

- **API 文档**: http://localhost:8001/docs
- **健康检查**: http://localhost:8001/health
- **数据库**: localhost:3306
- **Redis**: localhost:6379

如果使用完整模式（包含 Nginx）：
- **API 文档**: http://localhost/docs
- **健康检查**: http://localhost/health

## 🛠️ 常用命令

### 服务管理

```bash
# 启动服务
docker-compose up -d

# 停止服务
docker-compose down

# 重启服务
docker-compose restart

# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f api
```

### 数据库管理

```bash
# 进入 MySQL 容器
docker exec -it api_auto_mysql mysql -u root -p

# 备份数据库
docker exec api_auto_mysql mysqldump -u root -p api_auto > backup.sql

# 恢复数据库
docker exec -i api_auto_mysql mysql -u root -p api_auto < backup.sql
```

### 应用管理

```bash
# 进入应用容器
docker exec -it api_auto_app bash

# 查看应用日志
docker logs -f api_auto_app

# 重启应用
docker restart api_auto_app
```

## 🔍 故障排除

### 常见问题

#### 1. 服务启动失败

```bash
# 查看详细日志
docker-compose logs

# 检查端口占用
netstat -tulpn | grep :8001
```

#### 2. 数据库连接失败

```bash
# 检查 MySQL 状态
docker-compose logs mysql

# 测试数据库连接
docker exec -it api_auto_mysql mysql -u api_user -p -e "SHOW DATABASES;"
```

#### 3. 应用无法访问

```bash
# 检查应用健康状态
curl http://localhost:8001/health

# 查看应用日志
docker-compose logs api
```

### 日志位置

- **应用日志**: `./logs/` 目录
- **MySQL 日志**: `docker logs api_auto_mysql`
- **Redis 日志**: `docker logs api_auto_redis`
- **Nginx 日志**: `docker logs api_auto_nginx`

## 🔒 安全建议

### 生产环境配置

1. **修改默认密码**
   ```bash
   # 修改 docker-compose.yml 中的密码
   MYSQL_ROOT_PASSWORD: your_secure_password
   MYSQL_PASSWORD: your_secure_password
   ```

2. **使用环境变量文件**
   ```bash
   # 创建 .env 文件
   MYSQL_ROOT_PASSWORD=your_secure_password
   MYSQL_PASSWORD=your_secure_password
   ```

3. **配置 SSL 证书**
   - 在 Nginx 配置中添加 SSL 证书
   - 使用 Let's Encrypt 或商业证书

4. **限制网络访问**
   - 配置防火墙规则
   - 使用 Docker 网络隔离

## 📈 性能优化

### 资源限制

```yaml
# 在 docker-compose.yml 中添加资源限制
services:
  api:
    deploy:
      resources:
        limits:
          memory: 1G
          cpus: '0.5'
        reservations:
          memory: 512M
          cpus: '0.25'
```

### 数据库优化

```yaml
# MySQL 配置优化
services:
  mysql:
    command: >
      --default-authentication-plugin=mysql_native_password
      --innodb-buffer-pool-size=256M
      --max-connections=200
```

## 🧹 清理命令

```bash
# 停止并删除所有容器
docker-compose down

# 删除所有数据卷（谨慎使用）
docker-compose down -v

# 删除所有镜像
docker-compose down --rmi all

# 清理未使用的资源
docker system prune -a
```

## 📞 技术支持

如果遇到问题，请：

1. 查看日志文件
2. 检查系统资源使用情况
3. 确认网络连接
4. 查看本文档的故障排除部分

更多帮助请参考项目文档或提交 Issue。 