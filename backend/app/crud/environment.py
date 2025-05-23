from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.environment import Environment, EnvironmentVariable
from app.schemas.environment import EnvironmentCreate, EnvironmentUpdate, EnvironmentVariableCreate, EnvironmentVariableUpdate


class CRUDEnvironment(CRUDBase[Environment, EnvironmentCreate, EnvironmentUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Environment]:
        """
        通过名称获取环境
        """
        result = await db.execute(select(Environment).filter(Environment.name == name))
        return result.scalar_one_or_none()

    async def get_variables(
        self, db: AsyncSession, *, environment_id: int, skip: int = 0, limit: int = 100
    ) -> List[EnvironmentVariable]:
        """
        获取环境变量列表
        """
        result = await db.execute(
            select(EnvironmentVariable)
            .filter(EnvironmentVariable.environment_id == environment_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_variable(
        self, db: AsyncSession, *, environment_id: int, obj_in: EnvironmentVariableCreate
    ) -> EnvironmentVariable:
        """
        创建环境变量
        """
        obj_in_data = obj_in.dict()
        db_obj = EnvironmentVariable(**obj_in_data, environment_id=environment_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_variable(
        self,
        db: AsyncSession,
        *,
        db_obj: EnvironmentVariable,
        obj_in: EnvironmentVariableUpdate
    ) -> EnvironmentVariable:
        """
        更新环境变量
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove_variable(self, db: AsyncSession, *, id: int) -> EnvironmentVariable:
        """
        删除环境变量
        """
        obj = await db.get(EnvironmentVariable, id)
        await db.delete(obj)
        await db.commit()
        return obj


environment = CRUDEnvironment(Environment) 