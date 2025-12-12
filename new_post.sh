#!/bin/bash
# OSMU 새 글 작성 도우미 스크립트
# 사용법: ./new_post.sh ai-tech "글 제목"

set -e

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 사용법 표시
usage() {
    echo "📝 OSMU 새 글 작성 도우미"
    echo ""
    echo "사용법:"
    echo "  ./new_post.sh <category> <title>"
    echo ""
    echo "카테고리:"
    echo "  - ai-tech   : AI/테크"
    echo "  - economy   : 경제"
    echo "  - life      : 라이프"
    echo "  - global    : 글로벌"
    echo ""
    echo "예시:"
    echo "  ./new_post.sh ai-tech \"최신 AI 생산성 도구 5가지\""
    exit 1
}

# 파라미터 확인
if [ $# -lt 2 ]; then
    usage
fi

CATEGORY=$1
TITLE=$2

# 카테고리 검증
case $CATEGORY in
    ai-tech|economy|life|global)
        ;;
    *)
        echo -e "${RED}❌ 잘못된 카테고리: $CATEGORY${NC}"
        usage
        ;;
esac

# 카테고리 한글명 매핑
case $CATEGORY in
    ai-tech)
        CATEGORY_KR="AI/테크"
        ;;
    economy)
        CATEGORY_KR="경제"
        ;;
    life)
        CATEGORY_KR="라이프"
        ;;
    global)
        CATEGORY_KR="글로벌"
        ;;
esac

# 날짜 및 슬러그 생성
DATE=$(date +%Y-%m-%d)
SLUG=$(echo "$TITLE" | iconv -t ascii//TRANSLIT | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/--*/-/g' | sed 's/^-//' | sed 's/-$//')
FILENAME="${DATE}-${SLUG}.md"
FILEPATH="_posts/${CATEGORY}/${FILENAME}"

# 디렉토리 생성
mkdir -p "_posts/${CATEGORY}"

# 파일 존재 확인
if [ -f "$FILEPATH" ]; then
    echo -e "${RED}❌ 파일이 이미 존재합니다: $FILEPATH${NC}"
    exit 1
fi

# Markdown 템플릿 생성
cat > "$FILEPATH" << EOF
---
title: "$TITLE"
date: $DATE
category: $CATEGORY
canonical_url: ""
summary: "여기에 글 요약을 작성하세요 (150자 이내, SEO에 중요)"
image: "https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80"
tags:
  - 태그1
  - 태그2
---

## 소개

여기에 글 내용을 작성하세요.

---

## 본문 1

내용...

---

## 본문 2

내용...

---

## 마무리

결론...
EOF

echo ""
echo -e "${GREEN}✅ 새 글이 생성되었습니다!${NC}"
echo ""
echo "📄 파일 정보:"
echo "   경로: $FILEPATH"
echo "   카테고리: $CATEGORY_KR ($CATEGORY)"
echo "   제목: $TITLE"
echo "   날짜: $DATE"
echo ""
echo "📝 다음 단계:"
echo "   1. 에디터로 파일 열기: code $FILEPATH"
echo "   2. 내용 작성 (Front Matter 필수 항목 채우기)"
echo "   3. 이미지 URL 교체 (https://unsplash.com 추천)"
echo "   4. 로컬 테스트: python automation/build_and_sync.py"
echo "   5. Git 커밋 & 푸시"
echo ""
echo "🚀 자동 배포: GitHub에 푸시하면 자동으로 배포됩니다!"
