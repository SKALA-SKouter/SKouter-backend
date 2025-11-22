"""
크롤러 추상 클래스
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseCrawler(ABC):
    """
    크롤러 추상 클래스
    """

    @abstractmethod
    def crawl(self, url: str) -> List[Dict[str, Any]]:
        """
        크롤링 메서드

        :param url: 크롤링할 URL
        :return: 크롤링된 데이터 리스트
        """
        # TODO: 크롤링 로직 구현
        pass

    @abstractmethod
    def parse(self, html: str) -> List[Dict[str, Any]]:
        """
        HTML 파싱 메서드

        :param html: HTML 콘텐츠
        :return: 파싱된 데이터 리스트
        """
        # TODO: 파싱 로직 구현
        pass
