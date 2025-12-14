# 🚀 Quick Start Guide

**AI 블로그 자동화 파이프라인** - 빠른 시작 가이드

---

## 📋 목차

1. [로컬 테스트](#로컬-테스트)
2. [GitHub Actions 설정](#github-actions-설정)
3. [개별 스크립트 실행](#개별-스크립트-실행)
4. [문제 해결](#문제-해결)

---

## 🧪 로컬 테스트

### **구조 검증 테스트** (API 키 불필요)

```bash
# 전체 파이프라인 구조 검증
python automation/test_pipeline_structure.py

# 출력 확인
cat automation/intermediate_outputs/step1_topic.json
cat automation/intermediate_outputs/step2_structured_content.json
cat automation/intermediate_outputs/step3_validated_content.json
```

**예상 결과**:
```
✅ Step 1: 주제 생성 포맷 검증 - PASS
✅ Step 2: 구조화된 콘텐츠 검증 - PASS
✅ Step 3: 이미지 검증 검증 - PASS
✅ Step 4: data.json 구조 검증 - PASS
✅ Step 5: HTML 렌더링 검증 - PASS
```

---

## 🔧 GitHub Actions 설정

### **1. 워크플로우 파일 업데이트** ⚠️

**중요**: 이 단계는 **수동으로** 진행해야 합니다.

1. GitHub 접속: https://github.com/ailifestudio/ailifestudio.github.io
2. 파일 열기: `.github/workflows/auto-update-ai.yml`
3. ✏️ **Edit** 클릭
4. 파일 내용을 `WORKFLOW_UPDATE.md`의 "신규 워크플로우 코드"로 교체
5. 커밋 메시지 입력: `🔧 Update to 4-step AI pipeline`
6. **Commit changes** 클릭

### **2. GitHub Actions 실행**

1. **Actions** 탭 클릭
2. "Auto Update Blog with AI" 워크플로우 선택
3. 우측 상단 **Run workflow** 버튼 클릭
4. `enable_ai`: **true** 선택
5. **Run workflow** 확인

### **3. 로그 확인**

워크플로우 실행 중 다음 단계들이 표시됩니다:

```
✅ Step 1: 주제 선정
   🎯 블루오션 키워드 발굴 중...
   
✅ Step 2: 글 작성
   📝 구조화된 콘텐츠 작성 중...
   
✅ Step 3: 이미지 생성 및 검수
   🎨 이미지 생성 및 Gemini Vision 검수 중...
   
✅ Step 4: data.json 저장
   💾 data.json 및 Markdown 파일 생성 중...
```

---

## 🔨 개별 스크립트 실행

### **전체 파이프라인 실행**

```bash
# 통합 스크립트
python automation/run_pipeline.py
```

### **단계별 실행**

```bash
# Step 1: 주제 선정
python automation/step1_topic_agent.py

# Step 2: 글 작성
python automation/step2_writer_agent.py

# Step 3: 이미지 생성 및 검수
python automation/step3_image_audit_agent.py

# Step 4: data.json 저장
python automation/step4_save_to_data_json.py
```

**필요 환경 변수**:
```bash
export GEMINI_API_KEY="your_api_key_here"
# 또는
export GEMINI_API_KEYS='["key1", "key2", "key3"]'
```

---

## 🐛 문제 해결

### **Q: 로컬에서 API 키 에러가 발생해요**

```
❌ GEMINI_API_KEY가 설정되지 않았습니다.
```

**해결책**:
1. API 키 없이 테스트: `python automation/test_pipeline_structure.py`
2. 또는 환경 변수 설정:
   ```bash
   export GEMINI_API_KEY="your_key"
   python automation/step1_topic_agent.py
   ```

### **Q: 중간 파일이 생성되지 않아요**

**확인 사항**:
```bash
# 디렉토리 존재 확인
ls -la automation/intermediate_outputs/

# 없다면 생성
mkdir -p automation/intermediate_outputs/
```

### **Q: 워크플로우 파일이 푸시되지 않아요**

```
[remote rejected] refusing to allow a GitHub App to create or update 
workflow without `workflows` permission
```

**해결책**: 이것은 GitHub 보안 정책입니다. **반드시 웹에서 수동으로 편집**하세요.

### **Q: Step 3에서 이미지가 생성되지 않아요**

**확인 사항**:
1. Gemini Vision 검수 로그 확인
2. `step3_validated_content.json` 파일 확인:
   ```bash
   cat automation/intermediate_outputs/step3_validated_content.json | grep -A 5 "validation"
   ```
3. "FAIL" 판정된 이미지는 자동으로 제거됩니다

### **Q: WordPress에 어떻게 연동하나요?**

**현재 상태**: 데이터 구조는 준비 완료  
**향후 계획**: `step5_wordpress_publisher.py` 구현 예정

```python
# 예정된 구조
def publish_to_wordpress(validated_content):
    # data.json → WordPress REST API
    # 이미지 업로드
    # 포스트 생성
    pass
```

---

## 📊 출력 파일 위치

### **중간 파일** (디버깅용)
```
automation/intermediate_outputs/
├── step1_topic.json              # 선정된 주제
├── step2_structured_content.json # 구조화된 콘텐츠
└── step3_validated_content.json  # 검증된 최종 콘텐츠
```

### **최종 파일**
```
data.json                         # 전체 블로그 데이터
contents/[제목].md                # Markdown 파일
automation/generated_images/      # 생성된 이미지
automation/thumbnails/            # 썸네일 이미지
```

---

## 🔄 일반적인 워크플로우

### **1. 로컬 개발**
```bash
# 1. 구조 검증
python automation/test_pipeline_structure.py

# 2. 중간 파일 확인
cat automation/intermediate_outputs/*.json

# 3. 개별 스크립트 디버깅 (필요시)
python automation/step1_topic_agent.py
```

### **2. GitHub Actions 배포**
```bash
# 1. 변경사항 커밋
git add .
git commit -m "🔧 Update pipeline scripts"
git push origin main

# 2. GitHub Actions 수동 실행
# (웹 인터페이스에서 Run workflow 클릭)

# 3. 로그 확인 및 검증
```

### **3. 콘텐츠 확인**
```bash
# 1. data.json 확인
cat data.json | jq '.posts[-1]'

# 2. Markdown 파일 확인
ls -lh contents/*.md | tail -1

# 3. 이미지 확인
ls -lh automation/generated_images/*.png
```

---

## 📚 추가 리소스

| 문서 | 용도 |
|-----|------|
| `PROJECT_STATUS_SUMMARY.md` | 전체 프로젝트 현황 |
| `WORKFLOW_UPDATE.md` | 워크플로우 수동 업데이트 가이드 |
| `PIPELINE_ARCHITECTURE.md` | 파이프라인 상세 설계 |
| `TEST_RESULTS.md` | 테스트 결과 보고서 |
| `QUICK_START.md` | 📍 **이 문서** |

---

## 🆘 긴급 지원

문제가 해결되지 않을 경우:

1. **로그 확인**: GitHub Actions 로그 전체 복사
2. **중간 파일 확인**: `automation/intermediate_outputs/*.json` 내용 확인
3. **환경 확인**: Python 버전, 설치된 패키지 확인
   ```bash
   python --version
   pip list | grep -E "(google|requests|pillow)"
   ```

---

## ✅ 체크리스트

배포 전 확인:

- [ ] `test_pipeline_structure.py` 실행 → 5/5 통과
- [ ] `WORKFLOW_UPDATE.md` 참조하여 워크플로우 업데이트
- [ ] GitHub Secrets에 `GEMINI_API_KEY` 등록됨
- [ ] Actions 탭에서 "Run workflow" 실행 가능
- [ ] 로그에서 4단계 모두 성공 확인
- [ ] `data.json` 및 `contents/*.md` 생성 확인

---

**마지막 업데이트**: 2025-12-14  
**버전**: 2.0.0  
**상태**: 🟢 프로덕션 준비 완료
