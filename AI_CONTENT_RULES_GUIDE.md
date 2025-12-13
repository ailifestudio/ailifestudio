# 📝 AI 콘텐츠 생성 규칙 가이드

## ✅ 최종 수정 완료 (2025-12-13)

### 🎯 핵심 변경사항
**기존 문제:**
- Rule 5에서 `<pre>` 태그를 허용 목록에 명시하지 않음
- Rule 7-8에서 `<pre>` 사용 지침이 모호함
- "스타일 박스를 사용하라"와 "pre 태그 사용" 지침이 충돌

**해결 방안:**
- ✅ Rule 5: `<pre>`, `<br>` 태그를 허용 목록에 명시적 추가
- ✅ Rule 7: 일반 팁용 `<p>` 스타일 박스 (💡 TIP)
- ✅ Rule 8: 코드/명령어/프롬프트는 `<pre>` 태그 필수 사용
- ✅ Rule 9: 경고용 `<p>` 스타일 박스 추가 (⚠️ 주의)

---

## 📋 AI 콘텐츠 생성 규칙 (최종본)

### Rule 0: 제목 및 강조
- 제목은 반드시 `<h2>` 태그 사용
- 중요 키워드는 `<strong>` 또는 `<mark>`로 강조

### Rule 1: 인사말 생략
- 인사말 없이 글 바로 시작

### Rule 2: 최소 길이
- 1500자 이상 작성

### Rule 3: 구성
```
- 제목 (<h2>)
- 서문 2-3문단 (<p>)
- 본문 4~6개 섹션 (<h3> 제목 + <p> 설명 또는 <ul><li> 리스트)
- 실무 활용 예시
- 주의사항 또는 한계점
- 정리 요약
```

### Rule 4: 이미지 키워드
- 각 큰 섹션마다 이미지 키워드 1줄 삽입
- 형식: `[IMAGE:설명]`
- 예시: `[IMAGE:ChatGPT interface showing conversation]`
- ⚠️ **반드시 영어로 구체적으로 작성**

### Rule 5: 허용 HTML 태그 ⭐
```html
<h2>, <h3>, <p>, <ul>, <li>, <strong>, <mark>, <pre>, <br>
```
**중요:** `<pre>` 태그가 명시적으로 허용됨!

### Rule 6: 강조 표현
- 중요 문장은 `<strong>` 또는 `<mark>`로 강조

### Rule 7: 일반 팁 박스 (💡 TIP)
```html
<p style="border-left:4px solid #3b82f6; background:#f0f9ff; padding:15px; border-radius:4px; margin:15px 0;">
<strong>💡 TIP:</strong> 내용
</p>
```
**사용 예:**
- 실무 팁
- 추천 사항
- 참고 정보

### Rule 8: 코드/명령어/프롬프트 예시 ⭐
```html
<pre style="background:#1e293b; color:#e2e8f0; padding:15px; border-radius:8px; white-space:pre-wrap; word-wrap:break-word; line-height:1.6; border:1px solid #334155; margin:15px 0;">
코드나 명령어 또는 프롬프트 예시
(여러 줄 가능, 자동 줄바꿈 적용됨)
</pre>
```
**사용 예:**
- Python/JavaScript 코드
- CLI 명령어
- AI 프롬프트 예시
- JSON/YAML 설정 파일

