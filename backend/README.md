# 接口自动化平台

一个轻量、高效、可扩展的接口自动化测试平台，支持多种触发方式、定时任务、Webhook集成等功能。

## 功能特性

- 🚀 **多种触发方式**：手动触发、定时任务、Webhook集成
- 📊 **实时监控**：执行状态监控、成功率统计、趋势分析
- 🔧 **环境管理**：多环境配置、变量管理、动态替换
- 📝 **报告生成**：详细的执行报告、日志记录、错误追踪
- 🎯 **模块化管理**：测试用例分组、批量执行、依赖管理

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd backend

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置数据库

编辑 `app/core/config.py` 文件，配置数据库连接信息：

```python
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_USER = "your_username"
MYSQL_PASSWORD = "your_password"
MYSQL_DB = "api_automation"
```

### 3. 启动应用

```bash
# 方式1：使用启动脚本
python start.py

# 方式2：直接使用uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 8001 --reload
```

应用启动时会自动：
- 创建数据库表
- 初始化基础数据（环境配置、默认模块）

### 4. 访问应用

- API文档：http://localhost:8001/docs
- 健康检查：http://localhost:8001/health

## 数据库管理

### 自动初始化

应用启动时自动创建表结构和基础数据。

### 手动管理

```bash
# 初始化数据库
python -m app.db.manage init

# 重置数据库
python -m app.db.manage reset

# 删除所有表（谨慎使用）
python -m app.db.manage drop
```

## API接口

### 核心功能

- **环境管理**：`/api/environments/*`
- **模块管理**：`/api/modules/*`
- **测试用例**：`/api/test-cases/*`
- **执行管理**：`/api/executions/*`
- **报告管理**：`/api/reports/*`

### 触发执行

- **手动触发**：`/api/trigger/*`
- **定时任务**：`/api/scheduler/*`
- **Webhook**：`/api/webhook/*`

### 监控统计

- **仪表盘**：`/api/dashboard/*`

## 项目结构

```
app/
├── api/                    # API接口
│   └── v1/                # API版本1
├── core/                   # 核心配置
├── crud/                   # 数据库操作
├── db/                     # 数据库管理
├── models/                 # 数据模型
├── schemas/                # 数据验证
├── services/               # 业务逻辑
└── main.py                 # 应用入口
```

## 开发指南

### 添加新的API接口

1. 在 `app/api/v1/` 下创建新的路由文件
2. 在 `app/schemas/` 下定义数据模型
3. 在 `app/services/` 下实现业务逻辑
4. 在 `app/api/v1/__init__.py` 中注册路由

### 添加新的数据模型

1. 在 `app/models/` 下创建模型文件
2. 在 `app/crud/` 下创建CRUD操作
3. 在 `app/schemas/` 下定义Schema
4. 更新数据库初始化脚本

## 部署

### Docker部署

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

### 生产环境配置

1. 设置环境变量
2. 配置数据库连接
3. 启用HTTPS
4. 配置反向代理
5. 设置日志轮转

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请提交 Issue 或联系开发团队。 