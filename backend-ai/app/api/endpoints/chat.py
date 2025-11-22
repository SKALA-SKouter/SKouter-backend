"""
챗봇 엔드포인트
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_db

router = APIRouter(prefix="/api/chat", tags=["chat"])


@router.post("")
async def chat(db: Session = Depends(get_db)):
    """
    챗봇 대화
    - POST /api/chat
    """
    # TODO: 챗봇 요청 처리
    return {"message": "Chat response"}
