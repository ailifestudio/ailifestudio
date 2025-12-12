# OSMU (One Source Multi Use) 시스템 완벽 가이드

## 📚 목차
- [시스템 개요](#시스템-개요)
- [아키텍처](#아키텍처)
- [설치 및 설정](#설치-및-설정)
- [사용 방법](#사용-방법)
- [WordPress 연동](#wordpress-연동)
- [SEO 최적화](#seo-최적화)
- [트러블슈팅](#트러블슈팅)

---

## 시스템 개요

### OSMU란?

**One Source Multi Use (일원다용)** 시스템은 하나의 Markdown 소스로부터 여러 플랫폼에 자동 배포하는 자동화 시스템입니다.

```
Markdown (.md)
    ↓
    ├─→ GitHub Pages (초고속 대시보드)
    │    • dashboard_summary.json (메인 페이지)
    │    • data/{category}/page_*.json (카테고리별 페이지)
    │
    └─→ WordPress (SEO 원본)
         • REST API 자동 발행
         • Canonical URL 자동 설정
         • 중복 방지
```

### 핵심 특징

1. **📝 Markdown 중심 작성**
   - Front Matter로 메타데이터 관리
   - 버전 관리 (Git)
   - 에디터 자유 선택

2. **⚡ GitHub Pages 초고속 로딩**
   - JSON 파일 분할 (dashboard + paginated)
   - 최신 50개 글만 메인 페이지 로드
   - 카테고리별 페이지네이션

3. **🎯 WordPress SEO 최적화**
   - Canonical URL로 SEO 링크 주스 집중
   - 중복 콘텐츠 페널티 방지
   - REST API 자동 동기화

4. **🤖 완전 자동화**
   - GitHub Actions 자동 실행
   - WordPress 동기화 실패 시 안전 폴백
   - 수동 트리거 지원

---

## 아키텍처

### 디렉토리 구조

```
webapp/
├── _posts/                          # Markdown 글 저장소
│   ├── ai-tech/                     # AI/테크 카테고리
│   │   └── 2025-12-12-example.md
│   ├── economy/                     # 경제 카테고리
│   ├── life/                        # 라이프 카테고리
│   └── global/                      # 글로벌 카테고리
│
├── data/                            # 생성된 JSON 데이터
│   ├── ai-tech/
│   │   ├── page_1.json
│   │   └── page_2.json
│   ├── economy/
│   ├── life/
│   └── global/
│
├── _includes/                       # 재사용 컴포넌트
│   └── seo_head.html                # SEO 헤드 태그
│
├── automation/                      # 자동화 스크립트
│   ├── build_and_sync.py           # OSMU 메인 빌드 스크립트
│   ├── config_osmu.json            # WordPress 설정
│   ├── requirements.txt            # Python 패키지
│   └── ...
│
├── .github/workflows/
│   └── deploy.yml                  # GitHub Actions 워크플로우
│
├── index.html                       # GitHub Pages 메인 페이지
├── article.html                     # 글 상세 페이지
├── dashboard_summary.json           # 메인 페이지용 데이터
└── data.json                        # 하위 호환용 (legacy)
```

### 데이터 흐름

```
1. Markdown 작성
   └─→ _posts/{category}/yyyy-mm-dd-slug.md

2. GitHub Push
   └─→ GitHub Actions 트리거

3. build_and_sync.py 실행
   ├─→ Markdown 파싱 (python-frontmatter)
   ├─→ HTML 변환 (markdown)
   ├─→ dashboard_summary.json 생성
   ├─→ data/{category}/page_*.json 생성
   └─→ WordPress REST API 동기화
       └─→ canonical_url 자동 업데이트

4. GitHub Pages 자동 배포
   └─→ https://ailifestudio.github.io/
```

---

## 설치 및 설정

### 1. 필수 요구사항

- Python 3.11+
- Git
- GitHub 계정
- WordPress 사이트 (선택)

### 2. Python 패키지 설치

```bash
pip install -r automation/requirements.txt
```

필수 패키지:
- `python-frontmatter`: Markdown Front Matter 파싱
- `markdown`: Markdown → HTML 변환
- `requests`: WordPress REST API 통신

### 3. WordPress 설정 (선택)

WordPress를 사용하는 경우:

#### 3.1 Application Password 생성

1. WordPress 대시보드 → 사용자 → 프로필
2. "Application Passwords" 섹션
3. 이름 입력 (예: "GitHub Actions")
4. "Add New Application Password" 클릭
5. 생성된 비밀번호 복사 (띄어쓰기 포함)

#### 3.2 GitHub Secrets 설정

GitHub 저장소 → Settings → Secrets and variables → Actions

3개의 Secret 추가:

| Name | Value | Example |
|------|-------|---------|
| `WP_URL` | WordPress 사이트 URL | `https://yourblog.com` |
| `WP_USERNAME` | WordPress 사용자명 | `admin` |
| `WP_APP_PASSWORD` | Application Password | `xxxx xxxx xxxx xxxx` |

#### 3.3 로컬 테스트용 설정 (선택)

`automation/config_osmu.json` 파일 생성:

```json
{
  "wordpress": {
    "url": "https://your-wordpress-site.com",
    "username": "your_username",
    "app_password": "your_app_password"
  },
  "pagination": {
    "items_per_page": 20,
    "dashboard_items": 50
  },
  "seo": {
    "enable_canonical": true,
    "wordpress_is_primary": true
  }
}
```

**⚠️ 중요:** `config_osmu.json`은 `.gitignore`에 추가하여 공개 저장소에 올리지 마세요!

---

## 사용 방법

### 1. Markdown 글 작성

#### 파일 이름 규칙
```
yyyy-mm-dd-slug.md
```

예시: `2025-12-12-ai-productivity-tips.md`

#### Front Matter 필수 항목

```markdown
---
title: "글 제목"
date: 2025-12-12
category: ai-tech
canonical_url: ""
summary: "글 요약 (150자 이내)"
image: "https://example.com/image.jpg"
tags:
  - AI
  - 생산성
---

## 본문 시작

여기에 Markdown 형식으로 글을 작성합니다...
```

#### Front Matter 필드 설명

| 필드 | 필수 | 설명 | 예시 |
|------|------|------|------|
| `title` | ✅ | 글 제목 | "AI 활용 생산성 팁" |
| `date` | ✅ | 작성 날짜 | `2025-12-12` |
| `category` | ✅ | 카테고리 | `ai-tech`, `economy`, `life`, `global` |
| `canonical_url` | ✅ | WordPress URL (자동 업데이트) | 초기값 `""` |
| `summary` | ✅ | 요약 (SEO용) | "150자 이내 요약" |
| `image` | ✅ | 대표 이미지 URL | "https://..." |
| `tags` | ⬜ | 태그 배열 | `["AI", "생산성"]` |

### 2. 로컬 테스트

```bash
# 빌드 스크립트 실행
python automation/build_and_sync.py

# 생성된 파일 확인
ls -lh dashboard_summary.json
ls -lh data/ai-tech/

# 로컬 서버 실행
python -m http.server 8000

# 브라우저에서 확인
# http://localhost:8000
```

### 3. GitHub 배포

```bash
# 변경사항 커밋
git add _posts/ automation/
git commit -m "✨ 새 글 추가: AI 생산성 팁"

# 푸시
git push origin main
```

**자동 실행:**
- GitHub Actions가 자동으로 트리거
- `build_and_sync.py` 실행
- JSON 파일 생성
- WordPress 동기화
- GitHub Pages 배포

### 4. 수동 워크플로우 실행

GitHub 저장소 → Actions → "OSMU Deploy" → "Run workflow"

옵션:
- **Skip WordPress sync**: WordPress 동기화 건너뛰기 (GitHub Pages만)

---

## WordPress 연동

### REST API 엔드포인트

`build_and_sync.py`는 다음 WordPress REST API를 사용합니다:

```
GET  /wp-json/wp/v2/posts?slug={slug}    # 기존 글 검색
POST /wp-json/wp/v2/posts                # 새 글 생성
POST /wp-json/wp/v2/posts/{id}           # 기존 글 업데이트
```

### 동기화 로직

```python
# 중복 방지 체크
existing_post = search_by_slug(slug)

if existing_post:
    # 기존 글 업데이트
    update_post(id, content)
else:
    # 새 글 생성
    create_post(content)

# canonical_url 자동 저장
update_markdown_frontmatter(canonical_url)
```

### 안전 폴백 (Fail-Safe)

WordPress 동기화 실패 시에도 GitHub Pages 배포는 계속 진행됩니다.

```python
try:
    sync_to_wordpress(posts)
except Exception as e:
    print("⚠️ WordPress sync failed, continuing deployment")
```

---

## SEO 최적화

### Canonical URL 시스템

#### 목적
- **SEO 링크 주스 집중**: 모든 검색 엔진 평가가 WordPress로 집중
- **중복 콘텐츠 방지**: GitHub Pages와 WordPress 간 중복 페널티 방지

#### 구현

**1. Markdown Front Matter**
```yaml
canonical_url: "https://yourblog.com/2025/12/ai-tips/"
```

**2. HTML Head 태그**
```html
<link rel="canonical" href="https://yourblog.com/2025/12/ai-tips/" />
```

**3. Open Graph**
```html
<meta property="og:url" content="https://yourblog.com/2025/12/ai-tips/" />
```

#### 자동 업데이트 프로세스

```
1. WordPress 글 발행
   └─→ REST API 응답에서 URL 획득

2. Markdown Front Matter 업데이트
   └─→ canonical_url: "https://..."

3. GitHub 자동 커밋
   └─→ Git push

4. 다음 배포 시 canonical tag 반영
```

### SEO 베스트 프랙티스

#### ✅ 권장사항

1. **WordPress를 Primary로 설정**
   ```json
   "seo": {
     "wordpress_is_primary": true
   }
   ```

2. **Canonical URL 필수 설정**
   - 모든 글에 canonical URL 존재
   - WordPress URL을 항상 사용

3. **GitHub Pages Noindex (선택)**
   - `_includes/seo_head.html`에 추가:
   ```html
   <meta name="robots" content="noindex, nofollow" />
   ```

#### ❌ 주의사항

- Canonical URL 없이 배포하지 않기
- GitHub Pages와 WordPress 양쪽에 다른 canonical 설정 금지
- 중복 콘텐츠 방지를 위해 canonical 필수

---

## 트러블슈팅

### 문제 1: WordPress 동기화 실패

**증상:**
```
❌ Failed to create post: 401 Unauthorized
```

**해결:**
1. Application Password 재생성
2. GitHub Secrets 재확인
3. WordPress REST API 활성화 확인
   ```bash
   curl https://yoursite.com/wp-json/wp/v2/posts
   ```

### 문제 2: JSON 파일 생성 안됨

**증상:**
- `dashboard_summary.json` 없음
- `data/` 디렉토리 비어있음

**해결:**
```bash
# _posts/ 디렉토리 확인
ls -R _posts/

# 수동 빌드 실행
python automation/build_and_sync.py

# 에러 로그 확인
python automation/build_and_sync.py 2>&1 | tee build.log
```

### 문제 3: Canonical URL 자동 업데이트 안됨

**증상:**
- `canonical_url: ""` 그대로 남음

**해결:**
1. Git write permission 확인
2. GitHub Actions workflow permission 설정
   - Settings → Actions → General
   - "Read and write permissions" 선택

### 문제 4: GitHub Pages 배포 안됨

**증상:**
- Actions는 성공했지만 사이트 업데이트 안됨

**해결:**
1. GitHub Pages 설정 확인
   - Settings → Pages
   - Source: "Deploy from a branch" (main)
2. 캐시 삭제 후 재접속
   ```
   Ctrl + Shift + R (캐시 무시 새로고침)
   ```

### 문제 5: Python 패키지 오류

**증상:**
```
ModuleNotFoundError: No module named 'frontmatter'
```

**해결:**
```bash
pip install --upgrade -r automation/requirements.txt
```

---

## 고급 설정

### 페이지네이션 커스터마이징

`automation/config_osmu.json`:

```json
{
  "pagination": {
    "items_per_page": 20,      // 카테고리 페이지당 글 수
    "dashboard_items": 50       // 메인 페이지 표시 글 수
  }
}
```

### 카테고리 추가

1. 디렉토리 생성
   ```bash
   mkdir -p _posts/new-category
   mkdir -p data/new-category
   ```

2. `build_and_sync.py` 업데이트
   ```python
   self.categories = {
       "ai-tech": "AI/테크",
       "economy": "경제",
       "life": "라이프",
       "global": "글로벌",
       "new-category": "새 카테고리"  # 추가
   }
   ```

3. `index.html` 카테고리 버튼 추가
   ```javascript
   const categories = ['전체', 'AI/테크', '경제', '라이프', '글로벌', '새 카테고리'];
   ```

---

## 워크플로우 스케줄

### 기본 스케줄 (매일 3회)

```yaml
schedule:
  - cron: '0 0,8,16 * * *'
```

- **UTC 00:00** → KST 09:00 (오전)
- **UTC 08:00** → KST 17:00 (저녁)
- **UTC 16:00** → KST 01:00 (새벽)

### 커스터마이징

```yaml
# 매일 1회 (자정)
- cron: '0 0 * * *'

# 평일만 (월-금)
- cron: '0 0 * * 1-5'

# 매시간
- cron: '0 * * * *'
```

---

## 참고 자료

### 공식 문서
- [Python Frontmatter](https://python-frontmatter.readthedocs.io/)
- [WordPress REST API](https://developer.wordpress.org/rest-api/)
- [GitHub Actions](https://docs.github.com/actions)
- [Markdown Guide](https://www.markdownguide.org/)

### 관련 파일
- [`automation/build_and_sync.py`](automation/build_and_sync.py) - 메인 빌드 스크립트
- [`_includes/seo_head.html`](_includes/seo_head.html) - SEO 헤드 컴포넌트
- [`workflow-deploy.yml`](workflow-deploy.yml) - GitHub Actions 워크플로우
- [`automation/config_osmu.json`](automation/config_osmu.json) - 설정 파일

---

## 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능

---

## 문의 및 지원

- GitHub Issues: 버그 리포트 및 기능 제안
- 문서 개선 제안 환영

---

**만든 이:** AI Life Studio  
**최종 업데이트:** 2025-12-12
