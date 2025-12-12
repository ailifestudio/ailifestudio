# 🔧 GitHub Actions 워크플로우 설정 가이드

## 📋 개요

GitHub App 권한 문제로 로컬에서 워크플로우 파일을 푸시할 수 없습니다.
대신 **GitHub 웹사이트에서 직접 생성**해야 합니다.

---

## 🚀 단계별 설정

### 1️⃣ GitHub 저장소 접속

https://github.com/ailifestudio/ailifestudio.github.io

### 2️⃣ Actions 탭 클릭

상단 메뉴에서 **Actions** 클릭

### 3️⃣ 새 워크플로우 생성

- **New workflow** 버튼 클릭
- **set up a workflow yourself** 링크 클릭

### 4️⃣ 파일명 설정

- 파일명을 `auto-update-ai.yml`로 변경

### 5️⃣ 아래 코드 복사 & 붙여넣기

```yaml
name: Auto Update Blog with AI

on:
  schedule:
    # 매일 오전 9시, 오후 3시, 오후 9시 (KST = UTC+9)
    - cron: '0 0,6,12 * * *'  # UTC 0시, 6시, 12시 = KST 9시, 15시, 21시
  workflow_dispatch:  # 수동 실행 가능
    inputs:
      enable_ai:
        description: 'AI 콘텐츠 생성 활성화'
        required: false
        default: 'true'
        type: choice
        options:
          - 'true'
          - 'false'

jobs:
  update-blog:
    runs-on: ubuntu-latest
    
    steps:
    - name: 📥 체크아웃
      uses: actions/checkout@v4
      
    - name: 🐍 Python 설정
      uses: actions/setup-python@v5
      with:
        python-version: '3.11'
        
    - name: 📦 의존성 설치
      run: |
        cd automation
        pip install -r requirements.txt
        
    - name: 🤖 블로그 자동 업데이트 (AI + RSS)
      env:
        GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
        OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
      run: |
        cd automation
        
        # AI 활성화 여부 확인
        ENABLE_AI="${{ github.event.inputs.enable_ai || 'true' }}"
        
        if [ "$ENABLE_AI" = "true" ] && [ -n "$GEMINI_API_KEY" ]; then
          echo "🤖 AI 콘텐츠 생성 + RSS 크롤링 모드"
          python blog_automation.py --rss-config config_korean.json
        else
          echo "📰 RSS 크롤링만 실행"
          python blog_automation.py --rss-config config_korean.json --no-ai
        fi
        
    - name: 📊 data.json 이동
      run: |
        if [ -f automation/data.json ]; then
          cp automation/data.json data.json
          echo "✅ data.json 업데이트 완료"
        else
          echo "❌ data.json 생성 실패"
          exit 1
        fi
        
    - name: 📤 변경사항 커밋 및 푸시
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        
        git add data.json
        
        # 변경사항이 있을 때만 커밋
        if ! git diff --staged --quiet; then
          # AI 생성 여부에 따라 커밋 메시지 변경
          if [ -n "${{ secrets.GEMINI_API_KEY }}" ]; then
            git commit -m "🤖 자동 업데이트 (AI + RSS): $(date +'%Y-%m-%d %H:%M')"
          else
            git commit -m "📰 자동 업데이트 (RSS): $(date +'%Y-%m-%d %H:%M')"
          fi
          
          git push
          echo "✅ 블로그 업데이트 완료!"
        else
          echo "ℹ️ 변경사항 없음"
        fi
```

### 6️⃣ 커밋

- **Commit changes...** 버튼 클릭
- 커밋 메시지: `🤖 AI 블로그 자동화 워크플로우 추가`
- **Commit changes** 클릭

---

## ✅ 설정 완료 확인

### 1. 워크플로우 파일 확인

- 저장소 루트에 `.github/workflows/auto-update-ai.yml` 파일 생성됨

### 2. 수동 실행 테스트

1. **Actions** 탭 클릭
2. **Auto Update Blog with AI** 선택
3. **Run workflow** 클릭
4. AI 활성화 선택: **true**
5. **Run workflow** 버튼 클릭

### 3. 실행 결과 확인

- 워크플로우 실행 로그 확인
- 약 3-5분 소요
- ✅ 성공 시: data.json 자동 업데이트

### 4. 블로그 확인

- https://ailifestudio.github.io/ 접속
- 새로운 콘텐츠 확인

---

## 🔧 문제 해결

### Q: 워크플로우 실행 실패
A: 
1. Actions 탭에서 로그 확인
2. GEMINI_API_KEY가 Secrets에 등록되었는지 확인
3. Python 패키지 설치 오류 확인

### Q: GEMINI_API_KEY 오류
A:
1. Settings → Secrets and variables → Actions
2. GEMINI_API_KEY 값 확인
3. 재입력 후 다시 실행

### Q: 자동 실행이 안 됨
A:
1. 워크플로우 파일의 cron 설정 확인
2. Actions가 활성화되어 있는지 확인
3. 저장소 Settings → Actions → General → "Allow all actions" 확인

---

## 📅 자동 실행 스케줄

- **오전 9시** (KST): AI 생성 + RSS
- **오후 3시** (KST): RSS만
- **오후 9시** (KST): RSS만

---

## 💡 추가 팁

### RSS만 실행하고 싶다면

워크플로우 수동 실행 시:
- AI 활성화: **false** 선택

### 다른 시간에 실행하려면

cron 표현식 수정:
```yaml
schedule:
  - cron: '0 */6 * * *'  # 6시간마다
  - cron: '0 9 * * 1'    # 매주 월요일 오전 9시
```

Cron 생성 도구: https://crontab.guru/

---

**✅ 워크플로우 설정이 완료되면 자동화가 시작됩니다!**

궁금한 점이 있으면 Issues에 남겨주세요. 🚀
