# 채용공고 크롤링 시스템 - 구현 가이드

## 프로젝트 개요

LangGraph 기반 Agent 아키텍처를 사용한 멀티 회사 채용공고 크롤링 시스템입니다.
플러그인 아키텍처(Registry 패턴)를 통해 새로운 회사 크롤러를 손쉽게 추가할 수 있습니다.

## 프로젝트 구조

```
crawler_agent/
├── crawlers/                    # 크롤러 모듈
│   ├── __init__.py
│   ├── base_crawler.py          # 추상 기본 클래스
│   ├── registry.py              # Registry 패턴 구현
│   ├── coupang.py               # Coupang 크롤러
│   ├── naver.py                 # Naver 크롤러
│   └── kakao.py                 # Kakao 크롤러
├── agents/                      # Agent 모듈
│   ├── __init__.py
│   ├── pdf_capture.py           # PDF 캡처 Agent (Selenium)
│   └── storage.py               # 저장소 Agent (로컬/S3)
├── tests/                       # 테스트
│   ├── __init__.py
│   ├── test_crawler.py          # 크롤러 테스트
│   └── test_storage.py          # 저장소 테스트
├── orchestrator.py              # LangGraph 기반 오케스트레이터
├── config.py                    # 설정 관리
├── main.py                      # 메인 실행 파일
├── utils.py                     # 유틸리티 함수
├── requirements.txt             # Python 의존성
├── pyproject.toml              # 현대적 패키징 설정
├── .env.example                # 환경 변수 예제
├── Makefile                    # 개발 명령어
└── README.md                   # 사용 설명서
```

## 핵심 컴포넌트 설명

### 1. BaseCrawler (crawlers/base_crawler.py)

모든 회사 크롤러가 구현해야 하는 추상 기본 클래스입니다.

```python
class BaseCrawler(ABC):
    @abstractmethod
    def get_company_name(self) -> str: ...

    @abstractmethod
    def get_job_list_urls(self) -> List[str]: ...

    @abstractmethod
    def extract_job_urls(self, html: str) -> List[Dict[str, str]]: ...

    @abstractmethod
    def get_wait_time(self) -> int: ...

    @abstractmethod
    def requires_selenium(self) -> bool: ...
```

### 2. CrawlerRegistry (crawlers/registry.py)

플러그인 레지스트리 패턴으로 크롤러를 관리합니다.

```python
registry = CrawlerRegistry()
registry.register(CoupangCrawler())
registry.register(NaverCrawler())

crawler = registry.get_crawler("Coupang")
companies = registry.list_companies()
```

### 3. PDFCaptureAgent (agents/pdf_capture.py)

Selenium을 사용하여 웹페이지를 PDF로 캡처합니다.

**주요 기능:**
- Chrome DevTools Protocol (CDP) 사용
- 전체 페이지 스크롤로 lazy-loading 콘텐츠 로드
- 헤드리스 모드 지원
- 타임아웃 및 에러 처리

### 4. StorageAgent (agents/storage.py)

PDF를 로컬 또는 S3에 저장합니다.

**주요 기능:**
- 로컬 파일 시스템 저장
- AWS S3 저장소 통합 (boto3)
- 메타데이터 저장
- 파일 삭제 기능

### 5. IntegratedCrawlerOrchestrator (orchestrator.py)

LangGraph 기반 워크플로우 오케스트레이터입니다.

**워크플로우:**
```
START
  ↓
fetch_job_list_page   (채용 목록 페이지 다운로드)
  ↓
extract_job_urls      (개별 공고 URL 추출)
  ↓
capture_pdfs          (PDF 캡처)
  ↓
store_pdfs            (저장소에 저장)
  ↓
END
```

## 회사별 크롤러 구현

### Coupang 크롤러

```python
class CoupangCrawler(BaseCrawler):
    def get_company_name(self) -> str:
        return "Coupang"

    def get_job_list_urls(self) -> List[str]:
        return ["https://www.coupang.com/np/pages/whatsnew/careers"]

    def requires_selenium(self) -> bool:
        return True  # 동적 페이지

    def get_wait_time(self) -> int:
        return 5  # 5초 대기
```

### Naver 크롤러

```python
class NaverCrawler(BaseCrawler):
    def get_company_name(self) -> str:
        return "Naver"

    def get_job_list_urls(self) -> List[str]:
        return ["https://recruit.naver.com/rcrt/list.do"]

    def requires_selenium(self) -> bool:
        return False  # 정적 페이지

    def get_wait_time(self) -> int:
        return 3
```

