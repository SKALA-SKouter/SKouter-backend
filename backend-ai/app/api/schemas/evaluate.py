"""
공고 평가 Pydantic 스키마
"""
from pydantic import BaseModel
from typing import Optional


class JobEvaluateRequest(BaseModel):
    """
    공고 평가 요청 스키마
    """
    # TODO: 필드 정의
    job_id: Optional[str] = None


class JobEvaluateResponse(BaseModel):
    """
    공고 평가 응답 스키마
    """
    # TODO: 필드 정의
    score: Optional[float] = None
    feedback: Optional[str] = None
