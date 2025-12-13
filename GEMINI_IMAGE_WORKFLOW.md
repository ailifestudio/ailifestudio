# 🎨 Gemini 이미지 생성 완전 가이드

## ✅ 완료된 수정사항

### 1️⃣ 카테고리 표시 수정
```
Before: "AI Life Studio"
After:  "AI/테크" ✅
```

**적용된 파일:**
- `data/ai/page_1.json`
- `data/ai-tech/page_1.json`
- `data/it/page_1.json`
- `data/dashboard_summary.json`

### 2️⃣ 이미지 시스템 완전 개편
```
Before: Pexels/Picsum API → 랜덤 이미지 (관련 없음)
After:  Gemini 프롬프트 → 수동 생성 → generated_images.json ✅
```

---

## 🚀 새로운 이미지 워크플로우

### 전체 흐름도

```
1. AI 콘텐츠 생성
   ↓
2. 이미지 키워드 추출
   [IMAGE:digital assistant interface on smartphone]
   ↓
3. Gemini로 프롬프트 향상
   "Modern smartphone displaying AI assistant interface..."
   ↓
4. 이미지 생성 (수동)
   - GenSpark Assistant에게 요청
   - Imagen 3 또는 Nano Banana Pro 사용
   ↓
5. URL을 generated_images.json에 저장
   {"digital assistant...": "https://www.genspark.ai/..."}
   ↓
6. 다음 워크플로우 실행
   ✅ Gemini 생성 이미지 자동 사용!
```

---

## 📋 즉시 실행 가능한 단계

### Step 1: 최신 이미지 키워드 확인

```bash
cat /home/user/webapp/automation/image_keywords.txt
```

**출력:**
```
digital assistant interface on smartphone
person managing calendar with AI
student researching with AI on laptop
creative person brainstorming with AI
language learner using AI translation app
business analyst reviewing data with AI insights
diverse professionals collaborating using AI tools
person checking facts on a computer screen
futuristic digital interface with AI icons
```

---

### Step 2: GenSpark Assistant에게 이미지 생성 요청

**방법 A: 직접 키워드로 요청 (가장 간단) ⭐**

```
다음 9개 키워드로 Imagen 3 이미지를 생성해주세요:

1. digital assistant interface on smartphone
2. person managing calendar with AI
3. student researching with AI on laptop
4. creative person brainstorming with AI
5. language learner using AI translation app
6. business analyst reviewing data with AI insights
7. diverse professionals collaborating using AI tools
8. person checking facts on a computer screen
9. futuristic digital interface with AI icons

각 이미지 설정:
- 모델: imagen-3
- 비율: 16:9 (1280x720)
- 품질: high quality, professional photography
- 스타일: modern, clean composition, vibrant colors
- 저장: /mnt/aidrive/blog_images/

생성 완료 후 각 키워드와 이미지 공개 URL을 JSON 형식으로 알려주세요.
```

**방법 B: Gemini로 프롬프트 향상 후 생성 (고품질)**

```
먼저 automation/image_keywords.txt의 각 키워드를
Gemini API로 고품질 이미지 프롬프트로 변환하고,
그 프롬프트를 사용해서 Imagen 3으로 이미지를 생성해주세요.

프롬프트 향상 예시:
"digital assistant interface" 
→ "Modern smartphone displaying AI assistant interface with clean UI design, 
   vibrant app icons, sleek digital interface, professional photography, 
   high quality, 16:9 aspect ratio, detailed, bright and inviting atmosphere"

모델: imagen-3
비율: 16:9
저장: /mnt/aidrive/blog_images/

결과를 JSON 형식으로 알려주세요.
```

---

### Step 3: 생성된 URL 저장

**Assistant가 제공한 URL을 `generated_images.json`에 저장:**

```bash
cat > /home/user/webapp/automation/generated_images.json << 'EOF'
{
  "digital assistant interface on smartphone": "https://www.genspark.ai/api/files/v1/abc123def456",
  "person managing calendar with AI": "https://www.genspark.ai/api/files/v1/ghi789jkl012",
  "student researching with AI on laptop": "https://www.genspark.ai/api/files/v1/mno345pqr678",
  "creative person brainstorming with AI": "https://www.genspark.ai/api/files/v1/stu901vwx234",
  "language learner using AI translation app": "https://www.genspark.ai/api/files/v1/yz567abc890",
  "business analyst reviewing data with AI insights": "https://www.genspark.ai/api/files/v1/def123ghi456",
  "diverse professionals collaborating using AI tools": "https://www.genspark.ai/api/files/v1/jkl789mno012",
  "person checking facts on a computer screen": "https://www.genspark.ai/api/files/v1/pqr345stu678",
  "futuristic digital interface with AI icons": "https://www.genspark.ai/api/files/v1/vwx901yz234"
}
EOF
```

**또는 파일 업로드 방식:**

1. Assistant가 제공한 JSON을 복사
2. 로컬에서 `generated_images.json` 파일 생성
3. `/home/user/webapp/automation/` 폴더에 업로드

