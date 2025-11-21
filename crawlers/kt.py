import asyncio
import json
import logging
import re
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class KTCrawler(BaseCrawler):
    """
    KT 채용 공고 크롤러 (SPA 기반)

    React 기반 SPA로 동작하며, 네트워크 모니터링으로 공고 데이터를 수집합니다.
    URL: https://recruit.kt.com
    """

    def __init__(self):
        """초기화"""
        self.job_ids = set()
        self.jobs = {}

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "KT"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            KT 채용공고 URL 리스트
        """
        return [
            "https://recruit.kt.com/careers",
        ]

    async def extract_job_urls(self, page: Any) -> List[Dict[str, str]]:
        """
        SPA에서 모든 공고 URL 추출

        Args:
            page: Playwright page 객체

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        try:
            logger.info("KT 채용공고 페이지에서 공고 추출 중...")

            urls = self.get_job_list_urls()
            base_url = urls[0]
            logger.info(f"페이지 로딩: {base_url}")

            # 페이지 로드
            await page.goto(base_url, wait_until="networkidle", timeout=self.get_timeout())
            await asyncio.sleep(2)

            # JavaScript로 공고 링크 추출
            job_urls = await page.evaluate("""
                () => {
                    const links = document.querySelectorAll('a[href*="/careers/"]');
                    const jobs = [];
                    const seen = new Set();

                    for (const link of links) {
                        const href = link.href;
                        const match = href.match(/\\/careers\\/(\\d+)/);

                        if (match && !seen.has(match[1])) {
                            seen.add(match[1]);
                            const title = link.textContent?.trim() || 'Unknown';
                            jobs.push({
                                url: href,
                                job_id: match[1],
                                title: title
                            });
                        }
                    }

                    return jobs;
                }
            """)

            logger.info(f"총 {len(job_urls)}개 공고 URL 추출 완료")
            return job_urls

        except Exception as e:
            logger.error(f"공고 URL 추출 실패: {e}", exc_info=True)
            return []

    def _extract_job_id(self, url: str) -> str:
        """
        URL에서 job_id 추출

        Args:
            url: 공고 URL

        Returns:
            job_id
        """
        try:
            # URL 패턴: https://recruit.kt.com/careers/{job_id}
            match = re.search(r'/careers/(\d+)', url)
            if match:
                job_id = match.group(1)
                return f"kt_{job_id}"

            return f"kt_{hash(url) % 100000}"
        except:
            return f"kt_{hash(url) % 100000}"

    async def parse_job_detail(self, page: Any, url: str, idx: int) -> Optional[Dict[str, str]]:
        """공고 상세 페이지 파싱"""
        try:
            # 페이지 로드
            await page.goto(url, wait_until="domcontentloaded", timeout=self.get_timeout())
            await asyncio.sleep(self.get_wait_time())

            html = await page.content()

            # 기본 정보 추출
            title = ""
            try:
                soup = BeautifulSoup(html, 'html.parser')
                # h1 또는 제목 태그에서 제목 추출
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text(strip=True)
                else:
                    # 다른 제목 태그 시도
                    for tag in soup.find_all(['h2', 'h3']):
                        text = tag.get_text(strip=True)
                        if text and len(text) > 5:
                            title = text
                            break
            except:
                pass

            return {
                "url": url,
                "job_id": self._extract_job_id(url),
                "company": self.get_company_name(),
                "title": title,
                "posting_date": "",
                "closing_date": "",
                "location": "",
                "job_description": "",
                "required_qualifications": "",
                "preferred_qualifications": "",
                "company_description": "",
                "team_description": "",
                "selection_process": "",
                "notes": "",
                "html_content": html,
                "metadata": {
                    "crawled_at": asyncio.get_event_loop().time(),
                    "wait_time": self.get_wait_time(),
                }
            }

        except Exception as e:
            logger.debug(f"공고 상세 파싱 실패 [{idx}]: {str(e)[:100]}")
            # 부분 실패 처리 (기본 정보만 반환)
            return {
                "url": url,
                "job_id": self._extract_job_id(url),
                "company": self.get_company_name(),
                "title": "",
                "posting_date": "",
                "closing_date": "",
                "location": "",
                "job_description": "",
                "required_qualifications": "",
                "preferred_qualifications": "",
                "company_description": "",
                "team_description": "",
                "selection_process": "",
                "notes": f"파싱 오류: {str(e)[:50]}",
                "html_content": "",
                "metadata": {
                    "crawled_at": asyncio.get_event_loop().time(),
                    "wait_time": self.get_wait_time(),
                    "error": str(e)[:100]
                }
            }

    def get_wait_time(self) -> int:
        """페이지 로드 후 대기 시간(초)"""
        return 2

    def get_timeout(self) -> int:
        """페이지 로드 타임아웃(밀리초)"""
        return 30000

    def requires_selenium(self) -> bool:
        """Selenium 사용 여부"""
        return False

    def requires_playwright(self) -> bool:
        """Playwright 사용 여부"""
        return True

    def get_max_concurrent_jobs(self) -> int:
        """동시 처리 공고 수"""
        return 5
