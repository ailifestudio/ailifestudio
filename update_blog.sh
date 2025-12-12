#!/bin/bash

# 블로그 자동 업데이트 스크립트
# 사용법: ./update_blog.sh [config_file]

echo "🚀 AI Life Studio 블로그 자동 업데이트"
echo "=========================================="

# 설정 파일 경로
CONFIG=${1:-"automation/config.json"}

# automation 디렉토리로 이동
cd automation

# Python 스크립트 실행
if [ -f "$CONFIG" ]; then
    echo "📝 설정 파일: $CONFIG"
    python news_crawler.py $(basename $CONFIG)
else
    echo "📝 기본 설정 사용: config.json"
    python news_crawler.py
fi

# data.json을 메인 디렉토리로 복사
if [ -f "data.json" ]; then
    cp data.json ../data.json
    echo ""
    echo "✅ 블로그 업데이트 완료!"
    echo "📊 data.json 파일이 업데이트되었습니다."
    echo ""
    echo "다음 단계:"
    echo "  git add data.json"
    echo "  git commit -m '📰 뉴스 업데이트'"
    echo "  git push"
else
    echo "❌ data.json 생성 실패"
    exit 1
fi
