from typing import Any
from datetime import datetime

from sqlalchemy import Column, ForeignKey, JSON, String, Text, Integer, DateTime
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base
from app.models.test_case import TestCase


class Module(Base):
    """模块表"""
    __tablename__ = "modules"
    
    name = Column(String(100), nullable=False, comment='模块名称')
    description = Column(Text, nullable=True, comment='描述')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联关系
    variables: Mapped[list['ModuleVariable']] = relationship(
        'ModuleVariable',
        back_populates='module',
        cascade='all, delete-orphan'
    )
    test_cases: Mapped[list['TestCase']] = relationship(
        'TestCase',
        back_populates='module',
        cascade='all, delete-orphan'
    )
    executions: Mapped[list['Execution']] = relationship(
        'Execution',
        back_populates='module'
    )

    def __repr__(self):
        return f"<Module {self.name}>"


class ModuleVariable(Base):
    """模块变量表"""
    __tablename__ = "module_variables"
    
    name = Column(String(100), nullable=False, comment='变量名')
    value = Column(String(500), nullable=False, comment='变量值')
    description = Column(Text, nullable=True, comment='描述')
    extractor = Column(JSON, nullable=True, comment='提取器配置')
    module_id = Column(Integer, ForeignKey('modules.id', ondelete='CASCADE'), nullable=False, comment='模块ID')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关联关系
    module: Mapped[Module] = relationship('Module', back_populates='variables')
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not self.value.startswith('${') and not self.value.endswith('}'):
            self.value = f'${{{self.value}}}' 