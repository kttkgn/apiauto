#!/usr/bin/env python3
"""
数据库管理脚本
使用方法:
    python -m app.db.manage init    # 初始化数据库
    python -m app.db.manage reset   # 重置数据库
    python -m app.db.manage drop    # 删除所有表
"""

import asyncio
import sys
import logging
from app.db.init_db import init_db, drop_db, reset_db

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def main():
    """主函数"""
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  python -m app.db.manage init    # 初始化数据库")
        print("  python -m app.db.manage reset   # 重置数据库")
        print("  python -m app.db.manage drop    # 删除所有表")
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "init":
            logger.info("开始初始化数据库...")
            await init_db()
            logger.info("数据库初始化完成")
            
        elif command == "reset":
            logger.info("开始重置数据库...")
            await reset_db()
            logger.info("数据库重置完成")
            
        elif command == "drop":
            logger.warning("即将删除所有数据库表，此操作不可逆！")
            confirm = input("确认删除所有表？(输入 'yes' 确认): ")
            if confirm.lower() == 'yes':
                logger.info("开始删除数据库表...")
                await drop_db()
                logger.info("数据库表删除完成")
            else:
                logger.info("操作已取消")
                
        else:
            logger.error(f"未知命令: {command}")
            print("可用命令: init, reset, drop")
            
    except Exception as e:
        logger.error(f"操作失败: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 