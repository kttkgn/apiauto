from typing import Dict, List, Optional
from pydantic import BaseModel, Field


class TestCaseBase(BaseModel):
    """测试用例基础模型"""
    name: str = Field(..., description="用例名称")
    description: Optional[str] = Field(None, description="用例描述")
    method: str = Field(..., description="请求方法")
    path: str = Field(..., description="请求路径")
    headers: Optional[Dict] = Field(None, description="请求头")
    params: Optional[Dict] = Field(None, description="请求参数")
    body: Optional[Dict] = Field(None, description="请求体")
    assertions: Optional[Dict] = Field(None, description="断言规则")


class TestCaseCreate(TestCaseBase):
    """创建测试用例请求模型"""
    module_id: int = Field(..., description="所属模块ID")


class TestCaseUpdate(TestCaseBase):
    """更新测试用例请求模型"""
    module_id: Optional[int] = Field(None, description="所属模块ID")


class TestCase(TestCaseBase):
    """测试用例响应模型"""
    id: int
    module_id: int
    created_at: str
    updated_at: str

    class Config:
        from_attributes = True 