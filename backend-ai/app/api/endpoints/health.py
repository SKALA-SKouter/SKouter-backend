"""
헬스 체크 엔드포인트
"""
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("")
async def health_check():
    """
    서비스 상태 체크
    - GET /health
    """
    # TODO: 각 서비스 상태 확인
    return {
        "status": "healthy",
        "services": {
            "database": "ok",
            "redis": "ok",
            "qdrant": "ok"
        }
    }
