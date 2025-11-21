import asyncio
import logging
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class LineCrawler(BaseCrawler):
    """
    LINE 채용 공고 크롤러 (Playwright 기반)

    LINE 채용공고 페이지에서 무한 스크롤로 모든 공고를 수집합니다.
    https://careers.linecorp.com/ko/jobs/
    """

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "Line"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            LINE 채용공고 URL 리스트
        """
        return [
            "https://careers.linecorp.com/ko/jobs/?ca=All&ci=Gwacheon,Bundang&co=East%20Asia",
        ]

    async def extract_job_urls(self, page: Any) -> List[Dict[str, str]]:
        """
        현재 페이지에서 모든 공고 URL 추출 (무한 스크롤 처리)

        Args:
            page: Playwright page 객체

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        try:
            logger.info("LINE 채용공고 링크 추출 중 (무한 스크롤)...")

            # 페이지 네비게이션
            urls = self.get_job_list_urls()
            base_url = urls[0]
            logger.info(f"LINE 채용 페이지 로딩: {base_url}")
            await page.goto(base_url, wait_until="networkidle", timeout=self.get_timeout())
            await asyncio.sleep(3)  # 초기 로딩 대기

            # 무한 스크롤로 모든 공고 로드
            previous_count = 0
            max_attempts = 50  # 무한 루프 방지
            attempts = 0

            while attempts < max_attempts:
                # 현재 공고 개수 확인 (ul.job_list > li)
                current_count = await page.locator("ul.job_list > li").count()

                if current_count == previous_count:
                    # 더 이상 새 공고가 없으면 종료
                    logger.info(f"스크롤 완료 (현재 {current_count}개 공고)")
                    break

                if current_count > previous_count:
                    logger.info(f"현재 {current_count}개 공고 로드됨...")
                    attempts = 0  # 새 공고가 로드되면 카운터 리셋
                else:
                    attempts += 1

                previous_count = current_count

                # 마지막 공고까지 스크롤
                try:
                    last_job = await page.locator("ul.job_list > li").last
                    await last_job.scroll_into_view_if_needed()
                except:
                    pass

                await page.wait_for_timeout(1000)
                await asyncio.sleep(2.5)

            # 모든 공고 카드에서 URL과 제목 추출
            logger.info("공고 정보 수집 중...")
            job_links = await page.locator("ul.job_list > li > a").all()
            logger.info(f"총 {len(job_links)}개 링크 발견")

            job_urls = []

            for idx, link in enumerate(job_links, 1):
                try:
                    # href 속성 추출
                    href = await link.get_attribute("href")
                    if not href:
                        logger.debug(f"[{idx}/{len(job_links)}] href 없음")
                        continue

                    # 절대 URL 생성
                    full_url = "https://careers.linecorp.com" + href if href.startswith("/") else href

                    # 제목 추출
                    try:
                        title_elem = link.locator("h3.title")
                        title_count = await title_elem.count()
                        if title_count > 0:
                            title = await title_elem.inner_text(timeout=2000)
                            title = title.strip()

                            # span.label 텍스트 제거 (NEW, URGENT 등)
                            label_elem = title_elem.locator("span.label")
                            try:
                                label_text = await label_elem.inner_text(timeout=2000)
                                title = title.replace(label_text, "").strip()
                            except:
                                pass

                            if not title:
                                title = f"unknown_{idx}"
                        else:
                            title = f"unknown_{idx}"
                    except:
                        title = f"unknown_{idx}"

                    job_urls.append({
                        "url": full_url,
                        "job_id": self._extract_job_id(full_url),
                        "title": title
                    })
                    logger.debug(f"[{idx}/{len(job_links)}] {title[:40]}...")

                except Exception as e:
                    logger.warning(f"링크 처리 실패 [{idx}/{len(job_links)}]: {e}")
                    continue

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
            # URL에서 마지막 부분을 job_id로 사용
            parts = url.split("/")
            for part in reversed(parts):
                if part and not part.startswith("?"):
                    return f"line_{part[:50]}"
            return f"line_{hash(url) % 100000}"
        except:
            return f"line_{hash(url) % 100000}"

    async def parse_job_detail(self, page: Any, url: str, idx: int) -> Optional[Dict[str, str]]:
        """공고 상세 페이지 파싱"""
        try:
            await page.goto(url, wait_until="networkidle", timeout=self.get_timeout())
            await asyncio.sleep(self.get_wait_time())

            html = await page.content()
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
                "notes": "",
                "html_content": html,
                "metadata": {
                    "crawled_at": asyncio.get_event_loop().time(),
                    "wait_time": self.get_wait_time(),
                }
            }
        except Exception as e:
            logger.error(f"공고 상세 파싱 실패: {e}")
            return None

    def get_wait_time(self) -> int:
        """PDF 캡처 대기 시간(초)"""
        return 3

    def requires_selenium(self) -> bool:
        """Selenium 사용 여부"""
        return False
