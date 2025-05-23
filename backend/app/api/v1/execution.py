from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.execution import ExecutionService
from app.schemas.execution import (
    Execution,
    ExecutionCreate,
    ExecutionUpdate,
    ExecutionLog,
    ExecutionLogCreate,
    ExecutionDetail,
    ExecutionDetailCreate,
    ExecutionDetailUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[Execution])
async def get_executions(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取执行记录列表"""
    return await ExecutionService(db).get_executions(skip=skip, limit=limit)


@router.post("/", response_model=Execution)
async def create_execution(
    execution: ExecutionCreate,
    db: Session = Depends(get_db),
):
    """创建执行记录"""
    return await ExecutionService(db).create_execution(execution)


@router.get("/{execution_id}", response_model=Execution)
async def get_execution(
    execution_id: int,
    db: Session = Depends(get_db),
):
    """获取执行记录详情"""
    return await ExecutionService(db).get_execution(execution_id)


@router.put("/{execution_id}", response_model=Execution)
async def update_execution(
    execution_id: int,
    execution: ExecutionUpdate,
    db: Session = Depends(get_db),
):
    """更新执行记录"""
    return await ExecutionService(db).update_execution(execution_id, execution)


@router.delete("/{execution_id}")
async def delete_execution(
    execution_id: int,
    db: Session = Depends(get_db),
):
    """删除执行记录"""
    await ExecutionService(db).delete_execution(execution_id)
    return {"message": "执行记录已删除"}


@router.get("/{execution_id}/logs", response_model=List[ExecutionLog])
async def get_execution_logs(
    execution_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取执行日志列表"""
    return await ExecutionService(db).get_logs(execution_id, skip=skip, limit=limit)


@router.post("/{execution_id}/logs", response_model=ExecutionLog)
async def create_execution_log(
    execution_id: int,
    log: ExecutionLogCreate,
    db: Session = Depends(get_db),
):
    """创建执行日志"""
    return await ExecutionService(db).create_log(execution_id, log)


@router.get("/{execution_id}/details", response_model=List[ExecutionDetail])
async def get_execution_details(
    execution_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """获取执行详情列表"""
    return await ExecutionService(db).get_details(execution_id, skip=skip, limit=limit)


@router.post("/{execution_id}/details", response_model=ExecutionDetail)
async def create_execution_detail(
    execution_id: int,
    detail: ExecutionDetailCreate,
    db: Session = Depends(get_db),
):
    """创建执行详情"""
    return await ExecutionService(db).create_detail(execution_id, detail)


@router.put("/details/{detail_id}", response_model=ExecutionDetail)
async def update_execution_detail(
    detail_id: int,
    detail: ExecutionDetailUpdate,
    db: Session = Depends(get_db),
):
    """更新执行详情"""
    return await ExecutionService(db).update_detail(detail_id, detail) 