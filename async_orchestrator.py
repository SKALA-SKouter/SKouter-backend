"""
비동기 Playwright 기반 크롤링 오케스트레이터

특징:
- 완전 비동기 처리
- 이미지 캡처 지원 (PNG/JPEG)
- HTML, 스크린샷 저장
- 동시 처리로 성능 최적화
"""

import asyncio
import json
import logging
import base64
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from dataclasses import dataclass, asdict

from playwright.async_api import async_playwright, Page
from playwright_stealth import Stealth
from crawlers import CrawlerRegistry, BaseCrawler
from agents import StorageAgent, PlaywrightCaptureAgent

logger = logging.getLogger(__name__)


@dataclass
class JobPostingData:
    """채용공고 데이터 모델"""
    url: str
    job_id: str
    title: str
    company: str
    html_content: str  # 원본 HTML
    posting_date: str
    closing_date: str
    location: str
    job_description: str
    required_qualifications: str
    preferred_qualifications: str
    company_description: str
    team_description: str
    selection_process: str
    notes: str
    metadata: Dict[str, Any]
    vector_embedding: Optional[List[float]] = None  # 벡터 임베딩
    screenshot_bytes: Optional[bytes] = None  # 스크린샷 바이너리 데이터
    created_at: str = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """딕셔너리로 변환"""
        return asdict(self)

    def to_json_metadata(self) -> str:
        """JSON 메타데이터로 변환 (HTML, 스크린샷, 벡터 제외)"""
        data = self.to_dict()
        data.pop("html_content", None)  # HTML은 제외
        data.pop("screenshot_bytes", None)  # 스크린샷 바이너리는 제외
        data.pop("vector_embedding", None)  # 벡터도 제외
        return json.dumps(data, ensure_ascii=False, indent=2)


