from typing import Dict, List, Optional
from .base_crawler import BaseCrawler


class CrawlerRegistry:
    """
    플러그인 아키텍처 기반 크롤러 레지스트리
    """

    def __init__(self):
        self._crawlers: Dict[str, BaseCrawler] = {}

    def register(self, crawler: BaseCrawler) -> None:
        """
        크롤러 등록

        Args:
            crawler: BaseCrawler를 상속한 크롤러 인스턴스
        """
        company_name = crawler.get_company_name()
        if company_name in self._crawlers:
            raise ValueError(f"Crawler for '{company_name}' is already registered")
        self._crawlers[company_name] = crawler
        print(f"[OK] Registered crawler for: {company_name}")

    def get_crawler(self, company_name: str) -> Optional[BaseCrawler]:
        """
        회사별 크롤러 조회

        Args:
            company_name: 회사명

        Returns:
            크롤러 인스턴스 또는 None
        """
        return self._crawlers.get(company_name)

    def get_all_crawlers(self) -> Dict[str, BaseCrawler]:
        """
        전체 크롤러 목록 반환

        Returns:
            {company_name: crawler_instance} 딕셔너리
        """
        return self._crawlers.copy()

    def list_companies(self) -> List[str]:
        """
        등록된 모든 회사명 반환

        Returns:
            회사명 리스트
        """
        return list(self._crawlers.keys())

    def is_registered(self, company_name: str) -> bool:
        """
        해당 회사 크롤러가 등록되었는지 확인

        Args:
            company_name: 회사명

        Returns:
            등록 여부
        """
        return company_name in self._crawlers
