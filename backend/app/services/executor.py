import asyncio
import json
import time
from typing import Dict, List, Optional, Any
import httpx
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.environment import Environment, EnvironmentVariable
from app.models.module import Module, ModuleVariable
from app.models.test_case import TestCase
from app.models.execution import Execution, ExecutionLog, ExecutionDetail
from app.services.execution import ExecutionService
from app.schemas.execution import ExecutionCreate, ExecutionUpdate, ExecutionLogCreate, ExecutionDetailCreate
from app.crud.environment import environment
from app.crud.module import module
from app.crud.test_case import test_case as test_case_crud


class VariableExtractor:
    """变量提取器"""
    
    @staticmethod
    def extract_variable(response: Dict, extractor: Dict) -> Optional[str]:
        """从响应中提取变量"""
        try:
            source = extractor.get('source')
            expression = extractor.get('expression')
            
            if source == 'response_body':
                return VariableExtractor._extract_jsonpath(response.get('body', {}), expression)
            elif source == 'response_headers':
                headers = response.get('headers', {})
                return headers.get(expression)
            else:
                return None
        except (KeyError, TypeError, ValueError):
            return None
    
    @staticmethod
    def _extract_jsonpath(data: Dict, expression: str) -> Optional[str]:
        """简单的JSONPath提取实现"""
        if not expression.startswith('$.'):
            return None
            
        path = expression[2:]  # 去掉 '$.'
        keys = path.split('.')
        
        current = data
        for key in keys:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                return None
                
        return str(current) if current is not None else None


class RequestBuilder:
    """请求构建器"""
    
    def __init__(self, environment: Environment, module_vars: Dict[str, str] = None):
        self.environment = environment
        self.module_vars = module_vars or {}
        self.extracted_vars = {}
    
    def build_request(self, test_case: TestCase) -> Dict[str, Any]:
        """构建HTTP请求"""
        # 合并变量
        all_vars = {}
        all_vars.update(self.module_vars)
        all_vars.update(self.extracted_vars)
        
        # 构建URL
        url = self._replace_variables(f"{self.environment.base_url}{test_case.path}", all_vars)
        
        # 构建请求头
        headers = {}
        if self.environment.headers:
            headers.update(self.environment.headers)
        if test_case.headers:
            headers.update(test_case.headers)
        
        # 替换请求头中的变量
        headers = self._replace_variables_in_dict(headers, all_vars)
        
        # 构建请求参数
        params = {}
        if test_case.params:
            params = self._replace_variables_in_dict(test_case.params, all_vars)
        
        # 构建请求体
        body = None
        if test_case.body:
            body = self._replace_variables_in_dict(test_case.body, all_vars)
        
        return {
            'method': test_case.method,
            'url': url,
            'headers': headers,
            'params': params,
            'json': body if body and headers.get('Content-Type') == 'application/json' else None,
            'data': body if body and headers.get('Content-Type') != 'application/json' else None
        }
    
    def _replace_variables(self, text: str, variables: Dict[str, str]) -> str:
        """替换文本中的变量"""
        if not isinstance(text, str):
            return text
            
        for var_name, var_value in variables.items():
            placeholder = f"${{{var_name}}}"
            text = text.replace(placeholder, str(var_value))
        
        return text
    
    def _replace_variables_in_dict(self, data: Dict, variables: Dict[str, str]) -> Dict:
        """递归替换字典中的变量"""
        if not isinstance(data, dict):
            return data
            
        result = {}
        for key, value in data.items():
            if isinstance(value, str):
                result[key] = self._replace_variables(value, variables)
            elif isinstance(value, dict):
                result[key] = self._replace_variables_in_dict(value, variables)
            elif isinstance(value, list):
                result[key] = [self._replace_variables_in_dict(item, variables) if isinstance(item, dict) else item for item in value]
            else:
                result[key] = value
        
        return result
    
    def update_extracted_vars(self, new_vars: Dict[str, str]):
        """更新提取的变量"""
        self.extracted_vars.update(new_vars)


