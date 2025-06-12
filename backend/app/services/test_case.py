from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.test_case import test_case
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate


class TestCaseService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_test_case(self, test_case_id: int):
        """获取测试用例详情"""
        db_test_case = await test_case.get(self.db, id=test_case_id)
        if not db_test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        return db_test_case

    async def get_test_cases(
        self,
        skip: int = 0,
        limit: int = 100,
        module_id: Optional[int] = None
    ):
        """获取测试用例列表"""
        return await test_case.get_multi(
            self.db,
            skip=skip,
            limit=limit,
            module_id=module_id
        )

    async def create_test_case(self, test_case_in: TestCaseCreate):
        """创建测试用例"""
        # 检查名称是否已存在
        db_test_case = await test_case.get_by_name(self.db, name=test_case_in.name)
        if db_test_case:
            raise HTTPException(status_code=400, detail="测试用例名称已存在")
        return await test_case.create(self.db, obj_in=test_case_in)

    async def update_test_case(
        self,
        test_case_id: int,
        test_case_in: TestCaseUpdate
    ):
        """更新测试用例"""
        db_test_case = await test_case.get(self.db, id=test_case_id)
        if not db_test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        return await test_case.update(
            self.db,
            db_obj=db_test_case,
            obj_in=test_case_in
        )

    async def delete_test_case(self, test_case_id: int):
        """删除测试用例"""
        db_test_case = await test_case.get(self.db, id=test_case_id)
        if not db_test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        return await test_case.remove(self.db, id=test_case_id) 