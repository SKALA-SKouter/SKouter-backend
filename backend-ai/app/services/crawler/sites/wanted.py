"""
원티드 크롤러
"""
from app.services.crawler.base_crawler import BaseCrawler


class WantedCrawler(BaseCrawler):
    """
    원티드 채용정보 크롤러
    """

    def crawl(self, url: str):
        """
        원티드 크롤링
        """
        # TODO: 원티드 크롤링 로직
        pass

    def parse(self, html: str):
        """
        원티드 HTML 파싱
        """
        # TODO: 원티드 파싱 로직
        pass
