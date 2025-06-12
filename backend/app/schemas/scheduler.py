from typing import Optional
from pydantic import BaseModel, Field


class ScheduleSingleCase(BaseModel):
    """调度单个测试用例模型"""
    task_id: str = Field(..., description="任务ID")
    test_case_id: int = Field(..., description="测试用例ID")
    environment_id: int = Field(..., description="环境ID")
    schedule_time: str = Field(..., description="调度时间(ISO格式)")
    executor: Optional[str] = Field("scheduler", description="执行人")


class ScheduleModule(BaseModel):
    """调度模块模型"""
    task_id: str = Field(..., description="任务ID")
    module_id: int = Field(..., description="模块ID")
    environment_id: int = Field(..., description="环境ID")
    schedule_time: str = Field(..., description="调度时间(ISO格式)")
    executor: Optional[str] = Field("scheduler", description="执行人")


class ScheduleRecurring(BaseModel):
    """调度重复任务模型"""
    task_id: str = Field(..., description="任务ID")
    task_type: str = Field(..., description="任务类型(single/module/all)")
    target_id: int = Field(..., description="目标ID(测试用例ID/模块ID/环境ID)")
    environment_id: int = Field(..., description="环境ID")
    interval_minutes: int = Field(..., ge=1, description="重复间隔(分钟)")
    executor: Optional[str] = Field("scheduler", description="执行人")


class ScheduleResponse(BaseModel):
    """调度响应模型"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    test_case_id: Optional[int] = Field(None, description="测试用例ID")
    module_id: Optional[int] = Field(None, description="模块ID")
    environment_id: Optional[int] = Field(None, description="环境ID")
    schedule_time: Optional[str] = Field(None, description="调度时间")
    task_type: Optional[str] = Field(None, description="任务类型")
    target_id: Optional[int] = Field(None, description="目标ID")
    interval_minutes: Optional[int] = Field(None, description="重复间隔")


class TaskStatus(BaseModel):
    """任务状态模型"""
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    cancelled: bool = Field(..., description="是否已取消") 