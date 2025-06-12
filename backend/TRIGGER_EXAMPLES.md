# 接口自动化执行触发方式使用示例

## 概述

本项目支持多种接口自动化执行触发方式，满足不同场景的需求。以下是详细的使用示例：

## 1. 手动触发执行

### 1.1 执行单个测试用例

```bash
# 异步执行（推荐）
curl -X POST "http://localhost:8001/api/trigger/single" \
  -H "Content-Type: application/json" \
  -d '{
    "test_case_id": 1,
    "environment_id": 1,
    "executor": "manual"
  }'

# 快速测试（同步执行，立即返回结果）
curl -X POST "http://localhost:8001/api/trigger/quick-test?test_case_id=1&environment_id=1"
```

### 1.2 执行整个模块

```bash
curl -X POST "http://localhost:8001/api/trigger/module" \
  -H "Content-Type: application/json" \
  -d '{
    "module_id": 1,
    "environment_id": 1,
    "executor": "manual"
  }'
```

### 1.3 执行所有测试用例

```bash
curl -X POST "http://localhost:8001/api/trigger/all" \
  -H "Content-Type: application/json" \
  -d '{
    "environment_id": 1,
    "executor": "manual"
  }'
```

### 1.4 批量执行指定测试用例

```bash
curl -X POST "http://localhost:8001/api/trigger/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "test_case_ids": [1, 2, 3, 4],
    "environment_id": 1,
    "executor": "batch"
  }'
```

### 1.5 查询执行状态

```bash
curl -X GET "http://localhost:8001/api/trigger/status/123"
```

## 2. 定时任务触发

### 2.1 调度单个测试用例的定时执行

```bash
curl -X POST "http://localhost:8001/api/scheduler/single" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "task_001",
    "test_case_id": 1,
    "environment_id": 1,
    "schedule_time": "2024-03-21T10:00:00",
    "executor": "scheduler"
  }'
```

### 2.2 调度模块的定时执行

```bash
curl -X POST "http://localhost:8001/api/scheduler/module" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "module_task_001",
    "module_id": 1,
    "environment_id": 1,
    "schedule_time": "2024-03-21T02:00:00",
    "executor": "scheduler"
  }'
```

### 2.3 调度重复执行任务

```bash
# 每30分钟执行一次模块测试
curl -X POST "http://localhost:8001/api/scheduler/recurring" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "recurring_001",
    "task_type": "module",
    "target_id": 1,
    "environment_id": 1,
    "interval_minutes": 30,
    "executor": "scheduler"
  }'

# 每小时执行一次全量测试
curl -X POST "http://localhost:8001/api/scheduler/recurring" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "recurring_002",
    "task_type": "all",
    "target_id": 1,
    "environment_id": 1,
    "interval_minutes": 60,
    "executor": "scheduler"
  }'
```

### 2.4 管理定时任务

```bash
# 查看所有定时任务
curl -X GET "http://localhost:8001/api/scheduler/tasks"

# 查看特定任务状态
curl -X GET "http://localhost:8001/api/scheduler/tasks/task_001"

# 取消定时任务
curl -X DELETE "http://localhost:8001/api/scheduler/task_001"
```

## 3. Webhook触发

### 3.1 通用Webhook触发

```bash
# 生成签名（Python示例）
import hashlib
import hmac
import json

payload = json.dumps({
    "execution_type": "single",
    "target_id": 1,
    "environment_id": 1,
    "executor": "webhook"
})

secret = "your-webhook-secret-key"
signature = hmac.new(
    secret.encode('utf-8'),
    payload.encode('utf-8'),
    hashlib.sha256
).hexdigest()

# 发送Webhook请求
curl -X POST "http://localhost:8001/api/webhook/trigger" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=${signature}" \
  -H "X-Webhook-Secret: default" \
  -d '{
    "execution_type": "single",
    "target_id": 1,
    "environment_id": 1,
    "executor": "webhook"
  }'
```

