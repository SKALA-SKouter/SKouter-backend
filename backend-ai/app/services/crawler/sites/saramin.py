"""
사람인 크롤러
"""
from app.services.crawler.base_crawler import BaseCrawler


class SaraminCrawler(BaseCrawler):
    """
    사람인 채용정보 크롤러
    """

    def crawl(self, url: str):
        """
        사람인 크롤링
        """
        # TODO: 사람인 크롤링 로직
        pass

    def parse(self, html: str):
        """
        사람인 HTML 파싱
        """
        # TODO: 사람인 파싱 로직
        pass
