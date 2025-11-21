import asyncio
import logging
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class NaverCrawler(BaseCrawler):
    """
    네이버 채용 공고 크롤러 (Playwright 기반)

    네이버 채용공고 페이지에서 모든 공고를 무한 스크롤로 수집합니다.
    https://recruit.navercorp.com/rcrt/list.do
    """

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "Naver"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            네이버 채용공고 URL 리스트
        """
        return [
            "https://recruit.navercorp.com/rcrt/list.do",
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
            logger.info("네이버 채용공고 링크 추출 중 (무한 스크롤)...")
            
            # 페이지 네비게이션
            urls = self.get_job_list_urls()
            base_url = urls[0]
            logger.info(f"네이버 채용 페이지 로딩: {base_url}")
            await page.goto(base_url, wait_until="networkidle", timeout=self.get_timeout())
            await asyncio.sleep(3)  # 초기 로딩 대기

            # 무한 스크롤로 모든 공고 로드
            previous_count = 0
            max_attempts = 50  # 무한 루프 방지
            attempts = 0

            while attempts < max_attempts:
                # 현재 공고 개수 확인
                current_count = await page.locator("li.card_item").count()

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

                # 페이지 끝까지 스크롤
                await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                await page.wait_for_timeout(2000)
                await asyncio.sleep(1.5)

            # 모든 공고 카드에서 annoId와 제목 추출
            logger.info("공고 정보 수집 중...")
            job_cards = await page.locator("li.card_item").all()
            logger.info(f"총 {len(job_cards)}개 카드 발견")

            job_urls = []

            for idx, card in enumerate(job_cards, 1):
                try:
                    # 제목 추출
                    try:
                        title_elem = card.locator("h4.card_title").first
                        title_count = await title_elem.count()
                        if title_count > 0:
                            title = await title_elem.inner_text(timeout=2000)
                            title = title.strip()
                        else:
                            title = f"unknown_{idx}"
                    except:
                        title = f"unknown_{idx}"

                    # annoId 추출
                    anno_id = ""
                    try:
                        # 방법 1: onclick 속성에서 추출
                        onclick_attr = await card.get_attribute("onclick")
                        if onclick_attr and "show(" in onclick_attr:
                            anno_id = onclick_attr.split("show(")[1].split(")")[0].strip("'\"")
                    except:
                        pass

                    if not anno_id:
                        try:
                            # 방법 2: a 태그의 onclick에서 추출
                            link = card.locator("a").first
                            link_count = await link.count()
                            if link_count > 0:
                                onclick_attr = await link.get_attribute("onclick")
                                if onclick_attr and "show(" in onclick_attr:
                                    anno_id = onclick_attr.split("show(")[1].split(")")[0].strip("'\"")
                        except:
                            pass

                    if not anno_id:
                        try:
                            # 방법 3: data 속성에서 추출
                            anno_id = await card.get_attribute("data-annoid")
                            if not anno_id:
                                anno_id = await card.get_attribute("data-id")
                        except:
                            pass

                    if anno_id:
                        # URL 구성
                        detail_url = f"https://recruit.navercorp.com/rcrt/view.do?annoId={anno_id}"
                        job_urls.append({
                            "url": detail_url,
                            "job_id": self._extract_job_id(detail_url),
                            "title": title
                        })
                        logger.debug(f"[{idx}/{len(job_cards)}] {title[:40]}... (annoId: {anno_id})")

                except Exception as e:
                    logger.warning(f"카드 처리 실패 [{idx}/{len(job_cards)}]: {e}")
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
            job_id (annoId)
        """
        try:
            if "annoId=" in url:
                anno_id = url.split("annoId=")[1].split("&")[0]
                return f"naver_{anno_id}"
            return f"naver_{hash(url) % 100000}"
        except:
            return f"naver_{hash(url) % 100000}"


    async def parse_job_detail(self, page, url: str, idx: int):
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
            return None

    def get_wait_time(self) -> int:
        """PDF 캡처 대기 시간(초)"""
        return 3

    def requires_selenium(self) -> bool:
        """Selenium 사용 여부"""
        return False