### 3.2 CI/CD专用Webhook

```bash
curl -X POST "http://localhost:8001/api/webhook/ci-cd" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=${signature}" \
  -d '{
    "execution_type": "module",
    "target_id": 1,
    "environment_id": 1,
    "executor": "ci-cd"
  }'
```

### 3.3 监控系统专用Webhook

```bash
curl -X POST "http://localhost:8001/api/webhook/monitoring" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=${signature}" \
  -d '{
    "execution_type": "single",
    "target_id": 1,
    "environment_id": 1,
    "executor": "monitoring"
  }'
```

### 3.4 获取Webhook配置

```bash
curl -X GET "http://localhost:8001/api/webhook/config"
```

## 4. 实际应用场景

### 4.1 开发阶段

```bash
# 开发过程中快速验证单个接口
curl -X POST "http://localhost:8001/api/trigger/quick-test?test_case_id=1&environment_id=1"

# 功能开发完成后执行模块测试
curl -X POST "http://localhost:8001/api/trigger/module" \
  -H "Content-Type: application/json" \
  -d '{
    "module_id": 1,
    "environment_id": 1,
    "executor": "developer"
  }'
```

### 4.2 CI/CD集成

```yaml
# GitLab CI配置示例
test_stage:
  stage: test
  script:
    - curl -X POST "http://localhost:8001/api/webhook/ci-cd" \
        -H "Content-Type: application/json" \
        -H "X-Webhook-Signature: sha256=${WEBHOOK_SIGNATURE}" \
        -d '{
          "execution_type": "module",
          "target_id": 1,
          "environment_id": 1,
          "executor": "gitlab-ci"
        }'
```

### 4.3 监控告警

```bash
# 系统告警时触发关键测试用例
curl -X POST "http://localhost:8001/api/webhook/monitoring" \
  -H "Content-Type: application/json" \
  -H "X-Webhook-Signature: sha256=${signature}" \
  -d '{
    "execution_type": "single",
    "target_id": 1,
    "environment_id": 1,
    "executor": "alert-system"
  }'
```

### 4.4 定期回归测试

```bash
# 每天凌晨2点执行全量回归测试
curl -X POST "http://localhost:8001/api/scheduler/recurring" \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "daily_regression",
    "task_type": "all",
    "target_id": 1,
    "environment_id": 1,
    "interval_minutes": 1440,
    "executor": "daily-scheduler"
  }'
```

## 5. 响应格式

### 5.1 成功响应

```json
{
  "message": "单个测试用例执行已触发",
  "execution_type": "single",
  "test_case_id": 1,
  "environment_id": 1
}
```

### 5.2 执行状态响应

```json
{
  "execution_id": 123,
  "name": "执行测试用例: 用户登录",
  "status": "running",
  "progress": {
    "current": 1,
    "total": 1
  },
  "created_at": "2024-03-21T10:00:00",
  "updated_at": "2024-03-21T10:00:05",
  "statistics": {
    "total": 1,
    "success": 1,
    "failed": 0,
    "success_rate": 100.0
  }
}
```

### 5.3 错误响应

```json
{
  "detail": "测试用例不存在"
}
```

## 6. 最佳实践

1. **选择合适的触发方式**：
   - 开发调试：使用快速测试
   - 功能验证：使用手动触发
   - 自动化流程：使用Webhook
   - 定期执行：使用定时任务

2. **环境管理**：
   - 开发环境：用于日常开发和调试
   - 测试环境：用于功能验证和回归测试
   - 生产环境：用于生产前验证

3. **执行策略**：
   - 单个测试用例：快速验证和调试
   - 模块测试：功能完整性验证
   - 全量测试：发布前质量保证

4. **监控和告警**：
   - 实时监控执行状态
   - 失败时及时告警
   - 定期生成执行报告

5. **安全考虑**：
   - Webhook使用签名验证
   - 限制执行权限
   - 记录执行日志 