from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, validator


class ReportBase(BaseModel):
    """报告基础模型"""
    name: str = Field(..., description="报告名称")
    execution_id: int = Field(..., description="执行ID")
    content: Optional[Dict] = Field(None, description="报告内容")
    total_cases: int = Field(0, description="总用例数")
    passed_cases: int = Field(0, description="通过用例数")
    failed_cases: int = Field(0, description="失败用例数")
    duration: Optional[int] = Field(None, description="执行时长(秒)")

    @validator('execution_id')
    def validate_execution_id(cls, v):
        """验证执行ID字段"""
        if v <= 0:
            raise ValueError('执行ID必须为正整数')
        return v


class ReportCreate(ReportBase):
    """创建报告请求模型"""
    pass


class ReportUpdate(ReportBase):
    """更新报告请求模型"""
    name: Optional[str] = Field(None, description="报告名称")
    content: Optional[Dict] = Field(None, description="报告内容")
    execution_id: Optional[int] = Field(None, description="执行ID")

    @validator('execution_id')
    def validate_execution_id(cls, v):
        """验证执行ID字段"""
        if v is not None and v <= 0:
            raise ValueError('执行ID必须为正整数或None')
        return v


class Report(ReportBase):
    """报告响应模型"""
    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class ReportStatistics(BaseModel):
    """报告统计信息"""
    total: int = Field(..., description="总报告数")
    success_rate: float = Field(..., description="成功率")
    avg_duration: int = Field(..., description="平均执行时长")
    trend: List[Dict] = Field(..., description="趋势数据")


class ReportSummary(BaseModel):
    """报告摘要"""
    total: int = Field(..., description="总用例数")
    passed: int = Field(..., description="通过数")
    failed: int = Field(..., description="失败数")
    duration: int = Field(..., description="执行时长")
    start_time: str = Field(..., description="开始时间")
    end_time: str = Field(..., description="结束时间")


class ReportCase(BaseModel):
    """报告用例详情"""
    id: int = Field(..., description="用例ID")
    name: str = Field(..., description="用例名称")
    status: str = Field(..., description="执行状态")
    request: Dict = Field(..., description="请求详情")
    response: Dict = Field(..., description="响应详情")
    assertions: List[Dict] = Field(..., description="断言结果")
    duration: int = Field(..., description="执行时长")
    logs: List[Dict] = Field(..., description="执行日志") 