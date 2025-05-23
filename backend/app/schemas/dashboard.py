from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class TestCaseStats(BaseModel):
    """测试用例统计"""
    total_count: int = Field(0, description="总用例数")
    today_new: int = Field(0, description="今日新增")


class ExecutionStats(BaseModel):
    """执行统计"""
    total_count: int = Field(0, description="总执行次数")
    today_count: int = Field(0, description="今日执行次数")


class SuccessRateStats(BaseModel):
    """成功率统计"""
    total_rate: float = Field(0, description="总成功率")
    today_rate: float = Field(0, description="今日成功率")


class DashboardStats(BaseModel):
    """首页统计数据"""
    test_cases: TestCaseStats = Field(..., description="测试用例统计")
    executions: ExecutionStats = Field(..., description="执行统计")
    success_rates: SuccessRateStats = Field(..., description="成功率统计") 