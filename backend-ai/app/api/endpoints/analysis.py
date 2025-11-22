"""
분석 결과 조회 엔드포인트
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

router = APIRouter(prefix="/api/analysis", tags=["analysis"])


@router.get("/{task_id}")
async def get_analysis_result(task_id: str, db: Session = Depends(get_db)):
    """
    분석 결과 조회
    - GET /api/analysis/{task_id}
    """
    # TODO: 분석 결과 조회 로직
    return {"task_id": task_id, "status": "pending", "result": None}
