# 표준 디렉토리 구조 (Standard Directory Structure)

## 📁 디렉토리 구조

이 프로젝트는 Jekyll 표준 구조(`_posts`, `_includes` 등)를 사용하지 않고, 커스텀 구조를 사용합니다.

```
/ (Root)
├── index.html               # [Frontend] data/dashboard_summary.json을 로드
├── article.html             # 글 상세 페이지
├── assets/
│   └── css/
├── contents/                # [Input] 원본 Markdown 파일 위치 ✅
│   ├── post1.md
│   └── post2.md
├── data/                    # [Output] UI용 JSON 데이터 ✅
│   ├── dashboard_summary.json
│   ├── ai/
│   │   ├── page_1.json
│   │   └── page_2.json
│   ├── it/
│   └── ...
├── feed/                    # [Output] WordPress용 피드 ✅
│   ├── rss.xml
│   └── full_export.json
└── automation/
    ├── build_blog.py        # [Script] 빌드 스크립트 ✅
    ├── config_blog.json     # 설정 파일
    └── requirements.txt
```

---

## 🎯 핵심 원칙

### 1. `contents/` - 원본 Markdown 저장소

**위치**: `/contents/`

**용도**:
- 모든 Markdown 글은 `contents/` 폴더에 저장
- 카테고리별 서브폴더 없음 (flat structure)
- Front Matter로 카테고리 지정

**파일명 규칙**:
```
YYYY-MM-DD-slug.md
```

예시:
```
contents/2025-12-12-ai-productivity.md
contents/2025-12-13-tech-news.md
```

**Front Matter 예시**:
```yaml
---
title: "글 제목"
date: 2025-12-12
category: ai          # ai, it, economy, life, global
canonical_url: ""
summary: "요약"
image: "https://..."
tags:
  - AI
  - Tech
---
```

---

### 2. `data/` - UI용 JSON 출력

**위치**: `/data/`

**자동 생성 파일**:
```
data/
├── dashboard_summary.json   # 메인 페이지용 (최신 50개)
├── ai/
│   ├── page_1.json          # AI 카테고리 1페이지 (20개)
│   └── page_2.json          # AI 카테고리 2페이지 (20개)
├── it/
│   └── page_1.json
└── ...
```

**dashboard_summary.json 구조**:
```json
{
  "updatedAt": "2025-12-12 10:00",
  "total": 150,
  "articles": [
    {
      "title": "글 제목",
      "source": "AI Life Studio",
      "time": "2시간 전",
      "summary": "요약...",
      "link": "/article.html?slug=...",
      "image": "https://...",
      "category": "AI",
      "type": "markdown",
      "slug": "2025-12-12-ai-productivity",
      "canonical_url": ""
    }
  ]
}
```

---

### 3. `feed/` - WordPress용 피드

**위치**: `/feed/`

**자동 생성 파일**:
```
feed/
├── rss.xml              # RSS 2.0 피드 (최신 20개)
└── full_export.json     # 전체 글 JSON 내보내기
```

**rss.xml**:
- WordPress 자동 가져오기용
- RSS 리더 지원
- 표준 RSS 2.0 포맷

**full_export.json**:
- WordPress REST API 일괄 업로드용
- 전체 글 백업
- 이전 가능한 JSON 포맷

---

## 🔧 빌드 스크립트

### `automation/build_blog.py`

**표준 경로 상수**:
```python
BASE_DIR = Path(__file__).parent.parent.resolve()
CONTENTS_DIR = BASE_DIR / "contents"    # ✅ 표준
DATA_DIR = BASE_DIR / "data"            # ✅ 표준
FEED_DIR = BASE_DIR / "feed"            # ✅ 표준
```

**디렉토리 검증**:
```python
# contents/ 필수 검증 (없으면 에러)
if not CONTENTS_DIR.exists():
    print("❌ ERROR: contents/ directory not found!")
    sys.exit(1)

# data/, feed/ 자동 생성 (없으면 생성)
DATA_DIR.mkdir(parents=True, exist_ok=True)
FEED_DIR.mkdir(parents=True, exist_ok=True)
```

**빌드 프로세스**:
1. `contents/`에서 Markdown 읽기
2. `data/dashboard_summary.json` 생성
3. `data/{category}/page_*.json` 생성
4. `feed/rss.xml` 생성
5. `feed/full_export.json` 생성
6. WordPress 동기화 (선택)

---

## 🚀 GitHub Actions

### `.github/workflows/deploy.yml`

**Trigger 경로**:
```yaml
on:
  push:
    paths:
      - 'contents/**'        # ✅ contents/ 변경 감지
      - 'automation/**'
```

**Artifact 배포**:
```yaml
- name: Commit and push changes
  run: |
    git add data/ feed/ contents/
    git commit -m "🤖 자동 빌드"
    git push origin main
```

