from fastapi import APIRouter
from app.api.v1 import (
    environment,
    module,
    execution,
    dashboard,
    test_case,
    report,
    trigger,
    scheduler,
    webhook
)

api_router = APIRouter()

# 环境管理
api_router.include_router(
    environment.router,
    prefix="/environments",
    tags=["环境管理"]
)

# 模块管理
api_router.include_router(
    module.router,
    prefix="/modules",
    tags=["模块管理"]
)

# 执行管理
api_router.include_router(
    execution.router,
    prefix="/executions",
    tags=["执行管理"]
)

# 触发执行
api_router.include_router(
    trigger.router,
    prefix="/trigger",
    tags=["触发执行"]
)

# 定时任务
api_router.include_router(
    scheduler.router,
    prefix="/scheduler",
    tags=["定时任务"]
)

# Webhook
api_router.include_router(
    webhook.router,
    prefix="/webhook",
    tags=["Webhook"]
)

# 仪表盘
api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["仪表盘"]
)

# 测试用例管理
api_router.include_router(
    test_case.router,
    prefix="/test-cases",
    tags=["测试用例管理"]
)

# 报告管理
api_router.include_router(
    report.router,
    prefix="/reports",
    tags=["报告管理"]
) 