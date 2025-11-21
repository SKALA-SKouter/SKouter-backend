"""
토스 채용 공고 크롤러 (Playwright 기반)

토스의 채용공고를 크롤링합니다.
"""

import asyncio
import logging
import re
from typing import List, Dict, Optional, Any
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class TossCrawler(BaseCrawler):
    """
    토스 채용 공고 크롤러 (Playwright 기반)

    토스의 채용공고를 크롤링합니다.
    """

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "Toss"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            토스 채용공고 URL 리스트
        """
        return [
            "https://toss.im/career/jobs",  # 토스 전체 포지션 및 공고
        ]

    async def extract_job_urls(self, page: Any) -> List[Dict[str, str]]:
        """
        채용공고 목록 페이지에서 개별 공고 URL 추출 (비동기)

        토스의 포지션 처리 로직:
        1. 포지션 목록 페이지에서 모든 포지션 로드
        2. 포지션별로:
           - span.css-zmjrej이 여러개면 → 계열사 선택 페이지 (토글 필요)
           - 아니면 → 직접 세부공고 페이지

        Args:
            page: Playwright page 객체

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        try:
            logger.info("토스 포지션 및 계열사 공고 추출 시작...")

            # 포지션 목록 페이지 로드
            list_url = self.get_job_list_urls()[0]
            logger.info(f"포지션 페이지 로드 중: {list_url}")
            try:
                await page.goto(list_url, wait_until="networkidle", timeout=self.get_timeout())
            except:
                logger.warning("networkidle 로드 실패, load로 재시도...")
                await page.goto(list_url, wait_until="load", timeout=self.get_timeout())
            logger.info("포지션 페이지 로드 완료")

            # 페이지 렌더링 대기
            await asyncio.sleep(2)

            # Step 1: 모든 포지션 로드 (전체 페이지 스크롤)
            logger.info("모든 포지션 로드를 위해 페이지 스크롤 중...")
            try:
                last_height = await page.evaluate("document.body.scrollHeight")
                scroll_count = 0
                max_scrolls = 100

                while scroll_count < max_scrolls:
                    await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
                    await asyncio.sleep(0.5)

                    new_height = await page.evaluate("document.body.scrollHeight")
                    if new_height == last_height:
                        logger.info(f"모든 포지션 로드 완료 (총 {scroll_count}회 스크롤)")
                        break

                    last_height = new_height
                    scroll_count += 1

                await page.evaluate("window.scrollTo(0, 0)")
                await asyncio.sleep(1)

            except Exception as e:
                logger.warning(f"페이지 스크롤 중 오류: {e}")

            # Step 2: 포지션 아이템 찾기 (li.css-1lnizc9)
            logger.info("포지션 아이템 수집 중...")
            job_links = []
            seen_urls = set()

            try:
                # 포지션 리스트 아이템 찾기 (li.css-1lnizc9)
                position_items = await page.locator("li.css-1lnizc9").all()
                logger.info(f"발견된 포지션 아이템: {len(position_items)}개")

                for pos_idx, item in enumerate(position_items):
                    try:
                        # Step 2-1: 포지션 제목 추출
                        pos_title = ""
                        try:
                            # p 태그나 직접 span에서 제목 추출
                            title_elem = item.locator("p")
                            if await title_elem.count() > 0:
                                pos_title = await title_elem.first.inner_text()
                            else:
                                # span에서 첫 번째 텍스트 추출
                                text = await item.inner_text()
                                if text:
                                    pos_title = text.split('\n')[0] if '\n' in text else text
                        except:
                            pos_title = f"Position {pos_idx}"

                        logger.info(f"[{pos_idx}] 포지션 처리: {pos_title[:40]}")

                        # Step 2-2: 해당 포지션 내 span.css-zmjrej 개수 확인 (계열사 수)
                        # span.css-zmjrej은 각 계열사 정보를 나타냄
                        try:
                            spans = await item.locator("span.css-zmjrej").all()
                            num_affiliates = len(spans)
                            logger.info(f"  계열사 수: {num_affiliates}개")

                            if num_affiliates > 1:
                                # 여러 계열사 = 계열사 배지 직접 클릭
                                logger.info(f"  다중 계열사 포지션 - 계열사 배지 클릭 시작...")

                                # 계열사 배지 찾기
                                badges = await item.locator('span[class*="zmjrej"]').all()
                                logger.info(f"  발견된 계열사 배지: {len(badges)}개")

                                # 각 배지를 클릭하여 상세 페이지 접근
                                for badge_idx, badge in enumerate(badges):
                                    try:
                                        # 배지 텍스트 (계열사명) 추출
                                        affiliate_name = await badge.text_content()
                                        logger.info(f"    [{badge_idx}] {affiliate_name} 배지 클릭...")

                                        # 배지 클릭 (새 탭 또는 페이지 네비게이션 발생)
                                        await badge.click(delay=100)
                                        await asyncio.sleep(2)

                                        # 현재 URL 확인
                                        current_url = page.url
                                        logger.info(f"    클릭 후 URL: {current_url}")

                                        # job-detail 페이지인 경우 URL 추출
                                        if 'job-detail' in current_url:
                                            match = re.search(r'job_id=([^&]+)', current_url)
                                            if match:
                                                job_id = match.group(1)
                                                if current_url not in seen_urls:
                                                    job_links.append({
                                                        'url': current_url,
                                                        'job_id': job_id,
                                                        'title': f"{pos_title}[{affiliate_name}]"
                                                    })
                                                    seen_urls.add(current_url)
                                                    logger.info(f"      [추가] {pos_title}[{affiliate_name}] -> {job_id}")

                                                # 목록으로 돌아가기
                                                await page.go_back()
                                                await asyncio.sleep(2)
                                        else:
                                            logger.warning(f"    배지 클릭 후 job-detail 페이지로 이동하지 않음")

                                    except Exception as e:
                                        logger.warning(f"    배지 {badge_idx} 처리 중 오류: {e}")

                            else:
                                # 단일 계열사 = 직접 li 클릭해서 세부공고 페이지 진입
                                logger.info(f"  단일 계열사 포지션 - 직접 클릭...")
                                try:
                                    await item.click()
                                    await asyncio.sleep(2)

                                    # 세부 공고 URL 추출
                                    current_url = page.url
                                    if 'job-detail' in current_url:
                                        # 현재 페이지가 세부공고 페이지
                                        match = re.search(r'job_id=([^&]+)', current_url)
                                        if match:
                                            job_id = match.group(1)
                                            job_links.append({
                                                'url': current_url,
                                                'job_id': job_id,
                                                'title': pos_title.strip()
                                            })
                                            seen_urls.add(current_url)
                                            logger.info(f"    [발견] {pos_title[:35]} -> {job_id}")

                                    # 목록으로 돌아가기
                                    await page.goto(list_url, wait_until="load", timeout=self.get_timeout())
                                    await asyncio.sleep(1)

                                except Exception as e:
                                    logger.warning(f"  단일 계열사 처리 중 오류: {e}")
                                    # 목록으로 돌아가기
                                    try:
                                        await page.goto(list_url, wait_until="load", timeout=self.get_timeout())
                                        await asyncio.sleep(1)
                                    except:
                                        pass

                        except Exception as e:
                            logger.warning(f"  포지션 처리 중 오류: {e}")

                    except Exception as e:
                        logger.warning(f"포지션 {pos_idx} 처리 중 오류: {e}")
                        continue

            except Exception as e:
                logger.error(f"공고 추출 중 오류: {e}", exc_info=True)

            logger.info(f"총 {len(job_links)}개 세부 공고 URL 추출됨")
            for idx, job in enumerate(job_links[:20], 1):
                logger.info(f"  [{idx}] {job['title'][:40]} -> {job['url'][:60]}")
            if len(job_links) > 20:
                logger.info(f"  ... 외 {len(job_links) - 20}개")

            return job_links

        except Exception as e:
            logger.error(f"공고 추출 중 오류: {e}", exc_info=True)
            return []

    async def parse_job_detail(self, page: Any, url: str, idx: int) -> Optional[Dict[str, str]]:
        """
        공고 상세 페이지 파싱 (비동기)

        두 가지 케이스를 처리:
        1. 다중 계열사: 계열사 선택 페이지 → 계열사 선택 필요 → 상세 페이지 로드
        2. 단일 계열사: 직접 상세 페이지 로드

        Args:
            page: Playwright page 객체
            url: 공고 URL
            idx: 공고 인덱스

        Returns:
            공고 상세 정보 딕셔너리
        """
        try:
            logger.info(f"[{idx}] 토스 공고 상세 페이지 파싱: {url}")

            # URL이 상대 경로인 경우 절대 URL로 변환
            if url.startswith('/'):
                url = "https://toss.im" + url
                logger.info(f"[{idx}] URL 변환: {url}")

            # 페이지 로드
            try:
                await page.goto(url, wait_until="networkidle", timeout=self.get_timeout())
            except:
                logger.warning(f"[{idx}] networkidle 로드 실패, load로 재시도...")
                await page.goto(url, wait_until="load", timeout=self.get_timeout())

            logger.info(f"[{idx}] 페이지 로드 완료: {url}")
            await asyncio.sleep(2)

            # Step 1: 페이지 유형 감지
            # 계열사 선택 페이지 vs 상세 페이지 판정
            page_html = await page.content()

            # Body 높이로 판정 (계열사 선택 페이지는 보통 2200px 이하)
            body_box = await page.locator("body").bounding_box()
            body_height = body_box['height'] if body_box else 0

            # 콘텐츠 영역 크기 확인
            content_elem = await page.query_selector('[class*="content"], [class*="description"], main, article')
            is_affiliate_selection_page = False

            if body_height < 2300 and "계열사" in page_html and not content_elem:
                is_affiliate_selection_page = True
                logger.info(f"[{idx}] 계열사 선택 페이지로 감지 (높이: {body_height}px)")
            else:
                logger.info(f"[{idx}] 직접 상세 페이지로 감지 (높이: {body_height}px)")

            # Step 2: 계열사 선택 페이지인 경우, 계열사 선택 후 상세 페이지 로드
            if is_affiliate_selection_page:
                logger.info(f"[{idx}] 계열사 선택 페이지에서 첫 번째 계열사 자동 선택...")
                try:
                    # Select 요소 찾기
                    select_elem = await page.query_selector('select')
                    if select_elem:
                        # 현재 선택된 옵션 확인
                        current_option = await page.query_selector('select option[selected]')
                        if current_option:
                            option_text = await current_option.inner_text()
                            logger.info(f"[{idx}] 현재 선택된 계열사: {option_text[:30]}")

                        # Select 요소의 change 이벤트가 트리거되도록 값 변경
                        await select_elem.select_option(index=0)
                        await asyncio.sleep(2)  # 선택 후 페이지 업데이트 대기

                        logger.info(f"[{idx}] 계열사 선택 완료, 페이지 업데이트 대기 중...")

                        # 페이지가 업데이트될 때까지 대기
                        try:
                            await page.wait_for_load_state("networkidle", timeout=self.get_timeout())
                        except:
                            await asyncio.sleep(2)

                        # 업데이트된 HTML 수집
                        page_html = await page.content()
                        logger.info(f"[{idx}] 페이지 업데이트 완료")
                    else:
                        logger.warning(f"[{idx}] Select 요소 찾기 실패, 현재 페이지로 진행")
                except Exception as e:
                    logger.warning(f"[{idx}] 계열사 선택 처리 실패: {e}, 현재 페이지로 진행")

            # Step 3: 아코디언 펼치기 (모든 섹션 펼침)
            logger.info(f"[{idx}] 아코디언 섹션 펼치기 시도...")
            try:
                buttons = await page.locator('button').all()
                click_count = 0
                for btn in buttons:
                    try:
                        is_visible = await btn.is_visible()
                        if is_visible:
                            text = await btn.inner_text()
                            try:
                                await btn.click(timeout=3000)
                                await asyncio.sleep(0.2)
                                click_count += 1
                            except:
                                pass
                    except:
                        pass

                logger.info(f"[{idx}] 아코디언 펼치기 완료 ({click_count}개 버튼 클릭)")
            except Exception as e:
                logger.warning(f"[{idx}] 아코디언 펼치기 중 오류: {e}")

            await asyncio.sleep(1)

            # Step 4: 최종 HTML 수집
            match = re.search(r'job_id=([^&]+)', url)
            job_id = match.group(1) if match else "unknown"

            html_content = await page.content()
            logger.info(f"[{idx}] 최종 HTML 수집 완료 ({len(html_content)} bytes)")

            # Step 5: 공고 제목 추출
            title = ""
            try:
                title_elem = await page.query_selector('h1')
                if title_elem:
                    title = await title_elem.inner_text()
                    # 제목에서 계열사 정보 제거 (예: "[토스뱅크] Job Title" → "Job Title")
                    title = re.sub(r'^\[.*?\]\s*', '', title).strip()
            except:
                pass

            # 회사명
            company = "Toss"

            # 공고 설명 텍스트
            job_description = ""
            try:
                content_elem = await page.query_selector('[class*="content"], [class*="description"], main, article')
                if content_elem:
                    job_description = await content_elem.inner_text()
            except:
                pass

            # Step 6: 세부 공고 페이지 여부 재확인
            is_detail_page = (
                len(job_description) > 200 or
                '직무' in html_content or
                '자격' in html_content or
                '요구' in html_content or
                '경험' in html_content
            )

            logger.info(f"[{idx}] 최종 페이지 판정: {'세부 페이지' if is_detail_page else '계열사 선택 페이지'}")

            # Step 7: 스크린샷 캡처
            screenshot_bytes = None
            if is_detail_page:
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
            else:
                logger.info(f"[{idx}] 계열사 선택 페이지 - 스크린샷 캡처 건너뜀")

            result = {
                'url': url,
                'job_id': job_id,
                'title': title.strip() if title else f'Toss Job {job_id}',
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
                    'source': 'toss',
                    'crawled_index': idx,
                    'is_detail_page': is_detail_page,
                    'was_affiliate_selection': is_affiliate_selection_page,
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
