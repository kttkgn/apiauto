import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from app.db.session import engine
from app.models.base import Base
from app.models.environment import Environment, EnvironmentVariable
from app.models.module import Module, ModuleVariable
from app.models.test_case import TestCase
from app.models.execution import Execution, ExecutionLog, ExecutionDetail
from app.models.report import Report

logger = logging.getLogger(__name__)


async def init_db() -> None:
    """初始化数据库"""
    try:
        # 创建所有表
        async with engine.begin() as conn:
            # 创建表结构
            await conn.run_sync(Base.metadata.create_all)
            logger.info("数据库表创建成功")
            
            # 检查是否需要初始化基础数据
            await _init_basic_data(conn)
            
    except Exception as e:
        logger.error(f"数据库初始化失败: {str(e)}")
        raise


async def _init_basic_data(conn) -> None:
    """初始化基础数据"""
    try:
        # 检查是否已有环境配置
        result = await conn.execute(text("SELECT COUNT(*) FROM environments"))
        count = result.scalar()
        
        if count == 0:
            # 创建默认环境配置
            await conn.execute(text("""
                INSERT INTO environments (name, base_url, headers, created_at, updated_at) 
                VALUES 
                ('开发环境', 'http://localhost:8080', '{"Content-Type": "application/json"}', NOW(), NOW()),
                ('测试环境', 'http://test-api.example.com', '{"Content-Type": "application/json"}', NOW(), NOW()),
                ('预发布环境', 'http://staging-api.example.com', '{"Content-Type": "application/json"}', NOW(), NOW())
            """))
            
            # 创建默认模块
            await conn.execute(text("""
                INSERT INTO modules (name, description, created_at, updated_at) 
                VALUES 
                ('用户管理', '用户相关的接口测试', NOW(), NOW()),
                ('订单管理', '订单相关的接口测试', NOW(), NOW()),
                ('商品管理', '商品相关的接口测试', NOW(), NOW())
            """))
            
            logger.info("基础数据初始化成功")
        else:
            logger.info("数据库已有数据，跳过基础数据初始化")
            
    except Exception as e:
        logger.warning(f"基础数据初始化失败: {str(e)}")


async def drop_db() -> None:
    """删除所有表（谨慎使用）"""
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            logger.info("数据库表删除成功")
    except Exception as e:
        logger.error(f"数据库表删除失败: {str(e)}")
        raise


async def reset_db() -> None:
    """重置数据库（删除并重新创建所有表）"""
    try:
        await drop_db()
        await init_db()
        logger.info("数据库重置成功")
    except Exception as e:
        logger.error(f"数据库重置失败: {str(e)}")
        raise 