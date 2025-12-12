# 🚀 OSMU Blog Automation System

**One Source Multi Use** - Markdown 기반 자동 블로그 배포 시스템

[![GitHub Pages](https://img.shields.io/badge/GitHub-Pages-success)](https://ailifestudio.github.io/)
[![WordPress](https://img.shields.io/badge/WordPress-Ready-blue)]()
[![Automation](https://img.shields.io/badge/Automation-GitHub_Actions-orange)]()

---

## 📋 시스템 개요

하나의 Markdown 소스로 **GitHub Pages**와 **WordPress**에 자동 배포하는 완전 자동화 시스템입니다.

```
Markdown (.md)
    ↓
    ├─→ GitHub Pages (초고속 대시보드)
    │    • JSON 파일 분할로 빠른 로딩
    │    • 카테고리별 페이지네이션
    │
    └─→ WordPress (SEO 원본)
         • REST API 자동 발행
         • Canonical URL 설정
         • 중복 방지
```

---

## ✨ 핵심 기능

### 1️⃣ Markdown 중심 작성 환경

- ✍️ **간편한 작성**: Markdown으로 글 작성
- 📝 **Front Matter**: YAML 메타데이터로 모든 정보 관리
- 🔄 **버전 관리**: Git으로 글 히스토리 추적
- 🎨 **에디터 자유**: VS Code, Typora, Obsidian 등 어디서나

### 2️⃣ GitHub Pages 초고속 로딩

- ⚡ **JSON 분할**: 메인 페이지는 50개 글만 로드
- 📊 **페이지네이션**: 카테고리별 20개씩 자동 분할
- 🎯 **카테고리 필터**: AI/테크, 경제, 라이프, 글로벌
- 📱 **반응형 디자인**: Tailwind CSS 기반

### 3️⃣ WordPress SEO 최적화

- 🔗 **Canonical URL**: SEO 링크 주스를 WordPress로 집중
- 🚫 **중복 방지**: 검색 엔진 페널티 없음
- 🤖 **자동 동기화**: REST API로 자동 발행/업데이트
- 🔒 **안전한 인증**: Application Password 사용

### 4️⃣ 완전 자동화

- ⏰ **스케줄 실행**: 매일 3회 자동 실행 (09:00, 17:00, 01:00 KST)
- 🔄 **Git Push 배포**: 코드 푸시 시 자동 배포
- 🛡️ **안전 폴백**: WordPress 실패 시에도 GitHub Pages 배포 계속
- 📲 **수동 트리거**: 필요 시 즉시 실행 가능

---

## 🎯 빠른 시작

### 1단계: 저장소 복제

```bash
git clone https://github.com/ailifestudio/ailifestudio.github.io.git
cd ailifestudio.github.io
```

### 2단계: Python 환경 설정

```bash
# Python 패키지 설치
pip install -r automation/requirements.txt
```

필수 패키지:
- `python-frontmatter`: Markdown Front Matter 파싱
- `markdown`: Markdown → HTML 변환
- `requests`: WordPress REST API
- `feedparser`, `beautifulsoup4`: RSS 뉴스 크롤링
- `google-generativeai`: AI 콘텐츠 생성

### 3단계: 첫 글 작성

```bash
# 새 글 작성 도우미 실행
./new_post.sh ai-tech "나의 첫 AI 블로그 글"
```

생성된 파일 (`_posts/ai-tech/2025-12-12-나의-첫-ai-블로그-글.md`) 편집:

```markdown
---
title: "나의 첫 AI 블로그 글"
date: 2025-12-12
category: ai-tech
canonical_url: ""
summary: "AI 블로그를 시작하며 느낀 점과 앞으로의 계획을 공유합니다."
image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80"
tags:
  - AI
  - 블로그
  - 시작
---

## 시작하며

안녕하세요! 오늘부터 AI 블로그를 시작합니다...
```

### 4단계: 로컬 테스트

```bash
# OSMU 빌드 실행
python automation/build_and_sync.py

# 로컬 서버 실행
python -m http.server 8000

# 브라우저에서 확인
# http://localhost:8000
```

### 5단계: GitHub 배포

```bash
# 변경사항 커밋
git add _posts/ dashboard_summary.json data/
git commit -m "✨ 첫 글 추가: 나의 첫 AI 블로그 글"

# GitHub에 푸시 (자동 배포 시작)
git push origin main
```

**🎉 완료!** GitHub Actions가 자동으로 배포를 시작합니다.

- 배포 진행: GitHub → Actions 탭에서 확인
- 배포 완료: 5-10분 후 https://ailifestudio.github.io/ 에서 확인

---

## 🔧 WordPress 연동 (선택)

WordPress 사이트가 있다면 SEO 최적화를 위해 연동을 추천합니다.

### 1단계: Application Password 생성

1. WordPress 대시보드 → 사용자 → 프로필
2. "Application Passwords" 섹션 찾기
3. 이름 입력 (예: "GitHub Actions")
4. "Add New Application Password" 클릭
5. **생성된 비밀번호 복사** (띄어쓰기 포함)

### 2단계: GitHub Secrets 설정

GitHub 저장소 → Settings → Secrets and variables → Actions

**3개의 Secret 추가:**

| Name | Description | Example |
|------|-------------|---------|
| `WP_URL` | WordPress 사이트 URL | `https://yourblog.com` |
| `WP_USERNAME` | WordPress 사용자명 | `admin` |
| `WP_APP_PASSWORD` | Application Password | `xxxx xxxx xxxx xxxx` |

### 3단계: 테스트

워크플로우 수동 실행:
1. GitHub → Actions → "OSMU Deploy"
2. "Run workflow" 클릭
3. 로그에서 WordPress 동기화 확인

**성공 메시지:**
```
✅ Created in WordPress: 나의 첫 AI 블로그 글
📝 Updated canonical URL: https://yourblog.com/2025/12/...
```

---

## 📂 프로젝트 구조

```
webapp/
├── _posts/                          # 📝 Markdown 글 저장소
│   ├── ai-tech/                     # AI/테크 카테고리
│   ├── economy/                     # 경제
│   ├── life/                        # 라이프
│   └── global/                      # 글로벌
│
├── data/                            # 📊 생성된 JSON 데이터
│   ├── ai-tech/page_1.json
│   ├── economy/page_1.json
│   └── ...
│
├── _includes/                       # 🎨 재사용 컴포넌트
│   └── seo_head.html                # SEO 메타 태그
│
├── automation/                      # 🤖 자동화 스크립트
│   ├── build_and_sync.py           # OSMU 메인 빌드
│   ├── ai_content_generator.py     # AI 콘텐츠 생성
│   ├── news_crawler.py             # RSS 뉴스 크롤링
│   ├── config_osmu.json            # WordPress 설정
│   └── requirements.txt
│
├── .github/workflows/
│   └── deploy.yml                  # 자동 배포 워크플로우
│
├── index.html                       # 메인 페이지
├── article.html                     # 글 상세 페이지
├── dashboard_summary.json           # 메인 페이지 데이터
├── new_post.sh                      # 새 글 생성 도우미
└── OSMU_GUIDE.md                    # 상세 가이드
```

---

## 🎨 글 작성 가이드

### Front Matter 필수 항목

| 필드 | 필수 | 설명 | 예시 |
|------|:----:|------|------|
| `title` | ✅ | 글 제목 | "AI 생산성 도구 Top 5" |
| `date` | ✅ | 작성 날짜 | `2025-12-12` |
| `category` | ✅ | 카테고리 | `ai-tech` |
| `canonical_url` | ✅ | WordPress URL (자동) | `""` |
| `summary` | ✅ | 요약 (150자 이내) | "최신 AI 도구 소개..." |
| `image` | ✅ | 대표 이미지 | "https://..." |
| `tags` | ⬜ | 태그 | `["AI", "생산성"]` |

### 카테고리 목록

| 디렉토리 | 한글명 | 설명 |
|----------|--------|------|
| `ai-tech` | AI/테크 | AI, 테크놀로지 관련 |
| `economy` | 경제 | 경제, 비즈니스 |
| `life` | 라이프 | 라이프스타일 |
| `global` | 글로벌 | 해외 뉴스 |

### Markdown 작성 팁

```markdown
---
title: "제목"
date: 2025-12-12
category: ai-tech
canonical_url: ""
summary: "요약"
image: "https://..."
tags: ["태그1", "태그2"]
---

## 메인 제목 (H2)

단락 내용...

### 소제목 (H3)

- 리스트 항목 1
- 리스트 항목 2

**굵은 글씨** *기울임* `코드`

> 인용구

![이미지 설명](https://...)

[링크 텍스트](https://...)
```

---

## ⚙️ 고급 설정

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

### 자동 실행 스케줄 변경

`.github/workflows/deploy.yml`:

```yaml
schedule:
  # 매일 09:00, 17:00, 01:00 KST 실행
  - cron: '0 0,8,16 * * *'
  
  # 매일 1회 (자정)
  # - cron: '0 0 * * *'
  
  # 평일만 (월-금)
  # - cron: '0 0 * * 1-5'
```

### 새 카테고리 추가

1. 디렉토리 생성
   ```bash
   mkdir -p _posts/new-category data/new-category
   ```

2. `build_and_sync.py` 업데이트
   ```python
   self.categories = {
       "ai-tech": "AI/테크",
       "new-category": "새 카테고리"  # 추가
   }
   ```

3. `index.html` 업데이트
   ```javascript
   const categories = ['전체', 'AI/테크', '새 카테고리'];
   ```

---

## 🔍 SEO 최적화 상세

### Canonical URL 시스템

#### 동작 방식

```
1. Markdown 작성 (canonical_url: "")
   ↓
2. WordPress 발행
   ↓
3. WordPress URL 획득
   ↓
4. Markdown Front Matter 자동 업데이트
   ↓
5. GitHub Pages에 canonical 태그 적용
```

#### HTML 출력

```html
<!-- GitHub Pages -->
<link rel="canonical" href="https://yourblog.com/2025/12/ai-tips/" />
<meta property="og:url" content="https://yourblog.com/2025/12/ai-tips/" />
```

#### SEO 효과

- ✅ **검색 엔진**: WordPress를 원본으로 인식
- ✅ **링크 주스**: 모든 SEO 가치가 WordPress로 집중
- ✅ **중복 방지**: 페널티 없음

---

## 🛠️ 트러블슈팅

### WordPress 동기화 실패

**증상:**
```
❌ Failed to create post: 401 Unauthorized
```

**해결:**
1. Application Password 재생성
2. GitHub Secrets 재확인 (`WP_APP_PASSWORD`)
3. WordPress REST API 활성화 확인:
   ```bash
   curl https://yoursite.com/wp-json/wp/v2/posts
   ```

### JSON 파일 생성 안됨

**증상:**
- `dashboard_summary.json` 없음

**해결:**
```bash
# _posts/ 확인
ls -R _posts/

# 수동 빌드
python automation/build_and_sync.py

# 에러 로그 확인
python automation/build_and_sync.py 2>&1 | tee build.log
```

### GitHub Pages 배포 안됨

**해결:**
1. Settings → Pages → Source: "Deploy from a branch" (main)
2. GitHub Actions → Workflow permissions → "Read and write permissions"
3. 캐시 삭제 후 재접속 (Ctrl + Shift + R)

---

## 📚 관련 문서

- [📖 OSMU 상세 가이드](OSMU_GUIDE.md) - 완전한 시스템 설명서
- [🏗️ 아키텍처 문서](ARCHITECTURE.md) - 시스템 구조 설명
- [⚡ 빠른 시작](QUICKSTART.md) - 초보자용 가이드
- [🤖 AI 콘텐츠 가이드](AI_CONTENT_GUIDE.md) - AI 자동 생성 기능

---

## 🤝 기여 및 지원

### 버그 리포트
GitHub Issues에 버그를 리포트해주세요.

### 기능 제안
새로운 기능 아이디어를 공유해주세요.

### 문서 개선
오타나 잘못된 정보를 발견하시면 PR을 보내주세요.

---

## 📄 라이선스

MIT License - 자유롭게 사용, 수정, 배포 가능합니다.

---

## 🎯 다음 단계

1. ✅ 첫 글 작성하기
2. ✅ GitHub Pages에서 확인하기
3. ⬜ WordPress 연동하기 (선택)
4. ⬜ 정기적으로 글 작성하기
5. ⬜ 커스터마이징하기

---

**만든 이:** AI Life Studio  
**최종 업데이트:** 2025-12-12  
**웹사이트:** https://ailifestudio.github.io/

---

**🌟 이 프로젝트가 도움이 되었다면 Star를 눌러주세요!**
