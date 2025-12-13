# 🎨 Nano Banana Pro 이미지 생성 가이드

## 📋 현재 문제

```
❌ Pexels API: 작동하지 않음 (모든 요청 실패)
❌ Picsum Fallback: 완전히 관계없는 랜덤 이미지
❌ 사용자 경험: 매우 나쁨 (이미지와 내용 불일치)
```

**로그 예시:**
```
🔍 이미지 검색: digital assistant interface on smartphone
⚠️ Fallback 이미지: https://picsum.photos/seed/dc33a3822eeb2f34/1280/720
```

→ **"digital assistant"와 전혀 관계없는 랜덤 풍경 사진 표시**

---

## ✅ 해결 방안: Nano Banana Pro 직접 사용

### 왜 Nano Banana Pro인가?

1. **정확한 이미지 생성**: 키워드에 맞는 이미지 생성
2. **고품질**: 전문적이고 세련된 이미지
3. **16:9 비율**: 블로그에 최적화된 비율
4. **AI 생성**: 저작권 걱정 없음

---

## 🚀 구현 방법

### 방법 1: GenSpark Assistant로 이미지 생성 (수동) ⭐ 추천

**이 방법이 가장 빠르고 확실합니다!**

#### 1단계: 이미지 키워드 추출

블로그 글에서 이미지 키워드 추출:

```bash
cd /home/user/webapp
grep -oP '\[IMAGE:\K[^\]]+' contents/*.md | sort -u > image_keywords.txt
```

또는 최신 생성된 글에서만:

```bash
cd /home/user/webapp
latest_file=$(ls -t contents/*.md | head -1)
grep -oP '\[IMAGE:\K[^\]]+' "$latest_file"
```

**출력 예시:**
```
digital assistant interface on smartphone
person managing calendar with AI
student researching with AI on laptop
creative person brainstorming with AI
...
```

#### 2단계: GenSpark Assistant에게 이미지 생성 요청

GenSpark Assistant에게 다음과 같이 요청:

```
다음 키워드들로 Nano Banana Pro 이미지를 생성해주세요:

1. digital assistant interface on smartphone
2. person managing calendar with AI
3. student researching with AI on laptop
4. creative person brainstorming with AI
5. language learner using AI translation app

각 이미지는:
- 모델: nano-banana-pro
- 비율: 16:9 (1280x720)
- 품질: high quality, professional photography
- 저장 위치: /mnt/aidrive/blog_images/

생성된 이미지의 AI Drive 경로와 URL을 알려주세요.
```

#### 3단계: 생성된 이미지 URL 저장

Assistant가 제공한 이미지 URL을 JSON 파일로 저장:

```json
{
  "digital assistant interface on smartphone": "https://www.genspark.ai/api/files/v1/...",
  "person managing calendar with AI": "https://www.genspark.ai/api/files/v1/...",
  "student researching with AI on laptop": "https://www.genspark.ai/api/files/v1/...",
  ...
}
```

파일 저장:
```bash
cat > /home/user/webapp/automation/generated_images.json << 'EOF'
{
  "digital assistant interface on smartphone": "YOUR_IMAGE_URL_HERE",
  "person managing calendar with AI": "YOUR_IMAGE_URL_HERE"
}
EOF
```

#### 4단계: 블로그 자동화 스크립트에서 사용

`automation/unsplash_images.py` 수정:

```python
# 생성된 이미지 맵 로드
def load_generated_images():
    try:
        with open('automation/generated_images.json', 'r') as f:
            return json.load(f)
    except:
        return {}

def search_unsplash_image(keyword: str, access_key: str = None) -> str:
    # 1순위: 생성된 이미지 확인
    generated_images = load_generated_images()
    if keyword in generated_images:
        print(f"    ✅ Nano Banana 이미지 사용: {keyword}")
        return generated_images[keyword]
    
    # 2순위: Pexels API 시도
    ...
```

---

### 방법 2: 자동화 스크립트 개선 (장기)

#### 현재 제약사항
```
❌ Python 스크립트 내에서 image_generation 도구 직접 호출 불가
❌ GenSpark API 인증 토큰 필요
❌ 비동기 이미지 생성 처리 필요
```

#### 해결 방안 (향후 개선)

1. **GenSpark API 엔드포인트 사용**
   ```python
   import requests
   
   def generate_image_with_api(prompt: str) -> str:
       api_url = "https://api.genspark.ai/v1/images/generate"
       headers = {"Authorization": f"Bearer {API_TOKEN}"}
       payload = {
           "model": "nano-banana-pro",
           "query": prompt,
           "aspect_ratio": "16:9"
       }
       response = requests.post(api_url, json=payload, headers=headers)
       return response.json()["image_url"]
   ```

