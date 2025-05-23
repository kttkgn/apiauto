from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class ReportBase(BaseModel):
    """报告基础模型"""
    name: str = Field(..., description="报告名称")
    execution_id: int = Field(..., description="执行记录ID")
    content: Dict = Field(..., description="报告内容")


class ReportCreate(ReportBase):
    """创建报告请求模型"""
    pass


class Report(ReportBase):
    """报告响应模型"""
    id: int
    created_at: str

    class Config:
        from_attributes = True


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