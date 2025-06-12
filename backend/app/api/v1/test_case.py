from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.test_case import TestCaseService
from app.schemas.test_case import TestCase, TestCaseCreate, TestCaseUpdate

router = APIRouter()


@router.get("/", response_model=List[TestCase])
async def get_test_cases(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    module_id: Optional[int] = Query(None, description="模块ID"),
    db: AsyncSession = Depends(get_db),
):
    """获取测试用例列表"""
    return await TestCaseService(db).get_test_cases(
        skip=skip,
        limit=limit,
        module_id=module_id
    )


@router.post("/", response_model=TestCase)
async def create_test_case(
    test_case: TestCaseCreate,
    db: AsyncSession = Depends(get_db),
):
    """创建测试用例"""
    return await TestCaseService(db).create_test_case(test_case)


@router.get("/{test_case_id}", response_model=TestCase)
async def get_test_case(
    test_case_id: int,
    db: AsyncSession = Depends(get_db),
):
    """获取测试用例详情"""
    return await TestCaseService(db).get_test_case(test_case_id)


@router.put("/{test_case_id}", response_model=TestCase)
async def update_test_case(
    test_case_id: int,
    test_case: TestCaseUpdate,
    db: AsyncSession = Depends(get_db),
):
    """更新测试用例"""
    return await TestCaseService(db).update_test_case(test_case_id, test_case)


@router.delete("/{test_case_id}")
async def delete_test_case(
    test_case_id: int,
    db: AsyncSession = Depends(get_db),
):
    """删除测试用例"""
    await TestCaseService(db).delete_test_case(test_case_id)
    return {"message": "测试用例已删除"} 