from typing import Dict, List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class EnvironmentBase(BaseModel):
    """环境基础模型"""
    name: str = Field(..., description="环境名称")
    base_url: str = Field(..., description="基础URL")
    headers: Optional[Dict] = Field(None, description="公共请求头")


class EnvironmentCreate(EnvironmentBase):
    """创建环境请求模型"""
    pass


class EnvironmentUpdate(EnvironmentBase):
    """更新环境请求模型"""
    name: Optional[str] = Field(None, description="环境名称")
    base_url: Optional[str] = Field(None, description="基础URL")


class Environment(EnvironmentBase):
    """环境响应模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    )


class EnvironmentVariableBase(BaseModel):
    """环境变量基础模型"""
    name: str = Field(..., description="变量名")
    value: str = Field(..., description="变量值")
    description: Optional[str] = Field(None, description="描述")
    extractor: Optional[Dict] = Field(None, description="提取器配置")


class EnvironmentVariableCreate(EnvironmentVariableBase):
    """创建环境变量请求模型"""
    pass


class EnvironmentVariableUpdate(EnvironmentVariableBase):
    """更新环境变量请求模型"""
    name: Optional[str] = Field(None, description="变量名")
    value: Optional[str] = Field(None, description="变量值")


class EnvironmentVariable(EnvironmentVariableBase):
    """环境变量响应模型"""
    id: int
    environment_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda v: v.isoformat() if v else None
        }
    ) 