from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.crud.execution import execution
from app.models.execution import Execution, ExecutionLog, ExecutionDetail
from app.models.test_case import TestCase
from app.models.module import Module
from app.models.environment import Environment
from app.schemas.execution import (
    ExecutionCreate,
    ExecutionUpdate,
    ExecutionLogCreate,
    ExecutionDetailCreate,
    ExecutionDetailUpdate,
)


class ExecutionService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_execution(self, execution_id: int) -> Execution:
        """
        获取执行记录详情
        """
        db_execution = await execution.get(self.db, id=execution_id)
        if not db_execution:
            raise HTTPException(status_code=404, detail="执行记录不存在")
        return db_execution

    async def get_executions(self, skip: int = 0, limit: int = 100) -> List[Execution]:
        """
        获取执行记录列表
        """
        return await execution.get_multi(self.db, skip=skip, limit=limit)

    async def create_execution(self, execution_in: ExecutionCreate) -> Execution:
        """
        创建执行记录
        """
        # 验证外键引用
        await self._validate_foreign_keys(execution_in)
        
        return await execution.create(self.db, obj_in=execution_in)

    async def _validate_foreign_keys(self, execution_in: ExecutionCreate):
        """
        验证外键引用是否存在
        """
        # 验证环境ID
        if execution_in.environment_id:
            result = await self.db.execute(
                select(Environment).filter(Environment.id == execution_in.environment_id)
            )
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"环境ID {execution_in.environment_id} 不存在")

        # 验证测试用例ID
        if execution_in.case_id:
            result = await self.db.execute(
                select(TestCase).filter(TestCase.id == execution_in.case_id)
            )
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"测试用例ID {execution_in.case_id} 不存在")

        # 验证模块ID
        if execution_in.module_id:
            result = await self.db.execute(
                select(Module).filter(Module.id == execution_in.module_id)
            )
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"模块ID {execution_in.module_id} 不存在")

    async def update_execution(
        self, execution_id: int, execution_in: ExecutionUpdate
    ) -> Execution:
        """
        更新执行记录
        """
        db_execution = await self.get_execution(execution_id)
        
        # 验证外键引用
        await self._validate_foreign_keys_update(execution_in)
        
        return await execution.update(
            self.db, db_obj=db_execution, obj_in=execution_in
        )

    async def _validate_foreign_keys_update(self, execution_in: ExecutionUpdate):
        """
        验证更新时的外键引用是否存在
        """
        # 验证环境ID
        if execution_in.environment_id is not None:
            result = await self.db.execute(
                select(Environment).filter(Environment.id == execution_in.environment_id)
            )
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"环境ID {execution_in.environment_id} 不存在")

        # 验证测试用例ID
        if execution_in.case_id is not None:
            result = await self.db.execute(
                select(TestCase).filter(TestCase.id == execution_in.case_id)
            )
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"测试用例ID {execution_in.case_id} 不存在")

        # 验证模块ID
        if execution_in.module_id is not None:
            result = await self.db.execute(
                select(Module).filter(Module.id == execution_in.module_id)
            )
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"模块ID {execution_in.module_id} 不存在")

    async def delete_execution(self, execution_id: int) -> Execution:
        """
        删除执行记录
        """
        db_execution = await self.get_execution(execution_id)
        return await execution.remove(self.db, id=execution_id)

    async def get_logs(
        self, execution_id: int, skip: int = 0, limit: int = 100
    ) -> List[ExecutionLog]:
        """
        获取执行日志列表
        """
        await self.get_execution(execution_id)  # 验证执行记录是否存在
        return await execution.get_logs(
            self.db, execution_id=execution_id, skip=skip, limit=limit
        )

    async def create_log(
        self, execution_id: int, log_in: ExecutionLogCreate
    ) -> ExecutionLog:
        """
        创建执行日志
        """
        await self.get_execution(execution_id)  # 验证执行记录是否存在
        return await execution.create_log(
            self.db, execution_id=execution_id, obj_in=log_in
        )

    async def get_details(
        self, execution_id: int, skip: int = 0, limit: int = 100
    ) -> List[ExecutionDetail]:
        """
        获取执行详情列表
        """
        await self.get_execution(execution_id)  # 验证执行记录是否存在
        return await execution.get_details(
            self.db, execution_id=execution_id, skip=skip, limit=limit
        )

    async def create_detail(
        self, execution_id: int, detail_in: ExecutionDetailCreate
    ) -> ExecutionDetail:
        """
        创建执行详情
        """
        await self.get_execution(execution_id)  # 验证执行记录是否存在
        
        # 验证测试用例ID
        if detail_in.test_case_id:
            result = await self.db.execute(
                select(TestCase).filter(TestCase.id == detail_in.test_case_id)
            )
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"测试用例ID {detail_in.test_case_id} 不存在")
        
        return await execution.create_detail(
            self.db, execution_id=execution_id, obj_in=detail_in
        )

    async def update_detail(
        self, detail_id: int, detail_in: ExecutionDetailUpdate
    ) -> ExecutionDetail:
        """
        更新执行详情
        """
        db_detail = await self.db.get(ExecutionDetail, detail_id)
        if not db_detail:
            raise HTTPException(status_code=404, detail="执行详情不存在")
        
        # 验证测试用例ID
        if detail_in.test_case_id is not None:
            result = await self.db.execute(
                select(TestCase).filter(TestCase.id == detail_in.test_case_id)
            )
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=400, detail=f"测试用例ID {detail_in.test_case_id} 不存在")
        
        return await execution.update_detail(
            self.db, db_obj=db_detail, obj_in=detail_in
        )

    async def remove_detail(self, detail_id: int) -> ExecutionDetail:
        """
        删除执行详情
        """
        db_detail = await self.db.get(ExecutionDetail, detail_id)
        if not db_detail:
            raise HTTPException(status_code=404, detail="执行详情不存在")
        return await execution.remove_detail(self.db, id=detail_id) 