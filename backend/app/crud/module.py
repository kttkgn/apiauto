from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.module import Module, ModuleVariable, TestCase
from app.schemas.module import ModuleCreate, ModuleUpdate, ModuleVariableCreate, ModuleVariableUpdate, TestCaseCreate, TestCaseUpdate


class CRUDModule(CRUDBase[Module, ModuleCreate, ModuleUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Module]:
        """
        通过名称获取模块
        """
        result = await db.execute(select(Module).filter(Module.name == name))
        return result.scalar_one_or_none()

    async def get_variables(
        self, db: AsyncSession, *, module_id: int, skip: int = 0, limit: int = 100
    ) -> List[ModuleVariable]:
        """
        获取模块变量列表
        """
        result = await db.execute(
            select(ModuleVariable)
            .filter(ModuleVariable.module_id == module_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_variable(
        self, db: AsyncSession, *, module_id: int, obj_in: ModuleVariableCreate
    ) -> ModuleVariable:
        """
        创建模块变量
        """
        obj_in_data = obj_in.dict()
        db_obj = ModuleVariable(**obj_in_data, module_id=module_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_variable(
        self,
        db: AsyncSession,
        *,
        db_obj: ModuleVariable,
        obj_in: ModuleVariableUpdate
    ) -> ModuleVariable:
        """
        更新模块变量
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove_variable(self, db: AsyncSession, *, id: int) -> ModuleVariable:
        """
        删除模块变量
        """
        obj = await db.get(ModuleVariable, id)
        await db.delete(obj)
        await db.commit()
        return obj

    async def get_test_cases(
        self, db: AsyncSession, *, module_id: int, skip: int = 0, limit: int = 100
    ) -> List[TestCase]:
        """
        获取测试用例列表
        """
        result = await db.execute(
            select(TestCase)
            .filter(TestCase.module_id == module_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_test_case(
        self, db: AsyncSession, *, module_id: int, obj_in: TestCaseCreate
    ) -> TestCase:
        """
        创建测试用例
        """
        obj_in_data = obj_in.dict()
        db_obj = TestCase(**obj_in_data, module_id=module_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_test_case(
        self,
        db: AsyncSession,
        *,
        db_obj: TestCase,
        obj_in: TestCaseUpdate
    ) -> TestCase:
        """
        更新测试用例
        """
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove_test_case(self, db: AsyncSession, *, id: int) -> TestCase:
        """
        删除测试用例
        """
        obj = await db.get(TestCase, id)
        await db.delete(obj)
        await db.commit()
        return obj


module = CRUDModule(Module) 