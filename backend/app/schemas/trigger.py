from typing import Optional
from pydantic import BaseModel, Field


class SingleCaseTrigger(BaseModel):
    """单个测试用例触发模型"""
    test_case_id: int = Field(..., description="测试用例ID")
    environment_id: int = Field(..., description="环境ID")
    executor: Optional[str] = Field("manual", description="执行人")


class ModuleTrigger(BaseModel):
    """模块测试触发模型"""
    module_id: int = Field(..., description="模块ID")
    environment_id: int = Field(..., description="环境ID")
    executor: Optional[str] = Field("manual", description="执行人")


class AllCasesTrigger(BaseModel):
    """全量测试触发模型"""
    environment_id: int = Field(..., description="环境ID")
    executor: Optional[str] = Field("manual", description="执行人")


class TriggerResponse(BaseModel):
    """触发响应模型"""
    message: str = Field(..., description="响应消息")
    execution_type: str = Field(..., description="执行类型")
    environment_id: int = Field(..., description="环境ID")
    test_case_id: Optional[int] = Field(None, description="测试用例ID")
    module_id: Optional[int] = Field(None, description="模块ID")


class ExecutionStatus(BaseModel):
    """执行状态模型"""
    execution_id: int = Field(..., description="执行ID")
    name: str = Field(..., description="执行名称")
    status: str = Field(..., description="执行状态")
    progress: dict = Field(..., description="执行进度")
    created_at: str = Field(..., description="创建时间")
    updated_at: str = Field(..., description="更新时间")
    statistics: dict = Field(..., description="统计信息") 