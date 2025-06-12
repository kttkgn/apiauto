from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.executor import TestExecutor
from app.schemas.trigger import (
    SingleCaseTrigger,
    ModuleTrigger,
    AllCasesTrigger,
    TriggerResponse
)
from app.schemas.execution import ExecutionCreate, ExecutionUpdate, ExecutionLogCreate

router = APIRouter()


@router.post("/single", response_model=TriggerResponse)
async def trigger_single_case(
    trigger: SingleCaseTrigger,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    触发执行单个测试用例
    
    这是最常用的触发方式，用于：
    1. 开发过程中快速验证单个接口
    2. 调试特定的测试用例
    3. 手动执行某个关键测试
    """
    executor = TestExecutor(db)
    
    # 在后台异步执行，避免阻塞API响应
    background_tasks.add_task(
        executor.execute_single_case,
        test_case_id=trigger.test_case_id,
        environment_id=trigger.environment_id,
        executor=trigger.executor or "manual"
    )
    
    return TriggerResponse(
        message="单个测试用例执行已触发",
        execution_type="single",
        test_case_id=trigger.test_case_id,
        environment_id=trigger.environment_id
    )


@router.post("/module", response_model=TriggerResponse)
async def trigger_module_execution(
    trigger: ModuleTrigger,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    触发执行整个模块的测试用例
    
    适用于：
    1. 功能模块的完整测试
    2. 回归测试
    3. 模块级别的质量验证
    """
    executor = TestExecutor(db)
    
    # 在后台异步执行
    background_tasks.add_task(
        executor.execute_module,
        module_id=trigger.module_id,
        environment_id=trigger.environment_id,
        executor=trigger.executor or "manual"
    )
    
    return TriggerResponse(
        message="模块测试执行已触发",
        execution_type="module",
        module_id=trigger.module_id,
        environment_id=trigger.environment_id
    )


@router.post("/all", response_model=TriggerResponse)
async def trigger_all_cases(
    trigger: AllCasesTrigger,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    触发执行所有测试用例
    
    适用于：
    1. 全量回归测试
    2. 发布前的完整验证
    3. 定期自动化测试
    """
    executor = TestExecutor(db)
    
    # 在后台异步执行
    background_tasks.add_task(
        executor.execute_all,
        environment_id=trigger.environment_id,
        executor=trigger.executor or "manual"
    )
    
    return TriggerResponse(
        message="全量测试执行已触发",
        execution_type="all",
        environment_id=trigger.environment_id
    )


@router.post("/quick-test")
async def quick_test(
    test_case_id: int,
    environment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    快速测试接口（同步执行，立即返回结果）
    
    适用于：
    1. 开发过程中的快速验证
    2. 需要立即看到结果的场景
    3. 调试和问题排查
    """
    executor = TestExecutor(db)
    
    try:
        execution = await executor.execute_single_case(
            test_case_id=test_case_id,
            environment_id=environment_id,
            executor="quick_test"
        )
        
        return {
            "success": True,
            "execution_id": execution.id,
            "status": execution.status,
            "message": "快速测试执行完成"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": "快速测试执行失败"
        }


@router.post("/batch")
async def batch_execute(
    test_case_ids: List[int] = Query(..., description="测试用例ID列表"),
    environment_id: int = Query(..., description="环境ID"),
    executor: str = Query("batch", description="执行人"),
    db: AsyncSession = Depends(get_db),
):
    """
    批量执行指定的测试用例
    
    适用于：
    1. 选择性地执行多个相关测试用例
    2. 特定场景的测试组合
    3. 自定义测试套件
    """
    if not test_case_ids:
        raise HTTPException(status_code=400, detail="测试用例ID列表不能为空")
    
    if len(test_case_ids) > 100:
        raise HTTPException(status_code=400, detail="批量执行数量不能超过100个")
    
    executor_service = TestExecutor(db)
    
    # 创建批量执行记录
    execution_data = ExecutionCreate(
        name=f"批量执行 {len(test_case_ids)} 个测试用例",
        scope='batch',
        environment_id=environment_id,
        executor=executor,
        status='running',
        progress={'current': 0, 'total': len(test_case_ids)}
    )
    
    from app.services.execution import ExecutionService
    execution_service = ExecutionService(db)
    execution = await execution_service.create_execution(execution_data)
    
    # 异步执行所有测试用例
    import asyncio
    
    async def execute_batch():
        try:
            for i, case_id in enumerate(test_case_ids):
                try:
                    await executor_service.execute_single_case(
                        test_case_id=case_id,
                        environment_id=environment_id,
                        executor=executor
                    )
                    
                    # 更新进度
                    update_data = ExecutionUpdate(
                        progress={'current': i + 1, 'total': len(test_case_ids)}
                    )
                    await execution_service.update_execution(
                        execution.id,
                        update_data
                    )
                    
                except Exception as e:
                    # 记录错误但继续执行
                    log_data = ExecutionLogCreate(
                        level='error',
                        message=f'测试用例 {case_id} 执行失败: {str(e)}'
                    )
                    await execution_service.create_log(
                        execution.id,
                        log_data
                    )
                    continue
            
            # 更新执行状态为完成
            update_data = ExecutionUpdate(status='success')
            await execution_service.update_execution(
                execution.id,
                update_data
            )
            
        except Exception as e:
            update_data = ExecutionUpdate(status='failed')
            await execution_service.update_execution(
                execution.id,
                update_data
            )
    
    # 在后台执行
    asyncio.create_task(execute_batch())
    
    return {
        "success": True,
        "execution_id": execution.id,
        "message": f"批量执行已触发，共 {len(test_case_ids)} 个测试用例"
    }


@router.get("/status/{execution_id}")
async def get_execution_status(
    execution_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取执行状态和进度
    
    用于：
    1. 监控执行进度
    2. 获取实时状态
    3. 前端轮询更新
    """
    from app.services.execution import ExecutionService
    execution_service = ExecutionService(db)
    
    try:
        execution = await execution_service.get_execution(execution_id)
        
        # 获取执行详情统计
        details = await execution_service.get_details(execution_id, skip=0, limit=1000)
        success_count = sum(1 for detail in details if detail.status == 'success')
        failed_count = sum(1 for detail in details if detail.status == 'failed')
        
        return {
            "execution_id": execution.id,
            "name": execution.name,
            "status": execution.status,
            "progress": execution.progress,
            "created_at": execution.created_at,
            "updated_at": execution.updated_at,
            "statistics": {
                "total": len(details),
                "success": success_count,
                "failed": failed_count,
                "success_rate": round(success_count / len(details) * 100, 2) if details else 0
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"执行记录不存在: {str(e)}") 