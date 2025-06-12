from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.dashboard import dashboard


class DashboardService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_stats(self) -> Dict[str, Any]:
        """获取仪表盘统计数据"""
        # 获取测试用例统计
        test_case_stats = await dashboard.get_test_case_stats(self.db)
        
        # 获取执行趋势
        execution_trend = await dashboard.get_execution_trend(self.db)
        
        # 获取报告摘要
        report_summary = await dashboard.get_report_summary(self.db)
        
        # 构建符合schema的数据结构
        return {
            "test_cases": {
                "total_count": test_case_stats.get("total_count", 0),
                "today_new": 0  # 暂时设为0，后续可以添加今日新增统计
            },
            "executions": {
                "total_count": sum(execution_trend.get("execution_counts", [])),
                "today_count": execution_trend.get("execution_counts", [0])[-1] if execution_trend.get("execution_counts") else 0
            },
            "success_rates": {
                "total_rate": test_case_stats.get("success_rate", 0),
                "today_rate": execution_trend.get("success_rates", [0])[-1] if execution_trend.get("success_rates") else 0
            }
        } 