### Kakao 크롤러

```python
class KakaoCrawler(BaseCrawler):
    def get_company_name(self) -> str:
        return "Kakao"

    def get_job_list_urls(self) -> List[str]:
        return ["https://careers.kakao.com/jobs"]

    def requires_selenium(self) -> bool:
        return True  # 동적 콘텐츠 있음

    def get_wait_time(self) -> int:
        return 4
```

## 새로운 회사 크롤러 추가

### Step 1: 크롤러 클래스 작성

`crawlers/amazon.py` 파일 생성:

```python
from typing import List, Dict
from bs4 import BeautifulSoup
from .base_crawler import BaseCrawler

class AmazonCrawler(BaseCrawler):
    def get_company_name(self) -> str:
        return "Amazon"

    def get_job_list_urls(self) -> List[str]:
        return ["https://amazon.jobs/..."]

    def extract_job_urls(self, html: str) -> List[Dict[str, str]]:
        soup = BeautifulSoup(html, "html.parser")
        job_list = []

        # HTML 파싱 로직 구현
        for item in soup.select(".job-item"):
            link = item.find("a", href=True)
            if link:
                job_list.append({
                    "url": link["href"],
                    "job_id": "amazon_001",
                    "title": link.get_text(strip=True)
                })

        return job_list

    def get_wait_time(self) -> int:
        return 3

    def requires_selenium(self) -> bool:
        return True
```

### Step 2: `crawlers/__init__.py` 업데이트

```python
from .amazon import AmazonCrawler

__all__ = [
    "BaseCrawler",
    "CrawlerRegistry",
    "CoupangCrawler",
    "NaverCrawler",
    "KakaoCrawler",
    "AmazonCrawler",  # 추가
]
```

### Step 3: `main.py`의 `setup_registry()` 업데이트

```python
def setup_registry() -> CrawlerRegistry:
    registry = CrawlerRegistry()

    crawlers = [
        CoupangCrawler(),
        NaverCrawler(),
        KakaoCrawler(),
        AmazonCrawler(),  # 추가
    ]

    for crawler in crawlers:
        registry.register(crawler)

    return registry
```

### Step 4: 실행

```bash
python main.py --company Amazon
```

## 사용 예제

### CLI 사용

```bash
# 특정 회사 크롤링
python main.py --company Coupang

# 모든 회사 크롤링
python main.py --all

# 크롤러 목록 확인
python main.py --list

# 결과 파일 지정
python main.py --company Naver --output results.json

# PDF 저장 디렉토리 지정
python main.py --all --pdf-dir ./my_pdfs
```

### Python 코드 사용

```python
from crawlers import CrawlerRegistry, CoupangCrawler, NaverCrawler
from agents import PDFCaptureAgent, StorageAgent
from orchestrator import IntegratedCrawlerOrchestrator

# 레지스트리 설정
registry = CrawlerRegistry()
registry.register(CoupangCrawler())
registry.register(NaverCrawler())

# 에이전트 초기화
pdf_capture = PDFCaptureAgent(headless=True)
storage = StorageAgent(local_base_path="./data/pdfs")

# 오케스트레이터 생성
orchestrator = IntegratedCrawlerOrchestrator(registry, storage, pdf_capture)

# 크롤링 실행
results = orchestrator.run_company("Coupang")

# 또는 모든 회사 크롤링
all_results = orchestrator.run_all_companies()

# 결과 저장
orchestrator.save_results_to_json(results, "results.json")
```

## 환경 설정

### 1. 의존성 설치

```bash
pip install -r requirements.txt
```

또는

```bash
make install
```

### 2. 환경 변수 설정

`.env.example`을 `.env`로 복사하고 필요한 값 설정:

```bash
cp .env.example .env
```

주요 설정:
- `STORAGE_TYPE`: "local", "s3", "both"
- `PDF_HEADLESS_MODE`: true/false
- `PDF_WAIT_TIME`: 대기 시간(초)
- `AWS_*`: S3 저장소 설정

### 3. ChromeDriver 설정

`webdriver-manager`가 자동으로 ChromeDriver를 설치합니다.
수동 설정이 필요한 경우:

```env
CHROME_DRIVER_PATH=/path/to/chromedriver
```

## 개발 명령어