**스타일 특징:**
- ✅ 어두운 배경 (#1e293b)
- ✅ 밝은 텍스트 색상 (#e2e8f0)
- ✅ 자동 줄바꿈 (`white-space: pre-wrap`)
- ✅ 가로 스크롤 없음 (`word-wrap: break-word`)
- ✅ 가독성 좋은 줄간격 (`line-height: 1.6`)

### Rule 9: 경고/주의사항 박스 (⚠️ 주의)
```html
<p style="border-left:4px solid #ef4444; background:#fef2f2; padding:15px; border-radius:4px; margin:15px 0;">
<strong>⚠️ 주의:</strong> 내용
</p>
```
**사용 예:**
- 보안 주의사항
- 데이터 손실 위험
- 사용 제약 사항
- API 사용량 제한

---

## 🎨 스타일 박스 종류별 사용 가이드

### 1️⃣ 💡 TIP 박스 (파란색)
**용도:** 실무 팁, 추천 사항
**배경:** 밝은 파란색 (#f0f9ff)
**테두리:** 파란색 (#3b82f6)

### 2️⃣ 🖥️ CODE 박스 (어두운 회색)
**용도:** 코드, 명령어, 프롬프트
**배경:** 어두운 회색 (#1e293b)
**텍스트:** 밝은 회색 (#e2e8f0)
**태그:** `<pre>` 필수

### 3️⃣ ⚠️ WARNING 박스 (빨간색)
**용도:** 경고, 주의사항
**배경:** 밝은 빨간색 (#fef2f2)
**테두리:** 빨간색 (#ef4444)

---

## 💡 실전 예시

### ✅ 올바른 사용 예시

#### 1. 일반 팁
```html
<p style="border-left:4px solid #3b82f6; background:#f0f9ff; padding:15px; border-radius:4px; margin:15px 0;">
<strong>💡 TIP:</strong> ChatGPT 프롬프트를 작성할 때는 구체적인 역할과 맥락을 먼저 제공하면 더 정확한 답변을 받을 수 있습니다.
</p>
```

#### 2. 프롬프트 예시
```html
<pre style="background:#1e293b; color:#e2e8f0; padding:15px; border-radius:8px; white-space:pre-wrap; word-wrap:break-word; line-height:1.6; border:1px solid #334155; margin:15px 0;">
너는 10년 경력의 마케팅 전문가야.
다음 제품의 SNS 광고 문구 3개를 작성해줘:
- 제품: AI 기반 이메일 자동 정리 서비스
- 타겟: 30-40대 직장인
- 톤앤매너: 친근하고 실용적
</pre>
```

#### 3. 경고
```html
<p style="border-left:4px solid #ef4444; background:#fef2f2; padding:15px; border-radius:4px; margin:15px 0;">
<strong>⚠️ 주의:</strong> API 키는 절대 GitHub 공개 저장소에 직접 커밋하지 마세요. 반드시 GitHub Secrets를 사용하세요.
</p>
```

### ❌ 잘못된 사용 예시

#### 1. `<pre>` 태그에 스타일 누락
```html
<!-- ❌ 스타일 없음 - 가독성 떨어짐 -->
<pre>
코드 예시
</pre>
```

#### 2. 코드를 `<p>` 태그로 표현
```html
<!-- ❌ 코드는 반드시 <pre> 사용 -->
<p>
print("Hello, World!")
</p>
```

#### 3. 허용되지 않은 태그 사용
```html
<!-- ❌ <div>, <span> 등 허용되지 않은 태그 -->
<div class="tip-box">
팁 내용
</div>
```

---

## 🔧 CSS 설정 (article.html)

### `.article-content pre` 스타일
```css
.article-content pre {
    background: #1e293b;
    color: #e2e8f0;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #334155;
    overflow: visible;
    white-space: pre-wrap;
    word-wrap: break-word;
    line-height: 1.6;
    max-width: 100%;
    font-family: 'Courier New', monospace;
    font-size: 0.95em;
    margin: 15px 0;
}
```

**특징:**
- ✅ 가로 스크롤 없음 (`overflow: visible`)
- ✅ 자동 줄바꿈 (`white-space: pre-wrap`)
- ✅ 긴 단어 줄바꿈 (`word-wrap: break-word`)
- ✅ 반응형 디자인 (`max-width: 100%`)

---

## 📊 규칙 요약표

| 규칙 | 용도 | 태그 | 스타일 필수 | 배경색 |
|------|------|------|------------|--------|
| Rule 7 | 일반 팁 | `<p>` | ✅ | 파란색 (#f0f9ff) |
| Rule 8 | 코드/명령어 | `<pre>` | ✅ | 어두운 회색 (#1e293b) |
| Rule 9 | 경고/주의 | `<p>` | ✅ | 빨간색 (#fef2f2) |

---

## 🚀 다음 워크플로우 실행 시 기대 결과

### 1️⃣ 생성되는 콘텐츠 형식
```html
<h2>나만의 AI 비서로 일상/업무 효율 높이는 시간 절약 실전법</h2>

[IMAGE:AI assistant interface on smartphone]

<p>서문 내용...</p>

<h3>1. ChatGPT 활용 팁</h3>
<p>본문 내용...</p>

<p style="border-left:4px solid #3b82f6; background:#f0f9ff; padding:15px; border-radius:4px; margin:15px 0;">
<strong>💡 TIP:</strong> 구체적인 역할을 부여하면 더 정확한 답변을 받을 수 있습니다.
</p>

<pre style="background:#1e293b; color:#e2e8f0; padding:15px; border-radius:8px; white-space:pre-wrap; word-wrap:break-word; line-height:1.6; border:1px solid #334155; margin:15px 0;">
너는 10년 경력의 마케팅 전문가야.
제품 설명서를 1페이지로 요약해줘.
</pre>

<p style="border-left:4px solid #ef4444; background:#fef2f2; padding:15px; border-radius:4px; margin:15px 0;">
<strong>⚠️ 주의:</strong> 개인정보는 AI에게 입력하지 마세요.
</p>
```

### 2️⃣ 사용자 경험 개선
- ✅ 코드 예시가 명확하게 표시됨
- ✅ 가로 스크롤이 없어 모바일에서도 읽기 편함
- ✅ 팁/경고가 시각적으로 구분됨
- ✅ 일관된 디자인 시스템 적용

---

## ✅ 최종 체크리스트

### 완료된 항목
- [x] Rule 5에 `<pre>`, `<br>` 태그 추가
- [x] Rule 7: 일반 팁 박스 스타일 정의
- [x] Rule 8: 코드/프롬프트용 `<pre>` 태그 명시
- [x] Rule 9: 경고 박스 스타일 추가
- [x] 모든 스타일 박스에 `margin: 15px 0` 추가
- [x] `article.html` CSS에서 `pre` 태그 스타일 최적화
- [x] `ai_content_generator.py` 프롬프트 규칙 개선
- [x] GitHub에 커밋 및 푸시 완료

### 다음 실행 시 확인 사항
1. **GitHub Actions 워크플로우 실행**
   - URL: `https://github.com/ailifestudio/ailifestudio.github.io/actions`
   - 워크플로우: "Auto Update Blog with AI"

2. **생성된 콘텐츠 확인**
   - `<pre>` 태그가 올바른 스타일로 적용되었는지
   - 팁 박스/경고 박스가 올바르게 표시되는지
   - 가로 스크롤 없이 모든 내용이 보이는지

3. **라이브 사이트 확인**
   - 메인: `https://ailifestudio.github.io`
   - 최신 AI 게시글: `https://ailifestudio.github.io/article.html?slug=...`

---

## 📝 주요 개선 사항 요약

### Before (수정 전)
```
문제점:
1. Rule 5에서 <pre> 태그가 허용 목록에 없음
2. "스타일 박스 사용" vs "<pre> 태그 사용" 충돌
3. AI 모델이 어떤 태그를 사용해야 할지 혼란
```

### After (수정 후)
```
해결:
1. <pre> 태그를 허용 목록에 명시적 추가
2. 용도별 명확한 가이드라인:
   - 일반 팁 → <p> 스타일 박스
   - 코드/프롬프트 → <pre> 태그
   - 경고 → <p> 스타일 박스
3. 각 규칙에 구체적인 HTML 예시 제공
```

---

## 🎉 결론

**이제 AI 콘텐츠 생성 프롬프트가 명확하고 일관성 있게 정리되었습니다!**

- ✅ `<pre>` 태그 사용 지침이 명확함
- ✅ 용도별 스타일 박스 구분이 명확함
- ✅ 허용 태그 목록에 모든 필요한 태그 포함
- ✅ 가로 스크롤 없이 모든 기기에서 잘 보임
- ✅ 일관된 디자인 시스템 적용

**다음 워크플로우 실행 시 개선된 콘텐츠를 확인하세요!** 🚀