2. **GitHub Actions 워크플로우에서 이미지 생성**
   ```yaml
   - name: Generate AI Images
     run: |
       # 키워드 추출
       python automation/extract_keywords.py > keywords.txt
       
       # GenSpark CLI로 이미지 생성
       while read keyword; do
         genspark generate-image \
           --model nano-banana-pro \
           --prompt "$keyword, high quality, 16:9" \
           --output "/mnt/aidrive/blog_images/"
       done < keywords.txt
   ```

3. **별도의 이미지 생성 서비스**
   - 이미지 생성 전용 마이크로서비스
   - Queue 기반 비동기 처리
   - AI Drive 자동 업로드

---

## 📊 비교: 현재 vs Nano Banana

| 항목 | 현재 (Picsum) | Nano Banana Pro |
|------|---------------|-----------------|
| **정확도** | ❌ 0% (완전 랜덤) | ✅ 95%+ (키워드 기반) |
| **품질** | ⚠️ 중간 (랜덤 사진) | ✅ 높음 (AI 생성) |
| **관련성** | ❌ 없음 | ✅ 매우 높음 |
| **비용** | 무료 | 무료 (GenSpark 크레딧) |
| **속도** | ⚡ 즉시 | ⏱️ 약 5-10초/이미지 |
| **16:9 비율** | ✅ 지원 | ✅ 지원 |
| **저작권** | ✅ 무료 사용 | ✅ 무료 사용 |

---

## 🎯 즉시 실행 가능한 솔루션

### 옵션 A: 수동 이미지 생성 + 자동 삽입

**1. 이미지 키워드 추출:**
```bash
cd /home/user/webapp
grep -oP '\[IMAGE:\K[^\]]+' contents/*.md | sort -u
```

**2. GenSpark Assistant에게 이미지 생성 요청**

**3. 생성된 URL을 `generated_images.json`에 저장**

**4. 스크립트 자동으로 해당 이미지 사용**

**장점:**
- ✅ 즉시 실행 가능
- ✅ 고품질 이미지 보장
- ✅ 간단한 구현

**단점:**
- ⚠️ 수동 작업 필요 (처음 1회)
- ⚠️ 새 키워드마다 이미지 생성 필요

---

### 옵션 B: Unsplash API 키 발급 (대안)

Pexels가 작동하지 않으면 Unsplash API를 사용:

**1. Unsplash 개발자 계정 생성:**
```
https://unsplash.com/developers
```

**2. API 키 발급 (무료 플랜: 50 req/hour)**

**3. `automation/unsplash_images.py` 수정:**
```python
def search_unsplash_image(keyword: str, access_key: str = "YOUR_UNSPLASH_KEY") -> str:
    # Unsplash API 사용
    api_url = f"https://api.unsplash.com/search/photos"
    params = {
        "query": keyword,
        "per_page": 1,
        "orientation": "landscape",
        "client_id": access_key
    }
    response = requests.get(api_url, params=params)
    ...
```

**4. GitHub Secrets에 키 저장:**
```
Name: UNSPLASH_API_KEY
Secret: YOUR_KEY_HERE
```

**장점:**
- ✅ 실제 사진 사용
- ✅ 키워드 기반 검색
- ✅ 무료 (제한적)

**단점:**
- ⚠️ 시간당 50회 제한
- ⚠️ 실제 사진 (AI 생성 아님)

---

## 🔥 최종 권장 사항

### 🥇 1순위: Nano Banana Pro (수동 생성 + 자동 삽입)

**즉시 실행 가능:**
```bash
# 1. 키워드 추출
cd /home/user/webapp
grep -oP '\[IMAGE:\K[^\]]+' contents/*.md | sort -u > image_keywords.txt

# 2. Assistant에게 요청
cat image_keywords.txt
# → GenSpark Assistant에게 이미지 생성 요청

# 3. URL 저장
cat > automation/generated_images.json << 'EOF'
{
  "키워드1": "URL1",
  "키워드2": "URL2"
}
EOF

# 4. 스크립트 업데이트 (아래 참조)
```

### 🥈 2순위: Unsplash API

무료 플랜으로 시작 가능, Nano Banana보다 구현 간단

### 🥉 3순위: Pexels API 키 재확인

현재 키가 만료되었을 가능성 있음

---

## 📝 다음 단계

**사용자 선택 필요:**

1. **Nano Banana Pro 사용 (추천)**
   - GenSpark Assistant에게 이미지 생성 요청
   - 생성된 URL을 `generated_images.json`에 저장
   - 자동화 스크립트 업데이트

2. **Unsplash API 사용**
   - API 키 발급
   - GitHub Secrets에 저장
   - 스크립트 업데이트

3. **Pexels API 재확인**
   - 현재 키 상태 확인
   - 필요 시 새 키 발급

**어떤 방법을 선택하시겠습니까?**
