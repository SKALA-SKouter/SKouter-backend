from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Any
import asyncio


class BaseCrawler(ABC):
    """
    모든 회사 크롤러가 구현해야 하는 추상 기본 클래스

    비동기(async) 크롤링을 지원합니다.
    """

    @abstractmethod
    def get_company_name(self) -> str:
        """회사명 반환"""
        pass

    @abstractmethod
    def get_job_list_urls(self) -> List[str]:
        """채용 목록 페이지 URL 리스트 반환"""
        pass

    @abstractmethod
    async def extract_job_urls(self, page: Any) -> List[Dict[str, str]]:
        """
        동적 페이지에서 개별 공고 URL 추출 (비동기)

        Args:
            page: Playwright page 객체 또는 requests 응답

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        pass

    @abstractmethod
    async def parse_job_detail(self, page: Any, url: str, idx: int) -> Optional[Dict[str, str]]:
        """
        공고 상세 페이지 파싱 (비동기)

        Args:
            page: Playwright page 객체
            url: 공고 URL
            idx: 공고 인덱스

        Returns:
            {
                'url': str,
                'job_id': str,
                'title': str,
                'company': str,
                'html': str,  # 원본 HTML
                'posting_date': str,
                'closing_date': str,
                'location': str,
                'job_description': str,
                'required_qualifications': str,
                'preferred_qualifications': str,
                'company_description': str,
                'team_description': str,
                'selection_process': str,
                'notes': str,
                'metadata': Dict[str, Any]  # 추가 메타데이터
            }
        """
        pass

    @abstractmethod
    def get_wait_time(self) -> int:
        """PDF 캡처 대기 시간(초)"""
        pass

    @abstractmethod
    def requires_selenium(self) -> bool:
        """동적 페이지 여부 (True/False)"""
        pass

    def requires_playwright(self) -> bool:
        """Playwright 사용 여부 (기본값: False)"""
        return False

    def get_retry_count(self) -> int:
        """재시도 횟수 (기본값: 3)"""
        return 3

    def get_timeout(self) -> int:
        """타임아웃 시간(밀리초) (기본값: 30000)"""
        return 30000

    def get_max_concurrent_jobs(self) -> int:
        """동시 처리 공고 수 (기본값: 3)"""
        return 3