class AssertionChecker:
    """断言检查器"""
    
    @staticmethod
    def check_assertions(response: Dict, assertions: List[Dict]) -> Dict[str, Any]:
        """检查断言"""
        if not assertions:
            return {'passed': True, 'results': []}
        
        results = []
        all_passed = True
        
        for assertion in assertions:
            result = AssertionChecker._check_single_assertion(response, assertion)
            results.append(result)
            if not result['passed']:
                all_passed = False
        
        return {
            'passed': all_passed,
            'results': results
        }
    
    @staticmethod
    def _check_single_assertion(response: Dict, assertion: Dict) -> Dict[str, Any]:
        """检查单个断言"""
        assertion_type = assertion.get('type')
        expected = assertion.get('expected')
        actual = None
        
        try:
            if assertion_type == 'status_code':
                actual = response.get('status_code')
            elif assertion_type == 'response_body':
                expression = assertion.get('expression')
                if expression:
                    actual = VariableExtractor._extract_jsonpath(response.get('body', {}), expression)
            elif assertion_type == 'response_headers':
                headers = response.get('headers', {})
                actual = headers.get(assertion.get('header_name'))
            elif assertion_type == 'response_time':
                actual = response.get('duration')
            else:
                return {
                    'passed': False,
                    'message': f'不支持的断言类型: {assertion_type}'
                }
            
            # 比较实际值和期望值
            passed = AssertionChecker._compare_values(actual, expected, assertion.get('operator', 'equals'))
            
            return {
                'passed': passed,
                'type': assertion_type,
                'expected': expected,
                'actual': actual,
                'operator': assertion.get('operator', 'equals')
            }
            
        except Exception as e:
            return {
                'passed': False,
                'message': f'断言检查失败: {str(e)}'
            }
    
    @staticmethod
    def _compare_values(actual: Any, expected: Any, operator: str) -> bool:
        """比较值"""
        try:
            if operator == 'equals':
                return actual == expected
            elif operator == 'not_equals':
                return actual != expected
            elif operator == 'contains':
                return str(expected) in str(actual)
            elif operator == 'not_contains':
                return str(expected) not in str(actual)
            elif operator == 'greater_than':
                return float(actual) > float(expected)
            elif operator == 'less_than':
                return float(actual) < float(expected)
            elif operator == 'greater_than_or_equal':
                return float(actual) >= float(expected)
            elif operator == 'less_than_or_equal':
                return float(actual) <= float(expected)
            else:
                return False
        except (ValueError, TypeError):
            return False


