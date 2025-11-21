"""
크롤러 테스트
"""

import pytest
from crawlers import CrawlerRegistry, CoupangCrawler, NaverCrawler, KakaoCrawler, BaseCrawler


class TestBaseCrawler:
    """BaseCrawler 테스트"""

    def test_cannot_instantiate_base_crawler(self):
        """BaseCrawler는 추상 클래스라 직접 인스턴스화 불가"""
        with pytest.raises(TypeError):
            BaseCrawler()


class TestCrawlerRegistry:
    """CrawlerRegistry 테스트"""

    def test_register_crawler(self):
        """크롤러 등록"""
        registry = CrawlerRegistry()
        coupang = CoupangCrawler()

        registry.register(coupang)
        assert registry.is_registered("Coupang")

    def test_get_crawler(self):
        """크롤러 조회"""
        registry = CrawlerRegistry()
        coupang = CoupangCrawler()
        registry.register(coupang)

        retrieved = registry.get_crawler("Coupang")
        assert retrieved is not None
        assert retrieved.get_company_name() == "Coupang"

    def test_get_nonexistent_crawler(self):
        """존재하지 않는 크롤러 조회"""
        registry = CrawlerRegistry()
        assert registry.get_crawler("NonExistent") is None

    def test_list_companies(self):
        """등록된 회사명 리스트"""
        registry = CrawlerRegistry()
        registry.register(CoupangCrawler())
        registry.register(NaverCrawler())

        companies = registry.list_companies()
        assert "Coupang" in companies
        assert "Naver" in companies

    def test_duplicate_registration(self):
        """중복 등록 실패"""
        registry = CrawlerRegistry()
        registry.register(CoupangCrawler())

        with pytest.raises(ValueError):
            registry.register(CoupangCrawler())


class TestCoupangCrawler:
    """CoupangCrawler 테스트"""

    def test_company_name(self):
        """회사명 반환"""
        crawler = CoupangCrawler()
        assert crawler.get_company_name() == "Coupang"

    def test_get_job_list_urls(self):
        """채용 목록 URL 반환"""
        crawler = CoupangCrawler()
        urls = crawler.get_job_list_urls()

        assert isinstance(urls, list)
        assert len(urls) > 0
        assert all(isinstance(url, str) for url in urls)

    def test_requires_selenium(self):
        """Selenium 필요 여부"""
        crawler = CoupangCrawler()
        assert isinstance(crawler.requires_selenium(), bool)

    def test_get_wait_time(self):
        """대기 시간"""
        crawler = CoupangCrawler()
        wait_time = crawler.get_wait_time()

        assert isinstance(wait_time, int)
        assert wait_time > 0

    def test_extract_job_urls_empty_html(self):
        """빈 HTML 처리"""
        crawler = CoupangCrawler()
        result = crawler.extract_job_urls("")

        assert isinstance(result, list)
        assert len(result) == 0


class TestNaverCrawler:
    """NaverCrawler 테스트"""

    def test_company_name(self):
        """회사명 반환"""
        crawler = NaverCrawler()
        assert crawler.get_company_name() == "Naver"

    def test_requires_selenium(self):
        """Selenium 필요 여부"""
        crawler = NaverCrawler()
        assert not crawler.requires_selenium()


class TestKakaoCrawler:
    """KakaoCrawler 테스트"""

    def test_company_name(self):
        """회사명 반환"""
        crawler = KakaoCrawler()
        assert crawler.get_company_name() == "Kakao"

    def test_requires_selenium(self):
        """Selenium 필요 여부"""
        crawler = KakaoCrawler()
        assert crawler.requires_selenium()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
