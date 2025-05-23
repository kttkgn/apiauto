# 后端详细设计文档

## 1. 数据库设计

### 1.1 环境配置表 (environments)
```sql
CREATE TABLE environments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '环境名称',
    base_url VARCHAR(255) NOT NULL COMMENT '基础URL',
    headers JSON COMMENT '公共请求头',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='环境配置表';
```

### 1.2 环境变量表 (environment_variables)
```sql
CREATE TABLE environment_variables (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    environment_id BIGINT NOT NULL COMMENT '环境ID',
    name VARCHAR(100) NOT NULL COMMENT '变量名',
    value TEXT NOT NULL COMMENT '变量值',
    description VARCHAR(255) COMMENT '描述',
    extractor JSON COMMENT '提取器配置',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_env_name (environment_id, name),
    FOREIGN KEY (environment_id) REFERENCES environments(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='环境变量表';
```

### 1.3 模块表 (modules)
```sql
CREATE TABLE modules (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '模块名称',
    description TEXT COMMENT '模块描述',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模块表';
```

### 1.4 模块变量表 (module_variables)
```sql
CREATE TABLE module_variables (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    module_id BIGINT NOT NULL COMMENT '模块ID',
    name VARCHAR(100) NOT NULL COMMENT '变量名',
    value TEXT NOT NULL COMMENT '变量值',
    description VARCHAR(255) COMMENT '描述',
    extractor JSON COMMENT '提取器配置',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_module_name (module_id, name),
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='模块变量表';
```

### 1.5 测试用例表 (test_cases)
```sql
CREATE TABLE test_cases (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    module_id BIGINT NOT NULL COMMENT '所属模块ID',
    name VARCHAR(100) NOT NULL COMMENT '用例名称',
    description TEXT COMMENT '用例描述',
    method VARCHAR(10) NOT NULL COMMENT '请求方法',
    path VARCHAR(255) NOT NULL COMMENT '请求路径',
    headers JSON COMMENT '请求头',
    params JSON COMMENT '请求参数',
    body JSON COMMENT '请求体',
    assertions JSON COMMENT '断言配置',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试用例表';
```

### 1.6 执行记录表 (executions)
```sql
CREATE TABLE executions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '执行名称',
    scope ENUM('single', 'module', 'all') NOT NULL COMMENT '执行范围',
    case_id BIGINT COMMENT '测试用例ID',
    module_id BIGINT COMMENT '模块ID',
    environment_id BIGINT NOT NULL COMMENT '环境ID',
    executor VARCHAR(100) NOT NULL COMMENT '执行人',
    params JSON COMMENT '执行参数',
    status ENUM('pending', 'running', 'success', 'failed') NOT NULL COMMENT '执行状态',
    progress INT NOT NULL DEFAULT 0 COMMENT '执行进度(0-100)',
    result JSON COMMENT '执行结果',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES test_cases(id) ON DELETE SET NULL,
    FOREIGN KEY (module_id) REFERENCES modules(id) ON DELETE SET NULL,
    FOREIGN KEY (environment_id) REFERENCES environments(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='执行记录表';
```

### 1.7 测试报告表 (reports)
```sql
CREATE TABLE reports (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '报告名称',
    execution_id BIGINT NOT NULL COMMENT '执行记录ID',
    content JSON NOT NULL COMMENT '报告内容',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='测试报告表';
```

### 1.8 执行日志表 (execution_logs)
```sql
CREATE TABLE execution_logs (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    execution_id BIGINT NOT NULL COMMENT '执行记录ID',
    level ENUM('info', 'warn', 'error') NOT NULL COMMENT '日志级别',
    message TEXT NOT NULL COMMENT '日志内容',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='执行日志表';
```

### 1.9 执行详情表 (execution_details)
```sql
CREATE TABLE execution_details (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    execution_id BIGINT NOT NULL COMMENT '执行记录ID',
    case_id BIGINT NOT NULL COMMENT '测试用例ID',
    status ENUM('success', 'failed') NOT NULL COMMENT '执行状态',
    request JSON NOT NULL COMMENT '请求详情',
    response JSON NOT NULL COMMENT '响应详情',
    assertions JSON NOT NULL COMMENT '断言结果',
    duration INT NOT NULL COMMENT '执行时长(ms)',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (execution_id) REFERENCES executions(id) ON DELETE CASCADE,
    FOREIGN KEY (case_id) REFERENCES test_cases(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='执行详情表';
```

