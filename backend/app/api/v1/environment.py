from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.environment import (
    Environment,
    EnvironmentCreate,
    EnvironmentUpdate,
    EnvironmentVariable,
    EnvironmentVariableCreate,
    EnvironmentVariableUpdate,
)
from app.services.environment import EnvironmentService

router = APIRouter()


@router.get("/", response_model=List[Environment])
async def get_environments(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    获取环境列表
    """
    service = EnvironmentService(db)
    return await service.get_environments(skip=skip, limit=limit)


@router.post("/", response_model=Environment)
async def create_environment(
    *,
    db: AsyncSession = Depends(get_db),
    environment_in: EnvironmentCreate,
):
    """
    创建环境
    """
    service = EnvironmentService(db)
    return await service.create_environment(environment_in)


@router.get("/{environment_id}", response_model=Environment)
async def get_environment(
    *,
    db: AsyncSession = Depends(get_db),
    environment_id: int,
):
    """
    获取环境详情
    """
    service = EnvironmentService(db)
    return await service.get_environment(environment_id)


@router.put("/{environment_id}", response_model=Environment)
async def update_environment(
    *,
    db: AsyncSession = Depends(get_db),
    environment_id: int,
    environment_in: EnvironmentUpdate,
):
    """
    更新环境
    """
    service = EnvironmentService(db)
    return await service.update_environment(environment_id, environment_in)


@router.delete("/{environment_id}", response_model=Environment)
async def delete_environment(
    *,
    db: AsyncSession = Depends(get_db),
    environment_id: int,
):
    """
    删除环境
    """
    service = EnvironmentService(db)
    return await service.delete_environment(environment_id)


@router.get("/{environment_id}/variables", response_model=List[EnvironmentVariable])
async def get_variables(
    *,
    db: AsyncSession = Depends(get_db),
    environment_id: int,
    skip: int = 0,
    limit: int = 100,
):
    """
    获取环境变量列表
    """
    service = EnvironmentService(db)
    return await service.get_variables(environment_id, skip=skip, limit=limit)


@router.post("/{environment_id}/variables", response_model=EnvironmentVariable)
async def create_variable(
    *,
    db: AsyncSession = Depends(get_db),
    environment_id: int,
    variable_in: EnvironmentVariableCreate,
):
    """
    创建环境变量
    """
    service = EnvironmentService(db)
    return await service.create_variable(environment_id, variable_in)


@router.put("/variables/{variable_id}", response_model=EnvironmentVariable)
async def update_variable(
    *,
    db: AsyncSession = Depends(get_db),
    variable_id: int,
    variable_in: EnvironmentVariableUpdate,
):
    """
    更新环境变量
    """
    service = EnvironmentService(db)
    return await service.update_variable(variable_id, variable_in)


@router.delete("/variables/{variable_id}", response_model=EnvironmentVariable)
async def delete_variable(
    *,
    db: AsyncSession = Depends(get_db),
    variable_id: int,
):
    """
    删除环境变量
    """
    service = EnvironmentService(db)
    return await service.delete_variable(variable_id) 