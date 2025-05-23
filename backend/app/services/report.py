from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.crud.report import report
from app.schemas.report import ReportCreate


class ReportService:
    def __init__(self, db: Session):
        self.db = db

    async def get_report(self, report_id: int):
        """获取报告详情"""
        db_report = report.get(self.db, id=report_id)
        if not db_report:
            raise HTTPException(status_code=404, detail="报告不存在")
        return db_report

    async def get_reports(
        self,
        skip: int = 0,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        """获取报告列表"""
        return report.get_list(
            self.db,
            skip=skip,
            limit=limit,
            start_time=start_time,
            end_time=end_time
        )

    async def create_report(self, report_in: ReportCreate):
        """创建报告"""
        return report.create(self.db, obj_in=report_in)

    async def delete_report(self, report_id: int):
        """删除报告"""
        db_report = report.get(self.db, id=report_id)
        if not db_report:
            raise HTTPException(status_code=404, detail="报告不存在")
        return report.remove(self.db, id=report_id)

    async def get_statistics(
        self,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ):
        """获取报告统计信息"""
        return report.get_statistics(
            self.db,
            start_time=start_time,
            end_time=end_time
        ) 