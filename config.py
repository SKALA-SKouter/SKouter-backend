"""
크롤러 설정 관리 모듈
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from dataclasses import dataclass
from typing import Optional

# .env 파일 로드
load_dotenv()


@dataclass
class CrawlerConfig:
    """크롤러 기본 설정"""

    log_level: str = os.getenv("CRAWLER_LOG_LEVEL", "INFO")
    timeout: int = int(os.getenv("CRAWLER_TIMEOUT", "30"))
    retry_count: int = int(os.getenv("CRAWLER_RETRY_COUNT", "3"))


@dataclass
class PDFCaptureConfig:
    """PDF 캡처 설정"""

    headless_mode: bool = os.getenv("PDF_HEADLESS_MODE", "true").lower() == "true"
    wait_time: int = int(os.getenv("PDF_WAIT_TIME", "5"))
    chrome_driver_path: Optional[str] = os.getenv("CHROME_DRIVER_PATH")
    window_width: int = 1920
    window_height: int = 1080


@dataclass
class StorageConfig:
    """저장소 설정"""

    storage_type: str = os.getenv("STORAGE_TYPE", "local")  # 'local', 's3', 'both'
    local_pdf_path: str = os.getenv("LOCAL_PDF_PATH", "./data/pdfs")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
    aws_access_key_id: Optional[str] = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_access_key: Optional[str] = os.getenv("AWS_SECRET_ACCESS_KEY")
    s3_bucket_name: Optional[str] = os.getenv("S3_BUCKET_NAME")

    def get_s3_config(self) -> Optional[dict]:
        """S3 설정 반환"""
        if self.storage_type in ["s3", "both"]:
            if all([self.aws_access_key_id, self.aws_secret_access_key, self.s3_bucket_name]):
                return {
                    "region": self.aws_region,
                    "access_key": self.aws_access_key_id,
                    "secret_key": self.aws_secret_access_key,
                    "bucket": self.s3_bucket_name,
                }
        return None


@dataclass
class OutputConfig:
    """출력 설정"""

    output_format: str = os.getenv("OUTPUT_FORMAT", "json")
    output_directory: str = os.getenv("OUTPUT_DIRECTORY", "./results")

    def __post_init__(self):
        """초기화 후 처리"""
        Path(self.output_directory).mkdir(parents=True, exist_ok=True)


@dataclass
class Config:
    """통합 설정"""

    crawler: CrawlerConfig = None
    pdf_capture: PDFCaptureConfig = None
    storage: StorageConfig = None
    output: OutputConfig = None

    def __post_init__(self):
        """기본값 설정"""
        if self.crawler is None:
            self.crawler = CrawlerConfig()
        if self.pdf_capture is None:
            self.pdf_capture = PDFCaptureConfig()
        if self.storage is None:
            self.storage = StorageConfig()
        if self.output is None:
            self.output = OutputConfig()


# 전역 설정 인스턴스
config = Config()
