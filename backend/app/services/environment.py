from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.environment import environment
from app.models.environment import Environment, EnvironmentVariable
from app.schemas.environment import (
    EnvironmentCreate,
    EnvironmentUpdate,
    EnvironmentVariableCreate,
    EnvironmentVariableUpdate,
)


class EnvironmentService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_environment(self, environment_id: int) -> Environment:
        """
        获取环境详情
        """
        db_environment = await environment.get(self.db, id=environment_id)
        if not db_environment:
            raise HTTPException(status_code=404, detail="环境不存在")
        return db_environment

    async def get_environments(self, skip: int = 0, limit: int = 100) -> List[Environment]:
        """
        获取环境列表
        """
        return await environment.get_multi(self.db, skip=skip, limit=limit)

    async def create_environment(self, environment_in: EnvironmentCreate) -> Environment:
        """
        创建环境
        """
        db_environment = await environment.get_by_name(self.db, name=environment_in.name)
        if db_environment:
            raise HTTPException(status_code=400, detail="环境名称已存在")
        return await environment.create(self.db, obj_in=environment_in)

    async def update_environment(
        self, environment_id: int, environment_in: EnvironmentUpdate
    ) -> Environment:
        """
        更新环境
        """
        db_environment = await self.get_environment(environment_id)
        return await environment.update(
            self.db, db_obj=db_environment, obj_in=environment_in
        )

    async def delete_environment(self, environment_id: int) -> Environment:
        """
        删除环境
        """
        db_environment = await self.get_environment(environment_id)
        return await environment.remove(self.db, id=environment_id)

    async def get_variables(
        self, environment_id: int, skip: int = 0, limit: int = 100
    ) -> List[EnvironmentVariable]:
        """
        获取环境变量列表
        """
        await self.get_environment(environment_id)  # 验证环境是否存在
        return await environment.get_variables(
            self.db, environment_id=environment_id, skip=skip, limit=limit
        )

    async def create_variable(
        self, environment_id: int, variable_in: EnvironmentVariableCreate
    ) -> EnvironmentVariable:
        """
        创建环境变量
        """
        await self.get_environment(environment_id)  # 验证环境是否存在
        return await environment.create_variable(
            self.db, environment_id=environment_id, obj_in=variable_in
        )

    async def update_variable(
        self, variable_id: int, variable_in: EnvironmentVariableUpdate
    ) -> EnvironmentVariable:
        """
        更新环境变量
        """
        db_variable = await self.db.get(EnvironmentVariable, variable_id)
        if not db_variable:
            raise HTTPException(status_code=404, detail="环境变量不存在")
        return await environment.update_variable(
            self.db, db_obj=db_variable, obj_in=variable_in
        )

    async def delete_variable(self, variable_id: int) -> EnvironmentVariable:
        """
        删除环境变量
        """
        db_variable = await self.db.get(EnvironmentVariable, variable_id)
        if not db_variable:
            raise HTTPException(status_code=404, detail="环境变量不存在")
        return await environment.remove_variable(self.db, id=variable_id) 