class AsyncPlaywrightOrchestrator:
    """
    비동기 Playwright 기반 크롤링 오케스트레이터

    워크플로우:
    1. 채용 목록 페이지 오픈
    2. 개별 공고 URL 추출
    3. 각 공고 상세 정보 파싱 (병렬 처리)
    4. 이미지 캡처 - PNG 포맷 (병렬 처리)
    5. 저장소에 저장 (HTML + PNG 이미지만 저장, 메타데이터 제외)
    """

    def __init__(
        self,
        registry: CrawlerRegistry,
        storage_agent: Optional[StorageAgent] = None,
        playwright_capture_agent: Optional[PlaywrightCaptureAgent] = None,
        headless: bool = True,
        use_vector_embedding: bool = False,
    ):
        """
        오케스트레이터 초기화

        Args:
            registry: CrawlerRegistry 인스턴스
            storage_agent: StorageAgent 인스턴스
            playwright_capture_agent: PlaywrightCaptureAgent 인스턴스
            headless: 헤드리스 모드
            use_vector_embedding: 벡터 임베딩 사용 여부
        """
        self.registry = registry
        self.storage_agent = storage_agent or StorageAgent()
        self.playwright_capture_agent = playwright_capture_agent or PlaywrightCaptureAgent(headless=headless)
        self.headless = headless
        self.use_vector_embedding = use_vector_embedding

    async def crawl_company(self, company_name: str, max_jobs: Optional[int] = None) -> Dict[str, Any]:
        """
        특정 회사 크롤링 (비동기)

        Args:
            company_name: 회사명
            max_jobs: 최대 공고 수 (None이면 전체)

        Returns:
            크롤링 결과
        """
        crawler = self.registry.get_crawler(company_name)
        if not crawler:
            logger.error(f"Crawler for {company_name} not found")
            return {"success": False, "error": f"Crawler for {company_name} not found"}

        logger.info(f"Starting crawl for {company_name}")
        start_time = datetime.now()

        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=self.headless)
                context = await browser.new_context(
                    viewport={"width": 1920, "height": 1080},
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    locale="ko-KR",
                )

                job_listings = []
                storage_results = []
                error_logs = []

                try:
                    # 1. 채용 목록 페이지에서 공고 URL 추출
                    page = await context.new_page()
                    # CloudFlare 우회를 위한 stealth 모드 적용
                    stealth = Stealth()
                    await stealth.apply_stealth_async(page)
                    job_urls = await self._extract_job_urls(page, crawler)

                    if max_jobs:
                        job_urls = job_urls[:max_jobs]

                    logger.info(f"Found {len(job_urls)} job postings")

                    # 2. 각 공고 상세 정보 파싱 (병렬 처리)
                    max_concurrent = crawler.get_max_concurrent_jobs()
                    job_postings = await self._parse_jobs_concurrent(
                        context, crawler, job_urls, max_concurrent
                    )

                    job_listings = [j for j in job_postings if j is not None]
                    logger.info(f"Parsed {len(job_listings)} job details")

                    # 3. PDF 캡처 및 저장 (병렬 처리)
                    storage_results = await self._save_jobs_concurrent(
                        job_listings, crawler, max_concurrent
                    )

                    logger.info(f"Saved {len([r for r in storage_results if r['success']])} jobs")

                except Exception as e:
                    error_msg = f"Error during crawling: {e}"
                    logger.error(error_msg, exc_info=True)
                    error_logs.append(error_msg)

                finally:
                    await context.close()
                    await browser.close()

                # 결과 정리
                elapsed = (datetime.now() - start_time).total_seconds()
                result = {
                    "success": len(job_listings) > 0,
                    "company_name": company_name,
                    "total_jobs": len(job_listings),
                    "successful_saves": len([r for r in storage_results if r["success"]]),
                    "failed_saves": len([r for r in storage_results if not r["success"]]),
                    "job_listings": job_listings,
                    "storage_results": storage_results,
                    "error_logs": error_logs,
                    "elapsed_seconds": elapsed,
                    "timestamp": datetime.now().isoformat(),
                }

                logger.info(f"Crawl completed for {company_name} in {elapsed:.2f}s")
                return result

        except Exception as e:
            logger.error(f"Fatal error in crawl_company: {e}", exc_info=True)
            return {
                "success": False,
                "company_name": company_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    async def crawl_all_companies(self, max_jobs: Optional[int] = None) -> Dict[str, Any]:
        """
        등록된 모든 회사 크롤링 (병렬 처리)

        Args:
            max_jobs: 회사당 최대 공고 수

        Returns:
            전체 크롤링 결과
        """
        companies = self.registry.list_companies()
        logger.info(f"Starting crawl for {len(companies)} companies")

        # 모든 회사를 병렬로 크롤링
        tasks = [self.crawl_company(company, max_jobs) for company in companies]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # 결과 정리
        company_results = {}
        for company, result in zip(companies, results):
            if isinstance(result, Exception):
                company_results[company] = {
                    "success": False,
                    "error": str(result),
                }
            else:
                company_results[company] = result

        return {
            "companies": company_results,
            "timestamp": datetime.now().isoformat(),
        }

    async def _extract_job_urls(self, page: Page, crawler: BaseCrawler) -> List[Dict[str, str]]:
        """채용 목록 페이지에서 공고 URL 추출"""
        try:
            # 크롤러의 extract_job_urls 메서드 호출 (회사별 맞춤 로직)
            logger.info(f"Calling {crawler.get_company_name()}'s extract_job_urls method")
            job_urls = await crawler.extract_job_urls(page)
            logger.info(f"Extracted {len(job_urls)} unique job URLs")
            return job_urls

        except Exception as e:
            logger.error(f"Error extracting job URLs: {e}", exc_info=True)
            return []

    async def _parse_jobs_concurrent(
        self,
        context,
        crawler: BaseCrawler,
        job_urls: List[Dict[str, str]],
        max_concurrent: int
    ) -> List[Optional[JobPostingData]]:
        """공고들을 병렬로 파싱"""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def parse_with_semaphore(url_dict: Dict[str, str], idx: int):
            async with semaphore:
                page = await context.new_page()
                # CloudFlare 우회를 위한 stealth 모드 적용
                stealth = Stealth()
                await stealth.apply_stealth_async(page)
                try:
                    job_data = await crawler.parse_job_detail(page, url_dict["url"], idx)

                    if job_data:
                        # 원본 HTML 캡처 (parse_job_detail에서 제공하지 않으면 현재 page에서 가져오기)
                        html_content = job_data.get("html", "")
                        if not html_content:
                            html_content = await page.content()

                        # 스크린샷 (parse_job_detail에서 제공된 경우만 사용)
                        screenshot_bytes = job_data.get("screenshot", None)

                        return JobPostingData(
                            url=job_data.get("url", url_dict["url"]),
                            job_id=job_data.get("job_id", url_dict.get("job_id", f"job_{idx}")),
                            title=job_data.get("title", ""),
                            company=job_data.get("company", crawler.get_company_name()),
                            html_content=html_content,
                            posting_date=job_data.get("posting_date", ""),
                            closing_date=job_data.get("closing_date", ""),
                            location=job_data.get("location", ""),
                            job_description=job_data.get("job_description", ""),
                            required_qualifications=job_data.get("required_qualifications", ""),
                            preferred_qualifications=job_data.get("preferred_qualifications", ""),
                            company_description=job_data.get("company_description", ""),
                            team_description=job_data.get("team_description", ""),
                            selection_process=job_data.get("selection_process", ""),
                            notes=job_data.get("notes", ""),
                            metadata=job_data.get("metadata", {}),
                            screenshot_bytes=screenshot_bytes,
                        )
                    return None

                except Exception as e:
                    logger.error(f"Error parsing job {idx}: {e}")
                    return None

                finally:
                    await page.close()

        # 병렬 파싱
        tasks = [
            parse_with_semaphore(url_dict, idx)
            for idx, url_dict in enumerate(job_urls, 1)
        ]
        return await asyncio.gather(*tasks)

    async def _save_jobs_concurrent(
        self,
        job_listings: List[JobPostingData],
        crawler: BaseCrawler,
        max_concurrent: int
    ) -> List[Dict[str, Any]]:
        """공고들을 병렬로 저장"""
        semaphore = asyncio.Semaphore(max_concurrent)

        async def save_with_semaphore(job: JobPostingData):
            async with semaphore:
                try:
                    company = crawler.get_company_name()
                    subfolder = datetime.now().strftime("%Y-%m-%d")

                    # 1. HTML 저장
                    html_path = await asyncio.to_thread(
                        self._save_html,
                        job.html_content,
                        company,
                        job.job_id,
                        job.title,
                        subfolder,
                    )

                    # 2. 스크린샷 저장 (parse_job_detail에서 제공된 경우)
                    screenshot_path = None
                    if job.screenshot_bytes:
                        screenshot_path = await asyncio.to_thread(
                            self.storage_agent.save_image_locally,
                            job.screenshot_bytes,
                            company,
                            job.job_id,
                            f"{job.title}_screenshot",
                            subfolder,
                            "png"
                        )
                        logger.info(f"Screenshot saved: {screenshot_path}")
                    else:
                        # 스크린샷이 없으면 PlaywrightCaptureAgent로 캡처 (기존 로직)
                        image_bytes = await self.playwright_capture_agent.capture_as_image(
                            job.url,
                            wait_time=crawler.get_wait_time(),
                            timeout=crawler.get_timeout(),
                            image_format="png"
                        )

                        if image_bytes:
                            screenshot_path = await asyncio.to_thread(
                                self.storage_agent.save_image_locally,
                                image_bytes,
                                company,
                                job.job_id,
                                job.title,
                                subfolder,
                                "png"
                            )

                    return {
                        "success": True,
                        "job_id": job.job_id,
                        "title": job.title,
                        "html_path": html_path,
                        "screenshot_path": screenshot_path,
                    }

                except Exception as e:
                    logger.error(f"Error saving job {job.job_id}: {e}")
                    return {
                        "success": False,
                        "job_id": job.job_id,
                        "error": str(e),
                    }

        # 병렬 저장
        tasks = [save_with_semaphore(job) for job in job_listings]
        return await asyncio.gather(*tasks)

    def _save_html(
        self,
        html_content: str,
        company: str,
        job_id: str,
        job_title: str,
        subfolder: str
    ) -> str:
        """HTML 파일 저장"""
        base_path = Path("./data/html")
        company_path = base_path / company / subfolder
        company_path.mkdir(parents=True, exist_ok=True)

        # job_id와 title에서 파일명으로 사용 불가능한 문자 제거
        safe_job_id = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in job_id)[:50]
        safe_title = "".join(c if c.isalnum() or c in ('-', '_') else '_' for c in job_title)[:50]
        filename = f"{safe_job_id}_{safe_title}.html"
        filepath = company_path / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html_content)

        logger.info(f"HTML saved: {filepath}")
        return str(filepath)

    def _save_json_metadata(
        self,
        job: JobPostingData,
        company: str,
        job_id: str,
        subfolder: str
    ) -> str:
        """JSON 메타데이터 저장"""
        base_path = Path("./data/metadata")
        company_path = base_path / company / subfolder
        company_path.mkdir(parents=True, exist_ok=True)

        filename = f"{job_id}_metadata.json"
        filepath = company_path / filename

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(job.to_json_metadata())

        logger.info(f"JSON metadata saved: {filepath}")
        return str(filepath)


async def main_example():
    """사용 예제"""
    from crawlers import WoowahanCrawler

    registry = CrawlerRegistry()
    registry.register(WoowahanCrawler())

    orchestrator = AsyncPlaywrightOrchestrator(
        registry=registry,
        headless=True,
        use_vector_embedding=False,
    )

    # 특정 회사 크롤링
    result = await orchestrator.crawl_company("Woowahan", max_jobs=5)
    print(json.dumps(result, indent=2, ensure_ascii=False, default=str))


if __name__ == "__main__":
    asyncio.run(main_example())