class TestExecutor:
    """测试执行器"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.execution_service = ExecutionService(db)
    
    async def execute_single_case(self, test_case_id: int, environment_id: int, executor: str = "system") -> Execution:
        """执行单个测试用例"""
        # 获取测试用例
        test_case = await test_case_crud.get(self.db, id=test_case_id)
        if not test_case:
            raise HTTPException(status_code=404, detail="测试用例不存在")
        
        # 获取环境配置
        env = await environment.get(self.db, id=environment_id)
        if not env:
            raise HTTPException(status_code=404, detail="环境配置不存在")
        
        # 创建执行记录
        execution_data = ExecutionCreate(
            name=f"执行测试用例: {test_case.name}",
            scope='single',
            case_id=test_case_id,
            environment_id=environment_id,
            executor=executor,
            status='running',
            progress={'current': 1, 'total': 1}
        )
        
        execution = await self.execution_service.create_execution(execution_data)
        
        try:
            # 执行测试
            await self._execute_test_case(execution, test_case, env)
            
            # 更新执行状态为成功
            update_data = ExecutionUpdate(
                status='success',
                progress={'current': 1, 'total': 1}
            )
            await self.execution_service.update_execution(execution.id, update_data)
            
        except Exception as e:
            # 记录错误日志
            log_data = ExecutionLogCreate(
                level='error',
                message=f'执行失败: {str(e)}'
            )
            await self.execution_service.create_log(execution.id, log_data)
            
            # 更新执行状态为失败
            update_data = ExecutionUpdate(
                status='failed',
                progress={'current': 1, 'total': 1}
            )
            await self.execution_service.update_execution(execution.id, update_data)
        
        return execution
    
    async def execute_module(self, module_id: int, environment_id: int, executor: str = "system") -> Execution:
        """执行整个模块的测试用例"""
        # 获取模块
        module_obj = await module.get(self.db, id=module_id)
        if not module_obj:
            raise HTTPException(status_code=404, detail="模块不存在")
        
        # 获取环境配置
        env = await environment.get(self.db, id=environment_id)
        if not env:
            raise HTTPException(status_code=404, detail="环境配置不存在")
        
        # 获取模块下的所有测试用例
        test_cases = await test_case_crud.get_by_module(self.db, module_id=module_id)
        if not test_cases:
            raise HTTPException(status_code=404, detail="模块下没有测试用例")
        
        # 创建执行记录
        execution_data = ExecutionCreate(
            name=f"执行模块: {module_obj.name}",
            scope='module',
            module_id=module_id,
            environment_id=environment_id,
            executor=executor,
            status='running',
            progress={'current': 0, 'total': len(test_cases)}
        )
        
        execution = await self.execution_service.create_execution(execution_data)
        
        try:
            # 执行所有测试用例
            await self._execute_test_cases(execution, test_cases, env, module_obj)
            
            # 更新执行状态为成功
            update_data = ExecutionUpdate(
                status='success',
                progress={'current': len(test_cases), 'total': len(test_cases)}
            )
            await self.execution_service.update_execution(execution.id, update_data)
            
        except Exception as e:
            # 记录错误日志
            log_data = ExecutionLogCreate(
                level='error',
                message=f'模块执行失败: {str(e)}'
            )
            await self.execution_service.create_log(execution.id, log_data)
            
            # 更新执行状态为失败
            update_data = ExecutionUpdate(status='failed')
            await self.execution_service.update_execution(execution.id, update_data)
        
        return execution
    
    async def execute_all(self, environment_id: int, executor: str = "system") -> Execution:
        """执行所有测试用例"""
        # 获取环境配置
        env = await environment.get(self.db, id=environment_id)
        if not env:
            raise HTTPException(status_code=404, detail="环境配置不存在")
        
        # 获取所有测试用例
        test_cases = await test_case_crud.get_multi(self.db, skip=0, limit=1000)
        if not test_cases:
            raise HTTPException(status_code=404, detail="没有测试用例")
        
        # 创建执行记录
        execution_data = ExecutionCreate(
            name="执行所有测试用例",
            scope='all',
            environment_id=environment_id,
            executor=executor,
            status='running',
            progress={'current': 0, 'total': len(test_cases)}
        )
        
        execution = await self.execution_service.create_execution(execution_data)
        
        try:
            # 执行所有测试用例
            await self._execute_test_cases(execution, test_cases, env)
            
            # 更新执行状态为成功
            update_data = ExecutionUpdate(
                status='success',
                progress={'current': len(test_cases), 'total': len(test_cases)}
            )
            await self.execution_service.update_execution(execution.id, update_data)
            
        except Exception as e:
            # 记录错误日志
            log_data = ExecutionLogCreate(
                level='error',
                message=f'全量执行失败: {str(e)}'
            )
            await self.execution_service.create_log(execution.id, log_data)
            
            # 更新执行状态为失败
            update_data = ExecutionUpdate(status='failed')
            await self.execution_service.update_execution(execution.id, update_data)
        
        return execution
    
    async def _execute_test_case(self, execution: Execution, test_case: TestCase, environment: Environment, module_obj: Module = None):
        """执行单个测试用例的具体逻辑"""
        # 获取模块变量
        module_vars = {}
        if module_obj:
            module_vars = {var.name: var.value for var in module_obj.variables}
        
        # 创建请求构建器
        request_builder = RequestBuilder(environment, module_vars)
        
        # 构建请求
        request_data = request_builder.build_request(test_case)
        
        # 记录开始日志
        log_data = ExecutionLogCreate(
            level='info',
            message=f'开始执行测试用例: {test_case.name}'
        )
        await self.execution_service.create_log(execution.id, log_data)
        
        # 发送请求
        start_time = time.time()
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.request(**request_data)
                
                # 构建响应数据
                response_data = {
                    'status_code': response.status_code,
                    'headers': dict(response.headers),
                    'body': response.json() if response.headers.get('content-type', '').startswith('application/json') else response.text,
                    'duration': int((time.time() - start_time) * 1000)
                }
                
                # 检查断言
                assertions_result = AssertionChecker.check_assertions(response_data, test_case.assertions or [])
                
                # 提取变量
                extracted_vars = {}
                if module_obj:
                    for var in module_obj.variables:
                        if var.extractor:
                            value = VariableExtractor.extract_variable(response_data, var.extractor)
                            if value:
                                extracted_vars[var.name] = value
                
                # 创建执行详情
                detail_data = ExecutionDetailCreate(
                    test_case_id=test_case.id,
                    status='success' if assertions_result['passed'] else 'failed',
                    request=request_data,
                    response=response_data,
                    assertions=assertions_result,
                    duration=response_data['duration']
                )
                
                await self.execution_service.create_detail(execution.id, detail_data)
                
                # 记录成功日志
                log_data = ExecutionLogCreate(
                    level='info',
                    message=f'测试用例执行成功: {test_case.name}'
                )
                await self.execution_service.create_log(execution.id, log_data)
                
        except Exception as e:
            # 记录失败详情
            detail_data = ExecutionDetailCreate(
                test_case_id=test_case.id,
                status='failed',
                request=request_data,
                response={'error': str(e)},
                duration=int((time.time() - start_time) * 1000)
            )
            
            await self.execution_service.create_detail(execution.id, detail_data)
            
            # 记录失败日志
            log_data = ExecutionLogCreate(
                level='error',
                message=f'测试用例执行失败: {test_case.name}, 错误: {str(e)}'
            )
            await self.execution_service.create_log(execution.id, log_data)
            
            raise
    
    async def _execute_test_cases(self, execution: Execution, test_cases: List[TestCase], environment: Environment, module_obj: Module = None):
        """执行多个测试用例"""
        for i, test_case in enumerate(test_cases):
            try:
                await self._execute_test_case(execution, test_case, environment, module_obj)
                
                # 更新进度
                update_data = ExecutionUpdate(
                    progress={'current': i + 1, 'total': len(test_cases)}
                )
                await self.execution_service.update_execution(execution.id, update_data)
                
            except Exception as e:
                # 继续执行下一个测试用例
                log_data = ExecutionLogCreate(
                    level='warn',
                    message=f'跳过失败的测试用例: {test_case.name}'
                )
                await self.execution_service.create_log(execution.id, log_data)
                continue 