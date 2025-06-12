from typing import List, Optional, Dict
from pydantic import BaseModel, Field


class WebhookTrigger(BaseModel):
    """Webhook触发模型"""
    execution_type: str = Field(..., description="执行类型(single/module/all)")
    target_id: int = Field(..., description="目标ID(测试用例ID/模块ID/环境ID)")
    environment_id: int = Field(..., description="环境ID")
    executor: Optional[str] = Field("webhook", description="执行人")


class WebhookResponse(BaseModel):
    """Webhook响应模型"""
    success: bool = Field(..., description="是否成功")
    execution_id: Optional[int] = Field(None, description="执行ID")
    message: str = Field(..., description="响应消息")
    error: Optional[str] = Field(None, description="错误信息")
    execution_type: str = Field(..., description="执行类型")


class WebhookEndpoint(BaseModel):
    """Webhook端点模型"""
    url: str = Field(..., description="端点URL")
    description: str = Field(..., description="端点描述")
    methods: List[str] = Field(..., description="支持的HTTP方法")
    auth: str = Field(..., description="认证方式")


class WebhookConfig(BaseModel):
    """Webhook配置模型"""
    endpoints: List[WebhookEndpoint] = Field(..., description="可用端点列表")
    signature_header: str = Field(..., description="签名头字段名")
    secret_header: str = Field(..., description="密钥头字段名")
    supported_secrets: List[str] = Field(..., description="支持的密钥类型") 