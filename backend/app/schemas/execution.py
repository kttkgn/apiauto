from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, validator


class ExecutionBase(BaseModel):
    """执行记录基础模型"""
    name: str = Field(..., description="执行名称")
    scope: str = Field(..., description="执行范围")
    case_id: Optional[int] = Field(None, description="测试用例ID")
    module_id: Optional[int] = Field(None, description="模块ID")
    environment_id: int = Field(..., description="环境ID")
    executor: str = Field(..., description="执行人")
    params: Optional[Dict] = Field(None, description="执行参数")
    status: str = Field(..., description="执行状态")
    progress: Optional[Dict] = Field(None, description="执行进度")
    result: Optional[Dict] = Field(None, description="执行结果")

    @validator('case_id', 'module_id')
    def validate_foreign_key_ids(cls, v):
        """验证外键ID字段"""
        if v is not None and v <= 0:
            raise ValueError('外键ID必须为正整数或None')
        return v

    @validator('environment_id')
    def validate_environment_id(cls, v):
        """验证环境ID字段"""
        if v <= 0:
            raise ValueError('环境ID必须为正整数')
        return v


class ExecutionCreate(ExecutionBase):
    """创建执行记录请求模型"""
    pass


class ExecutionUpdate(ExecutionBase):
    """更新执行记录请求模型"""
    name: Optional[str] = Field(None, description="执行名称")
    scope: Optional[str] = Field(None, description="执行范围")
    case_id: Optional[int] = Field(None, description="测试用例ID")
    module_id: Optional[int] = Field(None, description="模块ID")
    environment_id: Optional[int] = Field(None, description="环境ID")
    executor: Optional[str] = Field(None, description="执行人")
    status: Optional[str] = Field(None, description="执行状态")

    @validator('environment_id')
    def validate_environment_id(cls, v):
        """验证环境ID字段"""
        if v is not None and v <= 0:
            raise ValueError('环境ID必须为正整数或None')
        return v


class Execution(ExecutionBase):
    """执行记录响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


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
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class ExecutionDetailBase(BaseModel):
    """执行详情基础模型"""
    test_case_id: int = Field(..., description="测试用例ID")
    status: str = Field(..., description="执行状态")
    request: Optional[Dict] = Field(None, description="请求详情")
    response: Optional[Dict] = Field(None, description="响应详情")
    assertions: Optional[Dict] = Field(None, description="断言结果")
    duration: Optional[int] = Field(None, description="执行时长(ms)")

    @validator('test_case_id')
    def validate_test_case_id(cls, v):
        """验证测试用例ID字段"""
        if v <= 0:
            raise ValueError('测试用例ID必须为正整数')
        return v


class ExecutionDetailCreate(ExecutionDetailBase):
    """创建执行详情请求模型"""
    pass


class ExecutionDetailUpdate(ExecutionDetailBase):
    """更新执行详情请求模型"""
    test_case_id: Optional[int] = Field(None, description="测试用例ID")
    status: Optional[str] = Field(None, description="执行状态")

    @validator('test_case_id')
    def validate_test_case_id(cls, v):
        """验证测试用例ID字段"""
        if v is not None and v <= 0:
            raise ValueError('测试用例ID必须为正整数或None')
        return v


class ExecutionDetail(ExecutionDetailBase):
    """执行详情响应模型"""
    id: int
    execution_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    ) 