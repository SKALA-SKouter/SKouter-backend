# 🚀 SKouter 백엔드 프로젝트

채용 정보 서비스를 위한 Spring Boot 백엔드 API 서버입니다.

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

| 분류 | 기술 |
|------|------|
| **언어** | Java 17 |
| **프레임워크** | Spring Boot 3.5.7 |
| **빌드 도구** | Gradle |
| **데이터베이스** | MariaDB |
| **캐시** | Redis |
| **인증** | JWT (JSON Web Token) |
| **API 문서** | Swagger/OpenAPI |

---

## 🚀 시작하기

### 1️⃣ 사전 준비물

컴퓨터에 다음 프로그램이 설치되어 있어야 합니다:

- **Java 17** ([다운로드](https://adoptium.net/))
- **MariaDB** ([다운로드](https://mariadb.org/download/))
- **Git** ([다운로드](https://git-scm.com/))

> 💡 **확인 방법**: 터미널에서 `java -version` 입력 시 17 버전이 나와야 합니다.

---

### 2️⃣ 프로젝트 클론

```bash
# 레포지토리 클론
git clone https://github.com/SKALA-SKouter/SKouter-backend.git

# 프로젝트 폴더로 이동
cd SKouter-backend
```

---

### 3️⃣ 데이터베이스 설정

#### MariaDB 데이터베이스 생성

```bash
# MariaDB 접속
mysql -u root -p

# 데이터베이스 생성
CREATE DATABASE skouter CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 종료
exit;
```

#### DB 연결 정보 수정 (선택)

`src/main/resources/application.yml` 파일을 열어서 비밀번호를 수정하세요:

```yaml
spring:
  datasource:
    url: jdbc:mariadb://localhost:3306/skouter
    username: root
    password: 여기에_본인_비밀번호_입력  # 👈 수정
```

---

### 4️⃣ 프로젝트 실행

```bash
# 실행 권한 부여 (Mac/Linux, 최초 1회만)
chmod +x gradlew

# 빌드 (처음에는 시간이 좀 걸립니다)
./gradlew build

# 서버 실행
./gradlew bootRun
```

#### Windows 사용자
```bash
gradlew.bat bootRun
```

---

### 5️⃣ 실행 확인

브라우저에서 다음 주소를 열어보세요:

- **헬스체크**: http://localhost:8080/actuator/health
- **API 문서**: http://localhost:8080/swagger-ui.html

✅ `{"status":"UP"}` 메시지가 나오면 성공!

---

## 📁 프로젝트 구조 이해하기

### 전체 구조 (비유로 이해하기)

Spring Boot 프로젝트는 **레스토랑**이라고 생각하면 쉽습니다:

```
레스토랑 (Spring Boot)
├── 홀 (Controller)        👉 손님(프론트엔드)의 주문을 받는 곳
├── 주방 (Service)         👉 실제 요리(비즈니스 로직)를 하는 곳
├── 창고 (Repository)      👉 재료(데이터)를 보관하는 곳
├── 재료 목록 (Entity)      👉 DB 테이블과 1:1 매칭
├── 주문서 (DTO)           👉 손님과 주고받는 데이터 양식
└── 규칙 (Config)          👉 레스토랑 운영 규칙
```

---

### 폴더별 역할

#### 📂 `src/main/java/com/example/demo/`

```
demo/
├── config/              🔧 설정 파일들
│   ├── CorsConfig.java         프론트엔드 연결 허용
│   ├── JwtConfig.java          로그인 토큰 설정
│   ├── RedisConfig.java        캐시 설정
│   ├── SwaggerConfig.java      API 문서 설정
│   └── WebClientConfig.java    외부 API 호출 설정
│
├── controller/          🎤 API 엔드포인트 (아직 없음, 추가 예정)
│   └── (여기에 추가할 예정)
│
├── dto/                 📋 데이터 전송 양식
│   ├── request/              클라이언트 → 서버
│   │   ├── LoginRequest.java        로그인 요청
│   │   ├── JobSearchRequest.java    공고 검색 요청
│   │   └── ...
│   └── response/             서버 → 클라이언트
│       ├── ApiResponse.java         공통 응답 형식
│       ├── JobPostResponse.java     공고 정보 응답
│       └── ...
│
├── entity/              🗄️ 데이터베이스 테이블
│   ├── JobPost.java          채용공고 테이블
│   ├── Company.java          회사 테이블
│   ├── User.java             사용자 테이블
│   ├── Skill.java            스킬 테이블
│   └── ...
│
├── repository/          💾 데이터 접근 계층
│   ├── JobPostRepository.java   채용공고 DB 접근
│   ├── CompanyRepository.java   회사 DB 접근
│   └── ...
│
├── service/             🔨 비즈니스 로직
│   ├── job/
│   │   └── JobPostService.java   채용공고 관련 로직
│   ├── auth/
│   │   └── AuthService.java      인증/로그인 로직
│   └── ...
│
├── exception/           ⚠️ 에러 처리
│   ├── ErrorCode.java            에러 코드 정의
│   ├── BusinessException.java    커스텀 예외
│   └── GlobalExceptionHandler.java  전역 에러 핸들러
│
├── util/                🛠️ 유틸리티
│   └── JwtUtil.java              JWT 토큰 생성/검증
│
└── DemoApplication.java  ▶️ 프로그램 시작점
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

### 작업 시작 전 (필수!)

#### 1️⃣ 최신 코드 받기
```bash
git pull origin main
```

#### 2️⃣ 새 브랜치 만들기
```bash
# 예: WBS 3.2.2 공고 API 개발
git checkout -b feature/job-post-api
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

### 1. 서버가 시작되지 않아요!

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

### 2. DB 연결 오류

#### 증상: `Access denied for user 'root'@'localhost'`

**해결 방법**:
1. `application.yml`에서 비밀번호 확인
2. MariaDB가 실행 중인지 확인
```bash
# MariaDB 상태 확인 (Mac)
brew services list

# MariaDB 시작
brew services start mariadb
```

---

### 3. 빌드 실패

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

### 4. Lombok 에러

#### 증상: `Cannot resolve symbol 'getData'`

**해결 방법** (IntelliJ):
1. File > Settings > Plugins
2. "Lombok" 검색 및 설치
3. File > Settings > Build > Compiler > Annotation Processors
4. "Enable annotation processing" 체크
5. IntelliJ 재시작

---

## 📞 도움말

### 자주 묻는 질문

#### Q1. Entity를 수정했는데 DB에 반영이 안 돼요!
**A**: `application.yml`에서 `ddl-auto: update`로 설정되어 있는지 확인하세요. 또는 서버를 재시작하세요.

#### Q2. API 테스트는 어떻게 하나요?
**A**: Swagger UI 또는 Postman을 사용하세요. Swagger가 더 간편합니다.

#### Q3. 다른 팀원이 만든 코드가 안 돌아가요!
**A**:
```bash
# 최신 코드 받기
git pull origin main

# 의존성 다시 설치
./gradlew clean build
```

---

## 🎓 학습 자료

### 초보자를 위한 추천 자료

1. **Spring Boot 공식 가이드**: https://spring.io/guides/gs/spring-boot/
2. **JPA 기초**: https://spring.io/guides/gs/accessing-data-jpa/
3. **REST API 이해하기**: https://www.youtube.com/watch?v=iOueE9AXDQQ

---

## 🤝 기여하기

1. 이슈 확인: https://github.com/SKALA-SKouter/SKouter-backend/issues
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

- 프론트엔드: https://github.com/SKALA-SKouter/SKouter-frontend
- AI Agent: https://github.com/SKALA-SKouter/SKouter-AI-Agent

---

**마지막 업데이트**: 2025-11-20
