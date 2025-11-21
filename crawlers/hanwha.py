import asyncio
import logging
import os
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class HanwhaCrawler(BaseCrawler):
    """
    한화인 채용 공고 크롤러 (Playwright 기반)

    한화인 채용공고 페이지에서 필터링된 공고를 수집합니다.
    필터: 한화시스템/ICT, IT 직무
    https://www.hanwhain.com/web/apply/notification/list.do
    """

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "Hanwha"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            한화인 채용공고 URL 리스트 (전체 96개 공고)
        """
        return [
            "https://m.hanwhain.com/hanwha/jobs/jobs_recruit_list.do",
        ]

    async def extract_job_urls(self, page: Any) -> List[Dict[str, str]]:
        """
        현재 페이지에서 모든 공고 URL 추출 (무한 스크롤 지원)

        Args:
            page: Playwright page 객체

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        try:
            logger.info("한화인 채용공고 링크 추출 중...")

            # 페이지 네비게이션
            urls = self.get_job_list_urls()
            base_url = urls[0]
            logger.info(f"한화인 채용 페이지 로딩: {base_url}")
            await page.goto(base_url, wait_until="networkidle", timeout=self.get_timeout())
            await asyncio.sleep(3)  # 초기 로딩 대기

            # 무한 스크롤로 모든 공고 로드
            logger.info("무한 스크롤로 모든 공고 로드 중...")
            prev_height = 0
            max_scroll_attempts = 50  # 최대 스크롤 횟수
            scroll_count = 0

            while scroll_count < max_scroll_attempts:
                # 현재 높이 확인
                current_height = await page.evaluate("document.body.scrollHeight")

                if current_height == prev_height:
                    logger.debug(f"더 이상 로드할 컨텐츠 없음 (스크롤 {scroll_count}회)")
                    break

                prev_height = current_height

                # 페이지 끝까지 스크롤
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await asyncio.sleep(2)  # 로딩 대기

                scroll_count += 1
                logger.debug(f"스크롤 {scroll_count}회 - 높이: {current_height}")

            # 채용공고 링크 추출
            logger.info("공고 정보 수집 중...")

            # 모바일 페이지의 링크 선택자
            job_links = await page.locator("a").all()
            logger.info(f"총 {len(job_links)}개 링크 발견")

            job_urls = []
            job_urls_set = set()  # 중복 제거용

            for idx, link in enumerate(job_links, 1):
                try:
                    # href 속성 추출
                    href = await link.get_attribute("href")
                    if not href:
                        continue

                    # 공고 상세 페이지 URL 확인 (jobs_recruit_detail.do?rtSeq=...)
                    if "jobs_recruit_detail.do" in href:
                        # 절대 경로로 변환
                        if href.startswith("/"):
                            full_url = "https://m.hanwhain.com" + href
                        elif href.startswith("http"):
                            full_url = href
                        else:
                            full_url = "https://m.hanwhain.com/hanwha/jobs/" + href

                        # 중복 제거
                        if full_url in job_urls_set:
                            continue
                        job_urls_set.add(full_url)

                        # 제목 추출
                        try:
                            title = await link.inner_text(timeout=2000)
                            title = title.strip()
                            if not title:
                                title = f"unknown_{idx}"
                        except:
                            title = f"unknown_{idx}"

                        job_urls.append({
                            "url": full_url,
                            "job_id": self._extract_job_id(full_url),
                            "title": title
                        })
                        logger.debug(f"[{len(job_urls)}] {title[:50]}")

                except Exception as e:
                    logger.debug(f"링크 처리 스킵 [{idx}]: {e}")
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
            url: 공고 URL (jobs_recruit_detail.do?rtSeq=...)

        Returns:
            job_id
        """
        try:
            # URL에서 rtSeq 파라미터 추출 (새로운 모바일 URL)
            if "rtSeq=" in url:
                rt_seq = url.split("rtSeq=")[1].split("&")[0]
                return f"hanwha_{rt_seq}"

            # 폴백: URL의 마지막 부분 사용
            parts = url.split("/")
            for part in reversed(parts):
                if part and not part.startswith("?"):
                    return f"hanwha_{part[:50]}"

            return f"hanwha_{hash(url) % 100000}"
        except:
            return f"hanwha_{hash(url) % 100000}"

    async def parse_job_detail(self, page: Any, url: str, idx: int, screenshot_dir: Optional[str] = None) -> Optional[Dict[str, str]]:
        """공고 상세 페이지 파싱 (스크린샷 저장 포함)"""
        try:
            # 모바일 뷰포트 설정 (2560x1440 데스크톱 뷰포트로 모바일 렌더링 방지)
            await page.set_viewport_size({"width": 1280, "height": 960})

            await page.goto(url, wait_until="networkidle", timeout=self.get_timeout())
            await asyncio.sleep(self.get_wait_time())

            html = await page.content()

            # 기본 정보 추출
            title = ""
            try:
                title_elem = page.locator("div.visual.recruit2 h3, div.visual.recruit2 h4")
                if await title_elem.count() > 0:
                    title = await title_elem.first.inner_text(timeout=2000)
                    title = title.strip()
            except:
                pass

            # 스크린샷 캡처
            screenshot_bytes = None
            try:
                await asyncio.sleep(1)
                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(0.5)
                screenshot_bytes = await page.screenshot(full_page=True, timeout=60000)
                logger.info(f"[{idx}] 스크린샷 캡처 완료 ({len(screenshot_bytes)} bytes)")
            except Exception as e:
                logger.warning(f"[{idx}] 스크린샷 캡처 실패: {e}")

            job_data = {
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
                "screenshot": screenshot_bytes,
                "metadata": {
                    "crawled_at": asyncio.get_event_loop().time(),
                    "wait_time": self.get_wait_time(),
                }
            }

            return job_data
        except Exception as e:
            logger.error(f"공고 상세 파싱 실패: {e}")
            return None

    def get_wait_time(self) -> int:
        """PDF 캡처 대기 시간(초)"""
        return 3

    def requires_selenium(self) -> bool:
        """Selenium 사용 여부"""
        return False
