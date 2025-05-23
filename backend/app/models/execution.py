from sqlalchemy import Column, ForeignKey, JSON, String, Text, Integer
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base


class Execution(Base):
    """执行记录表"""
    
    name = Column(String(100), nullable=False, comment='执行名称')
    scope = Column(String(20), nullable=False, comment='执行范围')
    module_id = Column(Integer, ForeignKey('module.id'), comment='模块ID')
    environment_id = Column(Integer, ForeignKey('environment.id'), nullable=False, comment='环境ID')
    executor = Column(String(100), nullable=False, comment='执行人')
    params = Column(JSON, comment='执行参数')
    status = Column(String(20), nullable=False, comment='执行状态')
    progress = Column(JSON, comment='执行进度')
    result = Column(JSON, comment='执行结果')
    
    # 关联关系
    module: Mapped['Module'] = relationship('Module')
    environment: Mapped['Environment'] = relationship('Environment')
    logs: Mapped[list['ExecutionLog']] = relationship(
        'ExecutionLog',
        back_populates='execution',
        cascade='all, delete-orphan'
    )
    details: Mapped[list['ExecutionDetail']] = relationship(
        'ExecutionDetail',
        back_populates='execution',
        cascade='all, delete-orphan'
    )


class ExecutionLog(Base):
    """执行日志表"""
    
    execution_id = Column(Integer, ForeignKey('execution.id', ondelete='CASCADE'), nullable=False, comment='执行ID')
    level = Column(String(20), nullable=False, comment='日志级别')
    message = Column(Text, nullable=False, comment='日志消息')
    
    # 关联关系
    execution: Mapped[Execution] = relationship('Execution', back_populates='logs')


class ExecutionDetail(Base):
    """执行详情表"""
    
    execution_id = Column(Integer, ForeignKey('execution.id', ondelete='CASCADE'), nullable=False, comment='执行ID')
    test_case_id = Column(Integer, ForeignKey('test_case.id'), nullable=False, comment='测试用例ID')
    status = Column(String(20), nullable=False, comment='执行状态')
    request = Column(JSON, comment='请求详情')
    response = Column(JSON, comment='响应详情')
    assertions = Column(JSON, comment='断言结果')
    duration = Column(Integer, comment='执行时长(ms)')
    
    # 关联关系
    execution: Mapped[Execution] = relationship('Execution', back_populates='details')
    test_case: Mapped['TestCase'] = relationship('TestCase') 