import hashlib
import hmac
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Header, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.executor import TestExecutor
from app.schemas.webhook import (
    WebhookTrigger,
    WebhookResponse,
    WebhookConfig
)

router = APIRouter()

# 简单的Webhook密钥管理（实际项目中应该存储在数据库中）
WEBHOOK_SECRETS = {
    "default": "your-webhook-secret-key",
    "ci-cd": "ci-cd-webhook-secret",
    "monitoring": "monitoring-webhook-secret"
}


def verify_webhook_signature(payload: str, signature: str, secret: str) -> bool:
    """验证Webhook签名"""
    expected_signature = hmac.new(
        secret.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected_signature}", signature)


@router.post("/trigger", response_model=WebhookResponse)
async def webhook_trigger(
    request: Request,
    trigger: WebhookTrigger,
    x_webhook_signature: Optional[str] = Header(None),
    x_webhook_secret: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """
    Webhook触发接口自动化执行
    
    适用于：
    1. CI/CD流水线集成
    2. 监控系统告警触发
    3. 外部系统集成
    4. 自动化工作流
    """
    # 验证Webhook签名
    if x_webhook_signature:
        body = await request.body()
        payload = body.decode('utf-8')
        
        # 获取密钥
        secret_key = x_webhook_secret or "default"
        secret = WEBHOOK_SECRETS.get(secret_key)
        
        if not secret:
            raise HTTPException(status_code=401, detail="无效的Webhook密钥")
        
        if not verify_webhook_signature(payload, x_webhook_signature, secret):
            raise HTTPException(status_code=401, detail="Webhook签名验证失败")
    
    executor = TestExecutor(db)
    
    try:
        if trigger.execution_type == "single":
            execution = await executor.execute_single_case(
                test_case_id=trigger.target_id,
                environment_id=trigger.environment_id,
                executor=trigger.executor or "webhook"
            )
        elif trigger.execution_type == "module":
            execution = await executor.execute_module(
                module_id=trigger.target_id,
                environment_id=trigger.environment_id,
                executor=trigger.executor or "webhook"
            )
        elif trigger.execution_type == "all":
            execution = await executor.execute_all(
                environment_id=trigger.environment_id,
                executor=trigger.executor or "webhook"
            )
        else:
            raise HTTPException(status_code=400, detail="不支持的执行类型")
        
        return WebhookResponse(
            success=True,
            execution_id=execution.id,
            message=f"Webhook触发成功，执行ID: {execution.id}",
            execution_type=trigger.execution_type
        )
        
    except Exception as e:
        return WebhookResponse(
            success=False,
            error=str(e),
            message="Webhook触发失败",
            execution_type=trigger.execution_type
        )


@router.post("/ci-cd", response_model=WebhookResponse)
async def ci_cd_webhook(
    request: Request,
    trigger: WebhookTrigger,
    x_webhook_signature: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """
    CI/CD专用Webhook
    
    适用于：
    1. Git推送触发测试
    2. 代码合并触发回归测试
    3. 发布前自动化测试
    """
    # 验证CI/CD Webhook签名
    if x_webhook_signature:
        body = await request.body()
        payload = body.decode('utf-8')
        
        secret = WEBHOOK_SECRETS.get("ci-cd")
        if not verify_webhook_signature(payload, x_webhook_signature, secret):
            raise HTTPException(status_code=401, detail="CI/CD Webhook签名验证失败")
    
    executor = TestExecutor(db)
    
    try:
        # CI/CD通常执行全量测试或模块测试
        if trigger.execution_type == "module":
            execution = await executor.execute_module(
                module_id=trigger.target_id,
                environment_id=trigger.environment_id,
                executor="ci-cd"
            )
        elif trigger.execution_type == "all":
            execution = await executor.execute_all(
                environment_id=trigger.environment_id,
                executor="ci-cd"
            )
        else:
            raise HTTPException(status_code=400, detail="CI/CD只支持模块或全量执行")
        
        return WebhookResponse(
            success=True,
            execution_id=execution.id,
            message=f"CI/CD触发成功，执行ID: {execution.id}",
            execution_type=trigger.execution_type
        )
        
    except Exception as e:
        return WebhookResponse(
            success=False,
            error=str(e),
            message="CI/CD触发失败",
            execution_type=trigger.execution_type
        )


@router.post("/monitoring", response_model=WebhookResponse)
async def monitoring_webhook(
    request: Request,
    trigger: WebhookTrigger,
    x_webhook_signature: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    """
    监控系统专用Webhook
    
    适用于：
    1. 系统告警触发测试
    2. 性能监控触发
    3. 健康检查失败触发
    """
    # 验证监控Webhook签名
    if x_webhook_signature:
        body = await request.body()
        payload = body.decode('utf-8')
        
        secret = WEBHOOK_SECRETS.get("monitoring")
        if not verify_webhook_signature(payload, x_webhook_signature, secret):
            raise HTTPException(status_code=401, detail="监控Webhook签名验证失败")
    
    executor = TestExecutor(db)
    
    try:
        # 监控通常执行关键测试用例
        if trigger.execution_type == "single":
            execution = await executor.execute_single_case(
                test_case_id=trigger.target_id,
                environment_id=trigger.environment_id,
                executor="monitoring"
            )
        else:
            raise HTTPException(status_code=400, detail="监控只支持单个测试用例执行")
        
        return WebhookResponse(
            success=True,
            execution_id=execution.id,
            message=f"监控触发成功，执行ID: {execution.id}",
            execution_type=trigger.execution_type
        )
        
    except Exception as e:
        return WebhookResponse(
            success=False,
            error=str(e),
            message="监控触发失败",
            execution_type=trigger.execution_type
        )


@router.get("/config", response_model=WebhookConfig)
async def get_webhook_config():
    """
    获取Webhook配置信息
    
    用于：
    1. 查看可用的Webhook端点
    2. 获取签名验证信息
    3. 配置外部系统集成
    """
    return WebhookConfig(
        endpoints=[
            {
                "url": "/api/webhook/trigger",
                "description": "通用Webhook触发器",
                "methods": ["POST"],
                "auth": "签名验证"
            },
            {
                "url": "/api/webhook/ci-cd",
                "description": "CI/CD专用Webhook",
                "methods": ["POST"],
                "auth": "CI/CD签名验证"
            },
            {
                "url": "/api/webhook/monitoring",
                "description": "监控系统专用Webhook",
                "methods": ["POST"],
                "auth": "监控签名验证"
            }
        ],
        signature_header="X-Webhook-Signature",
        secret_header="X-Webhook-Secret",
        supported_secrets=list(WEBHOOK_SECRETS.keys())
    ) 