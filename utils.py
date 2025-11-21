"""
크롤러 유틸리티 함수들
"""

import os
import json
import hashlib
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlparse, urljoin
from datetime import datetime

logger = logging.getLogger(__name__)


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    파일명을 안전하게 정제

    Args:
        filename: 원본 파일명
        max_length: 최대 길이

    Returns:
        정제된 파일명
    """
    # 특수문자 제거
    safe_name = "".join(c if c.isalnum() or c in ('-', '_', '.') else '_' for c in filename)
    # 연속된 언더스코어 제거
    safe_name = "_".join(filter(None, safe_name.split('_')))
    # 최대 길이 제한
    return safe_name[:max_length].rstrip('_')


def normalize_url(url: str, base_url: Optional[str] = None) -> Optional[str]:
    """
    URL 정규화

    Args:
        url: 대상 URL
        base_url: 기본 URL (상대경로일 때)

    Returns:
        정규화된 절대 URL
    """
    try:
        if not url:
            return None

        # 이미 절대경로인 경우
        parsed = urlparse(url)
        if parsed.scheme:
            return url

        # 상대경로인 경우 기본 URL 사용
        if base_url:
            return urljoin(base_url, url)

        return None
    except Exception as e:
        logger.error(f"Error normalizing URL: {e}")
        return None


def extract_domain(url: str) -> Optional[str]:
    """
    URL에서 도메인 추출

    Args:
        url: 대상 URL

    Returns:
        도메인 (예: example.com)
    """
    try:
        parsed = urlparse(url)
        return parsed.netloc
    except Exception:
        return None


def hash_url(url: str) -> str:
    """
    URL의 SHA256 해시 생성

    Args:
        url: 대상 URL

    Returns:
        해시값
    """
    return hashlib.sha256(url.encode()).hexdigest()[:8]


def create_output_directory(base_path: str, company: str, date_folder: bool = True) -> Path:
    """
    출력 디렉토리 생성

    Args:
        base_path: 기본 경로
        company: 회사명
        date_folder: 날짜 폴더 생성 여부

    Returns:
        생성된 디렉토리 경로
    """
    path = Path(base_path) / company

    if date_folder:
        path = path / datetime.now().strftime("%Y-%m-%d")

    path.mkdir(parents=True, exist_ok=True)
    return path


def save_json(data: Any, file_path: str, pretty: bool = True) -> bool:
    """
    데이터를 JSON 파일로 저장

    Args:
        data: 저장할 데이터
        file_path: 파일 경로
        pretty: 포맷 여부

    Returns:
        성공 여부
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                json.dump(data, f, ensure_ascii=False)
        logger.info(f"Data saved to {file_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to save JSON: {e}")
        return False


def load_json(file_path: str) -> Optional[Dict]:
    """
    JSON 파일 로드

    Args:
        file_path: 파일 경로

    Returns:
        로드된 데이터
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load JSON: {e}")
        return None


def get_file_size(file_path: str) -> Optional[int]:
    """
    파일 크기 반환 (바이트)

    Args:
        file_path: 파일 경로

    Returns:
        파일 크기 또는 None
    """
    try:
        return os.path.getsize(file_path)
    except Exception as e:
        logger.error(f"Failed to get file size: {e}")
        return None


def format_file_size(size_bytes: int) -> str:
    """
    바이트를 읽기 쉬운 형식으로 변환

    Args:
        size_bytes: 바이트 단위 크기

    Returns:
        포맷된 크기 (예: 1.5 MB)
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"


def validate_url(url: str) -> bool:
    """
    URL 유효성 검사

    Args:
        url: 검사할 URL

    Returns:
        유효 여부
    """
    try:
        parsed = urlparse(url)
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False


def extract_job_id_from_url(url: str) -> Optional[str]:
    """
    URL에서 공고 ID 추출 시도

    Args:
        url: 대상 URL

    Returns:
        추출된 ID
    """
    try:
        # 마지막 경로 세그먼트 사용
        path = urlparse(url).path
        job_id = path.rstrip('/').split('/')[-1]
        return job_id if job_id and job_id.isalnum() else None
    except Exception:
        return None


def print_section(title: str, width: int = 60) -> None:
    """
    섹션 제목 출력

    Args:
        title: 제목
        width: 출력 너비
    """
    print("\n" + "=" * width)
    print(title.center(width))
    print("=" * width)


def print_subsection(title: str, width: int = 60) -> None:
    """
    서브섹션 제목 출력

    Args:
        title: 제목
        width: 출력 너비
    """
    print("\n" + "-" * width)
    print(title)
    print("-" * width)


def format_timestamp(dt: Optional[datetime] = None) -> str:
    """
    타임스탬프 포맷

    Args:
        dt: datetime 객체 (None이면 현재 시간)

    Returns:
        포맷된 타임스탬프
    """
    if dt is None:
        dt = datetime.now()
    return dt.strftime("%Y-%m-%d %H:%M:%S")
