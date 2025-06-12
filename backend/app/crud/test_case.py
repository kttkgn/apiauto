from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.test_case import TestCase
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate
from app.crud.base import CRUDBase


class CRUDTestCase(CRUDBase[TestCase, TestCaseCreate, TestCaseUpdate]):
    async def get_by_name(self, db: AsyncSession, name: str) -> Optional[TestCase]:
        """根据名称获取测试用例"""
        result = await db.execute(select(TestCase).filter(TestCase.name == name))
        return result.scalar_one_or_none()

    async def get_by_module(
        self,
        db: AsyncSession,
        *,
        module_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[TestCase]:
        """根据模块ID获取测试用例列表"""
        result = await db.execute(
            select(TestCase)
            .filter(TestCase.module_id == module_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        module_id: Optional[int] = None
    ) -> List[TestCase]:
        """获取测试用例列表"""
        query = select(TestCase)
        if module_id is not None:
            query = query.filter(TestCase.module_id == module_id)
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()


test_case = CRUDTestCase(TestCase) 