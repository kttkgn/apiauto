from datetime import datetime
from sqlalchemy import Column, ForeignKey, JSON, String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base


class Report(Base):
    """测试报告表"""
    __tablename__ = "reports"
    
    name = Column(String(100), nullable=False, comment='报告名称')
    execution_id = Column(Integer, ForeignKey('executions.id'), nullable=False, comment='执行ID')
    content = Column(JSON, comment='报告内容')
    total_cases = Column(Integer, nullable=False, default=0, comment='总用例数')
    passed_cases = Column(Integer, nullable=False, default=0, comment='通过用例数')
    failed_cases = Column(Integer, nullable=False, default=0, comment='失败用例数')
    duration = Column(Integer, nullable=True, comment='执行时长(秒)')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    
    # 关联关系
    execution: Mapped['Execution'] = relationship('Execution', back_populates='reports') 