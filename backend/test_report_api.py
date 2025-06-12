#!/usr/bin/env python3
"""
测试报告API的脚本
"""
import asyncio
import httpx
import json


async def test_report_api():
    """测试报告API"""
    base_url = "http://127.0.0.1:8001"
    
    async with httpx.AsyncClient() as client:
        print("=== 测试报告API ===")
        
        # 1. 测试获取报告列表
        print("\n1. 测试获取报告列表...")
        try:
            response = await client.get(f"{base_url}/api/reports/")
            
            if response.status_code == 200:
                reports = response.json()
                print(f"✅ 获取报告列表成功")
                print(f"   找到 {len(reports)} 个报告")
                for report in reports:
                    print(f"   - ID: {report.get('id')}, 名称: {report.get('name')}")
            else:
                print(f"❌ 获取报告列表失败: {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 获取报告列表异常: {e}")
        
        # 2. 测试获取报告统计
        print("\n2. 测试获取报告统计...")
        try:
            response = await client.get(f"{base_url}/api/reports/statistics")
            
            if response.status_code == 200:
                stats = response.json()
                print(f"✅ 获取报告统计成功")
                print(f"   总报告数: {stats.get('total', 0)}")
                print(f"   成功率: {stats.get('success_rate', 0)}%")
                print(f"   平均时长: {stats.get('avg_duration', 0)}ms")
            else:
                print(f"❌ 获取报告统计失败: {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 获取报告统计异常: {e}")


if __name__ == "__main__":
    asyncio.run(test_report_api()) 