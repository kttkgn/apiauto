from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.dashboard import DashboardService
from app.schemas.dashboard import DashboardStats

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: Session = Depends(get_db),
):
    """获取首页统计数据"""
    return await DashboardService(db).get_stats() 