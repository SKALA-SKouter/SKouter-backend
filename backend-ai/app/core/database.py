"""
데이터베이스 연결 세션 (Qdrant, MariaDB)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings


# TODO: SQLAlchemy 엔진 생성
engine = None

# TODO: Session 팩토리
SessionLocal = None


def get_db():
    """
    데이터베이스 세션 생성
    - 의존성 주입에 사용
    """
    # TODO: 데이터베이스 세션 반환
    pass


def init_db():
    """
    데이터베이스 초기화
    """
    # TODO: 데이터베이스 연결 및 테이블 생성
    pass
