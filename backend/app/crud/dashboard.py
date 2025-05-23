from datetime import date
from sqlalchemy import func, and_
from sqlalchemy.orm import Session

from app.models.test_case import TestCase
from app.models.execution import Execution, ExecutionDetail


class CRUDDashboard:
    def get_test_case_stats(self, db: Session):
        """获取测试用例统计"""
        # 获取总用例数
        total_count = db.query(func.count(TestCase.id)).scalar() or 0
        
        # 获取今日新增用例数
        today = date.today()
        today_new = db.query(func.count(TestCase.id)).filter(
            func.date(TestCase.created_at) == today
        ).scalar() or 0
        
        return {
            "total_count": total_count,
            "today_new": today_new
        }

    def get_execution_stats(self, db: Session):
        """获取执行统计"""
        # 获取总执行次数
        total_count = db.query(func.count(Execution.id)).scalar() or 0
        
        # 获取今日执行次数
        today = date.today()
        today_count = db.query(func.count(Execution.id)).filter(
            func.date(Execution.created_at) == today
        ).scalar() or 0
        
        return {
            "total_count": total_count,
            "today_count": today_count
        }

    def get_success_rate_stats(self, db: Session):
        """获取成功率统计"""
        # 获取总成功率
        total_executions = db.query(func.count(Execution.id)).scalar() or 0
        total_success = db.query(func.count(Execution.id)).filter(
            Execution.status == "success"
        ).scalar() or 0
        total_rate = (total_success / total_executions * 100) if total_executions > 0 else 0
        
        # 获取今日成功率
        today = date.today()
        today_executions = db.query(func.count(Execution.id)).filter(
            func.date(Execution.created_at) == today
        ).scalar() or 0
        today_success = db.query(func.count(Execution.id)).filter(
            and_(
                func.date(Execution.created_at) == today,
                Execution.status == "success"
            )
        ).scalar() or 0
        today_rate = (today_success / today_executions * 100) if today_executions > 0 else 0
        
        return {
            "total_rate": round(total_rate, 2),
            "today_rate": round(today_rate, 2)
        }

    def get_stats(self, db: Session):
        """获取所有统计数据"""
        return {
            "test_cases": self.get_test_case_stats(db),
            "executions": self.get_execution_stats(db),
            "success_rates": self.get_success_rate_stats(db)
        }


dashboard = CRUDDashboard() 