from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.module import (
    Module,
    ModuleCreate,
    ModuleUpdate,
    ModuleVariable,
    ModuleVariableCreate,
    ModuleVariableUpdate,
    TestCase,
    TestCaseCreate,
    TestCaseUpdate,
)
from app.services.module import ModuleService

router = APIRouter()


@router.get("/", response_model=List[Module])
async def get_modules(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    获取模块列表
    """
    service = ModuleService(db)
    return await service.get_modules(skip=skip, limit=limit)


@router.post("/", response_model=Module)
async def create_module(
    *,
    db: AsyncSession = Depends(get_db),
    module_in: ModuleCreate,
):
    """
    创建模块
    """
    service = ModuleService(db)
    return await service.create_module(module_in)


@router.get("/{module_id}", response_model=Module)
async def get_module(
    *,
    db: AsyncSession = Depends(get_db),
    module_id: int,
):
    """
    获取模块详情
    """
    service = ModuleService(db)
    return await service.get_module(module_id)


@router.put("/{module_id}", response_model=Module)
async def update_module(
    *,
    db: AsyncSession = Depends(get_db),
    module_id: int,
    module_in: ModuleUpdate,
):
    """
    更新模块
    """
    service = ModuleService(db)
    return await service.update_module(module_id, module_in)


@router.delete("/{module_id}", response_model=Module)
async def delete_module(
    *,
    db: AsyncSession = Depends(get_db),
    module_id: int,
):
    """
    删除模块
    """
    service = ModuleService(db)
    return await service.delete_module(module_id)


@router.get("/{module_id}/variables", response_model=List[ModuleVariable])
async def get_variables(
    *,
    db: AsyncSession = Depends(get_db),
    module_id: int,
    skip: int = 0,
    limit: int = 100,
):
    """
    获取模块变量列表
    """
    service = ModuleService(db)
    return await service.get_variables(module_id, skip=skip, limit=limit)


@router.post("/{module_id}/variables", response_model=ModuleVariable)
async def create_variable(
    *,
    db: AsyncSession = Depends(get_db),
    module_id: int,
    variable_in: ModuleVariableCreate,
):
    """
    创建模块变量
    """
    service = ModuleService(db)
    return await service.create_variable(module_id, variable_in)


@router.put("/variables/{variable_id}", response_model=ModuleVariable)
async def update_variable(
    *,
    db: AsyncSession = Depends(get_db),
    variable_id: int,
    variable_in: ModuleVariableUpdate,
):
    """
    更新模块变量
    """
    service = ModuleService(db)
    return await service.update_variable(variable_id, variable_in)


@router.delete("/variables/{variable_id}", response_model=ModuleVariable)
async def delete_variable(
    *,
    db: AsyncSession = Depends(get_db),
    variable_id: int,
):
    """
    删除模块变量
    """
    service = ModuleService(db)
    return await service.delete_variable(variable_id)


@router.get("/{module_id}/test-cases", response_model=List[TestCase])
async def get_test_cases(
    *,
    db: AsyncSession = Depends(get_db),
    module_id: int,
    skip: int = 0,
    limit: int = 100,
):
    """
    获取测试用例列表
    """
    service = ModuleService(db)
    return await service.get_test_cases(module_id, skip=skip, limit=limit)


@router.post("/{module_id}/test-cases", response_model=TestCase)
async def create_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    module_id: int,
    test_case_in: TestCaseCreate,
):
    """
    创建测试用例
    """
    service = ModuleService(db)
    return await service.create_test_case(module_id, test_case_in)


@router.put("/test-cases/{test_case_id}", response_model=TestCase)
async def update_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_case_id: int,
    test_case_in: TestCaseUpdate,
):
    """
    更新测试用例
    """
    service = ModuleService(db)
    return await service.update_test_case(test_case_id, test_case_in)


@router.delete("/test-cases/{test_case_id}", response_model=TestCase)
async def delete_test_case(
    *,
    db: AsyncSession = Depends(get_db),
    test_case_id: int,
):
    """
    删除测试用例
    """
    service = ModuleService(db)
    return await service.delete_test_case(test_case_id) 