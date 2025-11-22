"""
공통 Pydantic 스키마
"""
from pydantic import BaseModel
from typing import Any, Optional


class BaseResponse(BaseModel):
    """
    기본 응답 스키마
    """
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    """
    에러 응답 스키마
    """
    error: str
    status_code: int
    details: Optional[dict] = None
