"""
공고 생성 엔드포인트
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

router = APIRouter(prefix="/api/workshop", tags=["workshop"])


@router.post("/generate")
async def generate_job(db: Session = Depends(get_db)):
    """
    공고 생성
    - POST /api/workshop/generate
    """
    # TODO: 공고 생성 로직
    return {"job_id": None, "status": "processing"}
