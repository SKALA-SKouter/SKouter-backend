"""
포스코 채용공고 크롤러

AJAX API 방식으로 동작하며, 다중 회사 필터링 지원
기본 구조는 Playwright 기반 동적 페이지 처리
"""
import asyncio
import logging
from typing import List, Dict, Optional, Any
from playwright.async_api import Page
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class PoscoCrawler(BaseCrawler):
    """포스코 전용 크롤러"""

    def get_company_name(self) -> str:
        return "Posco"

    def get_job_list_urls(self) -> List[str]:
        """포스코 채용 목록 URL"""
        return ["https://recruit.posco.com/h22a01-front/H22A1000.html"]

    def get_wait_time(self) -> int:
        """페이지 로드 후 대기시간 (초)"""
        return 3

    def get_max_concurrent_jobs(self) -> int:
        """동시 처리 공고 수"""
        return 2

    def get_timeout(self) -> int:
        """타임아웃 (밀리초)"""
        return 30000

    def requires_playwright(self) -> bool:
        """Playwright 사용 여부"""
        return True

    def requires_selenium(self) -> bool:
        """Selenium 사용 여부"""
        return False

    async def extract_job_urls(self, page: Page) -> List[Dict[str, str]]:
        """
        포스코 채용 목록에서 공고 URL 추출

        페이지네이션 처리 포함
        """
        try:
            # 포스코 채용 페이지 기본 URL
            base_url = "https://recruit.posco.com/h22a01-front"
            job_list_url = self.get_job_list_urls()[0]

            logger.info(f"포스코 채용 페이지 로딩: {job_list_url}")

            # 페이지 네비게이션
            await page.goto(job_list_url, wait_until="networkidle", timeout=self.get_timeout())
            await asyncio.sleep(self.get_wait_time())

            # 회사 목록 대기 및 확인 - visible 상태로 변경하여 더 안정적으로
            try:
                await page.wait_for_selector("#SEARCH_COMP", state="visible", timeout=15000)
            except Exception:
                # 타이머아웃 시 선택자가 있는지만 확인
                selector_exists = await page.query_selector("#SEARCH_COMP")
                if not selector_exists:
                    logger.warning("회사 선택자를 찾을 수 없습니다")

            await asyncio.sleep(1)

            # 회사 목록 가져오기
            companies = await self._get_companies(page)
            logger.info(f"발견된 회사: {len(companies)}개")

            # 전체 공고 수집 (필터링 없음)
            job_list = await self._get_job_list(page, base_url)
            logger.info(f"추출된 공고 URL: {len(job_list)}개")

            return job_list

        except Exception as e:
            logger.error(f"URL 추출 실패: {e}")
            return []

    async def parse_job_detail(
        self, page: Page, url: str, idx: int
    ) -> Optional[Dict[str, Any]]:
        """
        개별 공고 상세 페이지 파싱

        Args:
            page: Playwright page 객체
            url: 공고 URL
            idx: 인덱스

        Returns:
            파싱된 공고 데이터
        """
        try:
            await page.goto(url, wait_until="networkidle", timeout=self.get_timeout())
            await asyncio.sleep(self.get_wait_time())

            # HTML 콘텐츠 획득
            html_content = await page.content()

            # 페이지에서 데이터 추출
            job_data = await page.evaluate(
                """
                () => {
                    // URL에서 job_id 추출
                    const urlParams = new URLSearchParams(window.location.search);
                    const job_id = urlParams.get('id') || 'unknown';

                    // 기본 정보 추출
                    const titleEl = document.querySelector('h1, .job-title, [class*="title"]');
                    const title = titleEl ? titleEl.textContent.trim() : '';

                    // 회사 정보
                    const companyEl = document.querySelector('[class*="company"]');
                    const company = companyEl ? companyEl.textContent.trim() : 'Posco';

                    // 지역 정보
                    const locationEl = document.querySelector('[class*="location"]');
                    const location = locationEl ? locationEl.textContent.trim() : '';

                    // 공고 설명
                    const descEl = document.querySelector('main, article, .content, [class*="detail"]');
                    const job_description = descEl ? descEl.textContent.trim().substring(0, 500) : '';

                    return {
                        job_id: job_id,
                        title: title,
                        company: company,
                        location: location,
                        job_description: job_description,
                        url: window.location.href,
                        posting_date: new Date().toISOString().split('T')[0],
                        closing_date: '',
                    };
                }
            """
            )

            if job_data and job_data.get("title"):
                # Step: 전체 페이지 스크린샷 캡처
                screenshot_bytes = None
                try:
                    await asyncio.sleep(1)
                    # 전체 페이지가 보이도록 스크롤 맨 위로 이동
                    await page.evaluate("window.scrollTo(0, 0)")
                    await asyncio.sleep(0.5)
                    # 전체 페이지 캡처 (full_page=True)
                    screenshot_bytes = await page.screenshot(full_page=True, timeout=60000)
                    logger.info(f"[{idx}] 스크린샷 캡처 완료 ({len(screenshot_bytes)} bytes)")
                except Exception as e:
                    logger.warning(f"[{idx}] 스크린샷 캡처 실패: {e}")

                job_data["html"] = html_content
                job_data["screenshot"] = screenshot_bytes
                job_data["metadata"] = {
                    "source": "posco",
                    "crawled_index": idx,
                }
                return job_data
            else:
                logger.warning(f"공고 데이터 파싱 실패: {url}")
                return None

        except Exception as e:
            logger.error(f"공고 상세 파싱 실패 ({idx}): {e}")
            return None

    # ========== 내부 메서드 ==========

    async def _get_companies(self, page: Page) -> List[Dict[str, str]]:
        """회사 목록 가져오기"""
        try:
            # 드롭다운이 로드될 때까지 재시도
            for attempt in range(10):
                companies = await page.evaluate(
                    """
                    () => {
                        const select = document.getElementById('SEARCH_COMP');
                        if (!select) return [];

                        const options = Array.from(select.options);
                        return options
                            .filter(opt => opt.value !== '')
                            .map(opt => ({
                                code: opt.value,
                                name: opt.text
                            }));
                    }
                """
                )

                if len(companies) > 0:
                    return companies

                await page.wait_for_timeout(500)

            return []

        except Exception as e:
            logger.error(f"회사 목록 조회 실패: {e}")
            return []

    async def _get_job_list(self, page: Page, base_url: str) -> List[Dict[str, str]]:
        """공고 목록 가져오기 (페이지네이션 처리)"""
        all_jobs = []
        page_num = 1
        max_pages = 50

        while page_num <= max_pages:
            await page.wait_for_timeout(1000)

            # 현재 페이지의 공고 추출
            current_jobs = await self._extract_current_page(page, base_url)

            if current_jobs:
                all_jobs.extend(current_jobs)
                logger.info(f"페이지 {page_num}: {len(current_jobs)}개 추출 (총 {len(all_jobs)}개)")
            else:
                logger.info(f"페이지 {page_num}: 공고 없음")
                # 첫 페이지에서 공고가 없으면 즉시 반환
                if page_num == 1:
                    logger.warning("첫 번째 페이지에서 공고를 찾을 수 없습니다")
                    return all_jobs

            # 다음 버튼 찾기 - 더 다양한 선택자 시도
            next_button = await page.query_selector(
                "a.next:not(.disabled), button.next:not(:disabled), a[onclick*='nextPage']:not(.disabled), a[href*='nextPage'], button[onclick*='nextPage']"
            )

            if not next_button:
                # 마지막 페이지
                logger.info(f"다음 버튼을 찾을 수 없습니다. 총 {len(all_jobs)}개 공고 수집 완료")
                break

            # 다음 페이지로 이동
            try:
                await next_button.click()
                await page.wait_for_timeout(2000)
                page_num += 1
            except Exception as e:
                logger.error(f"다음 페이지 이동 실패: {e}")
                break

        return all_jobs

    async def _extract_current_page(
        self, page: Page, base_url: str
    ) -> List[Dict[str, str]]:
        """현재 페이지의 공고 추출"""
        try:
            jobs = await page.evaluate(
                """
                () => {
                    const rows = document.querySelectorAll('table tbody tr');
                    const jobs = [];
                    console.log(`Found ${rows.length} rows in table`);

                    for (let i = 0; i < rows.length; i++) {
                        const row = rows[i];
                        const cells = row.querySelectorAll('td');
                        console.log(`Row ${i}: ${cells.length} cells`);

                        if (cells.length < 5) continue;

                        // 공고명 셀에서 링크 찾기
                        const titleCell = cells[3];
                        const link = titleCell.querySelector('a');

                        if (link) {
                            let job_id = null;

                            // href에서 id 파라미터 추출
                            const href = link.getAttribute('href') || '';
                            const hrefMatch = href.match(/[?&]id=([^&]+)/);
                            if (hrefMatch) {
                                job_id = hrefMatch[1];
                            }

                            // onclick에서 추출
                            if (!job_id) {
                                const onclick = link.getAttribute('onclick') || '';
                                const onclickMatch = onclick.match(/goDetail\\(['"]([^'"]+)['"]/);
                                if (onclickMatch) {
                                    job_id = onclickMatch[1];
                                }
                            }

                            if (job_id) {
                                jobs.push({
                                    job_id: job_id,
                                    company: cells[1].textContent.trim(),
                                    type: cells[2].textContent.trim(),
                                    title: titleCell.textContent.trim(),
                                    deadline: cells[4].textContent.trim()
                                });
                            }
                        }
                    }

                    return jobs;
                }
            """
            )

            # URL 생성
            job_urls = []
            for job in jobs:
                job_url = f"{base_url}/H22A1001.html?id={job['job_id']}"
                job_urls.append({"url": job_url, "job_id": job["job_id"], "title": job["title"]})

            logger.info(f"_extract_current_page: {len(job_urls)}개 job_url 생성 (총 {len(jobs)}개 job)")
            return job_urls

        except Exception as e:
            logger.error(f"페이지 공고 추출 실패: {e}", exc_info=True)
            return []

    def _normalize_url(self, href: str) -> str:
        """상대 URL을 절대 URL로 변환"""
        if href.startswith("http"):
            return href
        elif href.startswith("/"):
            return "https://recruit.posco.com" + href
        else:
            return "https://recruit.posco.com/" + href

    def _extract_job_id(self, url: str) -> str:
        """URL에서 job_id 추출"""
        # ?id=XXX 형식에서 추출
        import re

        match = re.search(r"id=([^&]+)", url)
        if match:
            return f"posco_{match.group(1)}"
        return f"posco_{url.split('/')[-1]}"