## 2. 接口设计

### 2.1 环境管理接口

#### 2.1.1 获取环境列表
- 请求方式：GET
- 接口路径：/api/environments
- 请求参数：
  - name: string (可选) - 环境名称搜索
  - page: number (可选) - 页码，默认1
  - size: number (可选) - 每页数量，默认10
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "items": [{
      "id": 1,
      "name": "开发环境",
      "base_url": "http://dev-api.example.com",
      "variables_count": 5,
      "created_at": "2024-03-20 10:00:00"
    }]
  }
}
```

#### 2.1.2 获取环境详情
- 请求方式：GET
- 接口路径：/api/environments/:id
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "开发环境",
    "base_url": "http://dev-api.example.com",
    "variables": [{
      "id": 1,
      "name": "token",
      "value": "${token}",
      "description": "认证令牌",
      "extractor": {
        "source": "response_body",
        "method": "jsonpath",
        "expression": "$.data.token"
      }
    }]
  }
}
```

#### 2.1.3 创建环境
- 请求方式：POST
- 接口路径：/api/environments
- 请求数据：
```json
{
  "name": "开发环境",
  "base_url": "http://dev-api.example.com",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer ${token}"
  },
  "variables": [{
    "name": "token",
    "value": "${token}",
    "description": "认证令牌",
    "extractor": {
      "source": "response_body",
      "method": "jsonpath",
      "expression": "$.data.token"
    }
  }]
}
```

#### 2.1.4 更新环境
- 请求方式：PUT
- 接口路径：/api/environments/:id
- 请求数据：同创建环境
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "开发环境",
    "base_url": "http://dev-api.example.com",
    "headers": {
      "Content-Type": "application/json",
      "Authorization": "Bearer ${token}"
    },
    "variables": [{
      "id": 1,
      "name": "token",
      "value": "${token}",
      "description": "认证令牌",
      "extractor": {
        "source": "response_body",
        "method": "jsonpath",
        "expression": "$.data.token"
      }
    }]
  }
}
```

#### 2.1.5 删除环境
- 请求方式：DELETE
- 接口路径：/api/environments/:id

#### 2.1.6 复制环境
- 请求方式：POST
- 接口路径：/api/environments/:id/copy
- 请求数据：
```json
{
  "name": "新环境名称"
}
```

#### 2.1.7 测试变量提取器
- 请求方式：POST
- 接口路径：/api/environments/variables/test
- 请求数据：
```json
{
  "source": "response_body",
  "method": "jsonpath",
  "expression": "$.data.token",
  "response": {
    "data": {
      "token": "abc123"
    }
  }
}
```
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "value": "abc123"
  }
}
```

### 2.2 模块管理接口

#### 2.2.1 获取模块列表
- 请求方式：GET
- 接口路径：/api/modules
- 请求参数：
  - name: string (可选) - 模块名称搜索
  - page: number (可选) - 页码，默认1
  - size: number (可选) - 每页数量，默认10
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "items": [{
      "id": 1,
      "name": "用户模块",
      "description": "用户相关的接口测试用例",
      "case_count": 10,
      "created_at": "2024-03-20 10:00:00"
    }]
  }
}
```

#### 2.2.2 获取模块详情
- 请求方式：GET
- 接口路径：/api/modules/:id
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "用户模块",
    "description": "用户相关的接口测试用例",
    "variables": [{
      "id": 1,
      "name": "user_id",
      "value": "${user_id}",
      "description": "用户ID",
      "extractor": {
        "source": "response_body",
        "method": "jsonpath",
        "expression": "$.data.id"
      }
    }]
  }
}
```

#### 2.2.3 创建模块
- 请求方式：POST
- 接口路径：/api/modules
- 请求数据：
```json
{
  "name": "用户模块",
  "description": "用户相关的接口测试用例",
  "variables": [{
    "name": "user_id",
    "value": "${user_id}",
    "description": "用户ID",
    "extractor": {
      "source": "response_body",
      "method": "jsonpath",
      "expression": "$.data.id"
    }
  }]
}
```
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "用户模块",
    "description": "用户相关的接口测试用例",
    "variables": [{
      "id": 1,
      "name": "user_id",
      "value": "${user_id}",
      "description": "用户ID",
      "extractor": {
        "source": "response_body",
        "method": "jsonpath",
        "expression": "$.data.id"
      }
    }]
  }
}
```

#### 2.2.4 更新模块
- 请求方式：PUT
- 接口路径：/api/modules/:id
- 请求数据：同创建模块

#### 2.2.5 删除模块
- 请求方式：DELETE
- 接口路径：/api/modules/:id

#### 2.2.6 测试变量提取器
- 请求方式：POST
- 接口路径：/api/modules/variables/test
- 请求数据：
```json
{
  "source": "response_body",
  "method": "jsonpath",
  "expression": "$.data.id",
  "response": {
    "data": {
      "id": 123
    }
  }
}
```
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "value": "123"
  }
}
```

