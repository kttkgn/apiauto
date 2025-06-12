from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.execution import Execution, ExecutionLog, ExecutionDetail
from app.schemas.execution import (
    ExecutionCreate,
    ExecutionUpdate,
    ExecutionLogCreate,
    ExecutionDetailCreate,
    ExecutionDetailUpdate,
)


class CRUDExecution(CRUDBase[Execution, ExecutionCreate, ExecutionUpdate]):
    async def get_logs(
        self, db: AsyncSession, *, execution_id: int, skip: int = 0, limit: int = 100
    ) -> List[ExecutionLog]:
        """
        获取执行日志列表
        """
        result = await db.execute(
            select(ExecutionLog)
            .filter(ExecutionLog.execution_id == execution_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_log(
        self, db: AsyncSession, *, execution_id: int, obj_in: ExecutionLogCreate
    ) -> ExecutionLog:
        """
        创建执行日志
        """
        obj_in_data = obj_in.model_dump()
        db_obj = ExecutionLog(**obj_in_data, execution_id=execution_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_details(
        self, db: AsyncSession, *, execution_id: int, skip: int = 0, limit: int = 100
    ) -> List[ExecutionDetail]:
        """
        获取执行详情列表
        """
        result = await db.execute(
            select(ExecutionDetail)
            .filter(ExecutionDetail.execution_id == execution_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_detail(
        self, db: AsyncSession, *, execution_id: int, obj_in: ExecutionDetailCreate
    ) -> ExecutionDetail:
        """
        创建执行详情
        """
        obj_in_data = obj_in.model_dump()
        db_obj = ExecutionDetail(**obj_in_data, execution_id=execution_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_detail(
        self,
        db: AsyncSession,
        *,
        db_obj: ExecutionDetail,
        obj_in: ExecutionDetailUpdate
    ) -> ExecutionDetail:
        """
        更新执行详情
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove_detail(self, db: AsyncSession, *, id: int) -> ExecutionDetail:
        """
        删除执行详情
        """
        obj = await db.get(ExecutionDetail, id)
        await db.delete(obj)
        await db.commit()
        return obj


execution = CRUDExecution(Execution) 