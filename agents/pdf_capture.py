import time
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service
import json

logger = logging.getLogger(__name__)


class PDFCaptureAgent:
    """
    Selenium을 사용하여 웹페이지를 PDF로 캡처하는 Agent
    """

    def __init__(self, headless: bool = True, chrome_driver_path: Optional[str] = None):
        """
        PDFCaptureAgent 초기화

        Args:
            headless: 헤드리스 모드 사용 여부
            chrome_driver_path: ChromeDriver 경로 (None이면 자동 감지)
        """
        self.headless = headless
        self.chrome_driver_path = chrome_driver_path
        self.driver = None

    def _initialize_driver(self) -> webdriver.Chrome:
        """Chrome 웹드라이버 초기화"""
        options = ChromeOptions()

        if self.headless:
            options.add_argument("--headless")

        # 기본 옵션 설정
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        # User-Agent 설정
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )

        # 드라이버 초기화
        try:
            if self.chrome_driver_path:
                service = Service(self.chrome_driver_path)
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver = webdriver.Chrome(options=options)
            return driver
        except Exception as e:
            logger.error(f"Failed to initialize Chrome driver: {e}")
            raise

    def _scroll_page(self, driver: webdriver.Chrome, wait_time: int) -> None:
        """
        전체 페이지를 스크롤하여 lazy-loading 콘텐츠 로드

        Args:
            driver: Selenium WebDriver
            wait_time: 각 스크롤 사이의 대기 시간(초)
        """
        try:
            # 현재 스크롤 위치
            last_height = driver.execute_script("return document.body.scrollHeight")

            while True:
                # 아래로 스크롤
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(wait_time)

                # 새로운 스크롤 높이
                new_height = driver.execute_script("return document.body.scrollHeight")

                if new_height == last_height:
                    break

                last_height = new_height

            # 페이지 상단으로 스크롤
            driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(1)

        except Exception as e:
            logger.warning(f"Error during page scrolling: {e}")

    def capture_as_pdf(
        self,
        url: str,
        wait_time: int = 5,
        timeout: int = 30,
        scroll: bool = True
    ) -> Optional[bytes]:
        """
        웹페이지를 PDF로 캡처

        Args:
            url: 캡처할 URL
            wait_time: 페이지 로드 후 대기 시간(초)
            timeout: 페이지 로드 타임아웃(초)
            scroll: 전체 페이지 스크롤 여부

        Returns:
            PDF 바이너리 데이터 또는 None (실패 시)
        """
        driver = None
        try:
            driver = self._initialize_driver()
            logger.info(f"Navigating to: {url}")

            # 페이지 로드
            driver.get(url)

            # 페이지 로드 완료 대기
            WebDriverWait(driver, timeout).until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )

            # 추가 대기 (동적 콘텐츠 로드)
            time.sleep(wait_time)

            # 전체 페이지 스크롤 (lazy-loading 콘텐츠 로드)
            if scroll:
                self._scroll_page(driver, wait_time=2)

            # PDF로 인쇄
            logger.info("Capturing page as PDF...")
            pdf_bytes = driver.execute_cdp_cmd(
                "Page.printToPDF",
                {
                    "landscape": False,
                    "displayHeaderFooter": False,
                    "printBackground": True,
                    "scale": 1,
                    "paperWidth": 8.5,
                    "paperHeight": 11,
                    "marginTop": 0,
                    "marginBottom": 0,
                    "marginLeft": 0,
                    "marginRight": 0,
                }
            )

            # 바이너리 데이터 추출
            pdf_data = pdf_bytes.get("data")
            if pdf_data:
                logger.info(f"PDF captured successfully from {url}")
                return pdf_data.encode("latin1")
            else:
                logger.error("No PDF data returned from Chrome")
                return None

        except Exception as e:
            logger.error(f"Error capturing PDF from {url}: {e}")
            return None

        finally:
            if driver:
                try:
                    driver.quit()
                except Exception as e:
                    logger.warning(f"Error closing driver: {e}")

    def capture_as_pdf_bulk(
        self,
        urls: list,
        wait_time: int = 5,
        timeout: int = 30,
        scroll: bool = True
    ) -> dict:
        """
        여러 URL을 PDF로 캡처

        Args:
            urls: 캡처할 URL 리스트
            wait_time: 페이지 로드 후 대기 시간(초)
            timeout: 페이지 로드 타임아웃(초)
            scroll: 전체 페이지 스크롤 여부

        Returns:
            {url: pdf_bytes} 또는 {url: None} (실패 시)
        """
        results = {}

        for url in urls:
            try:
                pdf_bytes = self.capture_as_pdf(
                    url=url,
                    wait_time=wait_time,
                    timeout=timeout,
                    scroll=scroll
                )
                results[url] = pdf_bytes
            except Exception as e:
                logger.error(f"Failed to capture {url}: {e}")
                results[url] = None

        return results
