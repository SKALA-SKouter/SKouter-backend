"""
공고 생성 Pydantic 스키마
"""
from pydantic import BaseModel
from typing import Optional


class JobGenerateRequest(BaseModel):
    """
    공고 생성 요청 스키마
    """
    # TODO: 필드 정의
    title: Optional[str] = None
    description: Optional[str] = None


class JobGenerateResponse(BaseModel):
    """
    공고 생성 응답 스키마
    """
    # TODO: 필드 정의
    job_id: Optional[str] = None
    status: Optional[str] = None
