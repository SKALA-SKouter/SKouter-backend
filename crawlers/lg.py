"""
LG 그룹 채용 공고 크롤러 (Playwright 기반)

LG 그룹의 채용공고를 크롤링합니다 (LG전자, LG유플러스, LG CNS, LG화학 등)
"""

import asyncio
import logging
import re
from typing import List, Dict, Optional, Any
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class LGCrawler(BaseCrawler):
    """
    LG 그룹 채용 공고 크롤러 (Playwright 기반)

    LG 그룹 계열사의 채용공고를 크롤링합니다.
    """

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "LG"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            LG 채용공고 기본 페이지 URL (체크박스로 필터 적용)
        """
        return [
            "https://careers.lg.com/apply",  # 기본 페이지 (체크박스로 LG CNS 필터 적용)
        ]

    async def extract_job_urls(self, page: Any) -> List[Dict[str, str]]:
        """
        채용공고 목록 페이지에서 개별 공고 URL 추출 (비동기)

        React 기반 SPA이므로:
        1. 회사 필터 토글 열기
        2. LG CNS 선택
        3. 필터링된 공고들의 URL 추출

        Args:
            page: Playwright page 객체

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        try:
            logger.info("LG CNS 채용공고 링크 추출 중...")

            # 채용 목록 페이지 로드
            list_url = self.get_job_list_urls()[0]
            logger.info(f"List page 로드 중: {list_url}")
            await page.goto(list_url, wait_until="networkidle", timeout=self.get_timeout())
            logger.info("List page 로드 완료")

            # 페이지 렌더링 대기
            await asyncio.sleep(2)

            # Step 1: LG CNS 체크박스 찾아서 클릭
            logger.info("LG CNS 체크박스 클릭 시도...")
            try:
                # 페이지의 모든 체크박스 찾기
                checkboxes = await page.locator('input[type="checkbox"]').all()
                logger.info(f"발견된 체크박스: {len(checkboxes)}개")

                cns_checkbox = None

                # 각 체크박스 확인
                for idx, checkbox in enumerate(checkboxes):
                    try:
                        # 체크박스의 부모 요소 확인
                        label = checkbox.locator("xpath=ancestor::label | ancestor::*[contains(@class, 'FormControlLabel')]").first

                        # 라벨 텍스트 확인
                        label_text = await label.inner_text()
                        if "LG CNS" in label_text:
                            cns_checkbox = checkbox
                            logger.info(f"LG CNS 체크박스 발견 (인덱스: {idx})")
                            break
                    except:
                        pass

                if cns_checkbox:
                    # 체크박스 클릭
                    await cns_checkbox.click(timeout=5000)
                    await asyncio.sleep(2)  # 필터링 적용 대기
                    logger.info("LG CNS 체크박스 클릭 완료 - 필터링 적용됨")
                else:
                    logger.warning("LG CNS 체크박스를 찾을 수 없음 - 모든 공고 표시 상태")

            except Exception as e:
                logger.warning(f"LG CNS 체크박스 클릭 실패: {e}")

            # Step 2: LG CNS 공고 찾기 (체크박스 클릭 후)
            job_links = []
            try:
                # LG CNS 공고 요소 찾기 ([LG CNS] 텍스트 포함)
                job_elements = await page.locator('text=/\\[LG CNS\\]/').all()
                logger.info(f"[LG CNS] 공고 요소 발견: {len(job_elements)}개")

                for idx, elem in enumerate(job_elements):
                    try:
                        # 공고 제목 텍스트 가져오기
                        title_text = await elem.inner_text()

                        logger.info(f"  [{idx+1}] 공고 처리: {title_text[:50]}")

                        # 클릭 가능한 부모 요소 찾기 (최대 10단계)
                        clickable_elem = elem
                        for _ in range(10):
                            try:
                                # 현재 요소 클릭
                                await clickable_elem.click(timeout=5000)
                                await asyncio.sleep(1)  # 페이지 이동 대기

                                # URL 확인
                                current_url = page.url
                                if "/apply/detail" in current_url or "id=" in current_url:
                                    # 상세 페이지로 이동했음
                                    match = re.search(r'id=(\d+)', current_url)
                                    if match:
                                        job_id = match.group(1)
                                        job_links.append({
                                            'url': current_url,
                                            'job_id': job_id,
                                            'title': title_text.strip()[:100]
                                        })
                                        logger.info(f"    URL 수집: {current_url}")
                                        break
                                    else:
                                        logger.warning(f"    ID 추출 실패: {current_url}")
                                        break
                                else:
                                    # 아직 상세 페이지가 아니면 부모 요소로 이동
                                    parent = clickable_elem.locator("xpath=parent::*").first
                                    if parent:
                                        clickable_elem = parent
                                    else:
                                        logger.warning(f"    부모 요소 없음")
                                        break
                            except Exception as e:
                                logger.debug(f"    클릭 시도 실패: {e}")
                                parent = clickable_elem.locator("xpath=parent::*").first
                                if parent:
                                    clickable_elem = parent
                                else:
                                    break

                        # 목록 페이지로 돌아가기
                        if len(job_links) > 0 and job_links[-1]['title'] == title_text.strip()[:100]:
                            await page.goto(list_url, wait_until="networkidle", timeout=self.get_timeout())
                            await asyncio.sleep(1)

                    except Exception as e:
                        logger.warning(f"공고 {idx} 처리 실패: {e}")
                        # 목록으로 돌아가기
                        try:
                            await page.goto(list_url, wait_until="networkidle", timeout=self.get_timeout())
                            await asyncio.sleep(1)
                        except:
                            pass
                        continue

            except Exception as e:
                logger.warning(f"공고 목록 추출 실패: {e}", exc_info=True)

            logger.info(f"총 {len(job_links)}개 공고 링크 추출됨")
            return job_links

        except Exception as e:
            logger.error(f"공고 추출 중 오류: {e}", exc_info=True)
            return []

    async def parse_job_detail(self, page: Any, url: str, idx: int) -> Optional[Dict[str, str]]:
        """
        공고 상세 페이지 파싱 (비동기) - 아코디언 펼침 방식

        LG CNS는 MUI 아코디언을 사용하므로 모든 Accordion을 펼친 후 content 추출

        Args:
            page: Playwright page 객체
            url: 공고 URL
            idx: 공고 인덱스

        Returns:
            {
                'url': str,
                'job_id': str,
                'title': str,
                'company': str,
                'html': str,  # 원본 HTML (아코디언 펼쳐진 상태)
                'posting_date': str,
                'closing_date': str,
                'location': str,
                'job_description': str,
                'required_qualifications': str,
                'preferred_qualifications': str,
                'company_description': str,
                'team_description': str,
                'selection_process': str,
                'notes': str,
                'screenshot': Optional[bytes],  # 펼쳐진 상태의 스크린샷
                'metadata': Dict[str, Any]
            }
        """
        try:
            logger.info(f"[{idx}] LG CNS 공고 상세 페이지 파싱: {url}")

            # 페이지 로드 (networkidle까지 대기)
            await page.goto(url, wait_until="networkidle", timeout=self.get_timeout())
            logger.info(f"[{idx}] 페이지 로드 완료: {url}")

            # 팝업 닫기 (닫기 버튼 클릭 또는 ESC 키)
            logger.info(f"[{idx}] 팝업 닫기 시도...")
            try:
                # 1. 닫기 버튼 찾기 (X 버튼)
                close_button = page.locator('button[aria-label*="close"], button[aria-label*="Close"], [role="button"][aria-label*="close"]').first
                if close_button:
                    try:
                        await close_button.click(timeout=3000)
                        await asyncio.sleep(0.5)
                        logger.info(f"[{idx}] 닫기 버튼으로 팝업 닫음")
                    except:
                        # 2. 실패하면 ESC 키
                        await page.keyboard.press("Escape")
                        await asyncio.sleep(0.5)
                        logger.info(f"[{idx}] ESC 키로 팝업 닫음")
                else:
                    # 2. 버튼이 없으면 ESC 키
                    await page.keyboard.press("Escape")
                    await asyncio.sleep(0.5)
                    logger.info(f"[{idx}] ESC 키로 팝업 닫음")
            except Exception as e:
                logger.warning(f"[{idx}] 팝업 닫기 실패: {e}")

            # URL에서 job_id 추출
            match = re.search(r'id=(\d+)', url)
            job_id = match.group(1) if match else "unknown"

            # 모든 MUI Accordion Summary를 펼치기
            logger.info(f"[{idx}] 아코디언 펼치기 시작...")
            accordion_summaries = await page.locator(".MuiAccordion-root .MuiAccordionSummary-root").all()
            logger.info(f"[{idx}] 발견된 아코디언 수: {len(accordion_summaries)}")

            for i, accordion in enumerate(accordion_summaries):
                try:
                    # 각 아코디언 클릭
                    await accordion.click()
                    logger.info(f"[{idx}] 아코디언 {i+1}/{len(accordion_summaries)} 펼침")
                    await asyncio.sleep(0.3)  # 애니메이션 대기
                except Exception as e:
                    logger.warning(f"[{idx}] 아코디언 {i+1} 펼치기 실패: {e}")
                    continue

            # 아코디언 펼침 애니메이션 완료 대기
            await asyncio.sleep(0.5)

            # 원본 HTML 수집 (펼쳐진 상태)
            html_content = await page.content()
            logger.info(f"[{idx}] HTML 수집 완료 ({len(html_content)} bytes)")

            # 펼쳐진 상태에서 스크린샷 캡처 (전체 페이지)
            screenshot_bytes = None
            try:
                # 폰트 및 이미지 로드 완료 대기
                await asyncio.sleep(2)
                screenshot_bytes = await page.screenshot(full_page=True, timeout=60000)
                logger.info(f"[{idx}] 스크린샷 캡처 완료 ({len(screenshot_bytes)} bytes)")
            except Exception as e:
                logger.warning(f"[{idx}] 스크린샷 캡처 실패: {e}")

            # 공고 제목
            title = ""
            try:
                title_elem = await page.query_selector('h1, .job-title, [class*="title"]')
                if title_elem:
                    title = await title_elem.inner_text()
            except:
                pass

            # 회사명 (LG CNS)
            company = "LG CNS"
            try:
                # 회사명이 표시되는 곳 찾기
                company_elem = await page.query_selector('[class*="company"], [class*="subsidiary"], [class*="companyName"]')
                if company_elem:
                    company_text = await company_elem.inner_text()
                    if company_text and company_text.strip():
                        company = company_text.strip()
            except:
                pass

            # 마감일
            closing_date = ""
            try:
                # 마감일 패턴: YYYY.MM.DD 또는 YYYY-MM-DD
                page_text = await page.inner_text('body')
                match = re.search(r'(\d{4}[.\-]\d{2}[.\-]\d{2})', page_text)
                if match:
                    closing_date = match.group(1)
            except:
                pass

            # 위치/근무지
            location = ""
            try:
                location_elem = await page.query_selector('[class*="location"], [class*="place"], [class*="workPlace"]')
                if location_elem:
                    location = await location_elem.inner_text()
            except:
                pass

            # 펼쳐진 아코디언에서 모든 텍스트 추출
            job_description = ""
            try:
                # 아코디언 내용 추출
                accordion_contents = await page.query_selector_all(".MuiAccordion-root .MuiCollapse-root")
                if accordion_contents:
                    descriptions = []
                    for content in accordion_contents:
                        try:
                            text = await content.inner_text()
                            if text.strip():
                                descriptions.append(text.strip())
                        except:
                            continue
                    job_description = "\n\n".join(descriptions)
                else:
                    # 아코디언 없으면 일반 description 추출
                    desc_elem = await page.query_selector('[class*="description"], [class*="content"], article')
                    if desc_elem:
                        job_description = await desc_elem.inner_text()
            except Exception as e:
                logger.warning(f"[{idx}] 아코디언 content 추출 실패: {e}")

            result = {
                'url': url,
                'job_id': job_id,
                'title': title.strip() if title else f'LG CNS Job {job_id}',
                'company': company,
                'html': html_content,
                'posting_date': '',
                'closing_date': closing_date,
                'location': location,
                'job_description': job_description[:5000] if job_description else '',
                'required_qualifications': '',
                'preferred_qualifications': '',
                'company_description': '',
                'team_description': '',
                'selection_process': '',
                'notes': '',
                'screenshot': screenshot_bytes,
                'metadata': {
                    'source': 'lg_cns',
                    'crawled_index': idx,
                    'accordion_expanded': len(accordion_summaries) > 0,
                    'accordion_count': len(accordion_summaries)
                }
            }

            logger.info(f"[{idx}] 파싱 완료: {result['title'][:50]}")
            return result

        except Exception as e:
            logger.error(f"[{idx}] 공고 파싱 실패: {e}", exc_info=True)
            return None

    def get_wait_time(self) -> int:
        """PDF 캡처 대기 시간(초)"""
        return 3

    def requires_selenium(self) -> bool:
        """동적 페이지 여부 (True/False)"""
        return False

    def requires_playwright(self) -> bool:
        """Playwright 사용 여부"""
        return True

    def get_max_concurrent_jobs(self) -> int:
        """동시 처리 공고 수"""
        return 3
