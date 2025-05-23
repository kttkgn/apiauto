from datetime import datetime
from typing import Any

from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """基础模型类"""
    
    @declared_attr
    def __tablename__(cls) -> str:
        """表名默认为类名小写"""
        return cls.__name__.lower()
    
    id = Column(Integer, primary_key=True, autoincrement=True, comment='主键ID')
    created_at = Column(DateTime, nullable=False, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    
    def to_dict(self) -> dict[str, Any]:
        """转换为字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns} 