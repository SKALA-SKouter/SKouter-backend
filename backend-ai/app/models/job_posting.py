"""
채용공고 DB 모델
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float
from datetime import datetime


class JobPosting:
    """
    채용공고 모델
    """
    __tablename__ = "job_postings"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)  # 공고 제목
    content = Column(Text, nullable=False)  # 공고 내용
    company_id = Column(Integer, nullable=False)  # 회사 ID
    salary_min = Column(Float)  # 최소 연봉
    salary_max = Column(Float)  # 최대 연봉
    location = Column(String(255))  # 근무지
    created_at = Column(DateTime, default=datetime.utcnow)  # 생성일
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # 수정일

    # TODO: 관계 설정