### 2.3 执行管理接口

#### 2.3.1 获取执行列表
- 请求方式：GET
- 接口路径：/api/executions
- 请求参数：
  - name: string (可选) - 执行名称搜索
  - status: string (可选) - 执行状态
  - page: number (可选) - 页码，默认1
  - size: number (可选) - 每页数量，默认10
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "items": [{
      "id": 1,
      "name": "用户模块测试",
      "scope": "module",
      "module_id": 1,
      "environment_id": 1,
      "status": "success",
      "created_at": "2024-03-20 10:00:00"
    }]
  }
}
```

#### 2.3.2 获取执行详情
- 请求方式：GET
- 接口路径：/api/executions/:id
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "用户模块测试",
    "scope": "module",
    "module_id": 1,
    "environment_id": 1,
    "executor": "admin",
    "params": {
      "key": "value"
    },
    "status": "success",
    "progress": 100,
    "result": {
      "total": 10,
      "passed": 8,
      "failed": 2,
      "duration": 5000,
      "cases": [{
        "id": 1,
        "name": "登录接口",
        "status": "success",
        "request": {
          "url": "/api/login",
          "method": "POST",
          "headers": {
            "Content-Type": "application/json"
          },
          "body": {
            "username": "test",
            "password": "123456"
          }
        },
        "response": {
          "status_code": 200,
          "headers": {
            "Content-Type": "application/json"
          },
          "body": {
            "code": 0,
            "data": {
              "token": "abc123"
            }
          }
        },
        "assertions": [{
          "name": "状态码",
          "expected": 200,
          "actual": 200,
          "result": true
        }],
        "duration": 500
      }]
    },
    "logs": [{
      "level": "info",
      "message": "开始执行测试用例",
      "created_at": "2024-03-20 10:00:00"
    }],
    "details": [{
      "id": 1,
      "case_id": 1,
      "status": "success",
      "request": {
        "url": "/api/login",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "username": "test",
          "password": "123456"
        }
      },
      "response": {
        "status_code": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "code": 0,
          "data": {
            "token": "abc123"
          }
        }
      },
      "assertions": [{
        "name": "状态码",
        "expected": 200,
        "actual": 200,
        "result": true
      }],
      "duration": 500
    }]
  }
}
```

#### 2.3.3 创建执行
- 请求方式：POST
- 接口路径：/api/executions
- 请求数据：
```json
{
  "name": "用户模块测试",
  "scope": "module",
  "module_id": 1,
  "environment_id": 1,
  "params": {
    "key": "value"
  }
}
```

#### 2.3.4 取消执行
- 请求方式：POST
- 接口路径：/api/executions/:id/cancel

#### 2.3.5 获取执行日志
- 请求方式：GET
- 接口路径：/api/executions/:id/logs
- 请求参数：
  - level: string (可选) - 日志级别
  - page: number (可选) - 页码，默认1
  - size: number (可选) - 每页数量，默认10
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "items": [{
      "id": 1,
      "level": "info",
      "message": "开始执行测试用例",
      "created_at": "2024-03-20 10:00:00"
    }]
  }
}
```

#### 2.3.6 获取执行详情列表
- 请求方式：GET
- 接口路径：/api/executions/:id/details
- 请求参数：
  - status: string (可选) - 执行状态
  - page: number (可选) - 页码，默认1
  - size: number (可选) - 每页数量，默认10
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "items": [{
      "id": 1,
      "case_id": 1,
      "status": "success",
      "request": {
        "url": "/api/login",
        "method": "POST",
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "username": "test",
          "password": "123456"
        }
      },
      "response": {
        "status_code": 200,
        "headers": {
          "Content-Type": "application/json"
        },
        "body": {
          "code": 0,
          "data": {
            "token": "abc123"
          }
        }
      },
      "assertions": [{
        "name": "状态码",
        "expected": 200,
        "actual": 200,
        "result": true
      }],
      "duration": 500
    }]
  }
}
```

