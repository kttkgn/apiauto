from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.services.report import ReportService
from app.schemas.report import (
    Report,
    ReportCreate,
    ReportStatistics
)

router = APIRouter()


@router.get("/", response_model=List[Report])
async def get_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取报告列表"""
    service = ReportService(db)
    return await service.get_reports(
        skip=skip,
        limit=limit,
        start_time=start_time,
        end_time=end_time
    )


@router.post("/", response_model=Report)
async def create_report(
    report_in: ReportCreate,
    db: AsyncSession = Depends(get_db)
):
    """创建报告"""
    service = ReportService(db)
    return await service.create_report(report_in)


@router.get("/statistics", response_model=ReportStatistics)
async def get_statistics(
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    db: AsyncSession = Depends(get_db)
):
    """获取报告统计信息"""
    service = ReportService(db)
    return await service.get_statistics(
        start_time=start_time,
        end_time=end_time
    )


@router.get("/{report_id}", response_model=Report)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """获取报告详情"""
    service = ReportService(db)
    return await service.get_report(report_id)


@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db)
):
    """删除报告"""
    service = ReportService(db)
    await service.delete_report(report_id)
    return {"message": "报告已删除"} 