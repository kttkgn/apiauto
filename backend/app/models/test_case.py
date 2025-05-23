from sqlalchemy import Column, Integer, String, JSON, ForeignKey, Text
from sqlalchemy.orm import relationship

from app.models.base import Base


class TestCase(Base):
    """测试用例模型"""
    __tablename__ = "test_cases"

    name = Column(String(100), nullable=False, comment="用例名称")
    description = Column(Text, nullable=True, comment="用例描述")
    module_id = Column(Integer, ForeignKey("modules.id"), nullable=False, comment="所属模块ID")
    method = Column(String(10), nullable=False, comment="请求方法")
    path = Column(String(200), nullable=False, comment="请求路径")
    headers = Column(JSON, nullable=True, comment="请求头")
    params = Column(JSON, nullable=True, comment="请求参数")
    body = Column(JSON, nullable=True, comment="请求体")
    assertions = Column(JSON, nullable=True, comment="断言规则")

    # 关联关系
    module = relationship("Module", back_populates="test_cases")
    execution_details = relationship("ExecutionDetail", back_populates="test_case")

    def __repr__(self):
        return f"<TestCase {self.name}>" 