### 2.4 测试报告接口

#### 2.4.1 获取报告列表
- 请求方式：GET
- 接口路径：/api/reports
- 请求参数：
  - name: string (可选) - 报告名称搜索
  - page: number (可选) - 页码，默认1
  - size: number (可选) - 每页数量，默认10
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "items": [{
      "id": 1,
      "name": "用户模块测试报告",
      "execution_id": 1,
      "created_at": "2024-03-20 10:00:00"
    }]
  }
}
```

#### 2.4.2 获取报告详情
- 请求方式：GET
- 接口路径：/api/reports/:id
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "name": "用户模块测试报告",
    "execution_id": 1,
    "content": {
      "summary": {
        "total": 10,
        "passed": 8,
        "failed": 2,
        "duration": 5000,
        "start_time": "2024-03-20 10:00:00",
        "end_time": "2024-03-20 10:00:05"
      },
      "cases": [{
        "id": 1,
        "name": "登录接口",
        "status": "success",
        "request": {
          "url": "/api/login",
          "method": "POST",
          "headers": {
            "Content-Type": "application/json"
          },
          "body": {
            "username": "test",
            "password": "123456"
          }
        },
        "response": {
          "status_code": 200,
          "headers": {
            "Content-Type": "application/json"
          },
          "body": {
            "code": 0,
            "data": {
              "token": "abc123"
            }
          }
        },
        "assertions": [{
          "name": "状态码",
          "expected": 200,
          "actual": 200,
          "result": true
        }],
        "duration": 500,
        "logs": [{
          "level": "info",
          "message": "开始执行测试用例",
          "created_at": "2024-03-20 10:00:00"
        }]
      }]
    }
  }
}
```

#### 2.4.3 下载报告
- 请求方式：GET
- 接口路径：/api/reports/:id/download
- 响应类型：application/pdf 或 application/zip

#### 2.4.4 删除报告
- 请求方式：DELETE
- 接口路径：/api/reports/:id

#### 2.4.5 获取报告统计信息
- 请求方式：GET
- 接口路径：/api/reports/statistics
- 请求参数：
  - start_time: string (可选) - 开始时间
  - end_time: string (可选) - 结束时间
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "success_rate": 80,
    "avg_duration": 5000,
    "trend": [{
      "date": "2024-03-20",
      "total": 10,
      "passed": 8,
      "failed": 2
    }]
  }
}
```

### 2.5 首页接口

#### 2.5.1 获取仪表盘数据
- 请求方式：GET
- 接口路径：/api/dashboard
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "statistics": {
      "total_cases": 100,
      "total_modules": 10,
      "total_environments": 5,
      "total_executions": 50,
      "success_rate": 85
    },
    "recent_executions": [{
      "id": 1,
      "name": "用户模块测试",
      "scope": "module",
      "module_id": 1,
      "environment_id": 1,
      "status": "success",
      "progress": 100,
      "created_at": "2024-03-20 10:00:00"
    }],
    "recent_reports": [{
      "id": 1,
      "name": "用户模块测试报告",
      "execution_id": 1,
      "created_at": "2024-03-20 10:00:00"
    }],
    "trend": {
      "dates": ["2024-03-14", "2024-03-15", "2024-03-16", "2024-03-17", "2024-03-18", "2024-03-19", "2024-03-20"],
      "executions": [10, 15, 8, 12, 20, 18, 25],
      "success_rates": [90, 85, 88, 92, 87, 90, 95]
    }
  }
}
```

#### 2.5.2 获取快速执行数据
- 请求方式：GET
- 接口路径：/api/dashboard/quick-execute
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "modules": [{
      "id": 1,
      "name": "用户模块",
      "case_count": 10
    }],
    "environments": [{
      "id": 1,
      "name": "开发环境",
      "base_url": "http://dev-api.example.com"
    }]
  }
}
```

#### 2.5.3 获取系统状态
- 请求方式：GET
- 接口路径：/api/dashboard/system-status
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "cpu_usage": 45.5,
    "memory_usage": 60.2,
    "disk_usage": 75.8,
    "running_executions": 2,
    "pending_executions": 5,
    "last_execution_time": "2024-03-20 10:00:00"
  }
}
```

