from typing import Dict, Any
from datetime import datetime, timedelta
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.test_case import TestCase
from app.models.execution import Execution, ExecutionStatus
from app.models.report import Report


class CRUDDashboard:
    async def get_test_case_stats(self, db: AsyncSession) -> Dict[str, Any]:
        """获取测试用例统计信息"""
        # 获取测试用例总数
        total_count = await db.scalar(select(func.count(TestCase.id))) or 0
        
        # 获取最近7天的执行统计
        seven_days_ago = datetime.now() - timedelta(days=7)
        executions = await db.execute(
            select(Execution)
            .where(Execution.created_at >= seven_days_ago)
        )
        executions = executions.scalars().all()
        
        # 统计成功和失败数量
        success_count = sum(1 for e in executions if e.status == ExecutionStatus.SUCCESS)
        failed_count = sum(1 for e in executions if e.status == ExecutionStatus.FAILED)
        
        # 计算成功率
        success_rate = (success_count / (success_count + failed_count) * 100) if (success_count + failed_count) > 0 else 0
        
        return {
            "total_count": total_count,
            "success_count": success_count,
            "failed_count": failed_count,
            "success_rate": round(success_rate, 2)
        }

    async def get_execution_trend(self, db: AsyncSession, days: int = 7) -> Dict[str, Any]:
        """获取执行趋势数据"""
        start_date = datetime.now() - timedelta(days=days)
        
        # 获取每日执行数量
        daily_executions = await db.execute(
            select(
                func.date(Execution.created_at).label('date'),
                func.count(Execution.id).label('count')
            )
            .where(Execution.created_at >= start_date)
            .group_by(func.date(Execution.created_at))
            .order_by(func.date(Execution.created_at))
        )
        daily_executions = daily_executions.all()
        
        # 获取每日成功率
        daily_success = await db.execute(
            select(
                func.date(Execution.created_at).label('date'),
                func.count(Execution.id).label('count')
            )
            .where(
                Execution.created_at >= start_date,
                Execution.status == ExecutionStatus.SUCCESS
            )
            .group_by(func.date(Execution.created_at))
            .order_by(func.date(Execution.created_at))
        )
        daily_success = daily_success.all()
        
        # 格式化数据
        dates = [(start_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days)]
        execution_counts = [0] * days
        success_rates = [0] * days
        
        for exec_data in daily_executions:
            date = exec_data.date.strftime('%Y-%m-%d')
            if date in dates:
                idx = dates.index(date)
                execution_counts[idx] = exec_data.count
        
        for success_data in daily_success:
            date = success_data.date.strftime('%Y-%m-%d')
            if date in dates:
                idx = dates.index(date)
                total = execution_counts[idx]
                if total > 0:
                    success_rates[idx] = round((success_data.count / total) * 100, 2)
        
        return {
            "dates": dates,
            "execution_counts": execution_counts,
            "success_rates": success_rates
        }

    async def get_report_summary(self, db: AsyncSession) -> Dict[str, Any]:
        """获取报告摘要信息"""
        # 获取最近一次报告
        latest_report = await db.execute(
            select(Report)
            .order_by(Report.created_at.desc())
            .limit(1)
        )
        latest_report = latest_report.scalar_one_or_none()
        
        if not latest_report:
            return {
                "total_cases": 0,
                "passed_cases": 0,
                "failed_cases": 0,
                "duration": 0,
                "created_at": None
            }
        
        return {
            "total_cases": latest_report.total_cases,
            "passed_cases": latest_report.passed_cases,
            "failed_cases": latest_report.failed_cases,
            "duration": latest_report.duration,
            "created_at": latest_report.created_at
        }


dashboard = CRUDDashboard() 