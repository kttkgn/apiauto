from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ExecutionBase(BaseModel):
    """执行记录基础模型"""
    name: str = Field(..., description="执行名称")
    scope: str = Field(..., description="执行范围")
    module_id: Optional[int] = Field(None, description="模块ID")
    environment_id: int = Field(..., description="环境ID")
    executor: str = Field(..., description="执行人")
    params: Optional[Dict] = Field(None, description="执行参数")
    status: str = Field(..., description="执行状态")
    progress: Optional[Dict] = Field(None, description="执行进度")
    result: Optional[Dict] = Field(None, description="执行结果")


class ExecutionCreate(ExecutionBase):
    """创建执行记录请求模型"""
    pass


class ExecutionUpdate(ExecutionBase):
    """更新执行记录请求模型"""
    name: Optional[str] = Field(None, description="执行名称")
    scope: Optional[str] = Field(None, description="执行范围")
    module_id: Optional[int] = Field(None, description="模块ID")
    environment_id: Optional[int] = Field(None, description="环境ID")
    executor: Optional[str] = Field(None, description="执行人")
    status: Optional[str] = Field(None, description="执行状态")


class Execution(ExecutionBase):
    """执行记录响应模型"""
    id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True


class ExecutionLogBase(BaseModel):
    """执行日志基础模型"""
    level: str = Field(..., description="日志级别")
    message: str = Field(..., description="日志消息")


class ExecutionLogCreate(ExecutionLogBase):
    """创建执行日志请求模型"""
    pass


class ExecutionLog(ExecutionLogBase):
    """执行日志响应模型"""
    id: int
    execution_id: int
    created_at: str

    class Config:
        from_attributes = True


class ExecutionDetailBase(BaseModel):
    """执行详情基础模型"""
    test_case_id: int = Field(..., description="测试用例ID")
    status: str = Field(..., description="执行状态")
    request: Optional[Dict] = Field(None, description="请求详情")
    response: Optional[Dict] = Field(None, description="响应详情")
    assertions: Optional[Dict] = Field(None, description="断言结果")
    duration: Optional[int] = Field(None, description="执行时长(ms)")


class ExecutionDetailCreate(ExecutionDetailBase):
    """创建执行详情请求模型"""
    pass


class ExecutionDetailUpdate(ExecutionDetailBase):
    """更新执行详情请求模型"""
    test_case_id: Optional[int] = Field(None, description="测试用例ID")
    status: Optional[str] = Field(None, description="执行状态")


class ExecutionDetail(ExecutionDetailBase):
    """执行详情响应模型"""
    id: int
    execution_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True 