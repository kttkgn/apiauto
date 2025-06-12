# 数据库管理

## 自动初始化

应用启动时会自动执行以下操作：

1. **创建数据库表**：根据模型定义自动创建所有必要的表
2. **初始化基础数据**：如果数据库为空，会自动创建默认的环境配置和模块

## 手动管理

### 使用管理脚本

```bash
# 初始化数据库（创建表并添加基础数据）
python -m app.db.manage init

# 重置数据库（删除所有表并重新创建）
python -m app.db.manage reset

# 删除所有表（谨慎使用）
python -m app.db.manage drop
```

### 使用Python代码

```python
from app.db.init_db import init_db, reset_db, drop_db

# 初始化数据库
await init_db()

# 重置数据库
await reset_db()

# 删除所有表
await drop_db()
```

## 数据库表结构

### 核心表

- **environments** - 环境配置表
- **environment_variables** - 环境变量表
- **modules** - 模块表
- **module_variables** - 模块变量表
- **test_cases** - 测试用例表
- **executions** - 执行记录表
- **execution_logs** - 执行日志表
- **execution_details** - 执行详情表
- **reports** - 测试报告表

### 表关系

```
Environment (1) ←→ (N) Execution (1) ←→ (N) ExecutionLog
Environment (1) ←→ (N) EnvironmentVariable
Module (1) ←→ (N) TestCase
Module (1) ←→ (N) ModuleVariable
Module (1) ←→ (N) Execution
TestCase (1) ←→ (N) ExecutionDetail
Execution (1) ←→ (N) ExecutionDetail
Execution (1) ←→ (N) Report
```

## 默认数据

### 环境配置

- 开发环境: `http://localhost:8080`
- 测试环境: `http://test-api.example.com`
- 预发布环境: `http://staging-api.example.com`

### 默认模块

- 用户管理
- 订单管理
- 商品管理

## 注意事项

1. **备份数据**：在执行 `reset` 或 `drop` 操作前，请确保已备份重要数据
2. **生产环境**：在生产环境中谨慎使用 `drop` 命令
3. **权限检查**：确保数据库用户有创建表的权限
4. **连接配置**：确保数据库连接配置正确 