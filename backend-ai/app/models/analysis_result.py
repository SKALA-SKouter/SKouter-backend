"""
분석 결과 DB 모델
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from datetime import datetime


class AnalysisResult:
    """
    분석 결과 모델
    """
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True)
    task_id = Column(String(100), nullable=False, unique=True)  # 작업 ID
    job_id = Column(Integer, nullable=False)  # 공고 ID
    analysis_type = Column(String(50), nullable=False)  # 분석 타입
    result = Column(JSON)  # 분석 결과
    status = Column(String(50), default="pending")  # 상태
    created_at = Column(DateTime, default=datetime.utcnow)  # 생성일
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 수정일

    # TODO: 관계 설정
