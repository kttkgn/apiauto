from typing import Any

from sqlalchemy import Column, ForeignKey, JSON, String, Text, Integer
from sqlalchemy.orm import Mapped, relationship

from app.models.base import Base


class Module(Base):
    """模块表"""
    
    name = Column(String(100), nullable=False, unique=True, comment='模块名称')
    description = Column(String(255), comment='描述')
    
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

    def __repr__(self):
        return f"<Module {self.name}>"


class ModuleVariable(Base):
    """模块变量表"""
    
    module_id = Column(Integer, ForeignKey('module.id', ondelete='CASCADE'), nullable=False, comment='模块ID')
    name = Column(String(100), nullable=False, comment='变量名')
    value = Column(Text, nullable=False, comment='变量值')
    description = Column(String(255), comment='描述')
    extractor = Column(JSON, comment='提取器配置')
    
    # 关联关系
    module: Mapped[Module] = relationship('Module', back_populates='variables')
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        if not self.value.startswith('${') and not self.value.endswith('}'):
            self.value = f'${{{self.value}}}'


class TestCase(Base):
    """测试用例表"""
    
    module_id = Column(Integer, ForeignKey('module.id', ondelete='CASCADE'), nullable=False, comment='模块ID')
    name = Column(String(100), nullable=False, comment='用例名称')
    description = Column(String(255), comment='描述')
    method = Column(String(10), nullable=False, comment='请求方法')
    path = Column(String(255), nullable=False, comment='请求路径')
    headers = Column(JSON, comment='请求头')
    params = Column(JSON, comment='请求参数')
    body = Column(JSON, comment='请求体')
    assertions = Column(JSON, comment='断言配置')
    
    # 关联关系
    module: Mapped[Module] = relationship('Module', back_populates='test_cases') 