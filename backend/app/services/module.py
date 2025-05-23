from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.module import module
from app.models.module import Module, ModuleVariable, TestCase
from app.schemas.module import (
    ModuleCreate,
    ModuleUpdate,
    ModuleVariableCreate,
    ModuleVariableUpdate,
    TestCaseCreate,
    TestCaseUpdate,
)


class ModuleService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_module(self, module_id: int) -> Module:
        """
        获取模块详情
        """
        db_module = await module.get(self.db, id=module_id)
        if not db_module:
            raise HTTPException(status_code=404, detail="模块不存在")
        return db_module

    async def get_modules(self, skip: int = 0, limit: int = 100) -> List[Module]:
        """
        获取模块列表
        """
        return await module.get_multi(self.db, skip=skip, limit=limit)

    async def create_module(self, module_in: ModuleCreate) -> Module:
        """
        创建模块
        """
        db_module = await module.get_by_name(self.db, name=module_in.name)
        if db_module:
            raise HTTPException(status_code=400, detail="模块名称已存在")
        return await module.create(self.db, obj_in=module_in)

    async def update_module(
        self, module_id: int, module_in: ModuleUpdate
    ) -> Module:
        """
        更新模块
        """
        db_module = await self.get_module(module_id)
        return await module.update(
            self.db, db_obj=db_module, obj_in=module_in
        )

    async def delete_module(self, module_id: int) -> Module:
        """
        删除模块
        """
        db_module = await self.get_module(module_id)
        return await module.remove(self.db, id=module_id)

    async def get_variables(
        self, module_id: int, skip: int = 0, limit: int = 100
    ) -> List[ModuleVariable]:
        """
        获取模块变量列表
        """
        await self.get_module(module_id)  # 验证模块是否存在
        return await module.get_variables(
            self.db, module_id=module_id, skip=skip, limit=limit
        )

    async def create_variable(
        self, module_id: int, variable_in: ModuleVariableCreate
    ) -> ModuleVariable:
        """
        创建模块变量
        """
        await self.get_module(module_id)  # 验证模块是否存在
        return await module.create_variable(
            self.db, module_id=module_id, obj_in=variable_in
        )

    async def update_variable(
        self, variable_id: int, variable_in: ModuleVariableUpdate
    ) -> ModuleVariable:
        """
        更新模块变量
        """
        db_variable = await self.db.get(ModuleVariable, variable_id)
        if not db_variable:
            raise HTTPException(status_code=404, detail="模块变量不存在")
        return await module.update_variable(
            self.db, db_obj=db_variable, obj_in=variable_in
        )

    async def delete_variable(self, variable_id: int) -> ModuleVariable:
        """
        删除模块变量
        """
        db_variable = await self.db.get(ModuleVariable, variable_id)
        if not db_variable:
            raise HTTPException(status_code=404, detail="模块变量不存在")
        return await module.remove_variable(self.db, id=variable_id)

    async def get_test_cases(
        self, module_id: int, skip: int = 0, limit: int = 100
    ) -> List[TestCase]:
        """
        获取测试用例列表
        """
        await self.get_module(module_id)  # 验证模块是否存在
        return await module.get_test_cases(
            self.db, module_id=module_id, skip=skip, limit=limit
        )

    async def create_test_case(
        self, module_id: int, test_case_in: TestCaseCreate
    ) -> TestCase:
        """
        创建测试用例
        """
        await self.get_module(module_id)  # 验证模块是否存在
        return await module.create_test_case(
            self.db, module_id=module_id, obj_in=test_case_in
        )

    async def update_test_case(
        self, test_case_id: int, test_case_in: TestCaseUpdate
    ) -> TestCase:
        """
        更新测试用例
        """
        db_test_case = await self.db.get(TestCase, test_case_id)
        if not db_test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        return await module.update_test_case(
            self.db, db_obj=db_test_case, obj_in=test_case_in
        )

    async def delete_test_case(self, test_case_id: int) -> TestCase:
        """
        删除测试用例
        """
        db_test_case = await self.db.get(TestCase, test_case_id)
        if not db_test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        return await module.remove_test_case(self.db, id=test_case_id) 