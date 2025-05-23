from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.models.report import Report
from app.schemas.report import ReportCreate


class CRUDReport:
    def get(self, db: Session, id: int) -> Optional[Report]:
        """获取报告"""
        return db.query(Report).filter(Report.id == id).first()

    def get_list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Report]:
        """获取报告列表"""
        query = db.query(Report)
        if start_time:
            query = query.filter(Report.created_at >= start_time)
        if end_time:
            query = query.filter(Report.created_at <= end_time)
        return query.offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: ReportCreate) -> Report:
        """创建报告"""
        db_obj = Report(
            name=obj_in.name,
            execution_id=obj_in.execution_id,
            content=obj_in.content
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> Report:
        """删除报告"""
        obj = db.query(Report).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_statistics(
        self,
        db: Session,
        *,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """获取报告统计信息"""
        query = db.query(Report)
        if start_time:
            query = query.filter(Report.created_at >= start_time)
        if end_time:
            query = query.filter(Report.created_at <= end_time)

        # 获取总报告数
        total = query.count()

        # 计算成功率
        success_count = 0
        total_duration = 0
        for report in query.all():
            content = report.content
            if content.get("summary", {}).get("passed", 0) == content.get("summary", {}).get("total", 0):
                success_count += 1
            total_duration += content.get("summary", {}).get("duration", 0)

        success_rate = (success_count / total * 100) if total > 0 else 0
        avg_duration = total_duration / total if total > 0 else 0

        # 获取趋势数据
        trend = []
        if start_time and end_time:
            current = start_time
            while current <= end_time:
                next_day = current + timedelta(days=1)
                day_reports = query.filter(
                    and_(
                        Report.created_at >= current,
                        Report.created_at < next_day
                    )
                ).all()

                day_total = len(day_reports)
                day_passed = sum(
                    1 for r in day_reports
                    if r.content.get("summary", {}).get("passed", 0) == r.content.get("summary", {}).get("total", 0)
                )
                day_failed = day_total - day_passed

                trend.append({
                    "date": current.strftime("%Y-%m-%d"),
                    "total": day_total,
                    "passed": day_passed,
                    "failed": day_failed
                })
                current = next_day

        return {
            "total": total,
            "success_rate": round(success_rate, 2),
            "avg_duration": round(avg_duration),
            "trend": trend
        }


report = CRUDReport() 