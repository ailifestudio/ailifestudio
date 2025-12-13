---
title: "OSMU 블로그 시스템에 오신 것을 환영합니다"
date: 2025-12-13
category: it
canonical_url: ""
summary: "표준 디렉토리 구조 기반의 완전 자동화된 블로그 시스템입니다. Markdown으로 글을 작성하면 GitHub Pages와 WordPress에 자동으로 배포됩니다."
image: "https://images.unsplash.com/photo-1504805572947-34fad45aed93?auto=format&fit=crop&w=800&q=80"
tags:
  - OSMU
  - Blog
  - Automation
  - GitHub Pages
---

## 🎉 환영합니다!

**OSMU (One Source Multi Use)** 블로그 시스템에 오신 것을 환영합니다.

이 시스템은 Jekyll이나 다른 정적 사이트 생성기 없이 **순수 Python과 JavaScript**로 구축된 자동화 블로그 플랫폼입니다.

---

## 🏗️ 표준 디렉토리 구조

이 시스템은 명확하고 예측 가능한 디렉토리 구조를 사용합니다:

```
/ (Root)
├── contents/          # 📝 [Input] 원본 Markdown 파일
├── data/              # 📊 [Output] UI용 JSON 데이터
│   ├── dashboard_summary.json
│   └── {category}/page_*.json
└── feed/              # 📡 [Output] WordPress용 피드
    ├── rss.xml
    └── full_export.json
```

---

## ✨ 핵심 기능

### 1️⃣ 간편한 글 작성

Markdown 파일을 `contents/` 폴더에 저장하기만 하면 됩니다.

**Front Matter 예시:**
```yaml
---
title: "글 제목"
date: 2025-12-13
category: ai          # ai, it, economy, life, global
summary: "글 요약"
image: "https://..."
tags:
  - 태그1
  - 태그2
---
```

### 2️⃣ 완전 자동화

Git에 푸시하면 GitHub Actions가 자동으로:
- ✅ Markdown 읽기
- ✅ JSON 데이터 생성
- ✅ RSS 피드 생성
- ✅ GitHub Pages 배포
- ✅ WordPress 동기화 (선택)

### 3️⃣ 초고속 로딩

- **JSON 파일 분할**: 메인 페이지는 최신 50개만 로드
- **카테고리별 페이지네이션**: 20개씩 나누어 로드
- **반응형 디자인**: Tailwind CSS 기반

### 4️⃣ SEO 최적화

- **Canonical URL**: WordPress로 SEO 링크 주스 집중
- **RSS 피드**: WordPress 자동 가져오기
- **Open Graph**: 소셜 미디어 공유 최적화

---

## 🚀 빠른 시작

### 1. 새 글 작성

```bash
# contents/ 폴더에 Markdown 파일 생성
echo '---
title: "나의 첫 글"
date: 2025-12-13
category: it
summary: "첫 글입니다"
image: "https://images.unsplash.com/photo-1..."
---

## 안녕하세요!

첫 글입니다.
' > contents/my-first-post.md
```

### 2. Git 푸시

```bash
git add contents/
git commit -m "✨ 새 글 추가: 나의 첫 글"
git push origin main
```

### 3. 자동 배포 확인

- **GitHub Actions**: Repository → Actions 탭에서 진행 상황 확인
- **웹사이트**: 5-10분 후 사이트 방문하여 확인

---

## 🎨 지원하는 카테고리

| 카테고리 키 | 표시명 | 설명 |
|------------|--------|------|
| `it` | IT/Tech | IT 및 테크놀로지 |
| `ai` | AI | 인공지능 |
| `economy` | Economy | 경제/비즈니스 |
| `life` | Lifestyle | 라이프스타일 |
| `global` | Global | 국제/글로벌 뉴스 |

---

## 🔧 고급 기능

### WordPress 연동

1. **Application Password 생성**
   - WordPress → 사용자 → 프로필
   - "Application Passwords" 섹션

2. **GitHub Secrets 설정**
   - Repository → Settings → Secrets → Actions
   - `WP_URL`, `WP_USERNAME`, `WP_APP_PASSWORD` 추가

3. **자동 동기화 활성화**
   - 글 푸시 시 WordPress에 자동 발행
   - Canonical URL 자동 설정

### 로컬 빌드 테스트

```bash
# 빌드 스크립트 실행
python automation/build_blog.py

# 로컬 서버 실행
python -m http.server 8000

# 브라우저에서 확인
# http://localhost:8000
```

---

## 📚 문서

- **[STANDARD_STRUCTURE.md](../STANDARD_STRUCTURE.md)**: 표준 디렉토리 구조 완벽 가이드
- **[README_OSMU.md](../README_OSMU.md)**: 빠른 시작 가이드
- **[OSMU_GUIDE.md](../OSMU_GUIDE.md)**: 상세 시스템 설명서

---

## 🎯 장점

### ✅ 간편함
- Markdown만 작성
- Git push만 하면 배포 완료
- 복잡한 설정 없음

### ✅ 빠름
- JSON 파일 분할로 초고속 로딩
- GitHub Pages 무료 호스팅
- CDN 자동 적용

### ✅ 안전함
- 표준 디렉토리 구조로 에러 방지
- 자동 검증 시스템
- 안전한 자격 증명 관리

### ✅ 확장 가능
- WordPress 연동
- RSS 피드 제공
- 카테고리 무제한 확장

---

## 💡 팁

### Markdown 작성 팁

1. **Front Matter 필수**: 모든 메타데이터 정확히 입력
2. **이미지 URL**: Unsplash 무료 이미지 활용
3. **요약 작성**: SEO를 위해 150자 이내로 명확하게
4. **태그 선택**: 관련 키워드 3-5개 선택

### Git 관리 팁

1. **자주 커밋**: 작은 단위로 자주 커밋
2. **의미 있는 메시지**: "✨ 새 글: 제목" 형식 사용
3. **푸시 전 확인**: 로컬 빌드 테스트 권장

---

## 🐛 문제 해결

### 빌드 실패 시

```bash
# 1. 디렉토리 구조 확인
ls -la contents/
ls -la data/
ls -la feed/

# 2. Python 패키지 설치
pip install python-frontmatter requests markdown

# 3. 로컬 빌드 테스트
python automation/build_blog.py
```

### 배포 안 될 때

1. **GitHub Actions 확인**: Actions 탭에서 에러 로그 확인
2. **GitHub Pages 설정 확인**: Settings → Pages → Source: main branch
3. **캐시 삭제**: 브라우저에서 Ctrl + Shift + R

---

## 🎊 시작하세요!

이제 `contents/` 폴더에 Markdown 파일을 추가하고 Git에 푸시하기만 하면 됩니다.

**자동으로:**
- ✅ JSON 데이터 생성
- ✅ RSS 피드 생성
- ✅ GitHub Pages 배포
- ✅ WordPress 동기화 (설정 시)

**Happy Blogging! 🚀**

---

*이 글은 OSMU 시스템의 첫 번째 예시 포스트입니다.*  
*자유롭게 수정하거나 삭제하세요!*
