import json
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict

from crawlers import CrawlerRegistry
from agents import PDFCaptureAgent, StorageAgent

logger = logging.getLogger(__name__)


class CrawlState(TypedDict):
    """크롤링 워크플로우 상태"""
    company_name: str
    job_list_urls: List[str]
    html_pages: Dict[str, str]
    job_urls: List[Dict[str, str]]
    pdf_results: Dict[str, Optional[bytes]]
    storage_results: List[Dict[str, Any]]
    error_logs: List[str]
    success_count: int
    failed_count: int


class IntegratedCrawlerOrchestrator:
    """
    LangGraph 기반 통합 크롤러 오케스트레이터

    워크플로우:
    1. fetch_job_list_page: 채용 목록 페이지 다운로드
    2. extract_job_urls: 개별 공고 URL 추출
    3. capture_pdfs: 개별 공고를 PDF로 캡처
    4. store_pdfs: PDF를 저장소에 저장
    """

    def __init__(
        self,
        registry: CrawlerRegistry,
        storage_agent: Optional[StorageAgent] = None,
        pdf_capture_agent: Optional[PDFCaptureAgent] = None,
    ):
        """
        오케스트레이터 초기화

        Args:
            registry: CrawlerRegistry 인스턴스
            storage_agent: StorageAgent 인스턴스 (None이면 자동 생성)
            pdf_capture_agent: PDFCaptureAgent 인스턴스 (None이면 자동 생성)
        """
        self.registry = registry
        self.storage_agent = storage_agent or StorageAgent()
        self.pdf_capture_agent = pdf_capture_agent or PDFCaptureAgent()
        self.graph = self._build_workflow()

    def _build_workflow(self) -> StateGraph:
        """LangGraph 워크플로우 빌드"""
        workflow = StateGraph(CrawlState)

        # 노드 추가
        workflow.add_node("fetch_job_list_page", self._fetch_job_list_page)
        workflow.add_node("extract_job_urls", self._extract_job_urls)
        workflow.add_node("capture_pdfs", self._capture_pdfs)
        workflow.add_node("store_pdfs", self._store_pdfs)

        # 엣지 추가
        workflow.add_edge(START, "fetch_job_list_page")
        workflow.add_edge("fetch_job_list_page", "extract_job_urls")
        workflow.add_edge("extract_job_urls", "capture_pdfs")
        workflow.add_edge("capture_pdfs", "store_pdfs")
        workflow.add_edge("store_pdfs", END)

        return workflow.compile()

    def _fetch_job_list_page(self, state: CrawlState) -> CrawlState:
        """
        채용 목록 페이지 다운로드

        Args:
            state: 워크플로우 상태

        Returns:
            업데이트된 상태 (html_pages 추가)
        """
        company_name = state["company_name"]
        logger.info(f"Fetching job list pages for {company_name}")

        crawler = self.registry.get_crawler(company_name)
        if not crawler:
            error_msg = f"Crawler for {company_name} not found"
            logger.error(error_msg)
            state["error_logs"].append(error_msg)
            state["job_list_urls"] = []
            state["html_pages"] = {}
            return state

        state["job_list_urls"] = crawler.get_job_list_urls()
        html_pages = {}

        for url in state["job_list_urls"]:
            try:
                if crawler.requires_selenium():
                    # Selenium으로 동적 페이지 로드
                    logger.info(f"Loading dynamic page: {url}")
                    pdf_bytes = self.pdf_capture_agent.capture_as_pdf(
                        url,
                        wait_time=crawler.get_wait_time(),
                        timeout=crawler.get_timeout(),
                        scroll=True
                    )
                    # PDF에서 텍스트 추출 시도 (간단히 HTML로 변환)
                    # 실제로는 pdfplumber 등을 사용해야 함
                    html_pages[url] = ""
                else:
                    # Requests로 정적 페이지 로드
                    logger.info(f"Fetching static page: {url}")
                    response = requests.get(url, timeout=crawler.get_timeout())
                    response.raise_for_status()
                    html_pages[url] = response.text

            except Exception as e:
                error_msg = f"Failed to fetch {url}: {e}"
                logger.error(error_msg)
                state["error_logs"].append(error_msg)

        state["html_pages"] = html_pages
        return state

    def _extract_job_urls(self, state: CrawlState) -> CrawlState:
        """
        개별 공고 URL 추출

        Args:
            state: 워크플로우 상태

        Returns:
            업데이트된 상태 (job_urls 추가)
        """
        company_name = state["company_name"]
        logger.info(f"Extracting job URLs for {company_name}")

        crawler = self.registry.get_crawler(company_name)
        if not crawler:
            return state

        job_urls = []

        for url, html in state["html_pages"].items():
            if not html:
                continue

            try:
                extracted = crawler.extract_job_urls(html)
                job_urls.extend(extracted)
                logger.info(f"Extracted {len(extracted)} job URLs from {url}")

            except Exception as e:
                error_msg = f"Failed to extract job URLs from {url}: {e}"
                logger.error(error_msg)
                state["error_logs"].append(error_msg)

        state["job_urls"] = job_urls
        logger.info(f"Total job URLs extracted: {len(job_urls)}")
        return state

    def _capture_pdfs(self, state: CrawlState) -> CrawlState:
        """
        개별 공고를 PDF로 캡처

        Args:
            state: 워크플로우 상태

        Returns:
            업데이트된 상태 (pdf_results 추가)
        """
        logger.info(f"Capturing PDFs for {len(state['job_urls'])} job postings")

        crawler = self.registry.get_crawler(state["company_name"])
        if not crawler:
            return state

        pdf_results = {}
        success = 0
        failed = 0

        for job_info in state["job_urls"]:
            job_url = job_info["url"]
            try:
                logger.info(f"Capturing PDF: {job_url}")
                pdf_bytes = self.pdf_capture_agent.capture_as_pdf(
                    job_url,
                    wait_time=crawler.get_wait_time(),
                    timeout=crawler.get_timeout(),
                    scroll=True
                )

                if pdf_bytes:
                    pdf_results[job_url] = pdf_bytes
                    success += 1
                else:
                    pdf_results[job_url] = None
                    failed += 1

            except Exception as e:
                error_msg = f"Failed to capture PDF from {job_url}: {e}"
                logger.error(error_msg)
                state["error_logs"].append(error_msg)
                pdf_results[job_url] = None
                failed += 1

        state["pdf_results"] = pdf_results
        state["success_count"] = success
        state["failed_count"] = failed

        logger.info(f"PDF capture completed: {success} success, {failed} failed")
        return state

    def _store_pdfs(self, state: CrawlState) -> CrawlState:
        """
        PDF를 저장소에 저장

        Args:
            state: 워크플로우 상태

        Returns:
            업데이트된 상태 (storage_results 추가)
        """
        logger.info("Storing PDFs")

        storage_results = []
        company_name = state["company_name"]

        for job_info in state["job_urls"]:
            job_url = job_info["url"]
            job_id = job_info.get("job_id", "unknown")
            job_title = job_info.get("title", "")

            pdf_bytes = state["pdf_results"].get(job_url)
            if not pdf_bytes:
                continue

            try:
                result = self.storage_agent.save_pdf(
                    pdf_bytes=pdf_bytes,
                    company=company_name,
                    job_id=job_id,
                    job_title=job_title,
                    subfolder=datetime.now().strftime("%Y-%m-%d")
                )

                storage_results.append({
                    "job_id": job_id,
                    "job_url": job_url,
                    "job_title": job_title,
                    **result
                })

                if result["success"]:
                    logger.info(f"Stored PDF: {job_id}")
                else:
                    error_msg = f"Failed to store PDF: {job_id}"
                    logger.error(error_msg)
                    state["error_logs"].append(error_msg)

            except Exception as e:
                error_msg = f"Error storing PDF {job_id}: {e}"
                logger.error(error_msg)
                state["error_logs"].append(error_msg)

        state["storage_results"] = storage_results
        logger.info(f"Stored {len(storage_results)} PDFs")
        return state

    def run_company(self, company_name: str) -> Dict[str, Any]:
        """
        특정 회사의 채용공고 크롤링 실행

        Args:
            company_name: 회사명

        Returns:
            크롤링 결과
        """
        if not self.registry.is_registered(company_name):
            logger.error(f"Crawler for {company_name} is not registered")
            return {"success": False, "error": f"Crawler for {company_name} not found"}

        logger.info(f"Starting crawl for {company_name}")

        initial_state: CrawlState = {
            "company_name": company_name,
            "job_list_urls": [],
            "html_pages": {},
            "job_urls": [],
            "pdf_results": {},
            "storage_results": [],
            "error_logs": [],
            "success_count": 0,
            "failed_count": 0,
        }

        try:
            final_state = self.graph.invoke(initial_state)

            result = {
                "success": True,
                "company_name": company_name,
                "total_jobs": len(final_state["job_urls"]),
                "pdfs_captured": len([p for p in final_state["pdf_results"].values() if p]),
                "pdfs_stored": len(final_state["storage_results"]),
                "storage_results": final_state["storage_results"],
                "error_logs": final_state["error_logs"],
                "timestamp": datetime.now().isoformat(),
            }

            logger.info(f"Crawl completed for {company_name}: {result}")
            return result

        except Exception as e:
            logger.error(f"Crawl failed for {company_name}: {e}")
            return {
                "success": False,
                "company_name": company_name,
                "error": str(e),
                "timestamp": datetime.now().isoformat(),
            }

    def run_all_companies(self) -> Dict[str, Dict[str, Any]]:
        """
        등록된 모든 회사의 채용공고 크롤링 실행

        Returns:
            {company_name: result} 형식의 결과
        """
        companies = self.registry.list_companies()
        logger.info(f"Starting crawl for all companies: {companies}")

        results = {}
        for company_name in companies:
            results[company_name] = self.run_company(company_name)

        return results

    def save_results_to_json(self, results: Dict, file_path: str) -> bool:
        """
        크롤링 결과를 JSON 파일로 저장

        Args:
            results: 크롤링 결과
            file_path: 저장할 파일 경로

        Returns:
            성공 여부
        """
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            logger.info(f"Results saved to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save results: {e}")
            return False
