from datetime import datetime
from enum import Enum
from sqlalchemy import Column, ForeignKey, JSON, String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base


class ExecutionStatus(str, Enum):
    """执行状态枚举"""
    PENDING = "pending"  # 等待执行
    RUNNING = "running"  # 执行中
    SUCCESS = "success"  # 执行成功
    FAILED = "failed"    # 执行失败
    SKIPPED = "skipped"  # 跳过执行


class Execution(Base):
    """执行记录表"""
    __tablename__ = "executions"
    
    name = Column(String(100), nullable=False, comment='执行名称')
    scope = Column(String(20), nullable=False, comment='执行范围')
    case_id = Column(Integer, ForeignKey('test_cases.id'), nullable=True, comment='测试用例ID')
    module_id = Column(Integer, ForeignKey('modules.id'), nullable=True, comment='模块ID')
    environment_id = Column(Integer, ForeignKey('environments.id'), nullable=False, comment='环境ID')
    executor = Column(String(100), nullable=False, comment='执行人')
    params = Column(JSON, comment='执行参数')
    status = Column(String(20), nullable=False, default=ExecutionStatus.PENDING, comment='执行状态')
    progress = Column(JSON, comment='执行进度')
    result = Column(JSON, comment='执行结果')
    start_time = Column(DateTime, nullable=True, comment='开始时间')
    end_time = Column(DateTime, nullable=True, comment='结束时间')
    duration = Column(Integer, nullable=True, comment='执行时长(秒)')
    total_cases = Column(Integer, nullable=False, default=0, comment='总用例数')
    passed_cases = Column(Integer, nullable=False, default=0, comment='通过用例数')
    failed_cases = Column(Integer, nullable=False, default=0, comment='失败用例数')
    skipped_cases = Column(Integer, nullable=False, default=0, comment='跳过用例数')
    error_message = Column(Text, nullable=True, comment='错误信息')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    test_case = relationship('TestCase', foreign_keys=[case_id])
    module = relationship('Module', back_populates='executions')
    environment = relationship('Environment', back_populates='executions')
    logs = relationship(
        'ExecutionLog',
        back_populates='execution',
        cascade='all, delete-orphan'
    )
    details = relationship(
        'ExecutionDetail',
        back_populates='execution',
        cascade='all, delete-orphan'
    )
    reports = relationship(
        'Report',
        back_populates='execution',
        cascade='all, delete-orphan'
    )


class ExecutionLog(Base):
    """执行日志表"""
    __tablename__ = "execution_logs"
    
    execution_id = Column(Integer, ForeignKey('executions.id', ondelete='CASCADE'), nullable=False, comment='执行ID')
    level = Column(String(20), nullable=False, comment='日志级别')
    message = Column(Text, nullable=False, comment='日志消息')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    
    # 关联关系
    execution = relationship('Execution', back_populates='logs')


class ExecutionDetail(Base):
    """执行详情表"""
    __tablename__ = "execution_details"
    
    execution_id = Column(Integer, ForeignKey('executions.id', ondelete='CASCADE'), nullable=False, comment='执行ID')
    test_case_id = Column(Integer, ForeignKey('test_cases.id'), nullable=False, comment='测试用例ID')
    status = Column(String(20), nullable=False, default=ExecutionStatus.PENDING, comment='执行状态')
    request = Column(JSON, comment='请求详情')
    response = Column(JSON, comment='响应详情')
    assertions = Column(JSON, comment='断言结果')
    duration = Column(Integer, comment='执行时长(ms)')
    start_time = Column(DateTime, nullable=True, comment='开始时间')
    end_time = Column(DateTime, nullable=True, comment='结束时间')
    error_message = Column(Text, nullable=True, comment='错误信息')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    # 关联关系
    execution = relationship('Execution', back_populates='details')
    test_case = relationship('TestCase', back_populates='execution_details') 