#### 2.5.4 获取通知列表
- 请求方式：GET
- 接口路径：/api/dashboard/notifications
- 请求参数：
  - page: number (可选) - 页码，默认1
  - size: number (可选) - 每页数量，默认10
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 100,
    "items": [{
      "id": 1,
      "type": "execution_complete",
      "title": "执行完成通知",
      "content": "用户模块测试执行完成，成功率：80%",
      "is_read": false,
      "created_at": "2024-03-20 10:00:00"
    }]
  }
}
```

#### 2.5.5 标记通知为已读
- 请求方式：PUT
- 接口路径：/api/dashboard/notifications/:id/read
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "id": 1,
    "is_read": true
  }
}
```

#### 2.5.6 获取待办事项
- 请求方式：GET
- 接口路径：/api/dashboard/todos
- 响应数据：
```json
{
  "code": 0,
  "data": {
    "total": 5,
    "items": [{
      "id": 1,
      "type": "failed_case",
      "title": "失败的测试用例",
      "content": "登录接口测试失败，请检查",
      "priority": "high",
      "created_at": "2024-03-20 10:00:00"
    }]
  }
}
```

## 3. 第三方组件/模块包设计

### 3.1 核心依赖
```json
{
  "dependencies": {
    "express": "^4.18.2",           // Web框架
    "mysql2": "^3.6.0",            // MySQL数据库驱动
    "sequelize": "^6.32.1",        // ORM框架
    "axios": "^1.4.0",             // HTTP客户端
    "jsonpath": "^1.1.1",          // JSONPath解析
    "joi": "^17.9.2",              // 数据验证
    "winston": "^3.10.0",          // 日志管理
    "jsonwebtoken": "^9.0.0",      // JWT认证
    "bcryptjs": "^2.4.3",          // 密码加密
    "cors": "^2.8.5",              // 跨域处理
    "helmet": "^7.0.0",            // 安全中间件
    "compression": "^1.7.4",       // 响应压缩
    "multer": "^1.4.5-lts.1",      // 文件上传
    "node-cron": "^3.0.2",         // 定时任务
    "nodemailer": "^6.9.3",        // 邮件发送
    "pdfkit": "^0.13.0",           // PDF生成
    "archiver": "^5.3.1"           // ZIP压缩
  }
}
```

### 3.2 开发依赖
```json
{
  "devDependencies": {
    "typescript": "^5.1.3",        // TypeScript支持
    "ts-node": "^10.9.1",          // TypeScript运行时
    "jest": "^29.5.0",             // 单元测试
    "supertest": "^6.3.3",         // API测试
    "eslint": "^8.42.0",           // 代码检查
    "prettier": "^2.8.8",          // 代码格式化
    "nodemon": "^2.0.22",          // 开发热重载
    "@types/node": "^20.2.5",      // Node.js类型定义
    "@types/express": "^4.17.17",  // Express类型定义
    "@types/jest": "^29.5.1"       // Jest类型定义
  }
}
```

### 3.3 项目结构
```
backend/
├── src/
│   ├── config/                 # 配置文件
│   ├── controllers/           # 控制器
│   ├── models/               # 数据模型
│   ├── services/            # 业务逻辑
│   ├── middlewares/        # 中间件
│   ├── utils/             # 工具函数
│   ├── routes/           # 路由定义
│   ├── types/           # 类型定义
│   └── app.ts          # 应用入口
├── tests/              # 测试文件
├── logs/              # 日志文件
├── package.json      # 项目配置
└── tsconfig.json    # TypeScript配置
```

### 3.4 主要功能模块

#### 3.4.1 变量提取器模块
- 支持JSONPath和正则表达式两种提取方式
- 支持响应头和响应体两种数据来源
- 提供提取规则测试功能

#### 3.4.2 测试执行引擎
- 支持HTTP请求发送
- 支持变量替换和提取
- 支持断言验证
- 支持并发执行
- 支持执行超时控制

#### 3.4.3 报告生成器
- 支持HTML格式报告
- 支持PDF格式报告
- 支持ZIP打包下载
- 支持报告模板定制

#### 3.4.4 邮件通知
- 支持执行完成通知
- 支持失败用例通知
- 支持自定义通知模板

#### 3.4.5 定时任务
- 支持定时执行测试
- 支持执行结果通知
- 支持任务调度管理 