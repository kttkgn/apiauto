from datetime import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.scheduler import SchedulerService
from app.schemas.scheduler import (
    ScheduleSingleCase,
    ScheduleModule,
    ScheduleRecurring,
    ScheduleResponse,
    TaskStatus
)

router = APIRouter()


@router.post("/single", response_model=ScheduleResponse)
async def schedule_single_case(
    schedule: ScheduleSingleCase,
    db: AsyncSession = Depends(get_db),
):
    """
    调度单个测试用例的定时执行
    
    适用于：
    1. 在特定时间执行某个测试用例
    2. 非工作时间执行测试
    3. 定时验证关键功能
    """
    scheduler = SchedulerService(db)
    
    # 解析调度时间
    try:
        schedule_time = datetime.fromisoformat(schedule.schedule_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="调度时间格式错误，请使用ISO格式")
    
    result = await scheduler.schedule_single_case(
        task_id=schedule.task_id,
        test_case_id=schedule.test_case_id,
        environment_id=schedule.environment_id,
        schedule_time=schedule_time,
        executor=schedule.executor or "scheduler"
    )
    
    return ScheduleResponse(**result)


@router.post("/module", response_model=ScheduleResponse)
async def schedule_module(
    schedule: ScheduleModule,
    db: AsyncSession = Depends(get_db),
):
    """
    调度模块的定时执行
    
    适用于：
    1. 定时执行整个功能模块的测试
    2. 定期回归测试
    3. 模块级别的质量监控
    """
    scheduler = SchedulerService(db)
    
    # 解析调度时间
    try:
        schedule_time = datetime.fromisoformat(schedule.schedule_time)
    except ValueError:
        raise HTTPException(status_code=400, detail="调度时间格式错误，请使用ISO格式")
    
    result = await scheduler.schedule_module(
        task_id=schedule.task_id,
        module_id=schedule.module_id,
        environment_id=schedule.environment_id,
        schedule_time=schedule_time,
        executor=schedule.executor or "scheduler"
    )
    
    return ScheduleResponse(**result)


@router.post("/recurring", response_model=ScheduleResponse)
async def schedule_recurring_task(
    schedule: ScheduleRecurring,
    db: AsyncSession = Depends(get_db),
):
    """
    调度重复执行任务
    
    适用于：
    1. 定期监控接口状态
    2. 持续集成测试
    3. 自动化质量保证
    """
    scheduler = SchedulerService(db)
    
    result = await scheduler.schedule_recurring_task(
        task_id=schedule.task_id,
        task_type=schedule.task_type,
        target_id=schedule.target_id,
        environment_id=schedule.environment_id,
        interval_minutes=schedule.interval_minutes,
        executor=schedule.executor or "scheduler"
    )
    
    return ScheduleResponse(**result)


@router.delete("/{task_id}", response_model=ScheduleResponse)
async def cancel_scheduled_task(
    task_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    取消定时任务
    
    用于：
    1. 停止不需要的定时任务
    2. 管理任务生命周期
    3. 资源清理
    """
    scheduler = SchedulerService(db)
    
    result = await scheduler.cancel_task(task_id)
    
    return ScheduleResponse(**result)


@router.get("/tasks", response_model=List[TaskStatus])
async def get_scheduled_tasks(
    db: AsyncSession = Depends(get_db),
):
    """
    获取所有已调度的任务
    
    用于：
    1. 查看当前所有定时任务
    2. 监控任务状态
    3. 任务管理
    """
    scheduler = SchedulerService(db)
    
    tasks = await scheduler.get_scheduled_tasks()
    
    return [TaskStatus(**task) for task in tasks]


@router.get("/tasks/{task_id}", response_model=TaskStatus)
async def get_task_status(
    task_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    获取特定任务的状态
    
    用于：
    1. 查看特定任务的详细信息
    2. 任务状态监控
    3. 调试和问题排查
    """
    scheduler = SchedulerService(db)
    
    tasks = await scheduler.get_scheduled_tasks()
    
    for task in tasks:
        if task["task_id"] == task_id:
            return TaskStatus(**task)
    
    raise HTTPException(status_code=404, detail="任务不存在") 