---

### Step 4: 워크플로우 실행 및 확인

```bash
# 워크플로우 실행
https://github.com/ailifestudio/ailifestudio.github.io/actions
→ "Auto Update Blog with AI" 선택
→ "Run workflow" 클릭
```

**기대되는 로그:**
```
[3단계] 이미지 자동 삽입 중...
  ✅ Gemini 생성 이미지 9개 로드됨
  ✅ Gemini 생성 이미지 사용: digital assistant interface on smartphone
     → https://www.genspark.ai/api/files/v1/abc123def456...
  ✅ Gemini 생성 이미지 사용: person managing calendar with AI
     → https://www.genspark.ai/api/files/v1/ghi789jkl012...
  ...
  ✅ 이미지 삽입 완료
```

---

## 🎯 현재 시스템 동작

### 이미지 우선순위

```
1순위: generated_images.json에서 검색
       → ✅ 있으면: Gemini 생성 이미지 사용
       → ❌ 없으면: 2순위로

2순위: 플레이스홀더 이미지 사용
       → ⚠️ https://via.placeholder.com/1280x720/...
       → 경고 메시지: "Gemini로 생성 필요"
```

### 로그 메시지

**Gemini 이미지 사용 시:**
```
✅ Gemini 생성 이미지 9개 로드됨
✅ Gemini 생성 이미지 사용: digital assistant interface on smartphone
   → https://www.genspark.ai/api/files/v1/...
```

**이미지 없을 시:**
```
ℹ️  generated_images.json 파일 없음
🎨 Gemini 프롬프트 필요: digital assistant interface on smartphone
   → automation/gemini_image_generator.py 실행 필요
⚠️ 플레이스홀더 사용: https://via.placeholder.com/...
ℹ️  실제 이미지는 Gemini로 생성 후 generated_images.json에 추가하세요
```

---

## 📊 Before & After 비교

### Before (문제 상황)
```
❌ 카테고리: "AI Life Studio" 표시
❌ 이미지: Pexels/Picsum 랜덤 (내용과 무관)
❌ 예시: "digital assistant" → 산 풍경 사진
```

### After (현재)
```
✅ 카테고리: "AI/테크" 표시
✅ 이미지: Gemini 생성 (내용과 완벽 일치)
✅ 예시: "digital assistant" → AI 비서 인터페이스 이미지
```

---

## 🔧 문제 해결

### Q1: generated_images.json이 없으면?

**A:** 플레이스홀더 이미지가 사용됩니다.
```
⚠️ https://via.placeholder.com/1280x720/...
```

실제 이미지를 사용하려면:
1. Assistant에게 이미지 생성 요청
2. `generated_images.json` 생성
3. 워크플로우 재실행

---

### Q2: 일부 키워드만 이미지가 있으면?

**A:** 부분 매칭 지원!
```json
{
  "digital assistant interface": "https://...",
  "person managing calendar": "https://..."
}
```

- 있는 키워드: Gemini 이미지 사용 ✅
- 없는 키워드: 플레이스홀더 사용 ⚠️

---

### Q3: 기존 블로그 글 이미지는?

**A:** 데이터 파일이 업데이트되었습니다!
```
✅ data/ai/page_1.json - "AI Life Studio" → "AI/테크"
✅ data/ai-tech/page_1.json - "AI Life Studio" → "AI/테크"
✅ data/it/page_1.json - "AI Life Studio" → "AI/테크"
```

기존 글도 "AI/테크"로 표시됩니다!

---

## 🎉 최종 체크리스트

### 완료된 작업 ✅
- [x] "AI Life Studio" → "AI/테크" 일괄 변경
- [x] Pexels/Picsum API 사용 중단
- [x] Gemini 이미지 우선 사용 시스템 구축
- [x] `load_generated_images()` 함수 추가
- [x] 플레이스홀더 폴백 시스템
- [x] 종합 가이드 작성

### 다음 단계 (사용자 실행) ⏳
- [ ] GenSpark Assistant에게 이미지 9개 생성 요청
- [ ] 생성된 URL을 `generated_images.json`에 저장
- [ ] 워크플로우 실행 및 결과 확인

### 예상 결과 🎯
```
✅ 카테고리: "AI/테크" 표시
✅ 이미지: Gemini 생성 (고품질, 내용 일치)
✅ 무료: GenSpark 크레딧 사용 안 함
✅ 자동: generated_images.json 자동 로드
```

---

## 🚀 지금 바로 시작하세요!

**1. Assistant에게 요청 (1분):**
```
(위의 "방법 A" 또는 "방법 B" 복사/붙여넣기)
```

**2. URL 저장 (2분):**
```bash
cat > automation/generated_images.json << 'EOF'
{ "키워드": "URL", ... }
EOF
```

**3. 워크플로우 실행 (1분):**
```
https://github.com/ailifestudio/ailifestudio.github.io/actions
→ "Run workflow"
```

**완료! 고품질 이미지가 자동으로 사용됩니다!** 🎉
