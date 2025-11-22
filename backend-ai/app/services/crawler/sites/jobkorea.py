"""
잡코리아 크롤러
"""
from app.services.crawler.base_crawler import BaseCrawler


class JobKoreaCrawler(BaseCrawler):
    """
    잡코리아 채용정보 크롤러
    """

    def crawl(self, url: str):
        """
        잡코리아 크롤링
        """
        # TODO: 잡코리아 크롤링 로직
        pass

    def parse(self, html: str):
        """
        잡코리아 HTML 파싱
        """
        # TODO: 잡코리아 파싱 로직
        pass
