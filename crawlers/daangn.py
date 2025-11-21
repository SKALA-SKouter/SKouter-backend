"""
당근마켓 채용 공고 크롤러 (Playwright 기반)

당근마켓의 채용공고를 크롤링합니다.
"""

import asyncio
import logging
import re
from typing import List, Dict, Optional, Any
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class DaangnCrawler(BaseCrawler):
    """
    당근마켓 채용 공고 크롤러 (Playwright 기반)

    당근마켓의 채용공고를 크롤링합니다.
    """

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "Daangn"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            당근마켓 채용공고 URL 리스트
        """
        return [
            "https://about.daangn.com/jobs/",  # 당근마켓 채용공고
        ]

    async def extract_job_urls(self, page: Any) -> List[Dict[str, str]]:
        """
        채용공고 목록 페이지에서 개별 공고 URL 추출 (비동기)

        Args:
            page: Playwright page 객체

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        try:
            logger.info("당근마켓 채용공고 링크 추출 중...")

            # 채용 목록 페이지 로드
            list_url = self.get_job_list_urls()[0]
            logger.info(f"List page 로드 중: {list_url}")
            try:
                await page.goto(list_url, wait_until="domcontentloaded", timeout=self.get_timeout())
            except:
                # timeout 발생 시 load로 재시도
                logger.warning("networkidle 로드 실패, load로 재시도...")
                await page.goto(list_url, wait_until="load", timeout=self.get_timeout())
            logger.info("List page 로드 완료")

            # 페이지 렌더링 대기
            await asyncio.sleep(2)

            # 공고 URL 추출
            job_links = []
            try:
                # JavaScript로 모든 채용 관련 링크 수집
                job_data = await page.evaluate("""() => {
                    const jobs = [];
                    const links = document.querySelectorAll('a[href*="/jobs/"]');

                    for (let link of links) {
                        const href = link.href;
                        const text = link.textContent.trim();

                        // job_id 추출 (/jobs/[id]/)
                        const match = href.match(/\/jobs\/(\d+)/);
                        if (match && href !== 'https://about.daangn.com/jobs/') {
                            const job_id = match[1];
                            const title = text || `Daangn Job ${job_id}`;

                            // 중복 제거
                            const exists = jobs.some(j => j.job_id === job_id);
                            if (!exists) {
                                jobs.push({
                                    url: href,
                                    job_id: job_id,
                                    title: title
                                });
                            }
                        }
                    }

                    return jobs;
                }""")

                job_links = job_data
                logger.info(f"발견된 공고 URL: {len(job_links)}개")

                for idx, job in enumerate(job_links[:20], 1):
                    logger.info(f"  [{idx}] {job['title'][:50]} -> {job['url']}")

                if len(job_links) > 20:
                    logger.info(f"  ... 이하 {len(job_links) - 20}개")

            except Exception as e:
                logger.warning(f"공고 링크 추출 실패: {e}", exc_info=True)

            logger.info(f"총 {len(job_links)}개 공고 링크 추출됨")
            return job_links

        except Exception as e:
            logger.error(f"공고 추출 중 오류: {e}", exc_info=True)
            return []

    async def parse_job_detail(self, page: Any, url: str, idx: int) -> Optional[Dict[str, str]]:
        """
        공고 상세 페이지 파싱 (비동기)

        Args:
            page: Playwright page 객체
            url: 공고 URL
            idx: 공고 인덱스

        Returns:
            공고 상세 정보 딕셔너리
        """
        try:
            logger.info(f"[{idx}] 당근 공고 상세 페이지 파싱: {url}")

            # 페이지 로드
            try:
                await page.goto(url, wait_until="domcontentloaded", timeout=self.get_timeout())
            except:
                logger.warning(f"[{idx}] 로드 실패, load로 재시도...")
                await page.goto(url, wait_until="load", timeout=self.get_timeout())
            logger.info(f"[{idx}] 페이지 로드 완료: {url}")

            # URL에서 job_id 추출
            match = re.search(r'/jobs/(\d+)', url)
            job_id = match.group(1) if match else "unknown"

            # 원본 HTML 수집
            html_content = await page.content()
            logger.info(f"[{idx}] HTML 수집 완료 ({len(html_content)} bytes)")

            # 스크린샷 캡처
            screenshot_bytes = None
            try:
                await asyncio.sleep(1)  # 페이지 렌더링 대기
                screenshot_bytes = await page.screenshot(full_page=True, timeout=60000)
                logger.info(f"[{idx}] 스크린샷 캡처 완료 ({len(screenshot_bytes)} bytes)")
            except Exception as e:
                logger.warning(f"[{idx}] 스크린샷 캡처 실패: {e}")

            # 공고 제목
            title = ""
            try:
                title_elem = await page.query_selector('h1, .job-title, [class*="title"]')
                if title_elem:
                    title = await title_elem.inner_text()
            except:
                pass

            # 회사명
            company = "Daangn"

            # 공고 설명 텍스트
            job_description = ""
            try:
                content_elem = await page.query_selector('[class*="content"], [class*="description"], main, article')
                if content_elem:
                    job_description = await content_elem.inner_text()
            except:
                pass

            result = {
                'url': url,
                'job_id': job_id,
                'title': title.strip() if title else f'Daangn Job {job_id}',
                'company': company,
                'html': html_content,
                'posting_date': '',
                'closing_date': '',
                'location': '',
                'job_description': job_description[:5000] if job_description else '',
                'required_qualifications': '',
                'preferred_qualifications': '',
                'company_description': '',
                'team_description': '',
                'selection_process': '',
                'notes': '',
                'screenshot': screenshot_bytes,
                'metadata': {
                    'source': 'daangn',
                    'crawled_index': idx,
                }
            }

            logger.info(f"[{idx}] 파싱 완료: {result['title'][:50]}")
            return result

        except Exception as e:
            logger.error(f"[{idx}] 공고 파싱 실패: {e}", exc_info=True)
            return None

    def get_wait_time(self) -> int:
        """스크린샷 캡처 대기 시간(초)"""
        return 2

    def requires_selenium(self) -> bool:
        """동적 페이지 여부 (True/False)"""
        return False

    def requires_playwright(self) -> bool:
        """Playwright 사용 여부"""
        return True

    def get_max_concurrent_jobs(self) -> int:
        """동시 처리 공고 수"""
        return 3
