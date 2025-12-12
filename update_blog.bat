@echo off
REM 블로그 자동 업데이트 스크립트 (Windows용)
REM 사용법: update_blog.bat [config_file]

echo 🚀 AI Life Studio 블로그 자동 업데이트
echo ==========================================

SET CONFIG=%1
IF "%CONFIG%"=="" SET CONFIG=config.json

cd automation

echo 📝 설정 파일: %CONFIG%
python news_crawler.py %CONFIG%

IF EXIST data.json (
    copy data.json ..\data.json
    echo.
    echo ✅ 블로그 업데이트 완료!
    echo 📊 data.json 파일이 업데이트되었습니다.
    echo.
    echo 다음 단계:
    echo   git add data.json
    echo   git commit -m "📰 뉴스 업데이트"
    echo   git push
) ELSE (
    echo ❌ data.json 생성 실패
    exit /b 1
)

cd ..
pause
