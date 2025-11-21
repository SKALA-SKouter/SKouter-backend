import asyncio
import logging
import random
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class PlaywrightCaptureAgent:
    """
    Playwright를 사용하여 웹페이지를 이미지로 캡처하는 Agent
    동적 콘텐츠 로드 및 봇 탐지 회피에 최적화되어 있음
    """

    def __init__(self, headless: bool = True):
        """
        PlaywrightCaptureAgent 초기화

        Args:
            headless: 헤드리스 모드 사용 여부
        """
        self.headless = headless
        # 실제 브라우저의 User-Agent들
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
        ]

    async def capture_as_image(
        self,
        url: str,
        wait_time: int = 5,
        timeout: int = 60000,
        scroll: bool = True,
        image_format: str = "png",
        stealth_mode: bool = True,
        use_viewport_only: bool = True,
        viewport_width: int = 1920,
        viewport_height: int = 1080
    ) -> Optional[bytes]:
        """
        Playwright로 웹페이지를 이미지로 캡처 (봇 탐지 회피 적용)

        Args:
            url: 캡처할 URL
            wait_time: 페이지 로드 후 대기 시간(초)
            timeout: 페이지 로드 타임아웃(밀리초)
            scroll: 전체 페이지 스크롤 여부
            image_format: 이미지 포맷 ('png' 또는 'jpeg')
            stealth_mode: 봇 탐지 회피 모드 사용 여부
            use_viewport_only: viewport만 캡처할지 여부 (전체 페이지 캡처 시 차단될 수 있음)

        Returns:
            이미지 바이너리 데이터 또는 None (실패 시)
        """
        try:
            from playwright.async_api import async_playwright
            from playwright_stealth import Stealth

            async with async_playwright() as p:
                # 봇 탐지 우회 브라우저 인자들
                launch_args = [
                    "--disable-blink-features=AutomationControlled",
                    "--no-service-autorun",
                ]

                browser = await p.chromium.launch(
                    headless=self.headless,
                    args=launch_args
                )

                # 컨텍스트 생성 시 속임수 적용
                context = await browser.new_context(
                    viewport={"width": viewport_width, "height": viewport_height},
                    user_agent=random.choice(self.user_agents),
                    # 타임존과 로케이션 설정 (자연스러운 환경)
                    locale="ko-KR",
                    timezone_id="Asia/Seoul",
                    geolocation={"latitude": 37.5665, "longitude": 126.9780},
                    permissions=["geolocation"],
                )

                page = await context.new_page()

                # Stealth 모드 적용
                if stealth_mode:
                    stealth_instance = Stealth()
                    await stealth_instance.apply_stealth_async(page)

                try:
                    logger.info(f"[Stealth] Navigating to: {url}")

                    # 봇 탐지 스크립트 무시
                    await page.add_init_script("""
                        // Playwright 탐지 우회
                        Object.defineProperty(navigator, 'webdriver', {
                            get: () => false,
                        });

                        // Chrome 탐지 우회
                        Object.defineProperty(navigator, 'plugins', {
                            get: () => [1, 2, 3, 4, 5],
                        });

                        // Permission 체크 우회
                        const originalQuery = window.navigator.permissions.query;
                        window.navigator.permissions.query = (parameters) => (
                            parameters.name === 'notifications' ?
                                Promise.resolve({ state: Notification.permission }) :
                                originalQuery(parameters)
                        );
                    """)

                    # 페이지 로드 (load로 시작, 타임아웃 안 나도록)
                    try:
                        await page.goto(url, wait_until="domcontentloaded", timeout=timeout)
                    except:
                        logger.warning(f"Timeout during goto, continuing...")
                        await page.wait_for_load_state("load", timeout=10000)

                    # 랜덤 대기 (인간적인 패턴)
                    await asyncio.sleep(random.uniform(wait_time, wait_time + 3))

                    # Cloudflare 체크
                    try:
                        cloudflare_check = await page.query_selector("div.cf-browser-verification")
                        if cloudflare_check:
                            logger.warning("[Stealth] Cloudflare 감지, 추가 대기...")
                            await asyncio.sleep(random.uniform(8, 12))
                    except:
                        pass

                    # 전체 페이지 스크롤 (lazy-loading 콘텐츠 로드) - 더 자연스럽게
                    if scroll:
                        await self._smart_scroll_page(page)
                    else:
                        # 스크롤 없어도 마우스 움직임 추가 (자연스러움)
                        await page.mouse.move(random.randint(100, 1800), random.randint(100, 1000))
                        await asyncio.sleep(random.uniform(0.5, 1.5))

                    logger.info(f"[Stealth] Capturing page as {image_format.upper()} image...")

                    # viewport만 캡처 (full_page=True는 차단될 수 있음)
                    image_bytes = await page.screenshot(
                        path=None,
                        full_page=not use_viewport_only,
                        type=image_format,
                        quality=95 if image_format == "jpeg" else None
                    )

                    logger.info(f"[Stealth] Image captured successfully from {url}")
                    return image_bytes

                finally:
                    await context.close()
                    await browser.close()

        except Exception as e:
            logger.error(f"[Stealth] Error capturing image from {url}: {e}")
            return None

    async def capture_as_pdf(
        self,
        url: str,
        wait_time: int = 5,
        timeout: int = 60000,
        scroll: bool = True
    ) -> Optional[bytes]:
        """
        (호환성 유지) Playwright로 웹페이지를 이미지로 캡처

        주의: 이전 PDF 캡처 대신 이미지 캡처를 수행합니다.

        Args:
            url: 캡처할 URL
            wait_time: 페이지 로드 후 대기 시간(초)
            timeout: 페이지 로드 타임아웃(밀리초)
            scroll: 전체 페이지 스크롤 여부

        Returns:
            이미지 바이너리 데이터 또는 None (실패 시)
        """
        logger.warning("capture_as_pdf() is deprecated, using capture_as_image() instead")
        return await self.capture_as_image(
            url=url,
            wait_time=wait_time,
            timeout=timeout,
            scroll=scroll,
            image_format="png"
        )

    async def _smart_scroll_page(self, page) -> None:
        """
        자연스럽게 페이지를 스크롤하여 lazy-loading 콘텐츠 로드 (봇 탐지 회피)

        Args:
            page: Playwright page 객체
        """
        try:
            last_height = await page.evaluate("document.body.scrollHeight")
            scroll_count = 0
            max_scrolls = 10  # 최대 스크롤 횟수 제한

            while scroll_count < max_scrolls:
                # 랜덤한 높이만큼 스크롤 (자연스러운 패턴)
                scroll_amount = random.randint(300, 800)
                await page.evaluate(f"window.scrollBy(0, {scroll_amount})")

                # 랜덤 대기 (마우스 움직임도 추가)
                await asyncio.sleep(random.uniform(0.5, 1.5))
                await page.mouse.move(
                    random.randint(100, 1800),
                    random.randint(100, 1000)
                )

                # 새로운 스크롤 높이
                new_height = await page.evaluate("document.body.scrollHeight")

                if new_height == last_height:
                    # 더 이상 콘텐츠가 로드되지 않으면 종료
                    break

                last_height = new_height
                scroll_count += 1

            # 페이지 상단으로 천천히 스크롤
            await page.evaluate("window.scrollTo(0, 0)")
            await asyncio.sleep(random.uniform(1, 2))

        except Exception as e:
            logger.warning(f"[Stealth] Error during page scrolling: {e}")

    async def _scroll_page(self, page) -> None:
        """
        (호환성 유지) 기존 _scroll_page는 _smart_scroll_page로 위임

        Args:
            page: Playwright page 객체
        """
        await self._smart_scroll_page(page)

    async def capture_as_image_bulk(
        self,
        urls: list,
        wait_time: int = 5,
        timeout: int = 60000,
        scroll: bool = True,
        image_format: str = "png"
    ) -> dict:
        """
        여러 URL을 이미지로 캡처

        Args:
            urls: 캡처할 URL 리스트
            wait_time: 페이지 로드 후 대기 시간(초)
            timeout: 페이지 로드 타임아웃(밀리초)
            scroll: 전체 페이지 스크롤 여부
            image_format: 이미지 포맷 ('png' 또는 'jpeg')

        Returns:
            {url: image_bytes} 또는 {url: None} (실패 시)
        """
        results = {}

        for url in urls:
            try:
                image_bytes = await self.capture_as_image(
                    url=url,
                    wait_time=wait_time,
                    timeout=timeout,
                    scroll=scroll,
                    image_format=image_format
                )
                results[url] = image_bytes
            except Exception as e:
                logger.error(f"Failed to capture {url}: {e}")
                results[url] = None

        return results

    async def capture_as_pdf_bulk(
        self,
        urls: list,
        wait_time: int = 5,
        timeout: int = 60000,
        scroll: bool = True
    ) -> dict:
        """
        (호환성 유지) 여러 URL을 이미지로 캡처

        주의: PDF 대신 이미지로 캡처합니다.

        Args:
            urls: 캡처할 URL 리스트
            wait_time: 페이지 로드 후 대기 시간(초)
            timeout: 페이지 로드 타임아웃(밀리초)
            scroll: 전체 페이지 스크롤 여부

        Returns:
            {url: image_bytes} 또는 {url: None} (실패 시)
        """
        logger.warning("capture_as_pdf_bulk() is deprecated, using capture_as_image_bulk() instead")
        return await self.capture_as_image_bulk(
            urls=urls,
            wait_time=wait_time,
            timeout=timeout,
            scroll=scroll,
            image_format="png"
        )
