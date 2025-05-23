from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.test_case import TestCase
from app.schemas.test_case import TestCaseCreate, TestCaseUpdate


class CRUDTestCase:
    def get(self, db: Session, id: int) -> Optional[TestCase]:
        """获取测试用例"""
        return db.query(TestCase).filter(TestCase.id == id).first()

    def get_by_name(self, db: Session, name: str) -> Optional[TestCase]:
        """根据名称获取测试用例"""
        return db.query(TestCase).filter(TestCase.name == name).first()

    def get_list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        module_id: Optional[int] = None
    ) -> List[TestCase]:
        """获取测试用例列表"""
        query = db.query(TestCase)
        if module_id is not None:
            query = query.filter(TestCase.module_id == module_id)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: TestCaseCreate) -> TestCase:
        """创建测试用例"""
        db_obj = TestCase(
            name=obj_in.name,
            description=obj_in.description,
            module_id=obj_in.module_id,
            method=obj_in.method,
            path=obj_in.path,
            headers=obj_in.headers,
            params=obj_in.params,
            body=obj_in.body,
            assertions=obj_in.assertions
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: TestCase,
        obj_in: TestCaseUpdate
    ) -> TestCase:
        """更新测试用例"""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> TestCase:
        """删除测试用例"""
        obj = db.query(TestCase).get(id)
        db.delete(obj)
        db.commit()
        return obj


test_case = CRUDTestCase() 