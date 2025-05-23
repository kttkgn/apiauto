from sqlalchemy import Column, ForeignKey, JSON, String, Text, Integer
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base


class Report(Base):
    """测试报告表"""
    
    name = Column(String(100), nullable=False, comment='报告名称')
    execution_id = Column(Integer, ForeignKey('execution.id'), nullable=False, comment='执行ID')
    content = Column(JSON, comment='报告内容')
    
    # 关联关系
    execution: Mapped['Execution'] = relationship('Execution') 