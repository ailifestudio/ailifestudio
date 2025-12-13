# 🚀 OSMU 시스템 빠른 시작 가이드

## 📋 목차
- [시스템 개요](#시스템-개요)
- [적용 순서](#적용-순서)
- [첫 글 작성](#첫-글-작성)
- [자동 배포](#자동-배포)
- [문제 해결](#문제-해결)

---

## 시스템 개요

### 표준 디렉토리 구조

```
/ (Root)
├── contents/                # 📝 원본 Markdown (여기에 글 작성!)
│   ├── welcome.md
│   └── my-post.md
├── data/                    # 📊 자동 생성 (UI용 JSON)
│   ├── dashboard_summary.json
│   └── {category}/page_*.json
├── feed/                    # 📡 자동 생성 (WordPress용)
│   ├── rss.xml
│   └── full_export.json
├── automation/
│   └── build_blog.py        # 🔧 빌드 스크립트
└── index.html               # 🎨 프론트엔드
```

### 핵심 원칙

1. **`contents/`에만 글 작성** - Jekyll의 `_posts/` 사용 안함
2. **`data/`, `feed/`는 자동 생성** - 직접 수정 불필요
3. **Git push만 하면 배포 완료** - GitHub Actions 자동 실행

---

## 적용 순서

### 1️⃣ 파일 확인

현재 프로젝트에 다음 파일들이 있는지 확인:

```bash
# 필수 파일
├── contents/                # ✅ 있음
├── automation/build_blog.py # ✅ 있음
└── index.html               # ✅ 있음

# 자동 생성 파일 (없어도 자동 생성됨)
├── data/                    # 빌드 시 생성
└── feed/                    # 빌드 시 생성
```

### 2️⃣ GitHub Actions 워크플로우 설정

**⚠️ 중요**: GitHub App 권한 제한으로 워크플로우는 웹에서 직접 생성해야 합니다.

#### 방법 A: GitHub 웹사이트에서 생성 (권장)

1. **GitHub 저장소 접속**
   ```
   https://github.com/ailifestudio/ailifestudio.github.io
   ```

2. **새 파일 생성**
   - 파일 경로: `.github/workflows/deploy.yml`
   - "Add file" → "Create new file" 클릭

3. **내용 복사**
   - 저장소의 `deploy-workflow-final.yml` 내용을 복사
   - 또는 아래 "워크플로우 전체 코드" 참조

4. **Commit**
   - Commit message: `🚀 Add deploy workflow`
   - "Commit new file" 클릭

#### 방법 B: 로컬에서 생성 후 웹에서 병합

```bash
# 로컬에서 파일 생성
cp deploy-workflow-final.yml .github/workflows/deploy.yml

# 커밋 (푸시는 실패할 수 있음)
git add .github/workflows/deploy.yml
git commit -m "🚀 Add deploy workflow"

# 푸시 시도 (실패하면 웹에서 수동 생성)
git push origin main
```

### 3️⃣ Workflow Permissions 설정

1. **Settings → Actions → General**
2. **"Workflow permissions" 섹션**
3. ✅ **"Read and write permissions" 선택**
4. **Save**

이 설정이 없으면 워크플로우가 `data/`, `feed/`를 커밋할 수 없습니다.

---

## 첫 글 작성

### 방법 1: 기존 예시 수정

```bash
# welcome.md 파일 수정
vi contents/welcome.md

# 또는 새 파일 생성
vi contents/my-first-post.md
```

### 방법 2: 템플릿 사용

```bash
cat > contents/my-post.md << 'EOF'
---
title: "나의 첫 블로그 글"
date: 2025-12-13
category: it
canonical_url: ""
summary: "OSMU 시스템으로 작성하는 첫 번째 글입니다."
image: "https://images.unsplash.com/photo-1504805572947-34fad45aed93?auto=format&fit=crop&w=800&q=80"
tags:
  - Blog
  - Tutorial
---

## 안녕하세요!

이것은 나의 첫 번째 블로그 글입니다.

### 소제목

Markdown으로 자유롭게 작성할 수 있습니다.

- 리스트 항목 1
- 리스트 항목 2

**굵은 글씨** *기울임* `코드`

EOF
```

### Front Matter 필드 설명

| 필드 | 필수 | 설명 | 예시 |
|------|:----:|------|------|
| `title` | ✅ | 글 제목 | "나의 첫 글" |
| `date` | ✅ | 작성 날짜 (YYYY-MM-DD) | `2025-12-13` |
| `category` | ✅ | 카테고리 | `it`, `ai`, `economy`, `life`, `global` |
| `canonical_url` | ✅ | WordPress URL (자동) | 초기값 `""` |
| `summary` | ✅ | 요약 (150자 이내) | "글 요약..." |
| `image` | ✅ | 대표 이미지 URL | "https://..." |
| `tags` | ⬜ | 태그 배열 | `["Tag1", "Tag2"]` |

---

## 자동 배포

### 1️⃣ 로컬 테스트 (선택)

```bash
# 빌드 테스트
python automation/build_blog.py

# 결과 확인
ls -lh data/dashboard_summary.json
ls -lh feed/rss.xml

# 로컬 서버 실행
python -m http.server 8000
# http://localhost:8000
```

### 2️⃣ Git 커밋 & 푸시

```bash
# 변경사항 확인
git status

# contents/ 파일 추가
git add contents/

# 커밋
git commit -m "✨ 새 글 추가: 나의 첫 글"

# 푸시 (자동 배포 시작!)
git push origin main
```

### 3️⃣ 배포 진행 확인

1. **GitHub Actions 확인**
   ```
   https://github.com/ailifestudio/ailifestudio.github.io/actions
   ```
   - "Deploy OSMU System" 워크플로우 클릭
   - 실시간 로그 확인

2. **예상 실행 시간**
   - 빌드: 30초 ~ 1분
   - 배포: 5 ~ 10분

3. **성공 확인**
   - ✅ 초록색 체크마크
   - 📊 "Deployment Summary" 로그 확인

### 4️⃣ 웹사이트 확인

```
https://ailifestudio.github.io/
```

- 새 글이 대시보드에 표시되는지 확인
- 카테고리 필터 작동 확인
- 글 상세 페이지 확인

---

## 문제 해결

### 문제 1: `contents/` 디렉토리가 없다고 나옴

**증상:**
```
❌ ERROR: contents/ directory missing!
```

**해결:**
```bash
# contents/ 폴더 생성
mkdir -p contents

# 예시 글 추가
cp welcome.md contents/

# 커밋 & 푸시
git add contents/
git commit -m "📁 Add contents directory"
git push origin main
```

### 문제 2: 워크플로우가 실행되지 않음

**원인:**
- `.github/workflows/deploy.yml` 파일이 없음
- Workflow permissions 설정 안 됨

**해결:**
1. 워크플로우 파일 존재 확인:
   ```bash
   ls -la .github/workflows/deploy.yml
   ```

2. Workflow permissions 확인:
   - Settings → Actions → General
   - "Read and write permissions" 선택

### 문제 3: 빌드는 성공했지만 사이트가 업데이트 안 됨

**원인:**
- GitHub Pages 배포 시간 지연 (5-10분)
- 브라우저 캐시

**해결:**
1. 5-10분 대기
2. 브라우저 캐시 삭제:
   ```
   Ctrl + Shift + R (Windows/Linux)
   Cmd + Shift + R (Mac)
   ```
3. GitHub Pages 설정 확인:
   - Settings → Pages
   - Source: "Deploy from a branch" (main)

### 문제 4: Python 패키지 에러

**증상:**
```
ModuleNotFoundError: No module named 'frontmatter'
```

**해결:**
```bash
# 로컬 환경
pip install python-frontmatter requests markdown

# GitHub Actions (자동 설치됨)
# deploy.yml에 이미 포함되어 있음
```

### 문제 5: data/ 또는 feed/ 폴더가 생성 안 됨

**원인:**
- 빌드 스크립트 실행 안 됨
- contents/ 폴더에 Markdown 파일 없음

**해결:**
```bash
# 1. Markdown 파일 확인
ls -la contents/*.md

# 2. 수동 빌드 실행
python automation/build_blog.py

# 3. 결과 확인
ls -lh data/
ls -lh feed/
```

---

## 자주 묻는 질문 (FAQ)

### Q1: 기존 `_posts/` 폴더의 글은 어떻게 하나요?

**A:** 모두 `contents/`로 이동하세요:

```bash
# 모든 Markdown 파일 복사
find _posts -name "*.md" -exec cp {} contents/ \;

# Front Matter 확인 (category 필드 필수)
# vi contents/*.md

# 커밋 & 푸시
git add contents/
git commit -m "📦 Migrate posts to contents/"
git push origin main
```

### Q2: 카테고리를 추가하려면?

**A:** `automation/config_blog.json` 수정:

```json
{
  "categories": {
    "it": "IT/Tech",
    "ai": "AI",
    "new-category": "새 카테고리"  // 추가
  }
}
```

그리고 `index.html`의 카테고리 버튼 목록도 업데이트:

```javascript
const categories = ['전체', 'IT/Tech', 'AI', '새 카테고리'];
```

### Q3: WordPress 연동은 어떻게 하나요?

**A:** GitHub Secrets 설정:

1. WordPress → 사용자 → 프로필
2. "Application Passwords" 생성
3. GitHub → Settings → Secrets → Actions
4. 3개의 Secret 추가:
   - `WP_URL`: `https://your-wordpress-site.com`
   - `WP_USERNAME`: `your_username`
   - `WP_APP_PASSWORD`: `생성된 비밀번호`

### Q4: 로컬에서만 테스트하려면?

**A:** 빌드 스크립트만 실행:

```bash
# 빌드 실행
python automation/build_blog.py

# 로컬 서버
python -m http.server 8000

# 브라우저
# http://localhost:8000
```

Git push 하지 않으면 GitHub Pages에 배포되지 않습니다.

---

## 체크리스트

### 초기 설정

- [ ] `contents/` 폴더 존재 확인
- [ ] `.github/workflows/deploy.yml` 생성
- [ ] Workflow permissions 설정 (Read and write)
- [ ] GitHub Pages 활성화 (main 브랜치)

### 글 작성

- [ ] `contents/`에 Markdown 파일 생성
- [ ] Front Matter 필수 필드 모두 채우기
- [ ] 이미지 URL 유효성 확인
- [ ] 로컬 빌드 테스트 (선택)

### 배포

- [ ] `git add contents/`
- [ ] `git commit -m "메시지"`
- [ ] `git push origin main`
- [ ] GitHub Actions 성공 확인
- [ ] 웹사이트에서 글 확인

---

## 다음 단계

### 일상적인 사용

```bash
# 1. 새 글 작성
vi contents/2025-12-13-my-post.md

# 2. 커밋 & 푸시
git add contents/
git commit -m "✨ 새 글: 제목"
git push origin main

# 3. 자동 배포 대기 (5-10분)
```

### 고급 기능

- **WordPress 연동**: Secrets 설정으로 자동 동기화
- **RSS 피드**: `feed/rss.xml`을 RSS 리더에 등록
- **카테고리 확장**: 원하는 만큼 카테고리 추가
- **디자인 커스터마이징**: `index.html` 수정

---

## 참고 문서

- **[STANDARD_STRUCTURE.md](STANDARD_STRUCTURE.md)**: 표준 디렉토리 구조 상세 가이드
- **[README_OSMU.md](README_OSMU.md)**: OSMU 시스템 전체 개요
- **[OSMU_GUIDE.md](OSMU_GUIDE.md)**: 고급 기능 및 커스터마이징

---

## 지원

### 문제가 해결되지 않을 때

1. **GitHub Actions 로그 확인**: 상세한 에러 메시지 확인
2. **로컬 빌드 테스트**: `python automation/build_blog.py`
3. **디렉토리 구조 확인**: `ls -la contents/ data/ feed/`
4. **GitHub Issues**: 버그 리포트

---

**🎉 축하합니다!**

OSMU 시스템이 준비되었습니다. 이제 `contents/`에 Markdown 파일만 추가하면 자동으로 배포됩니다.

**Happy Blogging! 🚀**

---

*Last Updated: 2025-12-13*  
*Version: Final v1.0.0*
