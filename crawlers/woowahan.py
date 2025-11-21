import asyncio
import re
import logging
from typing import List, Dict, Optional, Any
from .base_crawler import BaseCrawler

logger = logging.getLogger(__name__)


class WoowahanCrawler(BaseCrawler):
    """
    우아한형제들 채용 공고 크롤러 (Playwright 기반)

    개발/기술직군 채용공고를 크롤링합니다.
    """

    def get_company_name(self) -> str:
        """회사명 반환"""
        return "Woowahan"

    def get_job_list_urls(self) -> List[str]:
        """
        채용 목록 페이지 URL 리스트 반환

        Returns:
            우아한형제들 채용공고 URL 리스트
        """
        # 개발직군 필터링 URL (BA005001 = 개발/기술직군)
        return [
            "https://career.woowahan.com/?keyword=&category=jobGroupCodes%3ABA005001#recruit-list",
        ]

    async def extract_job_urls(self, page) -> List[Dict[str, str]]:
        """
        채용공고 목록 페이지에서 개별 공고 URL 추출 (비동기)

        Args:
            page: Playwright page 객체

        Returns:
            [{'url': '...', 'job_id': '...', 'title': '...'}] 형식의 리스트
        """
        links = await self.extract_job_links(page)
        return [
            {
                "url": link,
                "job_id": self._extract_job_id(link),
                "title": ""
            }
            for link in links
        ]

    def get_wait_time(self) -> int:
        """
        PDF 캡처 대기 시간(초)

        우아한형제들은 동적 로드가 있으므로 충분한 대기 필요
        """
        return 4

    def requires_selenium(self) -> bool:
        """
        동적 페이지 여부

        우아한형제들은 Playwright로 처리됨
        """
        return False

    def requires_playwright(self) -> bool:
        """
        Playwright 사용 여부

        우아한형제들은 Playwright 필요
        """
        return True

    async def extract_job_links(self, page) -> List[str]:
        """
        메인 페이지에서 채용공고 링크 추출 (무한 스크롤)

        Args:
            page: Playwright page 객체

        Returns:
            공고 링크 리스트
        """
        try:
            logger.info("메인 페이지 로딩 중...")
            await page.goto(
                self.get_job_list_urls()[0],
                wait_until='domcontentloaded',
                timeout=self.get_timeout()
            )

            # JavaScript 실행 대기
            logger.info("JavaScript 실행 대기 중...")
            await asyncio.sleep(2)

            # 무한 스크롤로 모든 공고 로드하기
            logger.info("무한 스크롤로 모든 공고 로드 중...")
            job_links = []
            previous_count = 0
            scroll_attempts = 0
            max_scroll_attempts = 20  # 최대 20번 스크롤

            while scroll_attempts < max_scroll_attempts:
                # 현재 페이지의 모든 공고 링크 추출
                try:
                    result = await page.evaluate("""
                        () => {
                            const links = [];
                            document.querySelectorAll('a[href]').forEach(a => {
                                const href = a.getAttribute('href');
                                // /recruitment/R*****/detail 형태의 URL 찾기
                                if (href && href.match(/\\/recruitment\\/R\\d+\\/detail/)) {
                                    links.push(href);
                                }
                            });
                            return [...new Set(links)];  // 중복 제거
                        }
                    """)

                    # 링크 업데이트
                    for href in result:
                        try:
                            full_url = self._normalize_url(href)
                            if full_url not in job_links:
                                job_links.append(full_url)
                        except Exception:
                            continue

                    logger.debug(f"스크롤 {scroll_attempts}: {len(job_links)}개 공고 발견")

                    # 새로운 공고가 로드되지 않으면 종료
                    if len(job_links) == previous_count:
                        logger.info("더 이상 새로운 공고가 로드되지 않음. 스크롤 종료")
                        break

                    previous_count = len(job_links)

                    # 페이지 끝까지 스크롤
                    await page.evaluate("() => window.scrollTo(0, document.documentElement.scrollHeight)")
                    await asyncio.sleep(1.5)  # 새 콘텐츠 로드 대기

                except Exception as e:
                    logger.warning(f"스크롤 중 오류: {e}")
                    break

                scroll_attempts += 1

            logger.info(f"총 {len(job_links)}개의 채용공고 링크 추출 (스크롤 {scroll_attempts}회)")

            return job_links

        except Exception as e:
            logger.error(f"채용공고 링크 추출 실패: {e}")
            return []

    async def parse_job_detail(self, page, url: str, idx: int, screenshot_dir: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        공고 상세 페이지 파싱 (비동기) - BaseCrawler 인터페이스 구현 (스크린샷 저장 포함)

        Args:
            page: Playwright page 객체
            url: 공고 URL
            idx: 인덱스
            screenshot_dir: 스크린샷 저장 디렉토리

        Returns:
            파싱된 공고 데이터 또는 None
        """
        try:
            # 큰 뷰포트 설정 (오른쪽 잘림 방지)
            await page.set_viewport_size({"width": 2560, "height": 1440})

            logger.info(f"[{idx}] 공고 파싱 중: {url}")
            await page.goto(url, wait_until='domcontentloaded', timeout=self.get_timeout())

            # JavaScript 로드 대기 (더 충분한 시간)
            await asyncio.sleep(4)  # 4초 대기

            job_data = {
                "url": url,
                "job_id": self._extract_job_id(url),
                "company": self.get_company_name(),
                "title": "",
                "posting_date": "",
                "closing_date": "",
                "location": "",
                "employment_type": "정규직",
                "company_description": "",
                "team_description": "",
                "job_description": "",
                "required_qualifications": "",
                "preferred_qualifications": "",
                "recruitment_schedule": "",
                "selection_process": "",
                "notes": "",
                "privacy_policy": "",
                "document_return_policy": "",
                "development_environment": "",
                "key_technologies": "",
                "metadata": {
                    "crawled_at": asyncio.get_event_loop().time(),
                    "wait_time": self.get_wait_time(),
                }
            }

            # JavaScript로 제목과 본문 함께 추출 (우아한형제들 특화)
            try:
                result = await page.evaluate("""
                    () => {
                        const data = {};

                        // 제목 추출
                        const titleEl = document.querySelector('.recruit-detail-title-inner');
                        if (titleEl) {
                            let text = titleEl.textContent.trim();
                            // [직군] 형식에서 실제 직종명 추출
                            const match = text.match(/\\[(.*?)\\]\\s*([^\\[]+)/);
                            if (match && match[2]) {
                                data.title = match[2].trim().substring(0, 150);
                            } else {
                                data.title = text.substring(0, 150);
                            }
                        } else {
                            // h1 태그 시도
                            const h1 = document.querySelector('h1');
                            if (h1) {
                                let text = h1.textContent.trim();
                                const match = text.match(/\\[(.*?)\\]\\s*(.+?)(?=\\[|$)/);
                                data.title = match && match[2] ? match[2].trim() : text.substring(0, 150);
                            }
                        }

                        // 본문 추출 (detail-view.editor-viewer)
                        const detailView = document.querySelector('.detail-view.editor-viewer');
                        if (detailView) {
                            const fullText = detailView.textContent.trim();
                            if (fullText && fullText.length > 10) {
                                data.jobDescription = fullText.substring(0, 10000);
                            }
                        }

                        // 만약 detail-view.editor-viewer가 없으면 .detail-view만 시도
                        if (!data.jobDescription) {
                            const detailViewOnly = document.querySelector('.detail-view');
                            if (detailViewOnly) {
                                const fullText = detailViewOnly.textContent.trim();
                                if (fullText && fullText.length > 10) {
                                    data.jobDescription = fullText.substring(0, 10000);
                                }
                            }
                        }

                        return data;
                    }
                """)
                job_data["title"] = result.get("title", "")
                job_data["job_description"] = result.get("jobDescription", "")

                logger.debug(f"추출된 제목: {job_data['title'][:50] if job_data['title'] else '(비어있음)'}")
                logger.debug(f"추출된 본문 길이: {len(job_data['job_description'])} 문자")

            except Exception as e:
                logger.warning(f"JavaScript 제목/본문 추출 실패: {e}")
                job_data["title"] = ""
                job_data["job_description"] = ""

            # 메타데이터 추출
            job_data["posting_date"] = await self._extract_meta(
                page,
                '게시일',
                '공고일'
            )
            job_data["closing_date"] = await self._extract_meta(
                page,
                '마감일',
                '마감'
            )
            job_data["location"] = await self._extract_meta(
                page,
                '근무지',
                '위치'
            )

            # 섹션별 내용 추출
            sections = await self._extract_sections(page)

            logger.debug(f"추출된 섹션: {list(sections.keys())}")

            # 우아한형제들 섹션 매핑
            section_mapping = {
                '회사소개': 'company_description',
                '조직소개': 'team_description',
                '팀소개': 'team_description',
                '지원자격': 'required_qualifications',
                '자격요건': 'required_qualifications',
                '우대사항': 'preferred_qualifications',
                '채용일정': 'recruitment_schedule',
                '채용 일정': 'recruitment_schedule',
                '전형절차': 'selection_process',
                '전형 절차': 'selection_process',
                '참고사항': 'notes',
                '필독사항': 'notes',
                '개인정보처리방침': 'privacy_policy',
                '개인정보 처리방침': 'privacy_policy',
                '서류반환정책': 'document_return_policy',
                '서류 반환 정책': 'document_return_policy',
                '개발환경': 'development_environment',
                '주요기술': 'key_technologies',
                '기술스택': 'key_technologies'
            }

            # 섹션 매핑 적용
            if sections:
                logger.info(f"추출된 섹션: {list(sections.keys())}")

            for section_title, content in sections.items():
                matched = False
                for kr_title, field_name in section_mapping.items():
                    # 정확한 매칭 또는 포함 관계 확인
                    if kr_title == section_title or kr_title in section_title:
                        # job_description은 이미 전체 본문으로 채워졌으므로 스킵
                        if field_name != 'job_description':
                            job_data[field_name] = content[:2000]  # 최대 2000자
                            logger.info(f"섹션 매핑: '{section_title}' → '{field_name}' ({len(content)} 문자)")
                            matched = True
                        break

                if not matched:
                    logger.debug(f"매핑 안 됨: '{section_title}'")

            # 스크린샷 저장
            if screenshot_dir:
                screenshot_path = await self._save_screenshot(
                    page, job_data, screenshot_dir, idx
                )
                if screenshot_path:
                    job_data["screenshot_path"] = screenshot_path
                    logger.info(f"[{idx}] 스크린샷 저장: {screenshot_path}")

            logger.info(f"파싱 완료: {job_data['title']}")
            return job_data

        except Exception as e:
            logger.error(f"공고 파싱 실패 ({url}): {e}")
            return None

    async def _extract_meta(self, page, *keywords) -> str:
        """메타데이터 추출"""
        try:
            # 페이지의 모든 텍스트 내용 가져오기
            text = await page.locator('body').text_content()

            for keyword in keywords:
                pattern = rf'{keyword}\s*[:：]\s*([^\n\r]+)'
                match = re.search(pattern, text)
                if match:
                    value = match.group(1).strip()
                    # 날짜 형식 확인
                    if re.search(r'\d{4}[-/\.]\d{1,2}[-/\.]\d{1,2}', value):
                        return value
                    # 지역 정보의 경우
                    if keyword == '근무지' or keyword == '위치':
                        return value.split('\n')[0].strip()

            return ""
        except Exception as e:
            logger.debug(f"메타데이터 추출 실패: {e}")
            return ""

    async def _extract_sections(self, page) -> Dict[str, str]:
        """섹션별 내용 추출 (강화된 파싱)"""
        sections = {}

        try:
            # 상세한 섹션 추출
            logger.debug("섹션별 데이터 추출 중...")
            result = await page.evaluate("""
                () => {
                    const sections = {};
                    const detailView = document.querySelector('.detail-view, .recruit-detail');
                    if (!detailView) return sections;

                    // 전체 텍스트 콘텐츠 가져오기
                    const fullText = detailView.innerText;

                    // 정규식을 사용하여 섹션 분리
                    // [섹션명] 패턴으로 섹션 찾기
                    const sectionPattern = /\\[([^\\[\\]]+)\\]/g;
                    const matches = Array.from(fullText.matchAll(sectionPattern));

                    matches.forEach((match, idx) => {
                        const title = match[1].trim();
                        const startIndex = match.index + match[0].length;

                        // 다음 섹션의 시작점 또는 텍스트의 끝
                        let endIndex = fullText.length;
                        if (idx < matches.length - 1) {
                            endIndex = matches[idx + 1].index;
                        }

                        // 섹션 내용 추출
                        let content = fullText.substring(startIndex, endIndex)
                            .trim()
                            .split('\\n')
                            .filter(line => line.trim().length > 0)
                            .slice(0, 100) // 최대 100줄
                            .join('\\n');

                        if (content.length > 0) {
                            sections[title] = content.substring(0, 3000);
                        }
                    });

                    return sections;
                }
            """)

            sections = result
            logger.debug(f"섹션 {len(sections)}개 추출: {list(sections.keys())}")

            return sections

        except Exception as e:
            logger.debug(f"섹션 추출 실패: {e}")
            return sections

    async def _save_screenshot(
        self, page: Any, job_data: Dict, screenshot_dir: str, idx: int
    ) -> Optional[str]:
        """
        페이지 스크린샷 저장 (우아한형제들 특화 - 넓은 뷰포트)

        Args:
            page: Playwright page 객체
            job_data: 공고 데이터
            screenshot_dir: 저장 디렉토리
            idx: 인덱스

        Returns:
            저장된 스크린샷 경로 또는 None
        """
        try:
            # 저장 디렉토리 생성 (os는 _normalize_url에서 import됨)
            import os
            os.makedirs(screenshot_dir, exist_ok=True)

            # 파일명 생성 (job_id + 제목) - 특수문자 제거
            job_id = job_data.get("job_id", f"job_{idx}")
            title = job_data.get("title", "Unknown")
            # Windows 파일명 특수문자 제거 (< > : " / \ | ? *)
            safe_title = title.replace("/", "_").replace("\\", "_").replace(":", "_").replace("<", "_").replace(">", "_").replace("|", "_").replace("?", "_").replace("*", "_").replace("\"", "_")[:50]
            filename = f"{job_id}_{safe_title}_screenshot.png"
            filepath = os.path.join(screenshot_dir, filename)

            # 전체 페이지 스크린샷 캡처 (2560x1440 뷰포트에서)
            screenshot_bytes = await page.screenshot(
                full_page=True,
                type="png"
            )

            # 파일 저장
            with open(filepath, "wb") as f:
                f.write(screenshot_bytes)

            return filepath

        except Exception as e:
            logger.warning(f"[{idx}] 스크린샷 저장 실패: {e}")
            return None

    def _extract_job_id(self, url: str) -> str:
        """URL에서 공고 ID 추출"""
        try:
            match = re.search(r'/recruitment/(R\d+)/', url)
            if match:
                return match.group(1)
            return url.split("/")[-1]
        except Exception:
            return "woowahan_unknown"

    def _normalize_url(self, url: str) -> str:
        """URL 정규화"""
        if url.startswith('http'):
            return url
        elif url.startswith('/'):
            return f"https://career.woowahan.com{url}"
        else:
            return f"https://career.woowahan.com/{url}"
