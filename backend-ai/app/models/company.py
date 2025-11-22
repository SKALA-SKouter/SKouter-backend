"""
회사 DB 모델
"""
from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime


class Company:
    """
    회사 모델
    """
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)  # 회사명
    description = Column(Text)  # 회사 설명
    website = Column(String(255))  # 회사 웹사이트
    industry = Column(String(100))  # 업종
    created_at = Column(DateTime, default=datetime.utcnow)  # 생성일
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 수정일

    # TODO: 관계 설정
