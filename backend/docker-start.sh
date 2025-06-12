#!/bin/bash

# 接口自动化平台 Docker 启动脚本

set -e

echo "🚀 启动接口自动化平台..."

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

# 检查 Docker Compose 是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 选择启动模式
echo "请选择启动模式："
echo "1) 完整模式（包含 Nginx 反向代理）"
echo "2) 简化模式（仅核心服务）"
read -p "请输入选择 (1/2): " choice

case $choice in
    1)
        echo "📦 启动完整模式..."
        docker-compose up -d
        ;;
    2)
        echo "📦 启动简化模式..."
        docker-compose -f docker-compose.simple.yml up -d
        ;;
    *)
        echo "❌ 无效选择，使用简化模式"
        docker-compose -f docker-compose.simple.yml up -d
        ;;
esac

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 10

# 检查服务状态
echo "🔍 检查服务状态..."
docker-compose ps

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "📋 访问地址："
echo "  - API 文档: http://localhost:8001/docs"
echo "  - 健康检查: http://localhost:8001/health"
echo "  - 数据库: localhost:3306"
echo "  - Redis: localhost:6379"
echo ""
echo "📝 常用命令："
echo "  - 查看日志: docker-compose logs -f"
echo "  - 停止服务: docker-compose down"
echo "  - 重启服务: docker-compose restart"
echo "  - 查看状态: docker-compose ps" 