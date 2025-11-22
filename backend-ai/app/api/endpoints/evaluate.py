"""
공고 평가 엔드포인트
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

router = APIRouter(prefix="/api/jobs", tags=["evaluate"])


@router.post("/evaluate")
async def evaluate_job(db: Session = Depends(get_db)):
    """
    공고 평가
    - POST /api/jobs/evaluate
    """
    # TODO: 공고 평가 로직
    return {"score": 0, "feedback": ""}
