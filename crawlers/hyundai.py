import asyncio
import json
import logging
import re
from typing import List, Dict, Optional, Any
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class HyundaiAutoEverCrawler(BaseCrawler):
    """
    현대오토에버 채용 공고 크롤러 (API 기반)

    Next.js 기반으로 동작하며, apply.json API에서 직접 공고 데이터를 수집합니다.
    URL: https://career.hyundai-autoever.com
    """

    def __init__(self):
        """초기화"""
        self.job_ids = set()
        self.build_id = None  # 동적 빌드 ID 저장

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "Hyundai"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            현대오토에버 채용공고 URL 리스트
        """
        return [
            "https://career.hyundai-autoever.com/ko/apply",
        ]

    async def _extract_build_id(self, page: Any) -> str:
        """
        Next.js 동적 빌드 ID 추출

        Args:
            page: Playwright page 객체

        Returns:
            빌드 ID 문자열
        """
        try:
            # 페이지 소스에서 빌드 ID 추출
            html = await page.content()

            # Next.js 빌드 ID 패턴들 (여러 개 시도):
            # 1. /_next/data/{BUILD_ID}/ 패턴 (더 정확함)
            # 2. /_next/static/{BUILD_ID}/ 패턴
            # 3. 기타 패턴
            patterns = [
                r'/_next/data/([A-Za-z0-9_-]+)/',              # _next/data 패턴 (가장 직접적)
                r'/_next/static/([A-Za-z0-9_-]{20,}?)/',       # 긴 문자열 (_next/static)
                r'"buildId":"([A-Za-z0-9_-]+)"',               # JSON에 명시된 buildId
            ]

            for pattern in patterns:
                match = re.search(pattern, html)
                if match:
                    build_id = match.group(1)
                    # CSS, JS 같은 파일명은 제외
                    if build_id not in ['css', 'js', 'json', 'html'] and len(build_id) > 5:
                        logger.debug(f"추출된 빌드 ID: {build_id}")
                        return build_id

            logger.warning("빌드 ID를 페이지에서 추출할 수 없음, 기본값 사용")
            return None
        except Exception as e:
            logger.error(f"빌드 ID 추출 실패: {e}")
            return None

    async def extract_job_urls(self, page: Any) -> List[Dict[str, str]]:
        """
        API에서 모든 공고 URL 추출

        Args:
            page: Playwright page 객체

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        try:
            logger.info("현대오토에버 채용공고 API에서 추출 중...")

            # 페이지 네비게이션
            urls = self.get_job_list_urls()
            base_url = urls[0]
            logger.info(f"페이지 로딩: {base_url}")

            # 페이지 로드
            await page.goto(base_url, wait_until="domcontentloaded", timeout=self.get_timeout())
            await asyncio.sleep(2)

            # 빌드 ID 추출
            build_id = await self._extract_build_id(page)
            if not build_id:
                logger.error("빌드 ID를 추출할 수 없음, 기본값 사용")
                build_id = "1Zpy49sCh_Kc82YSMD2YB"

            # apply.json API 호출
            api_url = f"https://career.hyundai-autoever.com/_next/data/{build_id}/ko/apply.json?locale=ko&page=apply"
            logger.info(f"API URL: {api_url}")

            response = await page.context.request.get(api_url, timeout=30000)

            if not response.ok:
                logger.error(f"API 응답 실패: {response.status}")
                return []

            # JSON 파싱
            body = await response.text()
            data = json.loads(body)

            # 공고 데이터 추출
            job_urls = []

            if "pageProps" in data and "dehydratedState" in data["pageProps"]:
                dehydrated = data["pageProps"]["dehydratedState"]

                if "queries" in dehydrated:
                    queries = dehydrated["queries"]

                    # Query 2: openings 배열 찾기
                    for query in queries:
                        query_key = query.get("queryKey", [])
                        if isinstance(query_key, list) and len(query_key) > 0 and query_key[0] == "openings":
                            state_data = query.get("state", {}).get("data", [])

                            if isinstance(state_data, list):
                                logger.info(f"API에서 {len(state_data)}개 공고 발견")

                                for opening in state_data:
                                    try:
                                        opening_id = opening.get("openingId")
                                        title = opening.get("title", "Unknown")

                                        if opening_id:
                                            url = f"https://career.hyundai-autoever.com/ko/o/{opening_id}"
                                            job_urls.append({
                                                "url": url,
                                                "job_id": f"hyundai_{opening_id}",
                                                "title": title
                                            })
                                            logger.debug(f"[{len(job_urls)}] {title[:50]}")
                                    except Exception as e:
                                        logger.debug(f"공고 처리 오류: {e}")
                                        continue
                            break

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
            # URL 패턴: https://career.hyundai-autoever.com/ko/o/{job_id}
            match = re.search(r'/o/(\d+)', url)
            if match:
                job_id = match.group(1)
                return f"hyundai_{job_id}"

            return f"hyundai_{hash(url) % 100000}"
        except:
            return f"hyundai_{hash(url) % 100000}"

    async def parse_job_detail(self, page: Any, url: str, idx: int) -> Optional[Dict[str, str]]:
        """공고 상세 페이지 파싱"""
        try:
            # 페이지 로드 시도 (연결 오류 시 재시도)
            max_retries = 2
            for attempt in range(max_retries):
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=self.get_timeout())
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.debug(f"페이지 로드 재시도 [{attempt+1}/{max_retries}]: {e}")
                        await asyncio.sleep(1)
                    else:
                        raise

            await asyncio.sleep(self.get_wait_time())

            html = await page.content()

            # 기본 정보 추출
            title = ""
            try:
                soup = BeautifulSoup(html, 'html.parser')
                # h1 태그에서 제목 추출
                h1 = soup.find('h1')
                if h1:
                    title = h1.get_text(strip=True)
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
            # 전체 실패가 아니라 부분 실패로 처리 (기본 정보만 반환)
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
        """페이지 로드 후 대기 시간(초) - 최소화"""
        return 1

    def get_timeout(self) -> int:
        """페이지 로드 타임아웃(밀리초) - 짧게"""
        return 30000  # 30초로 단축

    def requires_selenium(self) -> bool:
        """Selenium 사용 여부"""
        return False
