# 🐳 Docker 배포 가이드

SKouter 백엔드를 Docker로 배포하는 방법입니다.

---

## 📖 목차

1. [로컬에서 Docker 실행](#-로컬에서-docker-실행)
2. [GitHub Actions 자동 배포](#-github-actions-자동-배포)
3. [배포된 이미지 사용하기](#-배포된-이미지-사용하기)
4. [AWS 배포 (향후)](#-aws-배포-향후)

---

## 🚀 로컬에서 Docker 실행

### 1️⃣ 사전 준비

- **Docker Desktop 설치** ([다운로드](https://www.docker.com/products/docker-desktop))
- Docker가 실행 중인지 확인: `docker --version`

---

### 2️⃣ 환경 변수 설정

```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일 수정
nano .env
```

**.env 예시:**
```env
DB_USERNAME=skouter
DB_PASSWORD=my-strong-password
JWT_SECRET=my-jwt-secret-key-256-bits-minimum
```

---

### 3️⃣ Docker Compose로 실행

```bash
# 모든 서비스 실행 (MariaDB + Redis + Backend)
docker-compose up -d

# 로그 확인
docker-compose logs -f backend

# 상태 확인
docker-compose ps
```

**실행되는 서비스:**
- **MariaDB**: http://localhost:3306
- **Redis**: http://localhost:6379
- **Backend**: http://localhost:8080

---

### 4️⃣ 실행 확인

```bash
# 헬스체크
curl http://localhost:8080/actuator/health

# Swagger UI
open http://localhost:8080/swagger-ui.html
```

---

### 5️⃣ 종료 및 정리

```bash
# 서비스 중지
docker-compose down

# 데이터까지 삭제 (주의!)
docker-compose down -v
```

---

## ⚙️ GitHub Actions 자동 배포

### 작동 방식

```
코드 push (main 브랜치)
    ↓
GitHub Actions 자동 실행
    ↓
1. Gradle 빌드
2. 테스트 실행
3. Docker 이미지 생성
4. GitHub Container Registry에 Push
    ↓
완료! 🎉
```

---

### 설정 방법 (이미 완료됨!)

✅ 다음 파일들이 자동으로 생성되었습니다:
- `.github/workflows/docker-build.yml` - GitHub Actions 워크플로우
- `Dockerfile` - Docker 이미지 빌드 설정
- `docker-compose.yml` - 로컬 개발/테스트용
- `.dockerignore` - Docker 빌드에서 제외할 파일

---

### 자동 배포 확인

1. **코드 푸시**
```bash
git add .
git commit -m "feat: 새 기능 추가"
git push origin main
```

2. **GitHub Actions 확인**
   - GitHub 레포 → **Actions** 탭
   - "Docker Build and Push" 워크플로우 확인
   - 녹색 체크 표시 ✅ = 성공!

3. **생성된 이미지 확인**
   - GitHub 레포 → 우측 **Packages** 클릭
   - `skouter-backend` 이미지 확인

---

### 이미지 태그 설명

| 태그 | 설명 | 예시 |
|------|------|------|
| `latest` | main 브랜치 최신 | `ghcr.io/skala-skouter/skouter-backend:latest` |
| `main` | main 브랜치 | `ghcr.io/skala-skouter/skouter-backend:main` |
| `main-abc1234` | 커밋 해시 | `ghcr.io/skala-skouter/skouter-backend:main-abc1234` |

---

## 📦 배포된 이미지 사용하기

### 1️⃣ GitHub Container Registry 로그인

```bash
# Personal Access Token 생성 필요
# GitHub → Settings → Developer settings → Personal access tokens
# Scope: write:packages, read:packages

echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin
```

---

### 2️⃣ 이미지 Pull

```bash
# 최신 이미지
docker pull ghcr.io/skala-skouter/skouter-backend:latest

# 특정 버전
docker pull ghcr.io/skala-skouter/skouter-backend:main
```

---

### 3️⃣ 실행

```bash
docker run -d \
  --name skouter-backend \
  -p 8080:8080 \
  -e SPRING_PROFILES_ACTIVE=prod \
  -e DB_HOST=your-db-host \
  -e DB_USERNAME=skouter \
  -e DB_PASSWORD=your-password \
  -e REDIS_HOST=your-redis-host \
  -e JWT_SECRET=your-jwt-secret \
  ghcr.io/skala-skouter/skouter-backend:latest
```

---

## ☁️ AWS 배포 (향후)

### 옵션 1: AWS ECS (Elastic Container Service)

```yaml
# .github/workflows/aws-deploy.yml (예시)
- name: Deploy to ECS
  run: |
    aws ecs update-service \
      --cluster skouter-cluster \
      --service skouter-backend \
      --force-new-deployment
```

**필요한 설정:**
1. AWS 계정 생성
2. ECR (Elastic Container Registry) 생성
3. ECS 클러스터 및 서비스 생성
4. GitHub Secrets에 AWS 자격증명 추가

---

### 옵션 2: AWS EC2 (가상 서버)

```bash
# EC2 인스턴스에서 실행
ssh ubuntu@your-ec2-ip

# Docker 설치
sudo apt update
sudo apt install docker.io docker-compose

# 이미지 Pull 및 실행
docker pull ghcr.io/skala-skouter/skouter-backend:latest
docker run -d -p 8080:8080 ...
```

---

### 옵션 3: AWS Lightsail (간단한 서버)

- 가장 저렴하고 간단
- 월 $3.50부터 시작
- Docker 지원

---

## 🔧 문제 해결

### 1. Docker 빌드 실패

#### 증상: `Could not resolve dependencies`

```bash
# Gradle 캐시 삭제
./gradlew clean
docker-compose build --no-cache
```

---

### 2. GitHub Actions 실패

#### 증상: `Permission denied`

**해결**: GitHub → Settings → Actions → General
- **Workflow permissions**: Read and write permissions 체크

---

### 3. 이미지가 안 보여요

#### 증상: Packages 탭에 이미지 없음

**해결**:
1. GitHub Actions가 성공했는지 확인
2. 레포가 Public인지 확인 (Private이면 추가 설정 필요)
3. main 브랜치에 푸시했는지 확인

---

## 📊 모니터링

### 컨테이너 상태 확인

```bash
# 실행 중인 컨테이너
docker ps

# 로그 확인
docker logs -f skouter-backend

# 리소스 사용량
docker stats
```

---

### 헬스체크

```bash
# 백엔드 헬스
curl http://localhost:8080/actuator/health

# MariaDB 헬스
docker exec skouter-mariadb mysqladmin ping -h localhost

# Redis 헬스
docker exec skouter-redis redis-cli ping
```

---

## 🎯 다음 단계

### 지금 당장:
1. ✅ 로컬에서 `docker-compose up` 테스트
2. ✅ 코드 푸시해서 GitHub Actions 확인

### 나중에 (AWS 사용 시):
1. AWS 계정 생성
2. ECR 또는 EC2 선택
3. GitHub Actions에 배포 단계 추가
4. 도메인 연결 (선택)

---

## 💡 팁

### 개발 vs 프로덕션

```yaml
# docker-compose.dev.yml (개발용)
services:
  backend:
    build: .
    volumes:
      - ./src:/app/src  # 코드 실시간 반영
    environment:
      SPRING_PROFILES_ACTIVE: dev

# docker-compose.yml (프로덕션용)
services:
  backend:
    image: ghcr.io/skala-skouter/skouter-backend:latest
    environment:
      SPRING_PROFILES_ACTIVE: prod
```

---

## 📚 참고 자료

- [Docker 공식 문서](https://docs.docker.com/)
- [GitHub Actions 문서](https://docs.github.com/en/actions)
- [Spring Boot Docker 가이드](https://spring.io/guides/topicals/spring-boot-docker/)

---

**마지막 업데이트**: 2025-11-20
