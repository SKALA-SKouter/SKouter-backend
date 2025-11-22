# 🚀 SKouter 백엔드 프로젝트

채용 정보 서비스를 위한 멀티-백엔드 시스템입니다.

- **Spring Boot** (Java) - REST API 서버
- **FastAPI** (Python) - AI 분석 서버

---

## 📖 목차

1. [프로젝트 소개](#-프로젝트-소개)
2. [기술 스택](#-기술-스택)
3. [시작하기](#-시작하기)
4. [프로젝트 구조 이해하기](#-프로젝트-구조-이해하기)
5. [협업 가이드](#-협업-가이드)
6. [API 문서](#-api-문서)
7. [문제 해결](#-문제-해결)

---

## 🎯 프로젝트 소개

**SKouter**는 채용 공고를 크롤링하고 AI로 분석하여 사용자에게 최적의 공고를 추천하는 서비스입니다.

### 주요 기능
- ✅ 채용 공고 CRUD (생성, 조회, 수정, 삭제)
- ✅ 검색 및 필터링 (키워드, 지역, 경력, 스킬)
- ✅ 회사 정보 관리
- ✅ JWT 기반 사용자 인증
- ✅ AI 품질 분석 연동 (FastAPI)
- ✅ Redis 캐싱으로 성능 최적화

---

## 🛠 기술 스택

### 백엔드 (Spring Boot)

| 분류 | 기술 |
|------|------|
| **언어** | Java 17 |
| **프레임워크** | Spring Boot 3.5.7 |
| **빌드 도구** | Gradle 8.10 |
| **데이터베이스** | MariaDB 10.x |
| **캐시** | Redis (Port 16379) |
| **인증** | JWT (JSON Web Token) |
| **API 문서** | Swagger/OpenAPI |
| **ORM** | Spring Data JPA |
| **검색** | Qdrant (Vector DB) |

### AI 분석 서버 (FastAPI)

| 분류 | 기술 |
|------|------|
| **언어** | Python 3.10+ |
| **프레임워크** | FastAPI 0.104+ |
| **패키지 관리** | uv / pyproject.toml |
| **서버** | Uvicorn |
| **설정** | Pydantic Settings |

### 공통 인프라

| 분류 | 기술 |
|------|------|
| **컨테이너** | Docker & Docker Compose |
| **버전 관리** | Git |
| **협업** | GitHub |

---

## 🚀 시작하기

### 1️⃣ 사전 준비물

컴퓨터에 다음 프로그램이 설치되어 있어야 합니다:

#### 공통

- **Git** ([다운로드](https://git-scm.com/))
- **Docker & Docker Compose** ([다운로드](https://www.docker.com/products/docker-desktop))

#### Spring Boot 개발 (Java)

- **Java 17** ([다운로드](https://adoptium.net/))
- **Gradle 8.10+** (자동 설치됨)

#### FastAPI 개발 (Python)

- **Python 3.10+** ([다운로드](https://www.python.org/downloads/))
- **uv** (Python 패키지 관리자) - 또는 pip 사용

> 💡 **확인 방법**
>
> ```bash
> java -version        # 17 버전 확인
> python --version    # 3.10+ 버전 확인
> docker --version    # Docker 설치 확인
> ```

---

### 2️⃣ 프로젝트 클론

```bash
# 레포지토리 클론
git clone https://github.com/SKALA-SKouter/SKouter-backend.git

# 프로젝트 폴더로 이동
cd SKouter-backend
```

---

### 3️⃣ 환경 설정

#### 환경 변수 파일 생성

루트 디렉토리에서 `.env.example`을 복사하여 `.env` 파일을 생성하세요:

```bash
cp .env.example .env
```

`.env` 파일을 열어서 필요한 값을 설정하세요:

```env
# Spring Boot (Java)
SPRING_DATASOURCE_USERNAME=root
SPRING_DATASOURCE_PASSWORD=your_password
SPRING_DATASOURCE_URL=jdbc:mariadb://localhost:3306/skouter
SPRING_REDIS_HOST=localhost
SPRING_REDIS_PORT=16379
JWT_SECRET_KEY=your-secret-key-change-this-in-production

# FastAPI (Python)
DATABASE_URL=mariadb://root:your_password@localhost:3306/skouter
REDIS_URL=redis://localhost:16379
```

#### Docker Compose로 데이터베이스 시작 (권장)

```bash
# 루트 디렉토리에서 Docker 서비스 시작
docker-compose up -d

# 서비스 상태 확인
docker-compose ps
```

이 명령어는 다음 서비스를 자동으로 시작합니다:

- **MariaDB** (포트 3306)
- **Redis** (포트 16379)
- **Qdrant Vector DB** (포트 6333)

#### 수동으로 MariaDB 설정 (선택)

Docker를 사용하지 않는 경우:

```bash
# MariaDB 접속
mysql -u root -p

# 데이터베이스 생성
CREATE DATABASE skouter CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 종료
exit;
```

---

### 4️⃣ 프로젝트 실행

이 프로젝트는 두 개의 백엔드 서비스로 구성되어 있습니다. 각각 독립적으로 또는 함께 실행할 수 있습니다.

#### Spring Boot 백엔드 (Java) 실행

```bash
# 실행 권한 부여 (Mac/Linux, 최초 1회만)
chmod +x gradlew

# 빌드 (처음에는 시간이 좀 걸립니다)
./gradlew clean build

# 서버 실행
./gradlew bootRun

# Windows 사용자
gradlew.bat bootRun
```

Spring Boot 서버는 [http://localhost:8080](http://localhost:8080) 에서 실행됩니다.

#### FastAPI 백엔드 (Python) 실행

```bash
# backend-ai 디렉토리로 이동
cd backend-ai

# 의존성 설치 (처음 1회만)
uv pip install -r requirements.txt
# 또는
pip install -r requirements.txt

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

FastAPI 서버는 [http://localhost:8000](http://localhost:8000) 에서 실행됩니다.

#### 두 서비스 모두 실행 (선택)

터미널을 두 개 띄우고 각각 위의 명령어를 실행하세요.

---

### 5️⃣ 실행 확인

#### Spring Boot 서버 확인

브라우저에서 다음 주소를 열어보세요:

- **헬스체크**: [http://localhost:8080/actuator/health](http://localhost:8080/actuator/health)
- **API 문서**: [http://localhost:8080/swagger-ui.html](http://localhost:8080/swagger-ui.html)

✅ `{"status":"UP"}` 메시지가 나오면 성공!

#### FastAPI 서버 확인

브라우저에서 다음 주소를 열어보세요:

- **자동 문서**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **대체 문서**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

✅ Swagger UI 또는 ReDoc이 표시되면 성공!

---

## 📁 프로젝트 구조 이해하기

### 전체 프로젝트 구조

이 프로젝트는 **모노레포(Monorepo)** 구조로 되어 있습니다:

```
SKouter-backend/                     # 루트 디렉토리
├── backend-core/                    # Spring Boot (Java) 백엔드
│   ├── src/main/java/               # Java 소스 코드
│   │   └── com/skouter/recruitai/   # 메인 패키지
│   ├── src/main/resources/          # 설정 파일 (application.yml)
│   └── src/test/                    # 테스트 코드
│
├── backend-ai/                      # FastAPI (Python) AI 분석 서버
│   ├── app/                         # FastAPI 메인 앱
│   │   ├── main.py
│   │   ├── core/
│   │   └── api/
│   ├── requirements.txt             # Python 의존성
│   └── tests/                       # 테스트 코드
│
├── build.gradle                     # Java Gradle 설정
├── settings.gradle                  # Gradle 프로젝트 설정
├── pyproject.toml                   # Python 패키지 설정
├── docker-compose.yml               # Docker 서비스 정의
├── .env.example                     # 환경 변수 템플릿
├── README.md                        # 프로젝트 설명 (이 파일)
└── gradle/                          # Gradle Wrapper
    └── wrapper/
```

### Spring Boot 백엔드 구조

Spring Boot 프로젝트는 **회사 조직**이라고 생각하면 쉽습니다:

```
회사 조직 (Spring Boot)
├── 각 부서 (Domain)       👉 인증, 사용자, 회사, 공고, AI 등 비즈니스 단위
│   ├── Controller         👉 고객 응대 부분
│   ├── Service            👉 실제 업무 수행
│   ├── Repository         👉 데이터 관리
│   ├── Entity             👉 데이터 구조
│   └── DTO                👉 고객과 주고받는 서류
├── Config                 👉 회사 운영 규칙
└── Global                 👉 회사 전사적 규칙
```

---

### Spring Boot 도메인별 역할

#### 📂 `backend-core/src/main/java/com/skouter/recruitai/`

```
recruitai/
├── config/                  🔧 애플리케이션 설정
│   ├── SecurityConfig.java         Spring Security & JWT 설정
│   ├── WebConfig.java              CORS, 인터셉터 설정
│   ├── JpaConfig.java              JPA Auditing, QueryDSL 설정
│   ├── RedisConfig.java            Redis 연결 및 직렬화 설정
│   └── SwaggerConfig.java          Swagger/OpenAPI 문서 설정
│
├── domain/                  📦 비즈니스 도메인 (10개 도메인)
│   │
│   ├── auth/                🔐 인증/인가
│   │   ├── controller/
│   │   │   └── AuthController.java
│   │   ├── service/
│   │   │   ├── AuthService.java
│   │   │   └── TokenService.java
│   │   ├── dto/
│   │   │   ├── request/
│   │   │   └── response/
│   │   └── token/
│   │       ├── JwtProvider.java
│   │       ├── RefreshToken.java
│   │       └── RefreshTokenRepository.java
│   │
│   ├── user/                👤 사용자 (회원 정보, 설정)
│   │   ├── controller/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── entity/
│   │   └── dto/
│   │
│   ├── company/             🏢 기업 정보 (뉴스, 메모)
│   │   ├── controller/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── entity/
│   │   └── dto/
│   │
│   ├── job/                 💼 채용 공고 (북마크, Qdrant 검색)
│   │   ├── controller/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── entity/
│   │   └── dto/
│   │
│   ├── ai/                  🤖 AI 요청 관리 (Redis Publisher)
│   │   ├── controller/
│   │   ├── service/
│   │   └── dto/
│   │
│   ├── dashboard/           📊 대시보드 요약 통계
│   │   ├── controller/
│   │   ├── service/
│   │   └── dto/
│   │
│   ├── analytics/           📈 트렌드 분석
│   │   ├── controller/
│   │   ├── service/
│   │   └── dto/
│   │
│   ├── chat/                💬 챗봇 프록시 (FastAPI로 전달)
│   │   ├── controller/
│   │   ├── service/
│   │   └── dto/
│   │
│   ├── notification/        🔔 알림 (Slack Webhook)
│   │   ├── controller/
│   │   ├── service/
│   │   ├── repository/
│   │   ├── entity/
│   │   └── dto/
│   │
│   └── workshop/            🛠️ 공고 제작소 (템플릿 관리 및 생성)
│       ├── controller/
│       ├── service/
│       ├── repository/
│       ├── entity/
│       └── dto/
│
└── global/                  🌐 전역 공통 모듈
    ├── error/               ⚠️ 예외 처리
    │   ├── ErrorCode.java            에러 코드 enum
    │   ├── GlobalExceptionHandler.java
    │   ├── exception/
    │   │   ├── BusinessException.java
    │   │   ├── EntityNotFoundException.java
    │   │   ├── UnauthorizedException.java
    │   │   └── InvalidValueException.java
    │   └── dto/
    │       └── ErrorResponse.java
    │
    ├── common/              📝 공통 값 및 기본 엔티티
    │   ├── response/
    │   │   ├── ApiResponse.java       모든 API의 통일된 응답 포맷
    │   │   └── PageResponse.java      페이징 응답
    │   └── entity/
    │       └── BaseEntity.java        생성일, 수정일 등 공통 필드
    │
    ├── util/                🛠️ 유틸리티 클래스
    │   ├── JwtUtil.java              JWT 파싱 및 검증
    │   ├── DateUtil.java             날짜 변환
    │   ├── StringUtil.java           문자열 처리
    │   └── EncryptionUtil.java       비밀번호 암호화
    │
    └── client/              🔌 Infrastructure 레이어 (외부 시스템 연동)
        ├── fastapi/         FastAPI 서버 연동
        │   ├── FastApiClient.java
        │   ├── config/
        │   └── dto/
        └── redis/           Redis Pub/Sub
            ├── RedisPublisher.java
            └── RedisSubscriber.java
```

---

### 데이터 흐름 (요청부터 응답까지)

```
1. 프론트엔드가 요청
   ↓
2. Controller가 받음 (예: "채용공고 목록 주세요!")
   ↓
3. Service가 처리 (예: "검색 조건에 맞는 공고 찾기")
   ↓
4. Repository가 DB 조회 (예: "SELECT * FROM job_posts WHERE...")
   ↓
5. Entity를 DTO로 변환 (예: DB 데이터 → JSON)
   ↓
6. Controller가 응답
   ↓
7. 프론트엔드가 받음
```

### FastAPI 백엔드 구조

```
backend-ai/
├── app/
│   ├── main.py                   # FastAPI 앱 진입점
│   ├── core/
│   │   ├── config.py             # 설정 관리
│   │   └── security.py           # 인증/보안
│   ├── api/
│   │   ├── v1/
│   │   │   └── endpoints/        # API 엔드포인트
│   │   └── deps.py               # 의존성 주입
│   ├── models/                   # Pydantic 모델
│   ├── schemas/                  # 요청/응답 스키마
│   └── utils/                    # 유틸리티 함수
│
├── requirements.txt              # 의존성 명시
├── .env                          # 환경 변수 (git 제외)
└── tests/                        # 테스트 코드
```

---

## 📋 주요 설정 파일 경로

| 파일명 | 경로 | 설명 |
|--------|------|------|
| **Spring 설정** | `backend-core/src/main/resources/application.yml` | 데이터베이스, Redis, JWT 설정 |
| **Gradle 설정** | `build.gradle` | 라이브러리 의존성 정의 |
| **Python 설정** | `pyproject.toml` | Python 프로젝트 메타데이터 |
| **의존성** | `backend-ai/requirements.txt` | FastAPI 의존성 |
| **환경변수** | `.env` | 런타임 환경 변수 |
| **Docker** | `docker-compose.yml` | 개발 환경 서비스 |

---

### 주요 파일 설명

#### 1. Entity (데이터베이스 테이블)

**`JobPost.java`** - 채용공고 정보
```java
@Entity  // 이 클래스는 DB 테이블입니다
public class JobPost {
    @Id  // 기본키 (Primary Key)
    private Long id;

    private String title;        // 공고 제목
    private String content;      // 공고 내용
    private String location;     // 근무 지역
    private LocalDateTime deadline;  // 마감일

    @ManyToOne  // Company와 다대일 관계
    private Company company;     // 회사 정보
}
```

📌 **알아둘 점**:
- `@Entity`: 이 클래스가 DB 테이블이라는 의미
- `@Id`: 각 행을 구분하는 고유 번호
- `@ManyToOne`: 여러 공고가 하나의 회사에 속함

---

#### 2. Repository (데이터 접근)

**`JobPostRepository.java`** - 채용공고 DB 접근
```java
public interface JobPostRepository extends JpaRepository<JobPost, Long> {
    // 메서드 이름만으로 자동으로 쿼리 생성!
    List<JobPost> findByTitle(String title);
    List<JobPost> findByLocationContaining(String location);
}
```

📌 **알아둘 점**:
- `JpaRepository`를 상속받으면 기본 CRUD가 자동 제공됨
- 메서드 이름 규칙만 지키면 SQL 작성 불필요
- 예: `findByTitle` → `SELECT * FROM job_posts WHERE title = ?`

---

#### 3. Service (비즈니스 로직)

**`JobPostService.java`** - 채용공고 처리 로직
```java
@Service  // 이 클래스는 비즈니스 로직입니다
public class JobPostService {

    @Autowired  // 자동으로 Repository 주입
    private JobPostRepository repository;

    // 공고 검색
    public List<JobPost> searchJobs(String keyword) {
        return repository.findByTitleContaining(keyword);
    }

    // 공고 저장
    public JobPost saveJob(JobPost job) {
        return repository.save(job);
    }
}
```

📌 **알아둘 점**:
- `@Service`: Spring이 이 클래스를 관리하도록 표시
- `@Autowired`: 필요한 객체를 자동으로 주입
- 실제 비즈니스 로직(검색, 저장, 삭제 등)을 여기에 작성

---

#### 4. DTO (데이터 전송 객체)

**`JobSearchRequest.java`** - 검색 요청
```java
@Data  // Lombok: getter/setter 자동 생성
public class JobSearchRequest {
    private String keyword;      // 검색어
    private String location;     // 지역
    private String[] skills;     // 필요 스킬
    private int page = 0;        // 페이지 번호
    private int size = 20;       // 페이지 크기
}
```

**`JobPostResponse.java`** - 공고 응답
```java
@Data
public class JobPostResponse {
    private Long id;
    private String title;
    private String companyName;
    private String location;
    private LocalDateTime deadline;
}
```

📌 **알아둘 점**:
- **Entity vs DTO**: Entity는 DB 그대로, DTO는 클라이언트 전송용
- DTO를 사용하는 이유: 보안, 필요한 데이터만 전송, DB 구조 숨김

---

## 🤝 협업 가이드

### 모노레포 협업 규칙

이 프로젝트는 Java와 Python 두 가지 백엔드를 포함합니다. 다음 규칙을 따르세요:

- **Java 작업**: `backend-core/` 디렉토리에서만 수정
- **Python 작업**: `backend-ai/` 디렉토리에서만 수정
- **설정 파일**: 루트 디렉토리의 파일들 (`build.gradle`, `pyproject.toml`, `docker-compose.yml` 등)

### 작업 시작 전 (필수!)

#### 1️⃣ 최신 코드 받기

```bash
git pull origin main
```

#### 2️⃣ 새 브랜치 만들기

```bash
# 예: WBS 3.2.2 공고 API 개발 (Java)
git checkout -b feature/job-post-api

# 예: AI 분석 엔드포인트 개발 (Python)
git checkout -b feature/ai-analysis-api
```

---

### 작업 순서 (역할별)

#### 👨‍💻 **백엔드 개발자 A** - API 개발 담당

**작업 예시: 채용공고 목록 API 만들기**

1. **Controller 작성** (`controller/JobPostController.java`)
```java
@RestController
@RequestMapping("/api/jobs")
public class JobPostController {

    @Autowired
    private JobPostService service;

    // GET /api/jobs - 목록 조회
    @GetMapping
    public ApiResponse<PageResponse<JobPostResponse>> getJobs(
        @RequestParam(required = false) String keyword,
        @RequestParam(defaultValue = "0") int page
    ) {
        return ApiResponse.success(service.getJobs(keyword, page));
    }
}
```

2. **Service 구현** (`service/job/JobPostService.java`)
```java
public PageResponse<JobPostResponse> getJobs(String keyword, int page) {
    // 1. Repository로 DB 조회
    Page<JobPost> posts = repository.findAll(PageRequest.of(page, 20));

    // 2. Entity → DTO 변환
    List<JobPostResponse> dtoList = posts.stream()
        .map(this::convertToDto)
        .collect(Collectors.toList());

    // 3. 페이징 정보 포함하여 반환
    return PageResponse.builder()
        .content(dtoList)
        .pageNumber(page)
        .build();
}
```

3. **테스트**
```bash
# 서버 실행
./gradlew bootRun

# 브라우저에서 확인
http://localhost:8080/swagger-ui.html
```

---

#### 👨‍💻 **백엔드 개발자 B** - DB 스키마 담당

**작업 예시: 새 테이블 추가**

1. **Entity 작성**
```java
@Entity
@Table(name = "bookmarks")  // 테이블명 지정
public class Bookmark {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    private User user;

    @ManyToOne
    private JobPost jobPost;

    private LocalDateTime createdAt;
}
```

2. **Repository 작성**
```java
public interface BookmarkRepository extends JpaRepository<Bookmark, Long> {
    List<Bookmark> findByUser(User user);
}
```

3. **서버 재시작하면 테이블 자동 생성!**

---

### Git 커밋 규칙

#### 커밋 메시지 형식
```
[타입] 작업 내용

타입:
- feat: 새 기능 추가
- fix: 버그 수정
- refactor: 코드 리팩토링
- docs: 문서 수정
- test: 테스트 추가
```

#### 예시
```bash
# 커밋
git add .
git commit -m "feat: 채용공고 목록 API 구현

- JobPostController에 GET /api/jobs 추가
- 페이징 및 검색 기능 포함
- Swagger 문서 작성 완료"

# 푸시
git push origin feature/job-post-api
```

---

### Pull Request (PR) 만들기

1. GitHub에서 **New Pull Request** 클릭
2. 제목: `[WBS 3.2.2] 채용공고 목록 API 구현`
3. 내용:
```markdown
## 작업 내용
- 채용공고 목록 조회 API 구현
- 검색 및 페이징 기능 추가

## 테스트 방법
1. 서버 실행: `./gradlew bootRun`
2. Swagger 접속: http://localhost:8080/swagger-ui.html
3. GET /api/jobs 엔드포인트 테스트

## 체크리스트
- [x] Controller 작성
- [x] Service 로직 구현
- [x] Swagger 문서 작성
- [x] 로컬 테스트 완료
```

4. **Reviewers** 지정 (팀원)
5. **Create Pull Request** 클릭

---

### 코드 리뷰 받기

#### 리뷰어가 확인할 것:
- ✅ 코드가 정상 작동하는가?
- ✅ 변수/메서드 이름이 명확한가?
- ✅ 주석이 필요한 곳에 있는가?
- ✅ 에러 처리가 되어 있는가?

#### 리뷰 반영 후:
```bash
# 수정 사항 반영
git add .
git commit -m "fix: 리뷰 반영 - 에러 처리 추가"
git push origin feature/job-post-api
```

#### Merge 후:
```bash
# main 브랜치로 이동
git checkout main

# 최신 코드 받기
git pull origin main

# 작업 브랜치 삭제
git branch -d feature/job-post-api
```

---

## 📚 API 문서

### Swagger 사용법

1. 서버 실행 후 http://localhost:8080/swagger-ui.html 접속
2. API 목록에서 테스트할 API 선택
3. **Try it out** 클릭
4. 파라미터 입력
5. **Execute** 클릭하여 실행

### 주요 API 목록 (개발 예정)

| 메서드 | 경로 | 설명 |
|--------|------|------|
| GET | `/api/jobs` | 채용공고 목록 |
| GET | `/api/jobs/{id}` | 채용공고 상세 |
| POST | `/api/jobs` | 채용공고 생성 |
| PUT | `/api/jobs/{id}` | 채용공고 수정 |
| DELETE | `/api/jobs/{id}` | 채용공고 삭제 |
| GET | `/api/companies` | 회사 목록 |
| POST | `/api/auth/login` | 로그인 |
| POST | `/api/auth/register` | 회원가입 |

---

## 🔧 문제 해결

### 1. Spring Boot 서버가 시작되지 않아요!

#### 증상: `Port 8080 is already in use`

```bash
# 8080 포트 사용 중인 프로세스 찾기 (Mac/Linux)
lsof -i :8080

# 프로세스 종료
kill -9 [PID]

# Windows
netstat -ano | findstr :8080
taskkill /PID [PID] /F
```

---

### 2. FastAPI 서버가 시작되지 않아요!

#### 증상: `Port 8000 is already in use`

```bash
# 8000 포트 사용 중인 프로세스 찾기
lsof -i :8000      # Mac/Linux
netstat -ano | findstr :8000  # Windows

# 포트 변경하여 실행
uvicorn app.main:app --reload --port 8001
```

---

### 3. DB 연결 오류

#### 증상: `Access denied for user 'root'@'localhost'`

**해결 방법**:

1. `.env` 파일에서 비밀번호 확인
2. MariaDB가 실행 중인지 확인

```bash
# Docker를 사용하는 경우
docker-compose ps

# MariaDB 상태 확인 (수동 설치)
brew services list          # Mac

# MariaDB 시작
brew services start mariadb
```

---

### 4. Redis 연결 오류

#### 증상: `Connection refused` (포트 16379 또는 6379)

**해결 방법**:

```bash
# Docker로 Redis 실행 중인지 확인
docker-compose ps

# 수동으로 Redis 시작 (또는 docker-compose 사용)
redis-server --port 16379
```

---

### 5. Java 빌드 실패

#### 증상: `Compilation failed`

**해결 방법**:

```bash
# 캐시 삭제 후 재빌드
./gradlew clean build

# Gradle 데몬 재시작
./gradlew --stop
./gradlew build
```

---

### 6. Python 의존성 오류

#### 증상: `ModuleNotFoundError: No module named 'fastapi'`

**해결 방법**:

```bash
# backend-ai 디렉토리로 이동
cd backend-ai

# 의존성 설치
uv pip install -r requirements.txt
# 또는
pip install -r requirements.txt

# 설치된 패키지 확인
pip list
```

---

### 7. Lombok 에러 (Java)

#### 증상: `Cannot resolve symbol 'getData'`

**해결 방법** (IntelliJ):

1. File > Settings > Plugins
2. "Lombok" 검색 및 설치
3. File > Settings > Build > Compiler > Annotation Processors
4. "Enable annotation processing" 체크
5. IntelliJ 재시작

---

### 8. 다양한 모듈이 있을 때 헷갈려요!

#### Spring Boot 작업 vs FastAPI 작업

| 작업 | 디렉토리 | 빌드 도구 |
|------|---------|---------|
| **Java 개발** | `backend-core/` | Gradle |
| **Python 개발** | `backend-ai/` | pip/uv |
| **공통 설정** | 루트 | - |

각 디렉토리에서 해당 언어의 명령어만 사용하세요!

---

## 📞 도움말

### 자주 묻는 질문

#### Q1. Entity를 수정했는데 DB에 반영이 안 돼요

**A**: `backend-core/src/main/resources/application.yml`에서 `ddl-auto: update`로 설정되어 있는지 확인하세요. 또는 서버를 재시작하세요.

#### Q2. API 테스트는 어떻게 하나요

**A**: Swagger UI 또는 Postman을 사용하세요. Swagger가 더 간편합니다.

#### Q3. 다른 팀원이 만든 코드가 안 돌아가요

**A**:

```bash
# 최신 코드 받기
git pull origin main

# Java 의존성 다시 설치
./gradlew clean build

# Python 의존성 다시 설치
cd backend-ai
uv pip install -r requirements.txt
```

#### Q4. 모노레포에서 어떤 것을 수정해야 하나요

**A**: 작업 내용에 따라 수정할 디렉토리를 선택하세요:

- **Java/API 개발**: `backend-core/` 수정
- **AI/ML 개발**: `backend-ai/` 수정
- **환경 설정**: 루트 디렉토리 파일 수정

---

## 🎓 학습 자료

### 백엔드 (Java/Spring Boot)

- [Spring Boot 공식 가이드](https://spring.io/guides/gs/spring-boot/)
- [JPA 기초](https://spring.io/guides/gs/accessing-data-jpa/)
- [REST API 설계 원칙](https://restfulapi.net/)

### AI 분석 서버 (Python/FastAPI)

- [FastAPI 공식 문서](https://fastapi.tiangolo.com/)
- [Pydantic 데이터 검증](https://docs.pydantic.dev/)

---

## 🤝 기여하기

1. 이슈 확인: [GitHub Issues](https://github.com/SKALA-SKouter/SKouter-backend/issues)
2. 브랜치 생성: `git checkout -b feature/작업명`
3. 작업 후 커밋: `git commit -m "feat: 작업 내용"`
4. PR 생성 및 리뷰 요청

---

## 📄 라이선스

이 프로젝트는 팀 프로젝트이며 교육 목적으로 사용됩니다.

---

## 👥 팀원

- **PM**: 박현규
- **프론트엔드**: 고나연, 조성호
- **백엔드**: 신동건, 조석희
- **AI**: 전원

---

## 📌 관련 레포지토리

- [프론트엔드](https://github.com/SKALA-SKouter/SKouter-frontend)
- [AI Agent](https://github.com/SKALA-SKouter/SKouter-AI-Agent)

---

**마지막 업데이트**: 2025-11-23
