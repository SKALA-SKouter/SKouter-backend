"""
의존성 주입 (get_db 등)
"""
from typing import Generator
from app.core.database import SessionLocal


def get_db() -> Generator:
    """
    데이터베이스 세션 의존성 주입

    :return: 데이터베이스 세션
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
