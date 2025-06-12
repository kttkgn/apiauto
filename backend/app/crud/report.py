from typing import List, Optional
from datetime import datetime, timedelta
from sqlalchemy import func, and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.report import Report
from app.schemas.report import ReportCreate


class CRUDReport:
    async def get(self, db: AsyncSession, id: int) -> Optional[Report]:
        """获取报告"""
        result = await db.execute(select(Report).filter(Report.id == id))
        return result.scalar_one_or_none()

    async def get_list(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> List[Report]:
        """获取报告列表"""
        query = select(Report)
        if start_time:
            query = query.filter(Report.created_at >= start_time)
        if end_time:
            query = query.filter(Report.created_at <= end_time)
        result = await db.execute(query.offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, *, obj_in: ReportCreate) -> Report:
        """创建报告"""
        db_obj = Report(
            name=obj_in.name,
            execution_id=obj_in.execution_id,
            content=obj_in.content
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> Report:
        """删除报告"""
        obj = await db.get(Report, id)
        await db.delete(obj)
        await db.commit()
        return obj

    async def get_statistics(
        self,
        db: AsyncSession,
        *,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None
    ) -> dict:
        """获取报告统计信息"""
        query = select(Report)
        if start_time:
            query = query.filter(Report.created_at >= start_time)
        if end_time:
            query = query.filter(Report.created_at <= end_time)

        # 获取总报告数
        result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = result.scalar()

        # 获取所有报告
        result = await db.execute(query)
        reports = result.scalars().all()

        # 计算成功率
        success_count = 0
        total_duration = 0
        for report in reports:
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
                day_query = select(Report).filter(
                    and_(
                        Report.created_at >= current,
                        Report.created_at < next_day
                    )
                )
                result = await db.execute(day_query)
                day_reports = result.scalars().all()

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