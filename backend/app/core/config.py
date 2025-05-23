from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # 数据库配置
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "RootQwe123"
    MYSQL_DB: str = "api_auto"
    
    # Redis配置
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings() 