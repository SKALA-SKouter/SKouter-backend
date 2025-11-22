"""
챗봇 Pydantic 스키마
"""
from pydantic import BaseModel
from typing import Optional


class ChatRequest(BaseModel):
    """
    챗봇 요청 스키마
    """
    # TODO: 필드 정의
    message: Optional[str] = None


class ChatResponse(BaseModel):
    """
    챗봇 응답 스키마
    """
    # TODO: 필드 정의
    response: Optional[str] = None
