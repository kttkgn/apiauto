import asyncio
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.environment import environment
from app.crud.module import module
from app.crud.test_case import test_case
from app.services.executor import TestExecutor

logger = logging.getLogger(__name__)

class SchedulerService:
    """定时任务调度器"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.executor = TestExecutor(db)
        self.scheduled_tasks: Dict[str, asyncio.Task] = {}
    
    async def schedule_single_case(
        self,
        task_id: str,
        test_case_id: int,
        environment_id: int,
        schedule_time: datetime,
        executor: str = "scheduler"
    ) -> Dict:
        """调度单个测试用例的定时执行"""
        # 验证测试用例和环境是否存在
        test_case_obj = await test_case.get(self.db, id=test_case_id)
        if not test_case_obj:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        
        env_obj = await environment.get(self.db, id=environment_id)
        if not env_obj:
            raise HTTPException(status_code=404, detail="环境配置不存在")
        
        # 计算延迟时间
        delay = (schedule_time - datetime.now()).total_seconds()
        if delay <= 0:
            raise HTTPException(status_code=400, detail="调度时间不能早于当前时间")
        
        # 创建定时任务
        task = asyncio.create_task(
            self._delayed_execute_single_case(
                task_id, test_case_id, environment_id, executor, delay
            )
        )
        
        self.scheduled_tasks[task_id] = task
        
        return {
            "task_id": task_id,
            "test_case_id": test_case_id,
            "environment_id": environment_id,
            "schedule_time": schedule_time.isoformat(),
            "status": "scheduled"
        }
    
    async def schedule_module(
        self,
        task_id: str,
        module_id: int,
        environment_id: int,
        schedule_time: datetime,
        executor: str = "scheduler"
    ) -> Dict:
        """调度模块的定时执行"""
        # 验证模块和环境是否存在
        module_obj = await module.get(self.db, id=module_id)
        if not module_obj:
            raise HTTPException(status_code=404, detail="模块不存在")
        
        env_obj = await environment.get(self.db, id=environment_id)
        if not env_obj:
            raise HTTPException(status_code=404, detail="环境配置不存在")
        
        # 计算延迟时间
        delay = (schedule_time - datetime.now()).total_seconds()
        if delay <= 0:
            raise HTTPException(status_code=400, detail="调度时间不能早于当前时间")
        
        # 创建定时任务
        task = asyncio.create_task(
            self._delayed_execute_module(
                task_id, module_id, environment_id, executor, delay
            )
        )
        
        self.scheduled_tasks[task_id] = task
        
        return {
            "task_id": task_id,
            "module_id": module_id,
            "environment_id": environment_id,
            "schedule_time": schedule_time.isoformat(),
            "status": "scheduled"
        }
    
    async def schedule_recurring_task(
        self,
        task_id: str,
        task_type: str,  # 'single', 'module', 'all'
        target_id: int,  # test_case_id, module_id, or environment_id
        environment_id: int,
        interval_minutes: int,
        executor: str = "scheduler"
    ) -> Dict:
        """调度重复执行任务"""
        if interval_minutes < 1:
            raise HTTPException(status_code=400, detail="重复间隔不能少于1分钟")
        
        # 验证目标是否存在
        if task_type == 'single':
            test_case_obj = await test_case.get(self.db, id=target_id)
            if not test_case_obj:
                raise HTTPException(status_code=404, detail="测试用例不存在")
        elif task_type == 'module':
            module_obj = await module.get(self.db, id=target_id)
            if not module_obj:
                raise HTTPException(status_code=404, detail="模块不存在")
        
        env_obj = await environment.get(self.db, id=environment_id)
        if not env_obj:
            raise HTTPException(status_code=404, detail="环境配置不存在")
        
        # 创建重复任务
        task = asyncio.create_task(
            self._recurring_execute(
                task_id, task_type, target_id, environment_id, interval_minutes, executor
            )
        )
        
        self.scheduled_tasks[task_id] = task
        
        return {
            "task_id": task_id,
            "task_type": task_type,
            "target_id": target_id,
            "environment_id": environment_id,
            "interval_minutes": interval_minutes,
            "status": "scheduled"
        }
    
    async def cancel_task(self, task_id: str) -> Dict:
        """取消定时任务"""
        if task_id not in self.scheduled_tasks:
            raise HTTPException(status_code=404, detail="任务不存在")
        
        task = self.scheduled_tasks[task_id]
        task.cancel()
        
        try:
            await task
        except asyncio.CancelledError:
            pass
        
        del self.scheduled_tasks[task_id]
        
        return {
            "task_id": task_id,
            "status": "cancelled"
        }
    
    async def get_scheduled_tasks(self) -> List[Dict]:
        """获取所有已调度的任务"""
        tasks = []
        for task_id, task in self.scheduled_tasks.items():
            tasks.append({
                "task_id": task_id,
                "status": "running" if not task.done() else "completed",
                "cancelled": task.cancelled()
            })
        return tasks
    
    async def _delayed_execute_single_case(
        self, task_id: str, test_case_id: int, environment_id: int, executor: str, delay: float
    ):
        """延迟执行单个测试用例"""
        try:
            await asyncio.sleep(delay)
            await self.executor.execute_single_case(test_case_id, environment_id, executor)
        except Exception as e:
            logger.error(f"定时任务执行失败: {str(e)}")
        finally:
            # 清理任务
            if task_id in self.scheduled_tasks:
                del self.scheduled_tasks[task_id]
    
    async def _delayed_execute_module(
        self, task_id: str, module_id: int, environment_id: int, executor: str, delay: float
    ):
        """延迟执行模块"""
        try:
            await asyncio.sleep(delay)
            await self.executor.execute_module(module_id, environment_id, executor)
        except Exception as e:
            logger.error(f"定时任务执行失败: {str(e)}")
        finally:
            if task_id in self.scheduled_tasks:
                del self.scheduled_tasks[task_id]
    
    async def _recurring_execute(
        self, task_id: str, task_type: str, target_id: int, environment_id: int, 
        interval_minutes: int, executor: str
    ):
        """重复执行任务"""
        try:
            while True:
                await asyncio.sleep(interval_minutes * 60)  # 转换为秒
                
                if task_type == 'single':
                    await self.executor.execute_single_case(target_id, environment_id, executor)
                elif task_type == 'module':
                    await self.executor.execute_module(target_id, environment_id, executor)
                elif task_type == 'all':
                    await self.executor.execute_all(environment_id, executor)
                    
        except asyncio.CancelledError:
            # 任务被取消
            pass
        except Exception as e:
            logger.error(f"重复任务执行失败: {str(e)}")
        finally:
            if task_id in self.scheduled_tasks:
                del self.scheduled_tasks[task_id] 