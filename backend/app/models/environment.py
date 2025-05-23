from typing import Any

from sqlalchemy import Column, ForeignKey, JSON, String, Text, Integer
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base


class Environment(Base):
    """环境配置表"""
    
    name = Column(String(100), nullable=False, unique=True, comment='环境名称')
    base_url = Column(String(255), nullable=False, comment='基础URL')
    headers = Column(JSON, comment='公共请求头')
    
    # 关联关系
    variables: Mapped[list['EnvironmentVariable']] = relationship(
        'EnvironmentVariable',
        back_populates='environment',
        cascade='all, delete-orphan'
    )


class EnvironmentVariable(Base):
    """环境变量表"""
    
    environment_id = Column(Integer, ForeignKey('environment.id', ondelete='CASCADE'), nullable=False, comment='环境ID')
    name = Column(String(100), nullable=False, comment='变量名')
    value = Column(Text, nullable=False, comment='变量值')
    description = Column(String(255), comment='描述')
    extractor = Column(JSON, comment='提取器配置')
    
    # 关联关系
    environment: Mapped[Environment] = relationship('Environment', back_populates='variables')
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not self.value.startswith('${') and not self.value.endswith('}'):
            self.value = f'${{{self.value}}}' 