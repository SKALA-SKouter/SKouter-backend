"""
환경변수 설정 (Pydantic Settings)
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    애플리케이션 설정
    - 환경변수 로드 (pydantic-settings)
    """

    # FastAPI
    app_name: str = "SKouter AI Backend"
    app_version: str = "1.0.0"
    debug: bool = False

    # 데이터베이스
    database_url: str = ""  # TODO: MariaDB 연결 URL
    qdrant_url: str = ""  # TODO: Qdrant 벡터 DB URL

    # Redis
    redis_url: str = ""  # TODO: Redis 연결 URL

    # OpenAI
    openai_api_key: str = ""  # TODO: OpenAI API 키

    # 기타 설정
    log_level: str = "INFO"

    class Config:
        env_file = ".env"  # 루트 디렉토리의 .env 파일


settings = Settings()