**주요 검증**:
1. `contents/` 디렉토리 존재 확인
2. Markdown 파일 존재 확인
3. `data/`, `feed/` 생성 확인
4. `data/dashboard_summary.json` 생성 확인

---

## 🎨 프론트엔드

### `index.html`

**데이터 로드 경로**:
```javascript
// ✅ 표준 경로 (우선순위 1)
fetch('./data/dashboard_summary.json')

// Fallback (하위 호환성)
.catch(() => fetch('./dashboard_summary.json'))
.catch(() => fetch('./data.json'))
```

**카테고리 페이지 로드**:
```javascript
// 카테고리 페이지 데이터
fetch(`./data/${category}/page_${pageNum}.json`)
```

---

## ⚠️ 주의사항

### ❌ 사용 금지

1. **`_posts/` 디렉토리**
   - Jekyll 표준이지만 이 프로젝트에서는 사용 안함
   - 대신 `contents/` 사용

2. **`_includes/` 디렉토리**
   - Jekyll 템플릿 시스템 사용 안함
   - 순수 HTML + JavaScript

3. **루트 경로의 `dashboard_summary.json`**
   - 레거시 호환용으로만 지원
   - 표준은 `data/dashboard_summary.json`

### ✅ 권장사항

1. **Markdown 파일은 `contents/`에만 저장**
2. **Front Matter의 `category` 필드 필수**
3. **빌드 전 `contents/` 존재 확인**
4. **Git에 `data/`, `feed/` 커밋 (자동 생성이지만 배포 필요)**

---

## 🔄 마이그레이션 가이드

### 기존 `_posts/` 사용자

```bash
# 1. contents/ 폴더 생성
mkdir -p contents

# 2. 기존 글 복사
find _posts -name "*.md" -exec cp {} contents/ \;

# 3. Front Matter 확인 (category 필드)
# vi contents/*.md

# 4. 빌드 테스트
python automation/build_blog.py

# 5. 결과 확인
ls -lh data/dashboard_summary.json
ls -lh feed/rss.xml
```

### 기존 OSMU 시스템 사용자

```bash
# build_and_sync.py → build_blog.py 로 교체
python automation/build_blog.py

# 경로 자동 변환 (하위 호환성 유지)
# index.html이 자동으로 data/dashboard_summary.json 로드
```

---

## 📊 카테고리 설정

### `automation/config_blog.json`

```json
{
  "categories": {
    "it": "IT/Tech",
    "ai": "AI",
    "economy": "Economy",
    "life": "Lifestyle",
    "global": "Global"
  }
}
```

### Front Matter 카테고리 매핑

| `category` | 표시명 | `data/` 폴더 |
|------------|--------|--------------|
| `it` | IT/Tech | `data/it/` |
| `ai` | AI | `data/ai/` |
| `economy` | Economy | `data/economy/` |
| `life` | Lifestyle | `data/life/` |
| `global` | Global | `data/global/` |

---

## 🧪 테스트

### 로컬 테스트

```bash
# 1. 빌드 실행
python automation/build_blog.py

# 2. 결과 확인
ls -lh data/dashboard_summary.json
ls -lh data/ai/page_1.json
ls -lh feed/rss.xml
ls -lh feed/full_export.json

# 3. 로컬 서버 실행
python -m http.server 8000

# 4. 브라우저 확인
# http://localhost:8000
```

### CI/CD 테스트

```bash
# GitHub Actions 수동 트리거
# Repository → Actions → "Blog Deploy" → "Run workflow"
```

---

## 📝 요약

| 구분 | Jekyll 표준 | ❌ | 이 프로젝트 | ✅ |
|------|-------------|-----|-------------|-----|
| 원본 Markdown | `_posts/` | ❌ | `contents/` | ✅ |
| UI 데이터 | N/A | - | `data/` | ✅ |
| WordPress 피드 | N/A | - | `feed/` | ✅ |
| 빌드 스크립트 | Jekyll | ❌ | `build_blog.py` | ✅ |
| 프론트엔드 | Liquid | ❌ | JavaScript | ✅ |

---

## 🎯 결론

이 프로젝트는 Jekyll 표준 구조를 따르지 않습니다. 
대신 명확하고 예측 가능한 커스텀 구조를 사용하여 
"경로 에러"와 "빌드 실패"를 원천 차단합니다.

**핵심 3대 원칙**:
1. **`contents/`** - 모든 Markdown 원본
2. **`data/`** - UI용 JSON 출력
3. **`feed/`** - WordPress용 피드

이 구조를 절대적으로 준수하면 시스템이 완벽하게 작동합니다.

---

*Last Updated: 2025-12-13*  
*Version: Standard v1.0.0*
