from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class ModuleBase(BaseModel):
    """模块基础模型"""
    name: str = Field(..., description="模块名称")
    description: Optional[str] = Field(None, description="描述")


class ModuleCreate(ModuleBase):
    """创建模块请求模型"""
    pass


class ModuleUpdate(ModuleBase):
    """更新模块请求模型"""
    name: Optional[str] = Field(None, description="模块名称")


class Module(ModuleBase):
    """模块响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class ModuleVariableBase(BaseModel):
    """模块变量基础模型"""
    name: str = Field(..., description="变量名")
    value: str = Field(..., description="变量值")
    description: Optional[str] = Field(None, description="描述")
    extractor: Optional[Dict] = Field(None, description="提取器配置")


class ModuleVariableCreate(ModuleVariableBase):
    """创建模块变量请求模型"""
    pass


class ModuleVariableUpdate(ModuleVariableBase):
    """更新模块变量请求模型"""
    name: Optional[str] = Field(None, description="变量名")
    value: Optional[str] = Field(None, description="变量值")


class ModuleVariable(ModuleVariableBase):
    """模块变量响应模型"""
    id: int
    module_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


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
    pass


class TestCaseUpdate(TestCaseBase):
    """更新测试用例请求模型"""
    name: Optional[str] = Field(None, description="用例名称")
    description: Optional[str] = Field(None, description="用例描述")
    method: Optional[str] = Field(None, description="请求方法")
    path: Optional[str] = Field(None, description="请求路径")


class TestCase(TestCaseBase):
    """测试用例响应模型"""
    id: int
    module_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    ) 