```bash
# 의존성 설치
make install              # 기본 의존성
make install-dev         # 개발 도구 포함
make install-all         # 모든 옵션

# 테스트
make test                # 테스트 실행
make test-cov            # 커버리지 리포트 포함

# 코드 품질
make lint                # flake8 검사
make format              # black + isort 포맷
make type-check          # mypy 타입 검사

# 크롤링 실행
make run-coupang        # Coupang 크롤링
make run-naver          # Naver 크롤링
make run-kakao          # Kakao 크롤링
make run-all            # 모든 회사 크롤링

# 정리
make clean              # 캐시 및 빌드 파일 정리
```

## 워크플로우 상세 설명

### 1. fetch_job_list_page

채용 목록 페이지를 다운로드합니다.

- **정적 페이지** (requires_selenium=False): requests 사용
- **동적 페이지** (requires_selenium=True): Selenium 사용

### 2. extract_job_urls

다운로드한 HTML에서 개별 공고의 URL을 추출합니다.

각 크롤러가 회사 특화 선택자를 사용하여 구현합니다.

**반환 형식:**
```python
[
    {
        "url": "https://...",
        "job_id": "001",
        "title": "Software Engineer"
    },
    ...
]
```

### 3. capture_pdfs

개별 공고 페이지를 PDF로 캡처합니다.

- Selenium으로 페이지 로드
- 전체 페이지 스크롤 (lazy-loading 콘텐츠 로드)
- Chrome DevTools Protocol으로 PDF 생성
- 에러 발생 시 해당 공고만 스킵

### 4. store_pdfs

PDF를 저장소에 저장합니다.

- 로컬 파일 시스템: `./data/pdfs/{company}/{date}/`
- S3: `s3://{bucket}/{company}/{date}/`
- 메타데이터: job_id, job_title, timestamp

## 에러 처리 및 재시도

### 자동 재시도

- 최대 3회 재시도 (CRAWLER_RETRY_COUNT)
- 타임아웃: 30초 (CRAWLER_TIMEOUT)

### 부분 실패 처리

한 공고 크롤링 실패 시:
- 에러 로그 기록
- 나머지 공고 계속 크롤링
- 최종 결과에 에러 내용 포함

## 로깅

모든 작업은 자동으로 로깅됩니다:

- **파일**: `crawler.log`
- **콘솔**: 실시간 로그 출력
- **레벨**: INFO (환경 변수로 조정 가능)

## 결과 형식

### JSON 결과

```json
{
  "success": true,
  "company_name": "Coupang",
  "total_jobs": 50,
  "pdfs_captured": 45,
  "pdfs_stored": 45,
  "storage_results": [
    {
      "job_id": "001",
      "job_url": "https://...",
      "job_title": "Software Engineer",
      "local_path": "./data/pdfs/Coupang/2024-01-15/001_...",
      "s3_key": null,
      "success": true
    }
  ],
  "error_logs": [],
  "timestamp": "2024-01-15T10:30:00"
}
```

## 성능 최적화 팁

1. **헤드리스 모드**: Selenium 속도 향상
2. **대기 시간 조정**: 각 회사별 최적값 설정
3. **병렬 처리**: 다중 프로세스로 다른 회사 동시 크롤링
4. **S3 사용**: 대규모 PDF 저장 시 권장
5. **지연 로딩**: 필요시에만 PDF 캡처

## 테스트

### 단위 테스트 실행

```bash
pytest tests/ -v
```

### 커버리지 리포트

```bash
pytest tests/ --cov=crawlers --cov=agents --cov-report=html
```

## 라이선스

MIT License

## 지원 및 문제 해결

### 문제 해결

1. **ChromeDriver 오류**: webdriver-manager 재설치
   ```bash
   pip install --upgrade webdriver-manager
   ```

2. **Selenium 타임아웃**: PDF_WAIT_TIME 증가

3. **S3 접근 오류**: AWS 자격증명 확인

4. **HTML 파싱 실패**: 선택자 업데이트 필요

### 로그 확인

```bash
tail -f crawler.log
```

## 다음 단계

1. **데이터베이스 통합**: SQLite/PostgreSQL로 결과 저장
2. **스케줄링**: APScheduler로 주기적 크롤링
3. **API 서버**: FastAPI로 REST API 제공
4. **모니터링**: 크롤링 상태 대시보드
5. **알림**: 크롤링 결과 이메일/Slack 알림
