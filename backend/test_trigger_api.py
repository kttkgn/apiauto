#!/usr/bin/env python3
"""
测试 trigger API 的脚本
"""
import asyncio
import httpx
import json


async def test_trigger_api():
    """测试 trigger API"""
    base_url = "http://127.0.0.1:8001"
    
    async with httpx.AsyncClient() as client:
        print("=== 测试 Trigger API ===")
        
        # 1. 测试批量执行API
        print("\n1. 测试批量执行API...")
        try:
            # 使用查询参数传递列表
            params = {
                "test_case_ids": [1, 2],  # 假设存在的测试用例ID
                "environment_id": 1,
                "executor": "test_user"
            }
            
            response = await client.post(
                f"{base_url}/api/trigger/batch",
                params=params
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 批量执行API调用成功")
                print(f"   执行ID: {result.get('execution_id')}")
                print(f"   消息: {result.get('message')}")
            elif response.status_code == 400:
                result = response.json()
                print(f"⚠️  批量执行API返回400: {result.get('detail')}")
            else:
                print(f"❌ 批量执行API调用失败: {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 批量执行API异常: {e}")
        
        # 2. 测试快速测试API
        print("\n2. 测试快速测试API...")
        try:
            response = await client.post(
                f"{base_url}/api/trigger/quick-test",
                params={
                    "test_case_id": 1,  # 假设存在的测试用例ID
                    "environment_id": 1
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 快速测试API调用成功")
                print(f"   成功: {result.get('success')}")
                print(f"   执行ID: {result.get('execution_id')}")
                print(f"   状态: {result.get('status')}")
            elif response.status_code == 404:
                result = response.json()
                print(f"⚠️  快速测试API返回404: {result.get('detail')}")
            else:
                print(f"❌ 快速测试API调用失败: {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 快速测试API异常: {e}")
        
        # 3. 测试执行状态API
        print("\n3. 测试执行状态API...")
        try:
            response = await client.get(f"{base_url}/api/trigger/status/1")
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ 执行状态API调用成功")
                print(f"   执行ID: {result.get('execution_id')}")
                print(f"   名称: {result.get('name')}")
                print(f"   状态: {result.get('status')}")
                print(f"   进度: {result.get('progress')}")
            elif response.status_code == 404:
                result = response.json()
                print(f"⚠️  执行状态API返回404: {result.get('detail')}")
            else:
                print(f"❌ 执行状态API调用失败: {response.status_code}")
                print(f"   响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 执行状态API异常: {e}")


if __name__ == "__main__":
    asyncio.run(test_trigger_api()) 