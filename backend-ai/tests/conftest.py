"""
pytest fixtures 공통 설정
"""
import pytest


@pytest.fixture
def test_db():
    """
    테스트용 데이터베이스 세션
    """
    # TODO: 테스트 DB 세션 반환
    pass


@pytest.fixture
def test_redis():
    """
    테스트용 Redis 클라이언트
    """
    # TODO: 테스트 Redis 반환
    pass


@pytest.fixture
def test_client():
    """
    FastAPI 테스트 클라이언트
    """
    # TODO: TestClient 반환
    pass
