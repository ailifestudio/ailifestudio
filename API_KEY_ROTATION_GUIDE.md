# 🔄 API 키 로테이션 가이드

> **할당량 초과 시 자동으로 다음 키로 전환**

---

## 🎯 **문제 상황**

### **Gemini API 무료 할당량:**
- ❌ 월 15-60회 제한
- ❌ 분당 15회 제한
- ❌ 프로젝트당 할당량 적용

### **기존 문제:**
```
Quota exceeded for metric 'generate-content-free-tier-requests', limit: 30
→ 워크플로우 실패
```

---

## ✅ **해결책: API 키 로테이션**

여러 Google 계정으로 여러 프로젝트를 만들고, **API 키를 순환 사용**

---

## 📋 **설정 방법**

### **Step 1: 여러 API 키 발급**

#### **계정 1:**
```
https://aistudio.google.com/app/apikey
→ API 키 생성: AIzaSyC...key1
```

#### **계정 2:**
```
https://aistudio.google.com/app/apikey
→ API 키 생성: AIzaSyC...key2
```

#### **계정 3:**
```
https://aistudio.google.com/app/apikey
→ API 키 생성: AIzaSyC...key3
```

**팁:** 
- Gmail 계정을 여러 개 만들거나
- Google Workspace 계정 활용
- 가족/친구 계정 활용 (동의 하에)

---

### **Step 2: GitHub Secrets 설정**

#### **방법 A: 복수 키 (JSON 배열) - 추천**

```
https://github.com/ailifestudio/ailifestudio.github.io/settings/secrets/actions
```

**Secret 추가:**
- **Name**: `GEMINI_API_KEYS` (복수형 주의!)
- **Value** (JSON 배열 형식):
```json
["AIzaSyC...key1", "AIzaSyC...key2", "AIzaSyC...key3"]
```

**주의:** 
- 반드시 JSON 배열 형식 (`["key1", "key2"]`)
- 큰따옴표 사용
- 쉼표로 구분

---

#### **방법 B: 단일 키 (기존 방식)**

기존 `GEMINI_API_KEY` Secret 유지 가능:
- **Name**: `GEMINI_API_KEY`
- **Value**: `AIzaSyC...key1`

---

### **Step 3: 워크플로우 업데이트**

#### **현재 워크플로우:** `.github/workflows/auto-update-ai.yml`

```yaml
- name: 🤖 블로그 자동 업데이트 (AI + RSS)
  env:
    GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
    GEMINI_API_KEYS: ${{ secrets.GEMINI_API_KEYS }}  # 추가!
  run: |
    cd automation
    python blog_automation.py --rss-config config_korean.json
```

**이미 코드에 반영되어 있습니다!** ✅

---

## 🔄 **작동 원리**

### **1. 초기화**
```python
# 복수 키 우선
GEMINI_API_KEYS='["key1", "key2", "key3"]'

# 없으면 단일 키 사용
GEMINI_API_KEY='key1'
```

### **2. 자동 전환**
```
Key #1 시도 → 할당량 초과
    ↓
Key #2로 전환 → 성공! ✅
```

### **3. 에러 감지**
```python
if 'quota' in error_msg or 'limit' in error_msg:
    # 다음 키로 전환
    rotate_to_next_key()
```

---

## 📊 **예상 효과**

### **단일 키:**
- 월 15-60회 → **약 2회/일**

### **3개 키 로테이션:**
- 월 45-180회 → **약 6회/일**

### **5개 키 로테이션:**
- 월 75-300회 → **약 10회/일**

---

## 🧪 **테스트 방법**

### **로컬 테스트:**
```bash
cd /home/user/webapp/automation

# 환경변수 설정
export GEMINI_API_KEYS='["key1", "key2", "key3"]'

# 테스트 실행
python -c "
from ai_content_generator import AIContentGenerator
gen = AIContentGenerator('config_ai.json')
print(gen.generate_trending_topic())
"
```

### **GitHub Actions 테스트:**
```
1. GitHub → Actions
2. "Auto Update Blog with AI" 선택
3. "Run workflow" 클릭
4. 로그에서 "🔄 API 키 #2로 전환" 메시지 확인
```

---

## 💡 **추가 팁**

### **할당량 모니터링:**
```
https://aistudio.google.com/app/apikey
→ 각 키별 사용량 확인
```

### **키 관리 팁:**
- 월초에 모든 키의 할당량이 리셋됨
- 각 키에 메모 추가 (예: "블로그용 키 #1")
- 정기적으로 키 로테이션 로그 확인

### **비용 절감:**
- 무료 키 3-5개로 대부분의 사용 가능
- 유료 전환 시: 월 ~₩390 (30개 글 생성)

---

## ⚠️ **주의사항**

### **금지 사항:**
- ❌ 키를 Git에 커밋하지 마세요!
- ❌ 공개 저장소에 노출 금지
- ❌ 무분별한 계정 생성 (Google 정책 위반)

### **권장 사항:**
- ✅ GitHub Secrets 사용
- ✅ `.gitignore`에 config 파일 추가
- ✅ 적절한 사용 (스팸 방지)

---

## 🎯 **결론**

### **장점:**
- ✅ **완전 무료** (여러 무료 키 활용)
- ✅ **자동 전환** (할당량 초과 시)
- ✅ **간단 설정** (JSON 배열 한 줄)

### **단점:**
- ⚠️ 여러 Google 계정 필요
- ⚠️ 키 관리 필요

### **추천 대상:**
- 일 5-10회 이하 사용
- 비용 절감 원하시는 분
- 무료 범위 내 사용 원하시는 분

---

## 🚀 **즉시 적용**

1. **API 키 3개 발급** (Google 계정 3개)
2. **GitHub Secrets 등록**:
   ```
   Name: GEMINI_API_KEYS
   Value: ["key1", "key2", "key3"]
   ```
3. **워크플로우 재실행** (이미 지원됨)

---

**코드는 이미 준비되어 있습니다!** 🎉  
**키만 등록하시면 바로 작동합니다!**
